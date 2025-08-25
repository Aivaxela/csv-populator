# CSV Populator

A Windows application for efficient CSV data entry with dynamic field creation, ID management, and template support. Code generated almost entirely by Cursor AI.

## Features

- **Dynamic Fields**: Automatically creates new field/value pairs as you tab through
- **Smart Navigation**: TAB skips filled fields and creates new rows when needed
- **ID Management**: Supports alphanumeric IDs (e.g., "WO123" → "WO124")
- **Template System**: Load/save field templates as JSON files
- **Live Preview**: Real-time CSV preview as you enter data
- **Record Accumulation**: Build multiple records before export

## Usage

1. **Configure ID**: Enter ID name (e.g., "ID") and starting number (e.g., "123")
2. **Enter Data**: Type field names and values, use TAB to navigate
3. **New ID**: Press "New ID" button or Ctrl+Shift+N to start next record
4. **Export**: Click "Save to CSV" to export all accumulated records

## Keyboard Shortcuts

- **TAB**: Navigate between fields, skip filled fields, create new rows
- **Ctrl+Shift+N**: Create new ID and clear values
- **ENTER**: Same as TAB

## Requirements

- Python 3.x
- tkinter (included with Python)

## Running

```bash
python csv_populator.py
```

The application creates `csv_populator_output.csv` in the same directory when exporting.
