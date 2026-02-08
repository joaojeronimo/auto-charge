# Auto-Charge: Smart EV Charging for Home Assistant

Intelligent EV charging automations that maximize solar power usage and optimize charging based on grid export.

## Features

### 🔘 Auto-Charge Button Trigger
Automatically starts your EV charging when:
- **Nighttime hours** (configurable, default 10 PM - 8 AM) for cheap off-peak rates, OR
- **High solar export** (configurable threshold, default >1000W) to use excess solar

### ⚡ Dynamic Current Adjustment
Intelligently adjusts charging current in real-time:
- **Formula**: `Target Amps = (Exported Power - Buffer) / (Voltage × Phases)`
- **Responsive lowering**: Immediately reduces current when export drops
- **Stable raising**: Only increases current after sustained high export (prevents oscillation)
- **Configurable limits**: Set min/max current, voltage, buffer, and timing

## Installation

### Option 1: Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Automation" tab
3. Click the "+" button
4. Search for "Auto-Charge"
5. Click "Download"
6. Restart Home Assistant

### Option 2: Manual Installation

1. Download the blueprint files:
   - [Auto-Charge Button Trigger](blueprints/automation/auto_charge_button_trigger.yaml)
   - [Auto-Charge Dynamic Current](blueprints/automation/auto_charge_dynamic_current.yaml)

2. Copy them to your Home Assistant config directory:
   ```
   config/blueprints/automation/auto-charge/
   ```
   Note: Blueprint files should be in the `blueprints/automation/` subdirectory.

3. Restart Home Assistant or reload automations

## Usage

### Setting Up Button Trigger

1. Go to **Settings** → **Automations & Scenes**
2. Click **"+ Create Automation"** → **"Use a Blueprint"**
3. Select **"Auto-Charge Button Trigger"**
4. Configure:
   - **Button Entity**: Your charger's start button
   - **Power Sensor**: Grid power sensor (negative when exporting)
   - **Export Threshold**: Minimum export to trigger (default: 1000W)
   - **Night Hours**: Start and end times (default: 22:00 - 08:00)
5. Save the automation

### Setting Up Dynamic Current Adjustment

1. Go to **Settings** → **Automations & Scenes**
2. Click **"+ Create Automation"** → **"Use a Blueprint"**
3. Select **"Auto-Charge Dynamic Current Adjustment"**
4. Configure:
   - **Power Sensor**: Same grid power sensor
   - **Max Current Entity**: Your charger's current control (number entity)
   - **Voltage**: Your grid voltage (230V or 240V)
   - **Power Buffer**: Safety margin (default: 100W)
   - **Phases**: Number of phases (1 for single-phase, 3 for three-phase)
   - **Current Limits**: Min/Max current for your charger (e.g., 0-32A)
   - **Adjustment Interval**: How often to check (default: /20 = every 20s)
   - **Raise Delay**: Stabilization time before raising (default: 3 min)
5. Save the automation

## Requirements

### For Button Trigger:
- A **button entity** that starts charging (e.g., from EV charger integration)
- A **power sensor** that shows grid import/export (negative when exporting)

### For Dynamic Current Adjustment:
- A **number entity** that controls max charging current
- A **power sensor** (same as above)
- Charger must support dynamic current adjustment

## Compatible Chargers

Works with any Home Assistant integrated charger that supports:
- Start/stop buttons (for button trigger)
- Dynamic current control (for current adjustment)

**Tested with:**
- go-eCharger
- Wallbox
- Easee
- OCPP compatible chargers
- *(Add your charger here!)*

## How It Works

### Button Trigger Logic
```
Every minute, check:
IF (current_time between night_start and night_end)
   OR (grid_export > threshold)
THEN press the button
```

### Dynamic Current Logic
```
Every 20 seconds:
1. Calculate: target_amps = (exported_power - buffer) / (voltage × phases)
2. Clamp target_amps between min_current and max_current
3. IF target_amps < current_amps:
     → Lower immediately (responsive)
   ELSE IF target_amps > current_amps:
     → Wait 3 minutes, then raise (stable)
```

## Example Configuration

### Typical Solar Setup (230V, 3-phase):
- **Voltage**: 230V
- **Power Buffer**: 100W
- **Current Range**: 6-32A
- **Export Threshold**: 1500W (~6.5A × 230V)
- **Adjustment Interval**: 20 seconds
- **Raise Delay**: 3 minutes

### Single Phase Setup:
- **Voltage**: 230V or 240V
- **Power Buffer**: 100W
- **Current Range**: 6-16A
- **Export Threshold**: 1000W
- **Adjustment Interval**: 30 seconds
- **Raise Delay**: 5 minutes

## Troubleshooting

### Current not adjusting?
- Check that power sensor is negative when exporting
- Verify max current entity is writable
- Check automation traces in Home Assistant

### Too much oscillation?
- Increase **Raise Delay** (e.g., 5-10 minutes)
- Increase **Power Buffer** (e.g., 200-500W)
- Increase **Adjustment Interval** (e.g., 30-60 seconds)

### Importing from grid?
- Increase **Power Buffer** to create larger safety margin
- Check that power sensor readings are accurate

## Contributing

Contributions welcome! Please submit issues and pull requests on GitHub.

## License

MIT License - see LICENSE file for details

## Support

- 🐛 [Report Issues](https://github.com/yourusername/auto-charge/issues)
- 💬 [Discussions](https://github.com/yourusername/auto-charge/discussions)
- ⭐ Star this repo if you find it useful!

---

**Made with ☀️ for smart solar charging**
