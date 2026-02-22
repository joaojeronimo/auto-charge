# Auto-Charge: Smart EV Charging for Home Assistant

Intelligent EV charging automations that maximize solar power usage during the day and manage grid import limits at night.

## Features

### Solar Dynamic Current (Daytime)
Adjusts charging current in real-time based on available solar export:
- **Formula**: `Target Amps = (Grid Export + Current Charger Draw - Buffer) / (Voltage x Phases)`
- **Responsive lowering**: Immediately reduces current when export drops
- **Stable raising**: Only increases current after sustained high export (prevents oscillation)
- **Integer amps**: Always outputs whole-number amp values
- **Configurable limits**: Min/max current, voltage, buffer, raise delay, and schedule window

### Nightly Charge Dynamic Current
Manages charging overnight while keeping total grid import below a configurable limit:
- **Formula**: `Target Amps = (Max Import - Base Load - Buffer) / (Voltage x Phases)`
- **Import limiting**: Calculates base household load and ensures charging stays within your grid import cap
- **Enable switch**: Toggle night charging on/off via an `input_boolean` helper
- **Same smart logic**: Lowers immediately, raises only after sustained headroom

## Blueprints

| Blueprint | File | Purpose |
|-----------|------|---------|
| Auto-Charge Dynamic Current | `auto_charge_dynamic_current.yaml` | Solar-based daytime charging |
| Nightly Charge Dynamic Current | `night_charge_dynamic_current.yaml` | Grid-import-limited night charging |

## Installation

See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions.

### Quick Start

1. Go to **Settings** > **Automations & Scenes** > **Blueprints**
2. Click **"Import Blueprint"** and paste the blueprint URL from the repository
3. Repeat for each blueprint you want
4. Create automations from the blueprints and configure your entities

## Usage

### Setting Up Solar Dynamic Current

1. Go to **Settings** > **Automations & Scenes**
2. Click **"+ Create Automation"** > **"Use a Blueprint"**
3. Select **"Auto-Charge Dynamic Current Adjustment"**
4. Configure:
   - **Power Sensor**: Grid power sensor (negative when exporting)
   - **Max Current Entity**: Your charger's current control (number entity)
   - **Voltage**: Your grid voltage (default: 230V)
   - **Phases**: 1 for single-phase, 3 for three-phase (default: 1)
   - **Power Buffer**: Safety margin to avoid grid import (default: 100W)
   - **Min Current**: Minimum charging current (default: 0A)
   - **Max Current**: Maximum charging current (default: 32A)
   - **Raise Delay**: Minutes to wait before raising current (default: 3 min)
   - **Schedule Start/End**: Time window for solar charging (default: 09:00-22:00)
5. Save the automation

### Setting Up Nightly Charge

1. **Create an `input_boolean` helper** first:
   - Go to **Settings** > **Devices & Services** > **Helpers**
   - Click **"+ Create Helper"** > **"Toggle"**
   - Name it something like "Night Charge Enable"
   - This switch controls whether night charging is active

2. Go to **Settings** > **Automations & Scenes**
3. Click **"+ Create Automation"** > **"Use a Blueprint"**
4. Select **"Nightly Charge Dynamic Current"**
5. Configure:
   - **Power Sensor**: Grid power sensor (positive when importing)
   - **Max Current Entity**: Your charger's current control (number entity)
   - **Night Charge Enable Switch**: The `input_boolean` you created above
   - **Maximum Import Power**: Grid import cap in Watts (default: 3000W)
   - **Voltage**: Your grid voltage (default: 230V)
   - **Phases**: 1 for single-phase, 3 for three-phase (default: 1)
   - **Power Buffer**: Safety margin below import limit (default: 100W, min: 400W)
   - **Min Current**: Minimum charging current (default: 0A, max: 4A)
   - **Max Current**: Maximum charging current (default: 32A)
   - **Raise Delay**: Minutes to wait before raising current (default: 3 min)
   - **Schedule Start/End**: Night charging window (default: 22:00-08:00)
6. Save the automation

## Requirements

### For Solar Dynamic Current:
- A **power sensor** that shows grid import/export (negative when exporting)
- A **number entity** that controls max charging current
- Charger must support dynamic current adjustment

### For Nightly Charge:
- A **power sensor** that shows grid import (positive when importing)
- A **number entity** that controls max charging current
- An **`input_boolean` helper** to enable/disable night charging
- Charger must support dynamic current adjustment

## How It Works

### Solar Dynamic Current Logic
```
Every 20 seconds (during schedule window):
1. Read grid export and current charger amps
2. Calculate charger draw = current_amps x voltage x phases
3. Calculate available = grid_export + charger_draw - buffer
4. Calculate target_amps = available / (voltage x phases)  (truncated to integer)
5. Clamp between min_current and max_current
6. IF target < current → Lower immediately
   ELSE IF target > current AND stable for raise_delay → Raise
```

### Nightly Charge Logic
```
Every 20 seconds (during schedule window, if enable switch is ON):
1. Read grid import and current charger amps
2. Calculate charger draw = current_amps x voltage x phases
3. Calculate base_load = max(grid_import - charger_draw, 0)
4. Calculate available = max_import_power - base_load - buffer
5. Calculate target_amps = available / (voltage x phases)  (truncated to integer)
6. Clamp between min_current and max_current
7. IF target < current → Lower immediately
   ELSE IF target > current AND stable for raise_delay → Raise
```

## Example Configurations

See [EXAMPLES.md](EXAMPLES.md) for detailed configuration examples covering single-phase, three-phase, conservative, and aggressive setups.

### Quick Example: Single-Phase Solar (230V)
- **Voltage**: 230V | **Phases**: 1 | **Buffer**: 100W
- **Current Range**: 6-16A | **Raise Delay**: 3 min
- At 3000W export, 6A current: target = (3000 + 1380 - 100) / 230 = **18A** (clamped to 16A)

### Quick Example: Night Charge (3kW import limit)
- **Max Import**: 3000W | **Buffer**: 400W | **Voltage**: 230V
- **Current Range**: 0-32A | **Raise Delay**: 3 min
- At 500W base load: target = (3000 - 500 - 400) / 230 = **9A**

## Compatible Chargers

Works with any Home Assistant integrated charger that supports dynamic current control via a number entity.

**Tested with:**
- go-eCharger
- Wallbox
- Easee
- OCPP compatible chargers
- *(Add your charger here!)*

## Troubleshooting

### Current not adjusting?
- Check that power sensor is negative when exporting (solar blueprint) or positive when importing (night blueprint)
- Verify the max current entity is writable
- Check automation traces in Home Assistant
- Make sure you're within the schedule window

### Night charging not working?
- Check that the **enable switch** (`input_boolean`) is turned ON
- Verify the schedule window covers overnight (start > end is fine, e.g. 22:00-08:00)
- Check that `max_import_power` is set high enough for your needs

### Too much oscillation?
- Increase **Raise Delay** (e.g., 5-10 minutes)
- Increase **Power Buffer** (e.g., 200-500W)

### Importing from grid during solar charging?
- Increase **Power Buffer** to create larger safety margin
- Check that power sensor readings are accurate and update frequently

## Contributing

Contributions welcome! Please submit issues and pull requests on GitHub.

## License

MIT License - see LICENSE file for details.

## Support

- [Report Issues](https://github.com/yourusername/auto-charge/issues)
- [Discussions](https://github.com/yourusername/auto-charge/discussions)

---

**Made for smart solar charging**
