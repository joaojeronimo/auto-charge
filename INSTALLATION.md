# Installation Guide

## Prerequisites

- Home Assistant installed and running
- An EV charger integration with a **number entity** for current control
- A **power sensor** showing grid import/export if you use the solar charging blueprint
- A **Goodwe EMS mode select entity** for grid charging
- An **`input_boolean` helper** for each blueprint or toggle automation (created in steps below)

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

5. **Verify Installation**
   - Go to **Settings** > **Automations & Scenes**
   - Click **"Create Automation"** > **"Use a Blueprint"**
   - You should see **"Solar Charge Dynamic Current"**, **"Grid Charge"**, and **"Battery Discharge Power Toggle"**

## Method 2: Manual Installation

### Steps

1. **Download Blueprints**
   - Download the following files from the repository:
     - `blueprints/automation/solar_charge_dynamic_current.yaml`
     - `blueprints/automation/grid_charge.yaml`
     - `blueprints/automation/battery_discharge_power_toggle.yaml`

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
   - Same as Method 1 step 4

## Next Steps

### Create Enable Switches (Required for Both Blueprints)

Before configuring the blueprints, create `input_boolean` helpers for each mode you want:

1. Go to **Settings** > **Devices & Services** > **Helpers**
2. Click **"+ Create Helper"** > **"Toggle"**
3. Name it **"Solar Charge Enable"**
4. Save it
5. Repeat and create another toggle named **"Grid Charge Enable"**
6. If you want the battery toggle, create another helper such as **"Battery Discharge Hold"**

These toggle switches let you turn each charging mode on and off independently. You can add them to your dashboard for easy access.
When the solar charge switch is turned off, the blueprint sets the charger current to `0`.

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
   - **EMS Mode When Grid Charge Is Active**: Usually `Battery standby`
   - **EMS Mode When Grid Charge Is Inactive**: Usually `Auto`
4. Click **"Save"** and give it a name

The grid charge enable switch starts one grid-charge session and also tracks whether that session is active. When it is OFF, cheap prices will not start grid charging and the grid automation leaves the charger current unchanged. When the price rises above your threshold, the automation sets charger current to `0`, restores EMS mode to `Auto`, and turns the enable switch OFF.

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

### Enable Switch Not Listed?
- Make sure you created an `input_boolean` helper (not an `input_select` or other type)
- The entity selector filters by `input_boolean` domain — only toggle helpers will appear
- You need a separate `input_boolean` for each blueprint (solar and grid charge)

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
