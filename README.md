# CSV Populator

A Windows application for efficient CSV data entry with dynamic field creation, ID management, and template support. Code generated almost entirely by Cursor AI.

## Features

- Dynamic field creation with TAB navigation
- ID management with auto-incrementing
- Template system for field configurations
- Live CSV preview
- Desktop export by default

## Quick Start

```bash
# Run from source
python csv_populator.py

# Create executable (Windows)
build.bat
```

## Usage

1. Configure ID name and starting number
2. Enter field names and values (use TAB to navigate)
3. Press "New ID" to start next record
4. Click "Save to CSV" to export

## Requirements

- Python 3.8+ (for development)
- tkinter (included with Python)
