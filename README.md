# Auto-Charge: Smart EV Charging for Home Assistant

Intelligent EV charging automations that maximize solar power usage during the day and enable price-gated grid charging when energy is cheap.

## Features

### Coopernico GO 2.0 Energy Price Integration
Real-time energy price sensors for Coopernico GO 2.0 indexed tariff (Portugal):
- **One-click setup**: Install via HACS, add via UI — pick your OMIE sensor and tariff type
- **Automatic sensors**: Period, Energy, TAR, Total, Total c/ IVA 6%, Total c/ IVA 23%
- **All tariff types**: Simples, Bi-Horária, Tri-Horária
- **Semester-aware**: Automatic S1/S2 TAR switching (January-May / June-December)
- **Summer/winter periods**: Automatic DST detection for tri-horário schedules
- **Portuguese & English**: Full UI translations

### Solar Charge Dynamic Current (Daytime)
Adjusts charging current in real-time based on available solar export:
- **Formula**: `Target Amps = (Grid Export + Current Charger Draw - Buffer) / (Voltage x Phases)`
- **Responsive lowering**: Immediately reduces current when export drops (while still exporting)
- **Cloud resilience**: Only drops to minimum after 20s of sustained grid import (ignores brief clouds)
- **Fast raising**: Increases current on the next adjustment cycle when more surplus is available
- **Enable switch**: Toggle solar charging on/off via an `input_boolean` helper
- **Clean stop behavior**: Turning the switch off or leaving the schedule window sets the charger current to `0`
- **Integer amps**: Always outputs whole-number amp values
- **Configurable limits**: Active min/max current, voltage, phases, buffer, and schedule window

### Grid Charge
Controls grid charging from an energy price threshold:
- **Energy price control**: Only charges when the current energy price is at or below your configured maximum (€/kWh)
- **Goodwe battery protection**: Sets EMS mode to `Battery standby` before charging so the house battery is not used to charge the car
- **Single session helper**: The Grid Charge Enable Switch starts one grid-charge session and is turned off when that session stops
- **Cooperative stop behavior**: Stops charger current for the active grid-charge session, then restores EMS mode to `Auto`
- **Solar-friendly inactive state**: Leaves charger current untouched while the Grid Charge Enable Switch is off, so the solar blueprint can keep adjusting current
- **Startup sync**: Reapplies the correct current and EMS mode when Home Assistant starts

### Battery Discharge Power Toggle
Controls a battery discharge power limit from a dashboard-friendly toggle:
- **Toggle helper**: Uses an `input_boolean` as a simple stop/normal switch
- **Watt-based control**: Writes directly to a battery discharge `number` entity in Watts
- **Simple restore**: Toggle ON sets a stop value such as `0W`; toggle OFF restores your configured normal value
- **Price override**: If the current electricity price is at or above your threshold, battery discharge is restored automatically
- **Startup sync**: Reapplies the selected mode when Home Assistant starts

## Blueprints

| Blueprint | File | Purpose |
|-----------|------|---------|
| Solar Charge Dynamic Current | `solar_charge_dynamic_current.yaml` | Solar-based daytime charging |
| Grid Charge | `grid_charge.yaml` | Price-gated grid charging with Goodwe EMS mode control |
| Battery Discharge Power Toggle | `battery_discharge_power_toggle.yaml` | Toggle battery discharge power between stopped and normal values |

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

### Setting Up Solar Charge Dynamic Current

1. **Create an `input_boolean` helper** first:
   - Go to **Settings** > **Devices & Services** > **Helpers**
   - Click **"+ Create Helper"** > **"Toggle"**
   - Name it something like "Solar Charge Enable"
   - This switch controls whether solar charging is active

2. Go to **Settings** > **Automations & Scenes**
3. Click **"+ Create Automation"** > **"Use a Blueprint"**
4. Select **"Solar Charge Dynamic Current"**
5. Configure:
   - **Power Sensor**: Grid power sensor (negative when exporting)
   - **Max Current Entity**: Your charger's current control (number entity)
   - **Solar Charge Enable Switch**: The `input_boolean` you created above
   - **Voltage**: Your grid voltage (default: 230V)
   - **Phases**: 1 for single-phase, 3 for three-phase (default: 1)
   - **Power Buffer**: Safety margin to avoid grid import (default: 100W)
   - **Min Current**: Minimum charging current while solar charge is active (default: 0A)
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
   - **Maximum Current Control**: Your charger's current control (number entity)
   - **Maximum Current**: Current to set while charging is allowed (default: 32A)
   - **Grid Charge Enable Switch**: The `input_boolean` you created above
   - **Goodwe EMS Mode Entity**: Your Goodwe EMS mode select entity
   - **EMS Mode When Grid Charge Is Active**: `Battery standby`
   - **EMS Mode When Grid Charge Is Inactive**: `Auto`
6. Save the automation

### Setting Up Battery Discharge Power Toggle

1. **Create an `input_boolean` helper** first:
   - Go to **Settings** > **Devices & Services** > **Helpers**
   - Click **"+ Create Helper"** > **"Toggle"**
   - Name it something like "Battery Discharge Hold"
   - This switch controls whether battery discharge is stopped

2. Go to **Settings** > **Automations & Scenes**
3. Click **"+ Create Automation"** > **"Use a Blueprint"**
4. Select **"Battery Discharge Power Toggle"**
5. Configure:
   - **Toggle Helper**: The `input_boolean` you created above
   - **Discharge Power Entity**: Your battery discharge power `number` entity in Watts
   - **Electricity Price Sensor**: Sensor showing the current electricity price in €/kWh
   - **Price Threshold**: If price is at or above this value, discharge is enabled automatically
   - **Stopped Discharge Power**: Usually `0`
   - **Normal Discharge Power**: Your usual discharge limit, such as `5000`
6. Save the automation

## Requirements

### For Solar Charge Dynamic Current:
- A **power sensor** that shows grid import/export (negative when exporting)
- A **number entity** that controls max charging current
- An **`input_boolean` helper** to enable/disable solar charging
- Charger must support dynamic current adjustment

### For Grid Charge:
- An **energy price sensor** showing the current price in €/kWh
- A **number entity** that controls max charging current
- An **`input_boolean` helper** to enable/disable grid charging
- A **Goodwe EMS mode `select` entity**
- Charger must support setting current to `0` to stop charging

### For Battery Discharge Power Toggle:
- A **battery discharge power `number` entity** in Watts
- An **electricity price sensor** showing the current price in €/kWh
- An **`input_boolean` helper** to act as the stop/normal toggle

## How It Works

### Solar Charge Dynamic Current Logic
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
1. Set charger current to 0
```

### Grid Charge Logic
```
On price changes, enable switch changes, Home Assistant start, and every 20 seconds:
1. If enable switch is ON and energy price ≤ max price:
   - Set Goodwe EMS mode to Battery standby
   - Set charger maximum current to the configured Maximum Current
2. If the enable switch is ON and grid charging is no longer allowed, or the switch was just turned OFF:
   - Set charger maximum current to 0
   - Set Goodwe EMS mode to Auto
   - Turn the enable switch OFF
3. If the enable switch is OFF:
   - Leave charger maximum current unchanged so solar or other automations can control it
```

## Example Configurations

See [EXAMPLES.md](EXAMPLES.md) for detailed configuration examples covering single-phase, three-phase, conservative, and aggressive setups.

### Quick Example: Single-Phase Solar (230V)
- **Voltage**: 230V | **Phases**: 1 | **Buffer**: 100W
- **Current Range**: 6-16A
- At 3000W export, 6A current: target = (3000 + 1380 - 100) / 230 = **18A** (clamped to 16A)

### Quick Example: Grid Charge
- **Maximum Energy Price**: 0.10 €/kWh
- **Maximum Current**: 16A
- **EMS Active**: Battery standby | **EMS Inactive**: Auto
- When price is 0.09 €/kWh and the enable switch is ON, current is set to 16A
- When price rises above 0.10 €/kWh while the enable switch is ON, current is set to 0A, EMS mode is set to Auto, and the enable switch is turned OFF
- When the enable switch is OFF, grid charge leaves the current alone so solar charging can adjust it

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
- Check that the solar power sensor is negative when exporting if you are using the solar blueprint
- Verify the max current entity is writable
- Check automation traces in Home Assistant
- Make sure you're within the solar schedule window if you are using the solar blueprint

### Grid charging not working?
- Check that the **enable switch** (`input_boolean`) is turned ON
- Verify the current energy price is at or below your configured maximum
- Verify the charger accepts `0` as a stop current and your configured active current as a start current
- Verify the Goodwe EMS options exactly match your select entity options, usually `Battery standby` and `Auto`

### Too much oscillation?
- For solar charging, increase **Power Buffer** (e.g., 200-500W)

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
