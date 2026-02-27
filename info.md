## Auto-Charge: Smart EV Charging + Coopernico GO Energy Prices

Intelligent EV charging automation blueprints and real-time Coopernico GO 2.0 energy price sensors for Home Assistant.

### What's Included

**Coopernico GO 2.0 Integration** — Real-time energy price sensors for the Coopernico GO indexed tariff (Portugal):
- Pick your OMIE sensor and tariff type (Simples / Bi-Horária / Tri-Horária)
- Automatic sensors: Period, Energy, TAR, Total, Total c/ IVA 6%, Total c/ IVA 23%
- Semester-aware TAR values, summer/winter period detection
- Portuguese & English translations

**Automation Blueprints**:
1. **Auto-Charge Dynamic Current** — Adjusts charging current in real-time based on available solar export
2. **Grid Charge** — Manages grid charging within a configurable import limit and energy price cap (€/kWh)

### Quick Start

1. Install via HACS (Integration category)
2. **Settings** > **Devices & Services** > **+ Add Integration** > **Coopernico GO**
3. Select your OMIE sensor and tariff type — sensors are created automatically

### Requirements

- Home Assistant 2023.4.0+
- An OMIE spot price sensor (e.g. from the [OMIE integration](https://github.com/luuuis/hass_omie))
- For charging blueprints: a power sensor and charger with current control

### Support

Need help? Check the [full documentation](https://github.com/joaoj/auto-charge) or [report an issue](https://github.com/joaoj/auto-charge/issues).
