# Auto-Charge: Smart EV Charging for Home Assistant

Intelligent EV charging automations that maximize solar power usage during the day and manage grid import limits at night.

## Features

### Coopernico GO 2.0 Energy Price Integration
Real-time energy price sensors for Coopernico GO 2.0 indexed tariff (Portugal):
- **One-click setup**: Install via HACS, add via UI — pick your OMIE sensor and tariff type
- **Automatic sensors**: Period, Energy, TAR, Total, Total c/ IVA 6%, Total c/ IVA 23%
- **All tariff types**: Simples, Bi-Horária, Tri-Horária
- **Semester-aware**: Automatic S1/S2 TAR switching (January-May / June-December)
- **Summer/winter periods**: Automatic DST detection for tri-horário schedules
- **Portuguese & English**: Full UI translations

### Solar Dynamic Current (Daytime)
Adjusts charging current in real-time based on available solar export:
- **Formula**: `Target Amps = (Grid Export + Current Charger Draw - Buffer) / (Voltage x Phases)`
- **Responsive lowering**: Immediately reduces current when export drops (while still exporting)
- **Cloud resilience**: Only drops to minimum after 20s of sustained grid import (ignores brief clouds)
- **Fast raising**: Increases current on the next adjustment cycle when more surplus is available
- **Enable switch**: Toggle solar charging on/off via an `input_boolean` helper
- **Clean stop behavior**: Turning the switch off or leaving the schedule window returns the charger to the configured minimum
- **Integer amps**: Always outputs whole-number amp values
- **Configurable limits**: Min/max current, voltage, phases, buffer, and schedule window

### Grid Charge
Manages grid charging while keeping total grid import below a configurable limit, with optional energy price awareness:
- **Formula**: `Target Amps = (Max Import - Base Load - Buffer) / (Voltage x Phases)`
- **Import limiting**: Calculates base household load and ensures charging stays within your grid import cap
- **Energy price control**: Only charges when the current energy price is below your configured maximum (€/kWh)
- **Enable switch**: Toggle charging on/off via an `input_boolean` helper
- **Same smart logic**: Lowers immediately, raises only after sustained headroom

## Blueprints

| Blueprint | File | Purpose |
|-----------|------|---------|
| Auto-Charge Dynamic Current | `auto_charge_dynamic_current.yaml` | Solar-based daytime charging |
| Grid Charge | `grid_charge.yaml` | Grid-import-limited charging with energy price control |

## Installation

### Coopernico GO 2.0 (via HACS)

1. Add this repository to HACS as a custom repository (Integration category)
2. Install **Coopernico GO 2.0** from HACS
3. Restart Home Assistant
4. Go to **Settings** > **Devices & Services** > **+ Add Integration**
5. Search for **Coopernico GO**
6. Select your **OMIE price sensor** and **tariff type** — done!

Sensors are created automatically under a "Coopernico GO" device. You can add multiple tariff types by adding the integration again.

### Blueprints

See [INSTALLATION.md](INSTALLATION.md) for detailed blueprint setup instructions.

1. Go to **Settings** > **Automations & Scenes** > **Blueprints**
2. Click **"Import Blueprint"** and paste the blueprint URL from the repository
3. Repeat for each blueprint you want
4. Create automations from the blueprints and configure your entities

## Usage

### Coopernico GO Sensors

After setup, you get these sensors (example for Tri-Horária):

| Sensor | Description |
|--------|-------------|
| **Period** | Current tariff period (Ponta / Cheias / Vazio) |
| **Energy** | Coopernico energy component before TAR & taxes |
| **TAR** | Current network access tariff |
| **Total** | Total price before IVA |
| **Total c/ IVA 6%** | With 6% IVA (first 200 kWh/month, ≤ 6.9 kVA) |
| **Total c/ IVA 23%** | With 23% IVA (beyond 200 kWh/month) |

**Formula**: `Energy = ((OMIE + 0.009) × 1.16) + 0.001` | `Total = Energy + TAR + CS + CR + TSE + IEC`

### Setting Up Solar Dynamic Current

1. **Create an `input_boolean` helper** first:
   - Go to **Settings** > **Devices & Services** > **Helpers**
   - Click **"+ Create Helper"** > **"Toggle"**
   - Name it something like "Solar Charge Enable"
   - This switch controls whether solar charging is active

2. Go to **Settings** > **Automations & Scenes**
3. Click **"+ Create Automation"** > **"Use a Blueprint"**
4. Select **"Auto-Charge Dynamic Current Adjustment"**
5. Configure:
   - **Power Sensor**: Grid power sensor (negative when exporting)
   - **Max Current Entity**: Your charger's current control (number entity)
   - **Solar Charge Enable Switch**: The `input_boolean` you created above
   - **Voltage**: Your grid voltage (default: 230V)
   - **Phases**: 1 for single-phase, 3 for three-phase (default: 1)
   - **Power Buffer**: Safety margin to avoid grid import (default: 100W)
   - **Min Current**: Minimum charging current (default: 0A)
   - **Max Current**: Maximum charging current (default: 32A)
   - **Schedule Start/End**: Time window for solar charging (default: 09:00-22:00)
6. Save the automation

### Setting Up Grid Charge

1. **Create an `input_boolean` helper** first (if you haven't already created one for solar charging, you need a separate one for grid charging):
   - Go to **Settings** > **Devices & Services** > **Helpers**
   - Click **"+ Create Helper"** > **"Toggle"**
   - Name it something like "Grid Charge Enable"
   - This switch controls whether grid charging is active

2. Go to **Settings** > **Automations & Scenes**
3. Click **"+ Create Automation"** > **"Use a Blueprint"**
4. Select **"Grid Charge"**
5. Configure:
   - **Energy Price Sensor**: Sensor showing current energy price in €/kWh
   - **Maximum Energy Price**: Maximum price at which charging is allowed (default: 0.10 €/kWh)
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
6. Save the automation

## Requirements

### For Solar Dynamic Current:
- A **power sensor** that shows grid import/export (negative when exporting)
- A **number entity** that controls max charging current
- An **`input_boolean` helper** to enable/disable solar charging
- Charger must support dynamic current adjustment

### For Grid Charge:
- An **energy price sensor** showing the current price in €/kWh
- A **power sensor** that shows grid import (positive when importing)
- A **number entity** that controls max charging current
- An **`input_boolean` helper** to enable/disable grid charging
- Charger must support dynamic current adjustment

## How It Works

### Solar Dynamic Current Logic
```
Every 20 seconds (during schedule window, if enable switch is ON):
1. Read grid export and current charger amps
2. Calculate charger draw = current_amps x voltage x phases
3. Calculate available = grid_export + charger_draw - buffer
4. Calculate target_amps = available / (voltage x phases)  (truncated to integer)
5. Clamp between min_current and max_current
6. IF target < current AND still exporting → Lower immediately
   ELSE IF importing for 20+ seconds → Apply the proportional reduction
   ELSE IF target > current → Raise on the next cycle

When the enable switch turns OFF or the schedule window ends:
1. Set charger current back to min_current
```

### Grid Charge Logic
```
Every 20 seconds (if enable switch is ON and energy price ≤ max price):
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
- **Current Range**: 6-16A
- At 3000W export, 6A current: target = (3000 + 1380 - 100) / 230 = **18A** (clamped to 16A)

### Quick Example: Grid Charge (3kW import limit)
- **Max Import**: 3000W | **Buffer**: 400W | **Voltage**: 230V | **Max Price**: 0.10 €/kWh
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
- Check that the **enable switch** (`input_boolean`) is turned ON
- Check that power sensor is negative when exporting (solar blueprint) or positive when importing (grid charge blueprint)
- Verify the max current entity is writable
- Check automation traces in Home Assistant
- Make sure you're within the schedule window

### Grid charging not working?
- Check that the **enable switch** (`input_boolean`) is turned ON
- Verify the current energy price is below your configured maximum
- Check that `max_import_power` is set high enough for your needs

### Too much oscillation?
- For grid charging, increase **Raise Delay** (e.g., 5-10 minutes)
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
