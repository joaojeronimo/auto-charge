# Configuration Examples

This document provides example configurations for common setups.

## Example 1: Single-Phase Solar Setup (230V, 16A Max)

### Scenario
- Single-phase home with solar panels
- 16A charger (e.g., portable EVSE)
- Grid power sensor shows negative when exporting
- Want to charge during night or when excess solar available

### Button Trigger Configuration
```yaml
Button Entity: button.mycharger_start
Power Sensor: sensor.home_grid_power
Export Threshold: 1500  # ~6.5A × 230V
Night Start: 22:00:00
Night End: 08:00:00
```

### Dynamic Current Configuration
```yaml
Power Sensor: sensor.home_grid_power
Max Current Entity: number.mycharger_max_current
Voltage: 230
Phases: 1          # Single-phase
Power Buffer: 150  # Conservative buffer
Min Current: 6     # Typical minimum for most chargers
Max Current: 16    # Single-phase max
Adjustment Interval: 30  # Check every 30 seconds
Raise Delay: 5     # Wait 5 minutes before raising
```

**Result:** Charger starts at night or when exporting >1.5kW, adjusts current to match available solar.

---

## Example 2: Three-Phase Solar Setup (230V, 32A Max)

### Scenario
- Three-phase home with large solar array
- 32A three-phase charger (e.g., wall-mounted)
- High solar production during day
- Want aggressive solar tracking

### Button Trigger Configuration
```yaml
Button Entity: button.wallbox_start
Power Sensor: sensor.solar_net_power
Export Threshold: 2000  # ~8.7A × 230V
Night Start: 23:00:00
Night End: 07:00:00
```

### Dynamic Current Configuration
```yaml
Power Sensor: sensor.solar_net_power
Max Current Entity: number.wallbox_max_current
Voltage: 230
Phases: 3            # Three-phase charger
Power Buffer: 100   # Tight buffer for good tracking
Min Current: 0      # Can stop charging if needed
Max Current: 32     # Three-phase max
Adjustment Interval: 20  # Fast response
Raise Delay: 3      # Standard raise delay
```

**Result:** Fast response to solar changes, charges up to 32A when sufficient solar available.

---

## Example 3: Time-of-Use Optimization

### Scenario
- Time-of-use electricity rates
- Solar panels with moderate production
- Want to prioritize solar, fallback to cheap night rate
- Don't want to import during peak hours

### Button Trigger Configuration
```yaml
Button Entity: button.charger_remote_start
Power Sensor: sensor.grid_import_export
Export Threshold: 1000
Night Start: 22:00:00  # When cheap rate starts
Night End: 06:00:00    # When cheap rate ends
```

### Dynamic Current Configuration
```yaml
Power Sensor: sensor.grid_import_export
Max Current Entity: number.charger_charging_current
Voltage: 240   # 240V region
Phases: 1      # Single-phase
Power Buffer: 200  # Larger buffer to avoid any import
Min Current: 6
Max Current: 32
Adjustment Interval: 20
Raise Delay: 5  # Conservative, avoid import during peak
```

**Result:** Charges on solar during day, switches to full power during cheap night rates.

---

## Example 4: Conservative Setup (Avoid Grid Import)

### Scenario
- Want to charge ONLY on excess solar
- Never import from grid for charging
- Have battery storage system
- Very sensitive to grid import

### Button Trigger Configuration
```yaml
Button Entity: button.ev_charger_start
Power Sensor: sensor.battery_grid_power
Export Threshold: 2000  # High threshold
Night Start: 23:00:00
Night End: 23:01:00  # Effectively disabled (1 min window)
```

### Dynamic Current Configuration
```yaml
Power Sensor: sensor.battery_grid_power
Max Current Entity: number.ev_max_current
Voltage: 230
Phases: 1            # Single-phase
Power Buffer: 500   # Very large buffer!
Min Current: 0      # Will stop if not enough export
Max Current: 32
Adjustment Interval: 15  # Fast response to avoid import
Raise Delay: 10     # Very conservative, wait 10 min
```

**Result:** Only charges on significant solar excess, very unlikely to import from grid.

---

## Example 5: Aggressive Solar Tracking

### Scenario
- Large solar array
- Want to use every bit of excess
- Don't mind occasional small imports
- Battery storage to handle fluctuations

### Button Trigger Configuration
```yaml
Button Entity: button.tesla_charger_start
Power Sensor: sensor.powerwall_grid_power
Export Threshold: 500  # Very sensitive
Night Start: 01:00:00  # Small night window
Night End: 05:00:00
```

### Dynamic Current Configuration
```yaml
Power Sensor: sensor.powerwall_grid_power
Max Current Entity: number.tesla_current_limit
Voltage: 240
Phases: 1            # Single-phase
Power Buffer: 50    # Minimal buffer
Min Current: 6
Max Current: 32
Adjustment Interval: 10  # Very responsive
Raise Delay: 2      # Quick to raise
```

**Result:** Tracks solar aggressively, starts charging with minimal excess, adjusts quickly.

---

## Sensor Requirements

Your power sensor should:
- Show **negative values** when exporting to grid
- Show **positive values** when importing from grid
- Update frequently (every few seconds ideally)
- Be reliable (not frequently unavailable)

### Common Sensor Entity IDs

**Solar Inverters:**
- `sensor.inverter_power`
- `sensor.solar_export_power`
- `sensor.pv_power`

**Smart Meters:**
- `sensor.grid_power`
- `sensor.home_power_import_export`
- `sensor.electricity_meter_power`

**Battery Systems:**
- `sensor.powerwall_grid_power`
- `sensor.battery_grid_power`
- `sensor.grid_feed_in`

### Testing Your Sensor

Check your sensor shows correct signs:
```
When exporting 2000W: sensor should show -2000
When importing 500W: sensor should show +500
When balanced: sensor should show near 0
```

---

## Troubleshooting Common Configs

### Problem: Charges at night but not on solar

**Check:**
- Export threshold too high
- Power sensor not showing negative when exporting
- Button trigger working but current adjustment not configured

### Problem: Too much grid import

**Fix:**
- Increase Power Buffer (try 300-500W)
- Increase Adjustment Interval (slower response)
- Increase Raise Delay (more conservative raising)

### Problem: Not using enough solar

**Fix:**
- Decrease Power Buffer (try 50-100W)
- Decrease Export Threshold
- Decrease Raise Delay (faster raising)
- Decrease Adjustment Interval (faster response)

### Problem: Charging stops and starts frequently

**Fix:**
- Increase Raise Delay (prevents oscillation)
- Increase Power Buffer (more stable)
- Increase Min Current (keeps charging active)

---

## Formula Reference

**Target Amperage Calculation:**
```
target_amps = (exported_power - power_buffer) / (voltage × phases)
```

**Examples (single-phase):**
- 3000W export, 100W buffer, 230V, 1 phase: `(3000-100)/(230×1) = 12.6A`
- 5000W export, 200W buffer, 240V, 1 phase: `(5000-200)/(240×1) = 20.0A`
- 1500W export, 500W buffer, 230V, 1 phase: `(1500-500)/(230×1) = 4.3A` → May be below min_current

**Examples (three-phase):**
- 9000W export, 100W buffer, 230V, 3 phases: `(9000-100)/(230×3) = 12.9A`
- 15000W export, 200W buffer, 230V, 3 phases: `(15000-200)/(230×3) = 21.4A`

**Power Needed for Target Current:**
```
power_needed = (target_amps × voltage × phases) + power_buffer
```

**Examples:**
- 16A target, 230V, 1 phase, 100W buffer: `(16×230×1)+100 = 3780W` needed
- 32A target, 240V, 1 phase, 200W buffer: `(32×240×1)+200 = 7880W` needed
- 16A target, 230V, 3 phases, 100W buffer: `(16×230×3)+100 = 11140W` needed

---

Need more help? Check the [main documentation](README.md) or [open an issue](https://github.com/yourusername/auto-charge/issues).
