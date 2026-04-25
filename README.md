# Growappy - Custom Component for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

A custom integration for [Home Assistant](https://www.home-assistant.io/) that tracks student attendance status from the Growappy platform.

## Features

- **Binary Sensor:** Provides a real-time status of whether a student is currently checked into school.
  - `on`: Student is checked in.
  - `off`: Student is checked out / not in school.

## Installation

### Method 1: HACS (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed and configured in your Home Assistant instance.
2. Open **HACS** from your sidebar.
3. Click on **Integrations**.
4. Click the three dots (⋮) in the top right corner and select **Custom repositories**.
5. Paste the URL of this repository into the **Repository** field.
6. Select **Integration** as the Category and click **Add**.
7. Once added, find the **Growappy** integration in the list and click **Download**.
8. Restart Home Assistant.

### Method 2: Manual Installation

1. Download the `custom_components/growappy` folder from this repository.
2. Copy the folder into your Home Assistant's `custom_components` directory.
3. Restart Home Assistant.

## Configuration

Once the integration is installed and Home Assistant has restarted, you can configure it via the UI:

1. Navigate to **Settings** > **Devices & Services**.
2. Click **+ Add Integration**.
3. Search for **Growappy** and follow the prompts to enter your credentials.

## API Documentation

This integration interacts with the official Growappy API. For more technical details on the data structures and endpoints, refer to the official documentation:
[https://api.growappy.com/v2/api/doc](https://api.growappy.com/v2/api/doc)

## Disclaimer

**This is a personal project.** This integration is not affiliated with, maintained, authorized, endorsed, or sponsored by Growappy or any of its affiliates or subsidiaries. Use it at your own risk.
