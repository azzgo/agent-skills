# Dot API Reference

This document provides detailed reference for the Dot API endpoints used in this skill.

## Base URL

```
https://api.mindreset.tech/api
```

## Authentication

All API requests require an API key in the Authorization header:

```
Authorization: Bearer {DOT_API_KEY}
```

## Endpoints

### List Devices

```
GET /quotes
```

Returns a list of all Quote/0 devices associated with the API key.

**Response:**
```json
[
  {
    "id": "device_serial_number",
    "name": "Device Name",
    "status": "online|offline",
    "firmware": "version",
    "last_seen": "timestamp"
  }
]
```

### Get Device Status

```
GET /quotes/{device_id}/status
```

Returns the current status of a specific device.

**Response:**
```json
{
  "id": "device_serial_number",
  "status": "online|offline",
  "battery": 85,
  "brightness": 50,
  "current_content": {
    "type": "text|image",
    "content": "content_data"
  },
  "last_updated": "timestamp"
}
```

### Display Text

```
POST /api/authV2/open/device/{device_id}/text
Content-Type: application/json
```

Display text content on the device.

**Request Body:**
```json
{
  "refreshNow": true,
  "title": "Title",
  "message": "Your text here",
  "signature": "Signature",
  "icon": "base64-encoded PNG",
  "link": "https://example.com",
  "taskKey": "task_identifier"
}
```

**Optional Fields:**
- `refreshNow`: Boolean, display immediately (default: true)
- `title`: Text title shown on screen
- `message`: Text content shown on screen (required)
- `signature`: Text signature shown on screen
- `icon`: Base64-encoded PNG icon data (40px×40px)
- `link`: http/https link or URL scheme for NFC tap
- `taskKey`: Specify which Text API content to update when multiple exist

### Display Image

```
POST /quotes/{device_id}/image
Content-Type: application/json
```

Display an image on the device.

**Request Body:**
```json
{
  "image_url": "https://example.com/image.png"
}
```

### Switch to Next Content

```
POST /quotes/{device_id}/next
```

Switches the device to display the next content item in the queue.

### List Device Tasks

```
GET /quotes/{device_id}/tasks
```

Returns a list of content tasks configured on the device.

**Response:**
```json
{
  "tasks": [
    {
      "id": "task_id",
      "name": "Task Name",
      "type": "text|image|rss",
      "schedule": "schedule_info",
      "enabled": true
    }
  ]
}
```

## Error Codes

- `401`: Unauthorized (invalid or missing API key)
- `404`: Device not found
- `400`: Bad request (invalid parameters)
- `500`: Server error

## Rate Limits

The API may have rate limits. Implement exponential backoff for retries.
