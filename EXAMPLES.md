# Configuration Examples

This document provides example configurations for common setups.

## Solar Charge Dynamic Current Examples

These examples use the **Solar Charge Dynamic Current** blueprint for daytime solar charging. All require an `input_boolean` helper for the enable switch.

### Example 1: Single-Phase Solar Setup (230V, 16A Max)

**Scenario:** Single-phase home with solar panels, 16A portable EVSE, conservative approach.

```yaml
Power Sensor: sensor.home_grid_power          # Negative when exporting
Max Current Entity: number.mycharger_max_current
Solar Charge Enable Switch: input_boolean.solar_charge_enable
Voltage: 230
Phases: 1
Power Buffer: 150    # Conservative buffer
Min Current: 6       # Typical minimum for most chargers
Max Current: 16      # Single-phase max
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
Solar Charge Enable Switch: input_boolean.solar_charge_enable
Voltage: 230
Phases: 3
Power Buffer: 100    # Tight buffer for good tracking
Min Current: 0       # Can stop charging if needed
Max Current: 32      # Three-phase max
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
Solar Charge Enable Switch: input_boolean.solar_charge_enable
Voltage: 230
Phases: 1
Power Buffer: 500    # Very large buffer!
Min Current: 0       # Will stop if not enough export
Max Current: 32
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
Solar Charge Enable Switch: input_boolean.solar_charge_enable
Voltage: 240
Phases: 1
Power Buffer: 50     # Minimal buffer
Min Current: 6       # Keep charging active
Max Current: 32
Schedule Start: 07:00:00
Schedule End: 21:00:00
```

---

## Grid Charge Examples

These examples use the **Grid Charge** blueprint for price-gated grid charging. All require an `input_boolean` helper for the enable switch.

### Example 5: Standard Price-Gated Night Charge

**Scenario:** Cheap overnight rate, charge at 16A while the price is at or below 0.10 €/kWh, and keep the Goodwe battery on standby while charging.

```yaml
Energy Price Sensor: sensor.coopernico_go_total  # Current price in €/kWh
Maximum Energy Price: 0.10                       # Charge at or below this price
Maximum Current Control: number.charger_charging_current
Maximum Current: 16
Grid Charge Enable Switch: input_boolean.grid_charge_enable
Goodwe EMS Mode Entity: select.goodwe_ems_mode
EMS Mode When Grid Charge Is Active: backup
EMS Mode When Grid Charge Is Inactive: general
```

**Behavior:**
- At 0.09 €/kWh with the enable switch ON, EMS mode is set to `backup`, then charger current is set to 16A
- With the enable switch OFF, grid charge will not start even if the price is cheap
- If the price rises above 0.10 €/kWh while grid charging is active, charger current is set to 0A and EMS mode is set to `general`
- While grid charge is inactive, it leaves charger current unchanged so solar charging can keep adjusting it

---

### Example 6: High-Power Cheap Window

**Scenario:** Charge as fast as the charger allows during a wider cheap-price window.

```yaml
Energy Price Sensor: sensor.coopernico_go_total  # Current price in €/kWh
Maximum Energy Price: 0.15                       # Higher threshold for fast charging
Maximum Current Control: number.wallbox_max_current
Maximum Current: 32
Grid Charge Enable Switch: input_boolean.grid_charge_enable
Goodwe EMS Mode Entity: select.goodwe_ems_mode
EMS Mode When Grid Charge Is Active: backup
EMS Mode When Grid Charge Is Inactive: general
```

---

### Example 7: Conservative Price Threshold

**Scenario:** Only charge at very low prices and limit the charger to 10A.

```yaml
Energy Price Sensor: sensor.coopernico_go_total  # Current price in €/kWh
Maximum Energy Price: 0.08                       # Very low price threshold
Maximum Current Control: number.ev_max_current
Maximum Current: 10
Grid Charge Enable Switch: input_boolean.grid_charge_enable
Goodwe EMS Mode Entity: select.goodwe_ems_mode
EMS Mode When Grid Charge Is Active: backup
EMS Mode When Grid Charge Is Inactive: general
```

---

## Battery Discharge Power Toggle Examples

These examples use the **Battery Discharge Power Toggle** blueprint for battery systems that only expose a watt-based discharge power limit.

### Example 8: Stop Battery Discharge with a Dashboard Toggle

**Scenario:** Your inverter exposes a `number` entity for maximum battery discharge power in Watts. You want a simple toggle to stop discharge temporarily, but still allow discharge automatically when the electricity price is high enough.

```yaml
Toggle Helper: input_boolean.battery_discharge_hold
Discharge Power Entity: number.battery_discharge_power
Electricity Price Sensor: sensor.coopernico_go_total
Price Threshold: 0.10
Stopped Discharge Power: 0
Normal Discharge Power: 5000
```

**Behavior:**
- Toggle **ON** → writes `0W` to the discharge power entity
- Toggle **OFF** → writes `5000W` back to the discharge power entity
- If electricity price rises to `0.10 €/kWh` or higher, it writes `5000W` even while the toggle remains ON

---

## Battery Preservation Max Charge Examples

These examples use the **Battery Preservation Max Charge** blueprint for battery systems that expose a writable maximum charge percentage.

### Example 9: Keep Battery Below High SOC Most of the Day

**Scenario:** Your inverter exposes a maximum charge percentage number entity. You want the battery capped at 95% normally, then capped at 90% from late afternoon until midnight.

```yaml
Battery Max Charge Entity: number.battery_max_charge
Normal Maximum Charge: 95
Preservation Maximum Charge: 90
Preservation Start Time: 16:00:00
Normal Restore Time: 00:00:00
```

**Behavior:**
- From `00:00` to `16:00`, writes `95%`
- From `16:00` to `00:00`, writes `90%`
- On Home Assistant restart or manual changes to the number entity, reapplies the scheduled value

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
- Check that your power sensor updates frequently enough to reflect the extra export.
- Check automation traces to see calculated `target_amps` vs `current_max_amps`.

### Problem: Too much grid import during solar charging

**Fix:**
- Increase Power Buffer (try 300-500W)
- Check that the power sensor sign and update rate are correct if import spikes linger

### Problem: Not using enough solar

**Fix:**
- Decrease Power Buffer (try 50-100W)
- Decrease Min Current to 0 if your charger supports it

### Problem: Grid charging not activating

**Check:**
- Is the **enable switch** (`input_boolean`) turned ON?
- Is the current energy price at or below your configured **Maximum Energy Price**?
- Is the price sensor available and numeric?
- Does your charger accept the configured **Maximum Current** value?

### Problem: Charging stops and starts frequently

**Fix:**
- Check whether your price sensor changes frequently around the threshold.
- Raise **Maximum Energy Price** slightly if you intentionally want to tolerate small price fluctuations.
- Use a tariff period sensor or schedule helper upstream if you want charging grouped into larger time windows.

---

## Formula Reference

### Solar Charge Dynamic Current
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

### Grid Charge
```
charge_allowed = enable_switch_on and current_price <= maximum_energy_price
active: set EMS mode to the configured active option, then set charger current to maximum_current
stop active session: set charger current to 0, then set EMS mode to the configured inactive option
inactive: leave charger current unchanged
```

The grid charge blueprint no longer calculates household load or import headroom. It is a price gate plus EMS mode control, and the enable switch is the only helper required.

---

Need more help? Check the [main documentation](README.md) or [open an issue](https://github.com/yourusername/auto-charge/issues).
