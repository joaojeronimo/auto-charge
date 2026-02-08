# Installation Guide

## Method 1: HACS (Recommended)

### Prerequisites
- Home Assistant installed and running
- HACS (Home Assistant Community Store) installed
  - If not installed, see: https://hacs.xyz/docs/setup/download

### Steps

1. **Open HACS**
   - Go to Home Assistant sidebar → **HACS**

2. **Add Custom Repository** (if not in default HACS)
   - Click the three dots menu (⋮) in the top right
   - Select **"Custom repositories"**
   - Add repository URL: `https://github.com/yourusername/auto-charge`
   - Category: **Automation**
   - Click **"Add"**

3. **Install Auto-Charge**
   - Go to HACS → **Automation** tab
   - Click **"Explore & Download Repositories"** (+)
   - Search for **"Auto-Charge"**
   - Click **"Download"**
   - Click **"Download"** again to confirm

4. **Restart Home Assistant**
   - Go to **Settings** → **System**
   - Click **"Restart"** (or use Developer Tools → YAML → Restart)

5. **Verify Installation**
   - Go to **Settings** → **Automations & Scenes**
   - Click **"Create Automation"** → **"Use a Blueprint"**
   - You should see **"Auto-Charge Button Trigger"** and **"Auto-Charge Dynamic Current Adjustment"**

## Method 2: Manual Installation

### Steps

1. **Download Blueprints**
   - Download the following files from the repository:
     - `blueprints/automation/auto_charge_button_trigger.yaml`
     - `blueprints/automation/auto_charge_dynamic_current.yaml`

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
   - Go to **Developer Tools** → **YAML**
   - Click **"Reload Automations"**
   - Or restart Home Assistant

5. **Verify Installation**
   - Same as HACS method step 5

## Next Steps

After installation, proceed to configure your automations:

### Configure Button Trigger

1. **Settings** → **Automations & Scenes** → **"Create Automation"**
2. Select **"Use a Blueprint"** → **"Auto-Charge Button Trigger"**
3. Fill in:
   - **Button Entity**: Your charger's start button (e.g., `button.charger_start`)
   - **Power Sensor**: Your grid power sensor (e.g., `sensor.grid_power`)
   - **Export Threshold**: e.g., `1000` (watts)
   - **Night Start**: e.g., `22:00:00`
   - **Night End**: e.g., `08:00:00`
4. Click **"Save"** and give it a name

### Configure Dynamic Current Adjustment

1. **Settings** → **Automations & Scenes** → **"Create Automation"**
2. Select **"Use a Blueprint"** → **"Auto-Charge Dynamic Current Adjustment"**
3. Fill in:
   - **Power Sensor**: Same as above (e.g., `sensor.grid_power`)
   - **Max Current Entity**: Your charger's current control (e.g., `number.charger_max_current`)
   - **Voltage**: Your grid voltage (e.g., `230` or `240`)
   - **Phases**: Number of phases (`1` for single-phase, `3` for three-phase)
   - **Power Buffer**: e.g., `100` (watts safety margin)
   - **Min Current**: e.g., `0` or `6` (amps, depending on your charger)
   - **Max Current**: e.g., `32` or `16` (amps, your charger's max)
   - **Adjustment Interval**: e.g., `/20` (every 20 seconds)
   - **Raise Delay**: e.g., `3` (minutes)
4. Click **"Save"** and give it a name

## Troubleshooting

### Blueprints Not Showing Up?
- Ensure files are in correct directory: `config/blueprints/automation/auto-charge/`
- Reload automations or restart Home Assistant
- Check file permissions (files should be readable)

### Can't Find My Entities?
- Make sure your charger integration is properly set up
- Check that entities exist in **Settings** → **Devices & Services** → **Entities**
- Power sensor should show negative values when exporting

### Need Help?
- Check the [full documentation](README.md)
- Review [troubleshooting section](README.md#troubleshooting)
- [Open an issue](https://github.com/yourusername/auto-charge/issues) on GitHub

## Updating

### HACS Update
1. Go to **HACS** → **Automation**
2. Find **"Auto-Charge"**
3. If update available, click **"Update"**
4. Restart Home Assistant

### Manual Update
1. Download latest blueprint files
2. Replace old files in `config/blueprints/automation/auto-charge/`
3. Reload automations or restart Home Assistant
4. Existing automations will automatically use new blueprint version
