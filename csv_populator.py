import tkinter as tk
from tkinter import ttk
import json
import os
import re
from datetime import datetime

class CSVPopulatorApp:
    """CSV data entry application with dynamic field creation, ID management, and template support."""
    
    def __init__(self, root):
        self.root = root
        self.field_pairs = []
        self.all_records = []
        
        self._setup_ui()
        self._initialize_data()
        self._bind_events()
    
    def _setup_ui(self):
        """Initialize all UI components."""
        self._setup_window()
        self._setup_main_frame()
        self._create_id_config_section()
        self._create_fields_section()
        self._create_preview_section()
        self._create_buttons_section()
        self._create_status_section()
    
    def _setup_window(self):
        """Configure main window properties."""
        self.root.title("CSV Populator")
        self.root.geometry("620x700")
        self.root.resizable(False, True)
        self.root.configure(bg='#f0f0f0')
    
    def _setup_main_frame(self):
        """Create and configure main application frame."""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
    
    def _create_id_config_section(self):
        """Create ID configuration section with name, number, and current ID display."""
        self.id_config_frame = ttk.Frame(self.main_frame)
        self.id_config_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.id_config_frame.columnconfigure(1, weight=1)
        self.id_config_frame.columnconfigure(3, weight=1)
        
        # ID Name configuration
        self.starting_id_name_label = ttk.Label(
            self.id_config_frame, 
            text="Starting ID Name:", 
            font=("Arial", 10, "bold")
        )
        self.starting_id_name_label.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        self.starting_id_name_entry = ttk.Entry(self.id_config_frame, width=15)
        self.starting_id_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        self.starting_id_name_entry.bind('<KeyRelease>', self._update_current_id_display)
        
        # ID Number configuration
        self.starting_id_number_label = ttk.Label(
            self.id_config_frame, 
            text="Starting ID Number:", 
            font=("Arial", 10, "bold")
        )
        self.starting_id_number_label.grid(row=0, column=2, padx=(0, 10), sticky=tk.W)
        
        self.starting_id_number_entry = ttk.Entry(self.id_config_frame, width=15)
        self.starting_id_number_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 20))
        self.starting_id_number_entry.bind('<KeyRelease>', self._update_current_id_display)
        
        # Current ID display
        self.current_id_label = ttk.Label(
            self.id_config_frame, 
            text="Current ID: ", 
            font=("Arial", 10, "bold"), 
            foreground="gray"
        )
        self.current_id_label.grid(row=1, column=0, columnspan=4, pady=(0, 10), sticky=tk.W)
        
        # Output file configuration
        self.filename_label = ttk.Label(
            self.id_config_frame, 
            text="Output File Path:", 
            font=("Arial", 10, "bold")
        )
        self.filename_label.grid(row=2, column=0, padx=(0, 10), sticky=tk.W)
        
        self.filename_entry = ttk.Entry(self.id_config_frame, width=35)
        self.filename_entry.grid(row=2, column=1, columnspan=3, sticky=(tk.W, tk.E), padx=(0, 20), pady=(0, 10))
        
        # Help text
        help_text = "Enter full path or just filename (will save to Desktop)"
        self.filename_help = ttk.Label(
            self.id_config_frame, 
            text=help_text, 
            font=("Arial", 8), 
            foreground="gray"
        )
        self.filename_help.grid(row=3, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))
        
        # Set default filename
        default_filename = os.path.join(self._get_desktop_path(), "output.csv")
        self.filename_entry.insert(0, default_filename)
    
    def _create_fields_section(self):
        """Create scrollable fields section with headers and initial field pair."""
        self.fields_frame = ttk.Frame(self.main_frame)
        self.fields_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.fields_frame.columnconfigure(1, weight=1)
        self.fields_frame.columnconfigure(3, weight=1)
        
        self._setup_scrollable_canvas()
        self._create_field_headers()
    
    def _setup_scrollable_canvas(self):
        """Setup canvas and scrollbar for dynamic field content."""
        self.canvas = tk.Canvas(self.fields_frame)
        self.scrollbar = ttk.Scrollbar(self.fields_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        for i in range(4):
            self.scrollable_frame.columnconfigure(i, weight=1)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=1, column=4, sticky=(tk.N, tk.S))
        
        self.fields_frame.columnconfigure(0, weight=1)
        self.fields_frame.rowconfigure(1, weight=1)
        
        # Bind mouse wheel events
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)
    
    def _create_field_headers(self):
        """Create field name and value headers."""
        self.field_header = ttk.Label(
            self.fields_frame,
            text="Field Name:",
            font=("Arial", 10, "bold")
        )
        self.field_header.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        self.value_header = ttk.Label(
            self.fields_frame,
            text="Value:",
            font=("Arial", 10, "bold")
        )
        self.value_header.grid(row=0, column=2, columnspan=2, sticky=tk.W)
    
    def _create_preview_section(self):
        """Create CSV preview section with scrollable text display."""
        self.preview_frame = ttk.Frame(self.main_frame)
        self.preview_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.preview_frame.columnconfigure(0, weight=1)
        self.preview_frame.rowconfigure(1, weight=1)
        
        self.preview_label = ttk.Label(
            self.preview_frame, 
            text="Preview:", 
            font=("Arial", 10, "bold")
        )
        self.preview_label.grid(row=0, column=0, sticky=tk.W)
        
        self.preview_canvas = tk.Canvas(self.preview_frame, height=150)
        self.preview_scrollbar = ttk.Scrollbar(
            self.preview_frame, 
            orient="vertical", 
            command=self.preview_canvas.yview
        )
        self.preview_text = tk.Text(
            self.preview_canvas, 
            wrap=tk.NONE, 
            height=8, 
            state=tk.DISABLED
        )
        
        self.preview_text.configure(yscrollcommand=self.preview_scrollbar.set)
        self.preview_canvas.create_window((0, 0), window=self.preview_text, anchor="nw")
        self.preview_canvas.configure(yscrollcommand=self.preview_scrollbar.set)
        
        self.preview_text.bind(
            '<Configure>', 
            lambda e: self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))
        )
        
        self.preview_canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.preview_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        self.preview_frame.columnconfigure(0, weight=1)
        self.preview_frame.rowconfigure(1, weight=1)
    
    def _create_buttons_section(self):
        """Create button section with all application controls."""
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.grid(row=6, column=0)
        
        buttons = [
            ("Save to CSV", self._save_to_csv),
            ("Load Template", self._load_template),
            ("Save Template", self._save_template),
            ("New ID (Ctrl+Shift+N)", self._new_id),
            ("Clear All", self._clear_all_fields)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(self.buttons_frame, text=text, command=command)
            if i < len(buttons) - 1:
                btn.pack(side=tk.LEFT, padx=(0, 10))
            else:
                btn.pack(side=tk.LEFT)
    
    def _create_status_section(self):
        """Create status label for user feedback."""
        self.status_label = ttk.Label(
            self.main_frame, 
            text="Ready", 
            font=("Arial", 9)
        )
        self.status_label.grid(row=7, column=0)
    
    def _initialize_data(self):
        """Initialize application data and create first field pair."""
        self._create_field_pair()
        self._update_current_id_display()
        self._update_csv_preview()
        self.starting_id_name_entry.focus_set()
    
    def _bind_events(self):
        """Bind keyboard shortcuts and events."""
        self.root.bind('<Tab>', self._handle_tab)
        self.root.bind('<Control-Shift-N>', self._new_id)
        self.main_frame.rowconfigure(4, weight=1)
    
    def _get_desktop_path(self):
        """Get the user's desktop path with fallback."""
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        return desktop if os.path.exists(desktop) else os.getcwd()
    
    def _get_current_id(self):
        """Get the current ID number from the entry field."""
        id_text = self.starting_id_number_entry.get().strip()
        return id_text if id_text else None
    
    def _update_current_id_display(self, event=None):
        """Update the current ID display label."""
        id_name = self.starting_id_name_entry.get().strip()
        current_id = self._get_current_id()
        
        if id_name and current_id is not None:
            self.current_id_label.config(text=f"Current ID: {current_id}")
        elif id_name:
            self.current_id_label.config(text=f"Current ID: {id_name} (no number)")
        elif current_id is not None:
            self.current_id_label.config(text=f"Current ID: {current_id} (no name)")
        else:
            self.current_id_label.config(text="Current ID: (not configured)")
    
    def _increment_id(self, current_id):
        """Increment alphanumeric ID by extracting numeric part and adding 1."""
        if not current_id:
            return None
        
        match = re.match(r'^([A-Za-z]*)(\d+)$', current_id)
        if match:
            prefix = match.group(1)
            number = int(match.group(2))
            return f"{prefix}{number + 1}"
        return current_id
    
    def _update_csv_preview(self):
        """Update the CSV preview text display."""
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        
        if not self.all_records:
            self.preview_text.insert(tk.END, "No records yet. Complete a row and press 'New ID' to see preview.")
        else:
            for record in self.all_records:
                field_names = record['field_names']
                values = record['values']
                
                self.preview_text.insert(tk.END, ','.join(field_names) + '\n')
                self.preview_text.insert(tk.END, ','.join(values) + '\n')
        
        self.preview_text.config(state=tk.DISABLED)
        self.preview_text.see(tk.END)
    
    def _create_field_pair(self):
        """Create a new field name/value pair row."""
        row = len(self.field_pairs) + 1
        
        pair_frame = ttk.Frame(self.scrollable_frame)
        pair_frame.grid(row=row, column=0, columnspan=4, sticky=(tk.W, tk.E))
        pair_frame.columnconfigure(0, weight=0)
        pair_frame.columnconfigure(1, weight=1)
        pair_frame.columnconfigure(2, weight=0)
        pair_frame.columnconfigure(3, weight=1)
        pair_frame.columnconfigure(4, weight=0)
        
        row_label = ttk.Label(pair_frame, text=f"Row {row}:")
        row_label.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        field_entry = ttk.Entry(pair_frame, width=30)
        field_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 20))
        
        value_entry = ttk.Entry(pair_frame, width=30)
        value_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(0, 10))
        
        current_index = len(self.field_pairs)
        delete_btn = ttk.Button(
            pair_frame, 
            text="×", 
            width=3,
            command=lambda idx=current_index: self._delete_field_pair(idx)
        )
        delete_btn.grid(row=0, column=4, padx=(10, 0))
        
        pair_data = {
            'frame': pair_frame,
            'field_entry': field_entry,
            'value_entry': value_entry,
            'row_label': row_label,
            'delete_btn': delete_btn
        }
        
        self.field_pairs.append(pair_data)
        
        # Bind events
        field_entry.bind('<Tab>', self._handle_tab)
        field_entry.bind('<Return>', self._handle_enter)
        value_entry.bind('<Tab>', self._handle_tab)
        value_entry.bind('<Return>', self._handle_enter)
        
        # Update scroll region and scroll to bottom
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()
        self.root.after(10, lambda: self.canvas.yview_moveto(1.0))
        
        return field_entry, value_entry
    
    def _handle_tab(self, event):
        """Handle TAB navigation with smart field skipping and new row creation."""
        current_widget = event.widget
        
        current_pair_index = None
        is_field_entry = False
        
        for i, pair in enumerate(self.field_pairs):
            if pair['field_entry'] == current_widget:
                current_pair_index = i
                is_field_entry = True
                break
            elif pair['value_entry'] == current_widget:
                current_pair_index = i
                is_field_entry = False
                break
        
        if current_pair_index is not None:
            if is_field_entry:
                if self.field_pairs[current_pair_index]['field_entry'].get().strip():
                    next_field = self._find_next_empty_field(current_pair_index, is_field_entry)
                    if next_field:
                        next_field.focus_set()
                        return "break"
                else:
                    self.field_pairs[current_pair_index]['value_entry'].focus_set()
                    return "break"
            else:
                if self.field_pairs[current_pair_index]['value_entry'].get().strip():
                    if current_pair_index == len(self.field_pairs) - 1:
                        new_field, new_value = self._create_field_pair()
                        new_field.focus_set()
                        self._update_row_labels()
                        return "break"
                    else:
                        next_field = self._find_next_empty_field(current_pair_index, is_field_entry)
                        if next_field:
                            next_field.focus_set()
                            return "break"
                else:
                    if current_pair_index == len(self.field_pairs) - 1:
                        new_field, new_value = self._create_field_pair()
                        new_field.focus_set()
                        self._update_row_labels()
                        return "break"
                    else:
                        next_pair_index = current_pair_index + 1
                        self.field_pairs[next_pair_index]['field_entry'].focus_set()
                        return "break"
        
        return None
    
    def _find_topmost_empty_field(self):
        """Find the first empty field from the top."""
        for pair in self.field_pairs:
            if not pair['field_entry'].get().strip():
                return pair['field_entry']
            elif not pair['value_entry'].get().strip():
                return pair['value_entry']
        return None
    
    def _find_next_empty_field(self, current_pair_index, is_field_entry):
        """Find next empty field while preventing infinite loops."""
        visited = set()
        current_index = current_pair_index
        current_is_field = is_field_entry
        
        while True:
            if current_is_field:
                current_field = self.field_pairs[current_index]['field_entry']
                current_value = self.field_pairs[current_index]['value_entry']
                
                if not current_field.get().strip():
                    return current_field
                elif not current_value.get().strip():
                    return current_value
                else:
                    current_is_field = False
            else:
                if current_index == len(self.field_pairs) - 1:
                    return None
                else:
                    current_index += 1
                    current_is_field = True
            
            visited_key = (current_index, current_is_field)
            if visited_key in visited:
                return None
            visited.add(visited_key)
    
    def _handle_enter(self, event):
        """Handle Enter key same as Tab."""
        return self._handle_tab(event)
    
    def _delete_field_pair(self, index):
        """Delete a field pair at the specified index."""
        if len(self.field_pairs) <= 1:
            return
        
        self.field_pairs[index]['frame'].destroy()
        del self.field_pairs[index]
        
        self._update_row_labels()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.status_label.config(text=f"Deleted row {index + 1}")
    
    def _update_row_labels(self):
        """Update row labels after deletion."""
        for i, pair in enumerate(self.field_pairs):
            pair['row_label'].config(text=f"Row {i + 1}:")
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _save_current_record(self):
        """Save the current form data as a record."""
        field_names = []
        values = []
        
        id_name = self.starting_id_name_entry.get().strip()
        current_id = self._get_current_id()
        
        if id_name and current_id is not None:
            field_names.append(id_name)
            values.append(str(current_id))
        
        for pair in self.field_pairs:
            field_name = pair['field_entry'].get().strip()
            value = pair['value_entry'].get().strip()
            
            if field_name and value:
                field_names.append(field_name)
                values.append(value)
        
        if len(field_names) > 1:
            record = {
                'field_names': field_names,
                'values': values
            }
            self.all_records.append(record)
            self._update_csv_preview()
    
    def _new_id(self, event=None):
        """Create a new ID and save the current record."""
        id_name = self.starting_id_name_entry.get().strip()
        current_id = self._get_current_id()
        
        if not id_name or current_id is None:
            self.status_label.config(text="Please configure both ID name and number first")
            return
        
        self._save_current_record()
        
        new_id = self._increment_id(current_id)
        
        if new_id:
            self.starting_id_number_entry.delete(0, tk.END)
            self.starting_id_number_entry.insert(0, new_id)
        else:
            self.status_label.config(text="Could not increment ID format")
            return
        
        # Clear value fields
        for pair in self.field_pairs:
            pair['value_entry'].delete(0, tk.END)
        
        # Focus on first empty field
        if self.field_pairs:
            topmost_empty = self._find_topmost_empty_field()
            if topmost_empty:
                topmost_empty.focus_set()
            else:
                self.field_pairs[0]['field_entry'].focus_set()
        
        self._update_current_id_display()
        self.status_label.config(text=f"New ID created: {new_id} - {len(self.all_records)} records saved")
    
    def _save_to_csv(self):
        """Save all records to a CSV file."""
        self._save_current_record()
        
        if not self.all_records:
            self.status_label.config(text="No records to save")
            return
        
        try:
            csv_content = ""
            
            for record in self.all_records:
                field_names = record['field_names']
                values = record['values']
                
                csv_content += ','.join(field_name for field_name in field_names) + '\n'
                csv_content += ','.join(value for value in values) + '\n'
            
            filename = self.filename_entry.get().strip()
            if not filename:
                filename = os.path.join(self._get_desktop_path(), "output.csv")
            elif not os.path.dirname(filename):
                filename = os.path.join(self._get_desktop_path(), filename)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(csv_content)
            
            # Show full path in status
            abs_path = os.path.abspath(filename)
            self.status_label.config(text=f"Saved {len(self.all_records)} records to: {abs_path}")
            
        except Exception as e:
            self.status_label.config(text=f"Error saving: {str(e)}")
    
    def _load_template(self):
        """Load a template file and populate fields."""
        try:
            from tkinter import filedialog
            
            filename = filedialog.askopenfilename(
                title="Select Template File",
                filetypes=[
                    ("JSON files", "*.json"),
                    ("All files", "*.*")
                ]
            )
            
            if not filename:
                return
            
            # Clear existing fields
            for pair in self.field_pairs:
                pair['frame'].destroy()
            self.field_pairs.clear()
            
            self.all_records.clear()
            self._update_csv_preview()
            self.fields_frame.update_idletasks()
            
            # Load template data
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                
                if isinstance(template_data, list):
                    field_names = template_data
                elif isinstance(template_data, dict) and 'fields' in template_data:
                    field_names = template_data['fields']
                elif isinstance(template_data, dict):
                    field_names = list(template_data.keys())
                else:
                    raise ValueError("Invalid JSON template format")
                
            except json.JSONDecodeError:
                self.status_label.config(text="Invalid JSON file format")
                return
            
            if not field_names:
                self.status_label.config(text="No valid field names found in template")
                return
            
            # Create fields from template
            for field_name in field_names:
                if field_name:
                    new_field, new_value = self._create_field_pair()
                    new_field.insert(0, field_name)
            
            self._update_row_labels()
            self.fields_frame.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            if self.field_pairs:
                self.field_pairs[0]['value_entry'].focus_set()
            
            self.status_label.config(text=f"Loaded template: {len(field_names)} fields from {os.path.basename(filename)}")
            
        except Exception as e:
            self.status_label.config(text=f"Error loading template: {str(e)}")
    
    def _save_template(self):
        """Save current field names as a template file."""
        try:
            from tkinter import filedialog
            
            field_names = []
            for pair in self.field_pairs:
                field_name = pair['field_entry'].get().strip()
                if field_name:
                    field_names.append(field_name)
            
            if not field_names:
                self.status_label.config(text="No field names to save as template")
                return
            
            filename = filedialog.asksaveasfilename(
                title="Save Template File",
                defaultextension=".json",
                filetypes=[
                    ("JSON files", "*.json"),
                    ("All files", "*.*")
                ]
            )
            
            if not filename:
                return
            
            template_data = {
                "fields": field_names,
                "description": f"Template created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "field_count": len(field_names)
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            
            self.status_label.config(text=f"Template saved: {len(field_names)} fields to {os.path.basename(filename)}")
            
        except Exception as e:
            self.status_label.config(text=f"Error saving template: {str(e)}")
    
    def _clear_all_fields(self):
        """Clear all field entries and reset to initial state."""
        for pair in self.field_pairs:
            pair['field_entry'].delete(0, tk.END)
            pair['value_entry'].delete(0, tk.END)
        
        while len(self.field_pairs) > 1:
            self._delete_field_pair(len(self.field_pairs) - 1)
        
        self.all_records.clear()
        self._update_csv_preview()
        
        # Reset filename to desktop path
        self.filename_entry.delete(0, tk.END)
        default_filename = os.path.join(self._get_desktop_path(), "output.csv")
        self.filename_entry.insert(0, default_filename)
        
        if self.field_pairs:
            self.field_pairs[0]['field_entry'].focus_set()
        
        self.status_label.config(text="All fields cleared")


def main():
    """Main application entry point."""
    root = tk.Tk()
    app = CSVPopulatorApp(root)
    
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    root.mainloop()


if __name__ == "__main__":
    main()
