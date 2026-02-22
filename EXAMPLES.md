# Configuration Examples

This document provides example configurations for common setups.

## Solar Dynamic Current Examples

These examples use the **Auto-Charge Dynamic Current Adjustment** blueprint for daytime solar charging.

### Example 1: Single-Phase Solar Setup (230V, 16A Max)

**Scenario:** Single-phase home with solar panels, 16A portable EVSE, conservative approach.

```yaml
Power Sensor: sensor.home_grid_power          # Negative when exporting
Max Current Entity: number.mycharger_max_current
Voltage: 230
Phases: 1
Power Buffer: 150    # Conservative buffer
Min Current: 6       # Typical minimum for most chargers
Max Current: 16      # Single-phase max
Raise Delay: 5       # Wait 5 minutes before raising
Schedule Start: 09:00:00
Schedule End: 22:00:00
```

**How it calculates** (at 3000W export, currently charging at 6A):
- Charger draw = 6 x 230 = 1380W
- Available = 3000 + 1380 - 150 = 4230W
- Target = 4230 / 230 = **18A** (clamped to 16A max)

---

### Example 2: Three-Phase Solar Setup (230V, 32A Max)

**Scenario:** Three-phase home with large solar array, wall-mounted 32A charger, aggressive tracking.

```yaml
Power Sensor: sensor.solar_net_power
Max Current Entity: number.wallbox_max_current
Voltage: 230
Phases: 3
Power Buffer: 100    # Tight buffer for good tracking
Min Current: 0       # Can stop charging if needed
Max Current: 32      # Three-phase max
Raise Delay: 3       # Standard raise delay
Schedule Start: 08:00:00
Schedule End: 20:00:00
```

**How it calculates** (at 5000W export, currently charging at 10A):
- Charger draw = 10 x 230 x 3 = 6900W
- Available = 5000 + 6900 - 100 = 11800W
- Target = 11800 / (230 x 3) = **17A**

---

### Example 3: Conservative Solar-Only (Avoid Grid Import)

**Scenario:** Only charge on excess solar, never import. Battery storage system, very sensitive to imports.

```yaml
Power Sensor: sensor.battery_grid_power
Max Current Entity: number.ev_max_current
Voltage: 230
Phases: 1
Power Buffer: 500    # Very large buffer!
Min Current: 0       # Will stop if not enough export
Max Current: 32
Raise Delay: 10      # Very conservative, wait 10 min
Schedule Start: 08:00:00
Schedule End: 18:00:00
```

**How it calculates** (at 2000W export, currently charging at 6A):
- Charger draw = 6 x 230 = 1380W
- Available = 2000 + 1380 - 500 = 2880W
- Target = 2880 / 230 = **12A**

---

### Example 4: Aggressive Solar Tracking

**Scenario:** Large solar array, want to use every bit of excess, don't mind occasional small imports.

```yaml
Power Sensor: sensor.powerwall_grid_power
Max Current Entity: number.tesla_current_limit
Voltage: 240
Phases: 1
Power Buffer: 50     # Minimal buffer
Min Current: 6       # Keep charging active
Max Current: 32
Raise Delay: 2       # Quick to raise
Schedule Start: 07:00:00
Schedule End: 21:00:00
```

---

## Nightly Charge Examples

These examples use the **Nightly Charge Dynamic Current** blueprint for overnight charging within a grid import limit. All require an `input_boolean` helper for the enable switch.

### Example 5: Standard Night Charge (3kW Import Limit)

**Scenario:** Cheap overnight rate, 3kW import limit to avoid breaker trips, single-phase.

```yaml
Power Sensor: sensor.grid_power               # Positive when importing
Max Current Entity: number.charger_charging_current
Night Charge Enable Switch: input_boolean.night_charge_enable
Maximum Import Power: 3000
Voltage: 230
Phases: 1
Power Buffer: 400    # Safety margin below limit
Min Current: 0
Max Current: 16
Raise Delay: 3
Schedule Start: 22:00:00
Schedule End: 06:00:00
```

**How it calculates** (at 800W household load, currently charging at 6A):
- Charger draw = 6 x 230 = 1380W
- Total import = 800 + 1380 = 2180W (what the sensor reads)
- Base load = 2180 - 1380 = 800W
- Available = 3000 - 800 - 400 = 1800W
- Target = 1800 / 230 = **7A**

---

### Example 6: High-Power Night Charge (7kW Import Limit)

**Scenario:** Higher import allowance, three-phase charger, want to charge as fast as possible overnight.

```yaml
Power Sensor: sensor.grid_import_power
Max Current Entity: number.wallbox_max_current
Night Charge Enable Switch: input_boolean.night_charge_enable
Maximum Import Power: 7000
Voltage: 230
Phases: 1
Power Buffer: 500
Min Current: 6
Max Current: 32
Raise Delay: 3
Schedule Start: 23:00:00
Schedule End: 07:00:00
```

**How it calculates** (at 1000W household load, currently charging at 16A):
- Charger draw = 16 x 230 = 3680W
- Total import = 1000 + 3680 = 4680W (what the sensor reads)
- Base load = 4680 - 3680 = 1000W
- Available = 7000 - 1000 - 500 = 5500W
- Target = 5500 / 230 = **23A**

---

### Example 7: Conservative Night Charge (Low Import Limit)

**Scenario:** Shared building supply, must keep total import very low, slow charging acceptable.

```yaml
Power Sensor: sensor.apartment_grid_power
Max Current Entity: number.ev_max_current
Night Charge Enable Switch: input_boolean.night_charge_enable
Maximum Import Power: 2000
Voltage: 230
Phases: 1
Power Buffer: 500
Min Current: 0
Max Current: 10
Raise Delay: 5
Schedule Start: 00:00:00
Schedule End: 06:00:00
```

---

## Sensor Requirements

Your power sensor should:
- Show **negative values** when exporting to grid (for solar blueprint)
- Show **positive values** when importing from grid (used by both blueprints)
- Update frequently (every few seconds ideally)
- Be reliable (not frequently unavailable)

### Common Sensor Entity IDs

**Smart Meters:**
- `sensor.grid_power`
- `sensor.home_power_import_export`
- `sensor.electricity_meter_power`

**Solar Inverters:**
- `sensor.inverter_power`
- `sensor.solar_export_power`

**Battery Systems:**
- `sensor.powerwall_grid_power`
- `sensor.battery_grid_power`

### Testing Your Sensor

Check your sensor shows correct signs:
```
When exporting 2000W: sensor should show -2000
When importing 500W: sensor should show +500
When balanced: sensor should show near 0
```

---

## Troubleshooting Common Configs

### Problem: Solar charging stuck at low amps despite high export

**Check:**
- The formula accounts for current charger draw. If the target seems low, check that the power sensor is reading correctly.
- Raise delay may be preventing the increase — wait for the configured delay period.
- Check automation traces to see calculated `target_amps` vs `current_max_amps`.

### Problem: Too much grid import during solar charging

**Fix:**
- Increase Power Buffer (try 300-500W)
- Increase Raise Delay (more conservative raising)

### Problem: Not using enough solar

**Fix:**
- Decrease Power Buffer (try 50-100W)
- Decrease Raise Delay (faster raising)
- Decrease Min Current to 0 if your charger supports it

### Problem: Night charging not activating

**Check:**
- Is the **enable switch** (`input_boolean`) turned ON?
- Is the current time within the schedule window?
- Is `max_import_power` set high enough? If base load exceeds the limit, target will be 0.

### Problem: Charging stops and starts frequently

**Fix:**
- Increase Raise Delay (prevents oscillation)
- Increase Power Buffer (more stable)
- Increase Min Current (keeps charging active)

---

## Formula Reference

### Solar Dynamic Current
```
charger_draw = current_amps x voltage x phases
available_watts = grid_export + charger_draw - power_buffer
target_amps = available_watts / (voltage x phases)    (truncated to integer)
```

The formula adds back the charger's current draw because the grid export sensor shows what's left *after* the charger is already consuming power.

**Examples (single-phase, 230V, 100W buffer):**
- 3000W export, 6A current: (3000 + 1380 - 100) / 230 = **18A**
- 1000W export, 0A current: (1000 + 0 - 100) / 230 = **3A**
- 500W export, 10A current: (500 + 2300 - 100) / 230 = **11A**

### Nightly Charge
```
charger_draw = current_amps x voltage x phases
base_load = max(grid_import - charger_draw, 0)
available_watts = max_import_power - base_load - power_buffer
target_amps = available_watts / (voltage x phases)    (truncated to integer)
```

The formula separates household base load from charger consumption to determine how much headroom remains within the import limit.

**Examples (single-phase, 230V, 3000W limit, 400W buffer):**
- 500W base load: (3000 - 500 - 400) / 230 = **9A**
- 1000W base load: (3000 - 1000 - 400) / 230 = **6A**
- 2000W base load: (3000 - 2000 - 400) / 230 = **2A**

---

Need more help? Check the [main documentation](README.md) or [open an issue](https://github.com/yourusername/auto-charge/issues).
