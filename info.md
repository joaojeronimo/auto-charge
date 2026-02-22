## Auto-Charge: Smart EV Charging

Intelligent EV charging automation blueprints that maximize solar power usage during the day and manage grid import limits at night.

### What's Included

This package contains **two automation blueprints**:

1. **Auto-Charge Dynamic Current Adjustment** — Adjusts charging current in real-time based on available solar export, accounting for current charger draw
2. **Nightly Charge Dynamic Current** — Manages overnight charging within a configurable grid import limit, with an on/off enable switch

### Quick Start

1. Go to **Settings** > **Automations & Scenes** > **Blueprints**
2. Click **"Import Blueprint"** and paste the blueprint URL from the repository
3. Repeat for the second blueprint
4. For night charging: create an `input_boolean` helper (**Settings** > **Devices & Services** > **Helpers** > **Toggle**)
5. Create automations from the blueprints and configure your entities
6. Save and enable!

### Key Features

- **Solar dynamic current** based on real-time grid export (single and three-phase)
- **Night charging** with grid import limiting and enable/disable switch
- **Smart algorithm** that lowers quickly, raises slowly (prevents oscillation)
- **Integer amp output** for clean charger control
- **Fully configurable** through Home Assistant UI — no coding required

### Requirements

- A power sensor that shows grid import/export
- An EV charger integration with a number entity for current control
- For night charging: an `input_boolean` helper to enable/disable

### Support

Need help? Check the [full documentation](https://github.com/yourusername/auto-charge) or [report an issue](https://github.com/yourusername/auto-charge/issues).
