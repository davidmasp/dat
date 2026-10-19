# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.2] - 2026-10-19

### Added

- Added the `figure-gallery` skill for building offline figure galleries in DAT
  atomic folders, with Git-tracked TOML legends, a shared HTML template, and a
  portable ZIP of linked figures.
- Documented the setup and rebuild workflow for figure galleries.

## [0.3.1] - 2026-10-15

### Removed

- Removed the DAT-provided template update workflow; generated projects are
  independent copies.

## [0.3.0] - 2026-10-15

### Added

- Added the `dat-atomic-folder` skill for creating and reviewing reproducible
  DAT analysis and data folders, including layout, dotenv, output, and Justfile
  conventions. It includes a scaffold helper for new atomic folders.
- Added the `just-sync` skill for adding documented rsync recipes to transfer
  selected inputs and outputs between a laptop and HPC system.
