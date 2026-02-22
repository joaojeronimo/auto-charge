# Installation Guide

## Prerequisites

- Home Assistant installed and running
- An EV charger integration with a **number entity** for current control
- A **power sensor** showing grid import/export
- For night charging: an **`input_boolean` helper** (created in step below)

## Method 1: Blueprint Import (Recommended)

### Steps

1. **Open Blueprints**
   - Go to **Settings** > **Automations & Scenes** > **Blueprints**

2. **Import Solar Dynamic Current Blueprint**
   - Click **"Import Blueprint"** (bottom right)
   - Paste the URL:
     ```
     https://github.com/yourusername/auto-charge/blob/main/blueprints/automation/auto_charge_dynamic_current.yaml
     ```
   - Click **"Preview"** then **"Import"**

3. **Import Nightly Charge Blueprint**
   - Click **"Import Blueprint"** again
   - Paste the URL:
     ```
     https://github.com/yourusername/auto-charge/blob/main/blueprints/automation/night_charge_dynamic_current.yaml
     ```
   - Click **"Preview"** then **"Import"**

4. **Verify Installation**
   - Go to **Settings** > **Automations & Scenes**
   - Click **"Create Automation"** > **"Use a Blueprint"**
   - You should see **"Auto-Charge Dynamic Current Adjustment"** and **"Nightly Charge Dynamic Current"**

## Method 2: Manual Installation

### Steps

1. **Download Blueprints**
   - Download the following files from the repository:
     - `blueprints/automation/auto_charge_dynamic_current.yaml`
     - `blueprints/automation/night_charge_dynamic_current.yaml`

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
   - Copy both blueprint YAML files to:
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

### Create Night Charge Enable Switch (Required for Night Charging)

Before configuring the nightly charge blueprint, create an `input_boolean` helper:

1. Go to **Settings** > **Devices & Services** > **Helpers**
2. Click **"+ Create Helper"** > **"Toggle"**
3. Name it something like **"Night Charge Enable"**
4. Save it

This toggle switch lets you turn night charging on and off. You can add it to your dashboard for easy access.

### Configure Solar Dynamic Current

1. **Settings** > **Automations & Scenes** > **"Create Automation"**
2. Select **"Use a Blueprint"** > **"Auto-Charge Dynamic Current Adjustment"**
3. Fill in:
   - **Power Sensor**: Your grid power sensor (e.g., `sensor.grid_power`) — must be negative when exporting
   - **Max Current Entity**: Your charger's current control (e.g., `number.charger_max_current`)
   - **Voltage**: Your grid voltage (e.g., `230` or `240`)
   - **Phases**: Number of phases (`1` for single-phase, `3` for three-phase)
   - **Power Buffer**: Safety margin in Watts (e.g., `100`)
   - **Min Current**: Minimum amps (e.g., `0` or `6` depending on your charger)
   - **Max Current**: Maximum amps (e.g., `16` or `32`)
   - **Raise Delay**: Minutes to wait before raising current (e.g., `3`)
   - **Schedule Start/End**: Time window for solar charging (e.g., `09:00` to `22:00`)
4. Click **"Save"** and give it a name

### Configure Nightly Charge

1. **Settings** > **Automations & Scenes** > **"Create Automation"**
2. Select **"Use a Blueprint"** > **"Nightly Charge Dynamic Current"**
3. Fill in:
   - **Power Sensor**: Your grid power sensor (e.g., `sensor.grid_power`) — positive when importing
   - **Max Current Entity**: Your charger's current control (e.g., `number.charger_max_current`)
   - **Night Charge Enable Switch**: The `input_boolean` you created above (e.g., `input_boolean.night_charge_enable`)
   - **Maximum Import Power**: Your grid import cap in Watts (e.g., `3000`)
   - **Voltage**: Your grid voltage (e.g., `230` or `240`)
   - **Phases**: Number of phases (`1` or `3`)
   - **Power Buffer**: Safety margin below import limit (e.g., `400`)
   - **Min Current**: Minimum amps (e.g., `0`)
   - **Max Current**: Maximum amps (e.g., `32`)
   - **Raise Delay**: Minutes to wait before raising current (e.g., `3`)
   - **Schedule Start/End**: Night charging window (e.g., `22:00` to `08:00`)
4. Click **"Save"** and give it a name

## Troubleshooting

### Blueprints Not Showing Up?
- Ensure files are in correct directory: `config/blueprints/automation/auto-charge/`
- Reload automations or restart Home Assistant
- Check file permissions (files should be readable)

### Can't Find My Entities?
- Make sure your charger integration is properly set up
- Check that entities exist in **Settings** > **Devices & Services** > **Entities**
- Power sensor should show negative values when exporting (solar) or positive when importing (night)

### Night Charge Enable Switch Not Listed?
- Make sure you created an `input_boolean` helper (not an `input_select` or other type)
- The entity selector filters by `input_boolean` domain — only toggle helpers will appear

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
