---
name: quote0-dot-screen
description: Control Quote/0 electronic screen devices via Dot API. Use when the user needs to interact with Quote/0 devices for: (1) Getting device information or status, (2) Displaying text content, (3) Displaying images, (4) Switching content, (5) Listing device tasks, (6) Managing devices via API
---

# Quote/0 Dot Screen Controller

## Overview

This skill provides control over Quote/0 electronic screen devices through the Dot Developer Platform APIs.

## Prerequisites

### API Key Setup

Check for `DOT_API_KEY` environment variable. If not set, guide the user to:
1. Visit https://dot.mindreset.tech/docs/service/open/get_api
2. Create an API key in the Dot. App
3. Export the key: `export DOT_API_KEY=xxx`

## Core Operations

### Device Management

**Get Device Serial Number**
- API: https://dot.mindreset.tech/docs/service/open/get_device_id
- Purpose: Retrieve device identifier for targeting specific devices

**List Devices**
- API: https://dot.mindreset.tech/docs/service/open/list_devices_api
- Purpose: Get all available devices and their information

**Get Device Status**
- API: https://dot.mindreset.tech/docs/service/open/device_status_api
- Purpose: Query device current state and connection status

### Content Control

**Display Text**
- API: https://dot.mindreset.tech/docs/service/open/text_api
- Purpose: Show text content on device screen
- Script: `scripts/display_text.py`

**Display Image**
- API: https://dot.mindreset.tech/docs/service/open/image_api
- Purpose: Show image content on device screen
- Script: `scripts/display_image.py`

**Switch to Next Content**
- API: https://dot.mindreset.tech/docs/service/open/device_next_api
- Purpose: Navigate to next content item
- Script: `scripts/switch_next.py`

**List Device Tasks**
- API: https://dot.mindreset.tech/docs/service/open/list_device_tasks_api
- Purpose: Get list of content tasks on device

