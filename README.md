# CSV Populator - Field/Value Pairs

A Windows application built in Python that creates field name and value pairs for data entry and exports to CSV format with field names in the first row and values in the second row.

## Features

- **Field/Value Pairs**: Each row contains a field name and its corresponding value
- **Dynamic Row Creation**: Start with 1 row, new ones are created automatically as you navigate
- **Smart TAB Navigation**: TAB moves from field name to value, then to next row's field name
- **Template Loading**: Load predefined field names from JSON files
- **Template Saving**: Save current field names as reusable JSON templates
- **CSV Export**: Field names in first row, values in second row
- **Clean Interface**: Modern Windows-style interface with clear column headers

## How It Works

1. **Start Typing**: The application starts with focus on the first field name
2. **Navigate with TAB**: Press TAB to move from field name to value in the same row
3. **Create New Rows**: TAB from the value field creates a new row and focuses on its field name
4. **Delete Rows**: Use the × button to remove unwanted rows (minimum 1 row maintained)
5. **Load Templates**: Use "Load Template" to populate fields from predefined templates
6. **Save Templates**: Use "Save Template" to save current field names as reusable templates
7. **Save Data**: Click "Save to CSV" to export your data

## CSV Output Format

The application creates a CSV file with:

- **First row**: Field names (comma-separated)
- **Second row**: Corresponding values (comma-separated)

**Example:**

```
Field Name 1,Field Name 2,Field Name 3
Value 1,Value 2,Value 3
```

## Requirements

- Python 3.6 or higher
- Windows operating system
- No additional packages required (uses tkinter from Python standard library)

## Installation & Usage

1. **Clone or Download**: Get the `csv_populator.py` file
2. **Run the Application**:
   ```bash
   python csv_populator.py
   ```
3. **Enter Field Names**: Start with the field name in the first text box
4. **Enter Values**: Use TAB to move to the value field
5. **Create New Rows**: TAB from the value field to create a new row
6. **Load Templates**: Use "Load Template" to populate fields from predefined templates
7. **Save Templates**: Use "Save Template" to save current field names as reusable templates
8. **Save Data**: Click "Save to CSV" when done

## Template Files

The application supports loading and saving field names as JSON template files.

### JSON Templates

**Simple List Format:**

```json
["First Name", "Last Name", "Email", "Phone"]
```

**Dictionary Format (Recommended):**

```json
{
  "fields": ["Project Name", "Manager", "Start Date", "Budget"],
  "description": "Template created on 2024-01-15 14:30:25",
  "field_count": 4
}
```

### Saving Templates

Use the "Save Template" button to save your current field configuration as a JSON template file. This creates a reusable template that you can load later or share with others.

## Keyboard Shortcuts

- **TAB**: Move from field name to value, then to next row's field name
- **ENTER**: Same as TAB (alternative navigation)
- **Mouse**: Click on any field to focus it

## Navigation Flow

1. **Field Name** → TAB → **Value** (same row)
2. **Value** → TAB → **Field Name** (next row, creates new row if at last position)

## File Output

The application saves data to `csv_populator_output.csv` in the same directory where the script is run. Only rows with field names are included in the output.

## Customization

You can modify the application by editing the Python file:

- Change window size in the `geometry()` call
- Modify field widths in the `Entry` widget creation
- Adjust styling and colors
- Add additional functionality

## Troubleshooting

- **No GUI appears**: Ensure Python is installed with tkinter support
- **Rows not creating**: Check that you're pressing TAB from the value field of the last row
- **Save errors**: Ensure you have write permissions in the current directory

## License

This application is provided as-is for educational and personal use.
