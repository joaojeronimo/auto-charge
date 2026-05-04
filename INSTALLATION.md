# Installation Guide

## Prerequisites

- Home Assistant installed and running
- An EV charger integration with a **number entity** for current control
- A **power sensor** showing grid import/export if you use the solar charging blueprint
- A **Goodwe EMS mode select entity** for grid charging
- A battery maximum charge **number entity** if you use the battery preservation blueprint
- An **`input_boolean` helper** for each blueprint that uses a dashboard toggle (created in steps below)

## Method 1: Blueprint Import (Recommended)

### Steps

1. **Open Blueprints**
   - Go to **Settings** > **Automations & Scenes** > **Blueprints**

2. **Import Solar Charge Dynamic Current Blueprint**
   - Click **"Import Blueprint"** (bottom right)
   - Paste the URL:
     ```
     https://github.com/yourusername/auto-charge/blob/main/blueprints/automation/solar_charge_dynamic_current.yaml
     ```
   - Click **"Preview"** then **"Import"**

3. **Import Grid Charge Blueprint**
   - Click **"Import Blueprint"** again
   - Paste the URL:
     ```
     https://github.com/yourusername/auto-charge/blob/main/blueprints/automation/grid_charge.yaml
     ```
   - Click **"Preview"** then **"Import"**

4. **Import Battery Discharge Power Toggle Blueprint**
   - Click **"Import Blueprint"** again
   - Paste the URL:
     ```
     https://github.com/yourusername/auto-charge/blob/main/blueprints/automation/battery_discharge_power_toggle.yaml
     ```
   - Click **"Preview"** then **"Import"**

5. **Import Battery Preservation Max Charge Blueprint**
   - Click **"Import Blueprint"** again
   - Paste the URL:
     ```
     https://github.com/yourusername/auto-charge/blob/main/blueprints/automation/battery_preservation_max_charge.yaml
     ```
   - Click **"Preview"** then **"Import"**

6. **Verify Installation**
   - Go to **Settings** > **Automations & Scenes**
   - Click **"Create Automation"** > **"Use a Blueprint"**
   - You should see **"Solar Charge Dynamic Current"**, **"Grid Charge"**, **"Battery Discharge Power Toggle"**, and **"Battery Preservation Max Charge"**

## Method 2: Manual Installation

### Steps

1. **Download Blueprints**
   - Download the following files from the repository:
     - `blueprints/automation/solar_charge_dynamic_current.yaml`
     - `blueprints/automation/grid_charge.yaml`
     - `blueprints/automation/battery_discharge_power_toggle.yaml`
     - `blueprints/automation/battery_preservation_max_charge.yaml`

2. **Create Directory**
   - Navigate to your Home Assistant config directory
   - Create directory structure:
     ```
     config/
     └── blueprints/
         └── automation/
             └── auto-charge/
     ```

3. **Copy Files**
   - Copy the blueprint YAML files to:
     ```
     config/blueprints/automation/auto-charge/
     ```

4. **Reload Automations**
   - Go to **Developer Tools** > **YAML**
   - Click **"Reload Automations"**
   - Or restart Home Assistant

5. **Verify Installation**
   - Same as Method 1 step 6

## Next Steps

### Create Enable Switches (Required Where Used)

Before configuring the blueprints that use dashboard toggles, create `input_boolean` helpers for each mode you want:

1. Go to **Settings** > **Devices & Services** > **Helpers**
2. Click **"+ Create Helper"** > **"Toggle"**
3. Name it **"Solar Charge Enable"**
4. Save it
5. Repeat and create another toggle named **"Grid Charge Enable"**
6. If you want the battery toggle, create another helper such as **"Battery Discharge Hold"**

These toggle switches let you turn each charging mode on and off independently. You can add them to your dashboard for easy access.
When the solar charge switch is turned off, the blueprint sets the charger current to `0`.
The battery preservation blueprint does not need an `input_boolean`; disabling the automation itself stops it from managing the max charge limit.

### Configure Solar Charge Dynamic Current

1. **Settings** > **Automations & Scenes** > **"Create Automation"**
2. Select **"Use a Blueprint"** > **"Solar Charge Dynamic Current"**
3. Fill in:
   - **Power Sensor**: Your grid power sensor (e.g., `sensor.grid_power`) — must be negative when exporting
   - **Max Current Entity**: Your charger's current control (e.g., `number.charger_max_current`)
   - **Solar Charge Enable Switch**: The `input_boolean` you created above (e.g., `input_boolean.solar_charge_enable`)
   - **Voltage**: Your grid voltage (e.g., `230` or `240`)
   - **Phases**: Number of phases (`1` for single-phase, `3` for three-phase)
   - **Power Buffer**: Safety margin in Watts (e.g., `100`)
   - **Min Current**: Minimum amps while solar charge is active (e.g., `0` or `6` depending on your charger)
   - **Max Current**: Maximum amps (e.g., `16` or `32`)
   - **Schedule Start/End**: Time window for solar charging (e.g., `09:00` to `22:00`)
4. Click **"Save"** and give it a name

### Configure Grid Charge

1. **Settings** > **Automations & Scenes** > **"Create Automation"**
2. Select **"Use a Blueprint"** > **"Grid Charge"**
3. Fill in:
   - **Energy Price Sensor**: Sensor showing current energy price in €/kWh (e.g., `sensor.coopernico_go_total`)
   - **Maximum Energy Price**: Maximum price at which charging is allowed in €/kWh (e.g., `0.10`)
   - **Maximum Current Control**: Your charger's current control (e.g., `number.charger_max_current`)
   - **Maximum Current**: Current to use while grid charging is allowed (e.g., `16` or `32`)
   - **Grid Charge Enable Switch**: The `input_boolean` you created above (e.g., `input_boolean.grid_charge_enable`)
   - **Goodwe EMS Mode Entity**: Your Goodwe EMS mode select entity (e.g., `select.goodwe_ems_mode`)
   - **EMS Mode When Grid Charge Is Active**: Usually `backup` for the Home Assistant GoodWe integration
   - **EMS Mode When Grid Charge Is Inactive**: Usually `general` for the Home Assistant GoodWe integration
4. Click **"Save"** and give it a name

The grid charge enable switch is the only helper this blueprint needs. When it is ON, cheap prices can start grid charging. When it is OFF, cheap prices will not start grid charging. The automation uses the configured active EMS mode to detect whether grid charging is currently active; if the price rises above your threshold during an active grid-charge session, it sets charger current to `0` and restores EMS mode to the configured inactive option.

### Configure Battery Discharge Power Toggle

1. **Settings** > **Automations & Scenes** > **"Create Automation"**
2. Select **"Use a Blueprint"** > **"Battery Discharge Power Toggle"**
3. Fill in:
   - **Toggle Helper**: Your battery stop/normal `input_boolean` (e.g., `input_boolean.battery_discharge_hold`)
   - **Discharge Power Entity**: Your inverter's battery discharge power `number` entity (e.g., `number.battery_discharge_power`)
   - **Electricity Price Sensor**: Your current electricity price sensor (e.g., `sensor.coopernico_go_total`)
   - **Price Threshold**: If price is at or above this value, discharge is enabled automatically (e.g., `0.10`)
   - **Stopped Discharge Power**: Usually `0`
   - **Normal Discharge Power**: Your usual discharge limit in Watts (e.g., `5000`)
4. Click **"Save"** and give it a name

### Configure Battery Preservation Max Charge

1. **Settings** > **Automations & Scenes** > **"Create Automation"**
2. Select **"Use a Blueprint"** > **"Battery Preservation Max Charge"**
3. Fill in:
   - **Battery Max Charge Entity**: Your battery maximum charge percentage number entity (e.g., `number.battery_max_charge`)
   - **Normal Maximum Charge**: The normal daily charge limit, such as `95`
   - **Preservation Maximum Charge**: The lower limit to use during the preservation window, such as `90`
   - **Preservation Start Time**: When to lower the limit, such as `16:00:00`
   - **Normal Restore Time**: When to restore the normal limit, such as `00:00:00`
4. Click **"Save"** and give it a name

## Troubleshooting

### Blueprints Not Showing Up?
- Ensure files are in correct directory: `config/blueprints/automation/auto-charge/`
- Reload automations or restart Home Assistant
- Check file permissions (files should be readable)

### Can't Find My Entities?
- Make sure your charger integration is properly set up
- Check that entities exist in **Settings** > **Devices & Services** > **Entities**
- The solar charging power sensor should show negative values when exporting
- The Goodwe EMS mode entity should be a `select` entity
- The battery preservation max charge entity should be a writable `number` entity

### Enable Switch Not Listed?
- Make sure you created an `input_boolean` helper (not an `input_select` or other type)
- The entity selector filters by `input_boolean` domain — only toggle helpers will appear
- You need a separate `input_boolean` for each toggle-based blueprint (for example solar charge, grid charge, and battery discharge hold)

### Need Help?
- Check the [full documentation](README.md)
- Review [configuration examples](EXAMPLES.md)
- [Open an issue](https://github.com/yourusername/auto-charge/issues) on GitHub

## Updating

### Blueprint Import Update
1. Go to **Settings** > **Automations & Scenes** > **Blueprints**
2. Find the Auto-Charge blueprints
3. If an update is available, a notification will appear
4. Click to update — existing automations will use the new version automatically

### Manual Update
1. Download latest blueprint files
2. Replace old files in `config/blueprints/automation/auto-charge/`
3. Reload automations or restart Home Assistant
4. Existing automations will automatically use new blueprint version
