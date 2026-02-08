## Auto-Charge: Smart EV Charging

Intelligent EV charging automation blueprints that maximize solar power usage and optimize charging based on grid export.

### What's Included

This package contains **two automation blueprints**:

1. **Auto-Charge Button Trigger** - Automatically starts charging during off-peak hours or when you have excess solar export
2. **Auto-Charge Dynamic Current Adjustment** - Continuously adjusts charging current to match available solar power

### Quick Start

1. Go to **Settings** → **Automations & Scenes** → **Blueprints**
2. Click **"Import Blueprint"** and paste the blueprint URL from the repository
3. Click **"Create Automation"** → **"Use a Blueprint"**
4. Look for **"Auto-Charge"** blueprints
5. Configure with your entities and preferences
6. Save and enable!

### Key Features

- ⚡ **Dynamic current adjustment** based on real-time solar export (single and three-phase)
- 🌙 **Night mode** for cheap off-peak charging
- 🛡️ **Bulletproof logic** with safety buffers and validation
- 🎛️ **Fully configurable** through Home Assistant UI
- 📊 **Smart algorithm** that lowers quickly, raises slowly (prevents oscillation)

### Requirements

- A power sensor that shows grid import/export (negative when exporting)
- An EV charger integration with:
  - A button entity for starting (Button Trigger blueprint), OR
  - A number entity for current control (Dynamic Current blueprint)

### Support

Need help? Check the [full documentation](https://github.com/yourusername/auto-charge) or [report an issue](https://github.com/yourusername/auto-charge/issues).
