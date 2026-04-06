"""Sensor platform for Coopernico GO 2.0."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_change,
)
from homeassistant.util import dt as dt_util

from .const import (
    CONF_OMIE_ENTITY,
    CONF_TARIFF,
    CR,
    CS,
    DOMAIN,
    FP,
    GO,
    IEC,
    K,
    REGULATED_COSTS,
    TAR,
    TARIFF_BI,
    TARIFF_OPTIONS,
    TARIFF_SIMPLES,
    TARIFF_TRI,
    TSE,
)

# Official BTN tri-horário daily cycle for Portugal Continental.
_TRI_DAILY_SCHEDULE = {
    "winter": (
        (8 * 60, 9 * 60, "cheias"),
        (9 * 60, 10 * 60 + 30, "ponta"),
        (10 * 60 + 30, 18 * 60, "cheias"),
        (18 * 60, 20 * 60 + 30, "ponta"),
        (20 * 60 + 30, 22 * 60, "cheias"),
    ),
    "summer": (
        (8 * 60, 10 * 60 + 30, "cheias"),
        (10 * 60 + 30, 13 * 60, "ponta"),
        (13 * 60, 19 * 60 + 30, "cheias"),
        (19 * 60 + 30, 21 * 60, "ponta"),
        (21 * 60, 22 * 60, "cheias"),
    ),
}


def _now() -> datetime:
    """Return Home Assistant local time."""
    return dt_util.now()


def _is_summer(dt: datetime) -> bool:
    """Check if datetime is in Portugal legal summer time."""
    return bool(dt.dst())


def _semester(dt: datetime) -> str:
    """Return current semester key."""
    return "s1" if dt.month < 6 else "s2"


def _bi_periodo(dt: datetime) -> str:
    """Return current bi-horário period."""
    return "fora_de_vazio" if 8 <= dt.hour < 22 else "vazio"


def _tri_periodo(dt: datetime) -> str:
    """Return current tri-horário period."""
    t = dt.hour * 60 + dt.minute
    schedule_key = "summer" if _is_summer(dt) else "winter"
    for start, end, period in _TRI_DAILY_SCHEDULE[schedule_key]:
        if start <= t < end:
            return period
    return "vazio"


def _requires_period_updates(tariff: str) -> bool:
    """Return True if the displayed period changes with the clock."""
    return tariff != TARIFF_SIMPLES


def _energy_price(omie_mwh: float) -> float:
    """Calculate Coopernico energy component: ((OMIE + K) * (1 + FP)) + GO.

    OMIE reports in EUR/MWh, convert to EUR/kWh first.
    """
    omie = omie_mwh / 1000.0
    return ((omie + K) * (1 + FP)) + GO


def _tar_simples(dt: datetime) -> float:
    return TAR["simples"][_semester(dt)]["flat"]


def _tar_bi(dt: datetime) -> float:
    return TAR["bi"][_semester(dt)][_bi_periodo(dt)]


def _tar_tri(dt: datetime) -> float:
    return TAR["tri"][_semester(dt)][_tri_periodo(dt)]


def _apply_iva6(energy: float, tar: float) -> float:
    """IVA 6% (first 200 kWh/month, contracts <= 6.9 kVA). IEC always at 23%."""
    return (energy + tar + CS + CR + TSE) * 1.06 + IEC * 1.23


def _apply_iva23(energy: float, tar: float) -> float:
    """IVA 23% (beyond 200 kWh/month)."""
    return (energy + tar + CS + CR + TSE + IEC) * 1.23


# Map tariff type to (period_func, tar_func, period_labels)
_TARIFF_MAP = {
    TARIFF_SIMPLES: (lambda _dt: "simples", _tar_simples),
    TARIFF_BI: (_bi_periodo, _tar_bi),
    TARIFF_TRI: (_tri_periodo, _tar_tri),
}

# Human-readable period labels
_PERIOD_LABELS = {
    "simples": "Simples",
    "fora_de_vazio": "Fora de Vazio",
    "vazio": "Vazio",
    "ponta": "Ponta",
    "cheias": "Cheias",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Coopernico GO sensors from a config entry."""
    omie_entity = entry.data[CONF_OMIE_ENTITY]
    tariff = entry.data[CONF_TARIFF]
    tariff_label = TARIFF_OPTIONS[tariff]

    device_info = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=f"Coopernico GO {tariff_label}",
        manufacturer="Coopernico",
        model="GO 2.0",
        entry_type=DeviceEntryType.SERVICE,
    )

    entities: list[SensorEntity] = [
        CoopernicoPeriodSensor(entry, omie_entity, tariff, device_info),
        CoopernicoEnergySensor(entry, omie_entity, device_info),
        CoopernicoTarSensor(entry, omie_entity, tariff, device_info),
        CoopernicoTotalSensor(entry, omie_entity, tariff, device_info),
        CoopernicoIva6Sensor(entry, omie_entity, tariff, device_info),
        CoopernicoIva23Sensor(entry, omie_entity, tariff, device_info),
    ]

    async_add_entities(entities, True)


class CoopernicoBaseSensor(SensorEntity):
    """Base class for Coopernico sensors that track an OMIE entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        omie_entity: str,
        device_info: DeviceInfo,
    ) -> None:
        self._entry = entry
        self._omie_entity = omie_entity
        self._attr_device_info = device_info
        self._track_time_updates = False

    async def async_added_to_hass(self) -> None:
        """Track OMIE entity state changes."""
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._omie_entity], self._handle_omie_update
            )
        )
        if self._track_time_updates:
            self.async_on_remove(
                async_track_time_change(
                    self.hass,
                    self._handle_time_update,
                    minute=[0, 30],
                    second=0,
                )
            )
        # Calculate initial value
        self._update_state()

    @callback
    def _handle_omie_update(self, event) -> None:
        """Handle OMIE sensor state change."""
        self._update_state()
        self.async_write_ha_state()

    @callback
    def _handle_time_update(self, now: datetime) -> None:
        """Handle time-driven tariff changes."""
        self._update_state()
        self.async_write_ha_state()

    def _get_omie_price(self) -> float | None:
        """Get current OMIE price from the tracked sensor."""
        state = self.hass.states.get(self._omie_entity)
        if state is None or state.state in ("unknown", "unavailable"):
            return None
        try:
            return float(state.state)
        except (ValueError, TypeError):
            return None

    def _update_state(self) -> None:
        """Override in subclasses to update state."""


class CoopernicoPeriodSensor(CoopernicoBaseSensor):
    """Shows the current tariff period."""

    _attr_icon = "mdi:clock-outline"
    _attr_name = "Period"

    def __init__(self, entry, omie_entity, tariff, device_info):
        super().__init__(entry, omie_entity, device_info)
        self._tariff = tariff
        self._attr_unique_id = f"{entry.entry_id}_period"
        self._track_time_updates = _requires_period_updates(tariff)

    def _update_state(self) -> None:
        dt = _now()
        period_func = _TARIFF_MAP[self._tariff][0]
        period = period_func(dt)
        self._attr_native_value = _PERIOD_LABELS.get(period, period)


class CoopernicoPriceSensor(CoopernicoBaseSensor):
    """Base for price sensors (€/kWh)."""

    _attr_native_unit_of_measurement = "€/kWh"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 4


class CoopernicoEnergySensor(CoopernicoPriceSensor):
    """Coopernico energy component (before TAR & taxes)."""

    _attr_icon = "mdi:lightning-bolt"
    _attr_name = "Energy price"

    def __init__(self, entry, omie_entity, device_info):
        super().__init__(entry, omie_entity, device_info)
        self._attr_unique_id = f"{entry.entry_id}_energy"

    def _update_state(self) -> None:
        omie = self._get_omie_price()
        if omie is None:
            self._attr_native_value = None
            return
        self._attr_native_value = round(_energy_price(omie), 4)


class CoopernicoTarSensor(CoopernicoPriceSensor):
    """Current TAR value."""

    _attr_icon = "mdi:transmission-tower"
    _attr_name = "TAR"

    def __init__(self, entry, omie_entity, tariff, device_info):
        super().__init__(entry, omie_entity, device_info)
        self._tariff = tariff
        self._attr_unique_id = f"{entry.entry_id}_tar"
        self._track_time_updates = True

    def _update_state(self) -> None:
        dt = _now()
        tar_func = _TARIFF_MAP[self._tariff][1]
        self._attr_native_value = round(tar_func(dt), 4)


class CoopernicoTotalSensor(CoopernicoPriceSensor):
    """Total price before IVA (energy + TAR + regulated costs)."""

    _attr_icon = "mdi:currency-eur"
    _attr_name = "Total"

    def __init__(self, entry, omie_entity, tariff, device_info):
        super().__init__(entry, omie_entity, device_info)
        self._tariff = tariff
        self._attr_unique_id = f"{entry.entry_id}_total"
        self._track_time_updates = True

    def _update_state(self) -> None:
        omie = self._get_omie_price()
        if omie is None:
            self._attr_native_value = None
            return
        dt = _now()
        energy = _energy_price(omie)
        tar_func = _TARIFF_MAP[self._tariff][1]
        tar = tar_func(dt)
        self._attr_native_value = round(energy + tar + REGULATED_COSTS, 4)


class CoopernicoIva6Sensor(CoopernicoPriceSensor):
    """Total price with IVA 6% (first 200 kWh/month, <= 6.9 kVA)."""

    _attr_icon = "mdi:currency-eur"
    _attr_name = "Total c/ IVA 6%"

    def __init__(self, entry, omie_entity, tariff, device_info):
        super().__init__(entry, omie_entity, device_info)
        self._tariff = tariff
        self._attr_unique_id = f"{entry.entry_id}_iva6"
        self._track_time_updates = True

    def _update_state(self) -> None:
        omie = self._get_omie_price()
        if omie is None:
            self._attr_native_value = None
            return
        dt = _now()
        energy = _energy_price(omie)
        tar_func = _TARIFF_MAP[self._tariff][1]
        tar = tar_func(dt)
        self._attr_native_value = round(_apply_iva6(energy, tar), 4)

    @property
    def extra_state_attributes(self):
        return {"description": "First 200 kWh/month (contracts \u2264 6.9 kVA)"}


class CoopernicoIva23Sensor(CoopernicoPriceSensor):
    """Total price with IVA 23% (beyond 200 kWh/month)."""

    _attr_icon = "mdi:currency-eur"
    _attr_name = "Total c/ IVA 23%"

    def __init__(self, entry, omie_entity, tariff, device_info):
        super().__init__(entry, omie_entity, device_info)
        self._tariff = tariff
        self._attr_unique_id = f"{entry.entry_id}_iva23"
        self._track_time_updates = True

    def _update_state(self) -> None:
        omie = self._get_omie_price()
        if omie is None:
            self._attr_native_value = None
            return
        dt = _now()
        energy = _energy_price(omie)
        tar_func = _TARIFF_MAP[self._tariff][1]
        tar = tar_func(dt)
        self._attr_native_value = round(_apply_iva23(energy, tar), 4)

    @property
    def extra_state_attributes(self):
        return {"description": "Beyond 200 kWh/month"}
