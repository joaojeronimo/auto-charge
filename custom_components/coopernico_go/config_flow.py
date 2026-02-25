"""Config flow for Coopernico GO 2.0."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.helpers import selector

from .const import (
    CONF_OMIE_ENTITY,
    CONF_TARIFF,
    DEFAULT_NAME,
    DOMAIN,
    TARIFF_OPTIONS,
    TARIFF_TRI,
)


class CoopernicoGoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Coopernico GO."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            omie_entity = user_input[CONF_OMIE_ENTITY]
            tariff = user_input[CONF_TARIFF]
            tariff_label = TARIFF_OPTIONS[tariff]

            await self.async_set_unique_id(f"{omie_entity}_{tariff}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"{DEFAULT_NAME} {tariff_label}",
                data={
                    CONF_OMIE_ENTITY: omie_entity,
                    CONF_TARIFF: tariff,
                },
            )

        tariff_options = [
            selector.SelectOptionDict(value=k, label=v)
            for k, v in TARIFF_OPTIONS.items()
        ]

        data_schema = vol.Schema(
            {
                vol.Required(CONF_OMIE_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        multiple=False,
                    ),
                ),
                vol.Required(
                    CONF_TARIFF, default=TARIFF_TRI
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=tariff_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
