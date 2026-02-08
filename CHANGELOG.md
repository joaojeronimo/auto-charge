# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-04

### Added
- Initial release with two automation blueprints
- Auto-Charge Button Trigger blueprint
  - Configurable nighttime hours
  - Configurable export threshold
  - UI-based entity selection
- Auto-Charge Dynamic Current Adjustment blueprint
  - Real-time current adjustment based on solar export
  - Configurable voltage, buffer, and current limits
  - Smart logic: lowers immediately, raises after delay
  - Prevents oscillation with configurable raise delay
- Comprehensive documentation
- HACS integration support
- MIT License

### Features
- Fully configurable through Home Assistant UI
- No coding required
- Works with any compatible EV charger integration
- Bulletproof error handling
- Sensor availability checks
- Proper value clamping and safety limits

## [Unreleased]

### Planned
- Multiple charger support
- Historical tracking and statistics
- Cost calculation integration
- Weather forecast integration
- Machine learning optimization
