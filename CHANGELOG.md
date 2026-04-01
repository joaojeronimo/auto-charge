# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-22

### Added
- Nightly Charge Dynamic Current blueprint
  - Grid import limiting with configurable max import power
  - Calculates base household load to determine charging headroom
  - Enable/disable switch via `input_boolean` helper
  - Configurable schedule, current limits, and raise delay
- Comprehensive documentation for both blueprints with formula explanations

### Changed
- Solar Dynamic Current formula now accounts for current charger draw
  - Old: `target = (export - buffer) / (voltage x phases)`
  - New: `target = (export + charger_draw - buffer) / (voltage x phases)`
  - Prevents the automation from getting stuck at low amps when surplus is available
- Solar Dynamic Current now outputs integer amps (was 1 decimal place)
- Solar Dynamic Current comparisons use integer math (was float)

### Removed
- Button Trigger blueprint references (was never a blueprint, only a raw automation example)

## [1.0.0] - 2026-02-04

### Added
- Initial release
- Auto-Charge Dynamic Current Adjustment blueprint
  - Real-time current adjustment based on solar export
  - Configurable voltage, buffer, and current limits
  - Smart logic: lowers immediately, raises after delay
  - Prevents oscillation with configurable raise delay
- HACS integration support
- MIT License

## [1.2.0] - 2026-02-23

### Added
- Solar Dynamic Current: Enable/disable switch via `input_boolean` helper (matches night charging)
- Solar Dynamic Current: Cloud resilience — only drops to minimum after 20s of sustained grid import
  - Brief cloud cover no longer causes unnecessary current drops to zero
  - Proportional lowering still happens immediately while exporting

### Changed
- Solar Dynamic Current now uses two triggers: periodic (every 20s) and sustained import (20s debounce)
- Both blueprints now require an `input_boolean` helper for enable/disable control
- Updated all documentation to reflect new enable switch and cloud resilience features

## [Unreleased]

### Changed
- Renamed "Nightly Charge Dynamic Current" blueprint to **"Grid Charge"** (`grid_charge.yaml`)
- Added **Energy Price Sensor** input — sensor showing current energy price in €/kWh
- Added **Maximum Energy Price** input — configurable price cap for charging (default: 0.10 €/kWh)
- Removed schedule start/end time inputs from Grid Charge (charging is now controlled by enable switch and energy price)
- Solar Dynamic Current now actively returns the charger to `min_current` when disabled or when the schedule window ends
- Solar Dynamic Current now enforces the configured `max_current` immediately instead of waiting on the import debounce path

### Planned
- Multiple charger support
- Historical tracking and statistics
- Cost calculation integration
