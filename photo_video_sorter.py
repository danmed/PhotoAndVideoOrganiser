import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk, simpledialog
import os
import shutil
import datetime
import json

PHOTO_EXTENSIONS = (
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.heic', '.heif',
    '.raw', '.nef', '.cr2', '.orf', '.sr2', '.arw', '.dng'
)
VIDEO_EXTENSIONS = (
    '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.mpg', '.mpeg',
    '.m4v', '.3gp'
)
ALL_MEDIA_EXTENSIONS = PHOTO_EXTENSIONS + VIDEO_EXTENSIONS

PRESET_FILE_NAME = "photo_sorter_presets.json"

class PhotoSorterApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Photo & Video Sorter")
        # self.root.geometry("750x650") 

        self.source_dir_var = tk.StringVar()
        self.dest_dir_var = tk.StringVar() # Correct variable for destination directory path
        self.move_files_var = tk.BooleanVar(value=True) 
        self.overwrite_var = tk.BooleanVar(value=False)
        self.presets = {}

        self.setup_ui()
        self.load_presets()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1) # Allow entry column to expand

        # --- Source Folder ---
        ttk.Label(main_frame, text="Source Folder:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=(5,2))
        source_entry = ttk.Entry(main_frame, textvariable=self.source_dir_var, width=60)
        source_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0,5), pady=(5,2))
        ttk.Button(main_frame, text="Browse...", command=self.browse_source_folder).grid(row=0, column=2, sticky=tk.W, padx=5, pady=(5,2))

        # --- Destination Folder ---
        ttk.Label(main_frame, text="Destination Folder:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=(0,5))
        dest_entry = ttk.Entry(main_frame, textvariable=self.dest_dir_var, width=60) # Uses self.dest_dir_var
        dest_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0,5), pady=(0,5))
        ttk.Button(main_frame, text="Browse...", command=self.browse_dest_folder).grid(row=1, column=2, sticky=tk.W, padx=5, pady=(0,5))

        # --- Presets ---
        preset_frame = ttk.LabelFrame(main_frame, text="Presets", padding="10")
        preset_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        preset_frame.columnconfigure(1, weight=1) 

        ttk.Label(preset_frame, text="Select Preset:").grid(row=0, column=0, sticky=tk.W, padx=(0,5), pady=2)
        self.preset_combobox = ttk.Combobox(preset_frame, state="readonly", width=30)
        self.preset_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0,5), pady=2)
        self.preset_combobox.bind("<<ComboboxSelected>>", self.on_preset_selected)

        ttk.Button(preset_frame, text="Save Current", command=self.save_current_as_preset).grid(row=0, column=2, padx=(0,5), pady=2)
        ttk.Button(preset_frame, text="Delete Selected", command=self.delete_selected_preset).grid(row=0, column=3, padx=(0,5), pady=2)

        # --- Options ---
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Checkbutton(options_frame, text="Move files (deletes originals from source)", variable=self.move_files_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Checkbutton(options_frame, text="Overwrite existing files in destination", variable=self.overwrite_var).pack(anchor=tk.W, padx=5, pady=2)

        # --- Process Button ---
        process_button_style = ttk.Style()
        process_button_style.configure("Accent.TButton", font=('Segoe UI', 10, 'bold'))
        self.process_button = ttk.Button(main_frame, text="Process Files", command=self.process_files_action, style="Accent.TButton")
        self.process_button.grid(row=4, column=0, columnspan=3, padx=5, pady=10)

        # --- Status Area ---
        status_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        status_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=(0,5))
        main_frame.rowconfigure(5, weight=1) 
        status_frame.columnconfigure(0, weight=1) 

        self.status_text = scrolledtext.ScrolledText(status_frame, wrap=tk.WORD, height=15, width=80, state=tk.DISABLED, relief=tk.SOLID, borderwidth=1)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2, pady=2)


    def log_message(self, message, clear_first=False):
        self.status_text.config(state=tk.NORMAL)
        if clear_first:
            self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def browse_folder(self, entry_var):
        folder_selected = filedialog.askdirectory(parent=self.root) 
        if folder_selected:
            entry_var.set(folder_selected)

    def browse_source_folder(self):
        self.browse_folder(self.source_dir_var)

    def browse_dest_folder(self): # This is the corrected method
        self.browse_folder(self.dest_dir_var) # Ensures it uses self.dest_dir_var

    def get_preset_file_path(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_dir = os.getcwd()
        return os.path.join(script_dir, PRESET_FILE_NAME)

    def load_presets(self):
        preset_file = self.get_preset_file_path()
        try:
            if os.path.exists(preset_file):
                with open(preset_file, 'r') as f:
                    self.presets = json.load(f)
            else:
                self.presets = {}
        except Exception as e:
            self.presets = {}
            self.log_message(f"Error loading presets: {e}")
        self.update_preset_combobox()

    def save_presets_to_file(self):
        preset_file = self.get_preset_file_path()
        try:
            with open(preset_file, 'w') as f:
                json.dump(self.presets, f, indent=4)
        except Exception as e:
            messagebox.showerror("Preset Error", f"Could not save presets to '{preset_file}':\n{e}", parent=self.root)
            self.log_message(f"Error saving presets: {e}")

    def update_preset_combobox(self):
        preset_names = sorted(list(self.presets.keys()))
        current_selection = self.preset_combobox.get()
        self.preset_combobox['values'] = preset_names
        if preset_names:
            if current_selection in preset_names:
                self.preset_combobox.set(current_selection)
            else:
                self.preset_combobox.current(0)
            self.on_preset_selected(None) 
        else:
            self.preset_combobox.set('')
            self.source_dir_var.set("")
            self.dest_dir_var.set("")


    def on_preset_selected(self, event):
        selected_preset_name = self.preset_combobox.get()
        if selected_preset_name and selected_preset_name in self.presets:
            preset_data = self.presets[selected_preset_name]
            self.source_dir_var.set(preset_data.get("source", ""))
            self.dest_dir_var.set(preset_data.get("destination", ""))

    def save_current_as_preset(self):
        source = self.source_dir_var.get()
        destination = self.dest_dir_var.get()

        if not source or not destination:
            messagebox.showwarning("Save Preset", "Source and Destination folders must be set to save a preset.", parent=self.root)
            return

        preset_name = simpledialog.askstring("Save Preset", "Enter a name for this preset:", parent=self.root)
        if preset_name:
            preset_name = preset_name.strip()
            if not preset_name:
                 messagebox.showwarning("Save Preset", "Preset name cannot be empty.", parent=self.root)
                 return

            if preset_name in self.presets and \
               not messagebox.askyesno("Overwrite Preset", f"Preset '{preset_name}' already exists. Overwrite?", parent=self.root):
                return
            
            self.presets[preset_name] = {"source": source, "destination": destination}
            self.save_presets_to_file()
            self.update_preset_combobox()
            self.preset_combobox.set(preset_name)
            self.log_message(f"Preset '{preset_name}' saved.")

    def delete_selected_preset(self):
        selected_preset_name = self.preset_combobox.get()
        if not selected_preset_name:
            messagebox.showwarning("Delete Preset", "No preset selected to delete.", parent=self.root)
            return

        if messagebox.askyesno("Delete Preset", f"Are you sure you want to delete the preset '{selected_preset_name}'?", parent=self.root):
            if selected_preset_name in self.presets:
                del self.presets[selected_preset_name]
                self.save_presets_to_file()
                self.update_preset_combobox()
                self.log_message(f"Preset '{selected_preset_name}' deleted.")
                if not self.preset_combobox.get(): 
                    self.source_dir_var.set("")
                    self.dest_dir_var.set("")
            else:
                messagebox.showerror("Delete Preset", "Selected preset not found. It might have been deleted externally.", parent=self.root)
                self.load_presets() 


    def get_file_date(self, file_path):
        try:
            stat_info = os.stat(file_path)
            timestamp = stat_info.st_birthtime
        except AttributeError:
            timestamp = os.path.getmtime(file_path)
        
        mtime = os.path.getmtime(file_path)
        if (timestamp < 100000000 or (mtime > timestamp and (mtime - timestamp > 3600))) and mtime > 0:
            timestamp = mtime
            
        return datetime.datetime.fromtimestamp(timestamp)

    def process_files_action(self):
        source_dir = self.source_dir_var.get()
        dest_dir = self.dest_dir_var.get()
        move_files = self.move_files_var.get()
        overwrite = self.overwrite_var.get()
        action_verb = "Moved" if move_files else "Copied"
        action_gerund = "Moving" if move_files else "Copying"


        if not source_dir or not dest_dir:
            messagebox.showerror("Error", "Source and Destination folders must be selected.", parent=self.root)
            return

        if not os.path.isdir(source_dir):
            messagebox.showerror("Error", f"Source folder not found: {source_dir}", parent=self.root)
            return
        
        abs_source_dir = os.path.abspath(source_dir)
        abs_dest_dir = os.path.abspath(dest_dir)
        if os.path.commonpath([abs_source_dir, abs_dest_dir]) == abs_source_dir and abs_source_dir != abs_dest_dir:
             if not messagebox.askyesno("Warning", "The destination folder appears to be inside the source folder. "
                                     "This could lead to files being reprocessed or unexpected behavior, "
                                     "especially if 'Move files' is selected. "
                                     "Are you sure you want to continue?", parent=self.root):
                return

        if not os.path.isdir(dest_dir):
            try:
                os.makedirs(dest_dir, exist_ok=True)
                self.log_message(f"Created destination folder: {dest_dir}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create destination folder: {dest_dir}\n{e}", parent=self.root)
                self.log_message(f"Error: Could not create destination folder: {dest_dir}\n{e}")
                return

        self.log_message(f"Starting file processing ({action_gerund.lower()})...", clear_first=True)
        processed_count = 0
        skipped_count = 0
        error_count = 0

        self.process_button.config(state=tk.DISABLED)
        self.root.update_idletasks()

        try:
            for root_folder, _, files in os.walk(source_dir, topdown=True):
                if os.path.abspath(root_folder).startswith(abs_dest_dir) and abs_dest_dir != abs_source_dir :
                    self.log_message(f"Skipping scan of destination subfolder: {root_folder}")
                    continue 

                for filename in files:
                    base, ext = os.path.splitext(filename)
                    if ext.lower() not in ALL_MEDIA_EXTENSIONS:
                        continue

                    source_file_path = os.path.join(root_folder, filename)

                    try:
                        file_date = self.get_file_date(source_file_path)
                        year = str(file_date.year)
                        month = f"{file_date.month:02d}"

                        target_year_dir = os.path.join(dest_dir, year)
                        target_month_dir = os.path.join(target_year_dir, month)

                        os.makedirs(target_month_dir, exist_ok=True)

                        target_file_path_original_name = os.path.join(target_month_dir, filename)
                        final_target_file_path = target_file_path_original_name

                        if os.path.abspath(source_file_path) == os.path.abspath(final_target_file_path):
                             self.log_message(f"Skipping '{filename}', source and target path are identical (already sorted).")
                             skipped_count +=1
                             continue

                        if os.path.exists(final_target_file_path):
                            if overwrite:
                                self.log_message(f"Overwriting '{filename}' in '{os.path.join(year, month)}' (Action: {action_gerund})")
                            else: 
                                counter = 1
                                new_filename_base = f"{base} ({counter})"
                                new_filename = f"{new_filename_base}{ext}"
                                final_target_file_path = os.path.join(target_month_dir, new_filename)
                                while os.path.exists(final_target_file_path):
                                    if os.path.abspath(source_file_path) == os.path.abspath(final_target_file_path):
                                        self.log_message(f"Skipping '{filename}', renamed target would be identical to source. Choose a different destination or clean up existing files.")
                                        final_target_file_path = None 
                                        break
                                    counter += 1
                                    new_filename_base = f"{base} ({counter})"
                                    new_filename = f"{new_filename_base}{ext}"
                                    final_target_file_path = os.path.join(target_month_dir, new_filename)
                                
                                if final_target_file_path: 
                                    self.log_message(f"'{filename}' exists. Renaming to '{new_filename}' in '{os.path.join(year, month)}'")
                                else: 
                                    skipped_count +=1
                                    continue
                        
                        if final_target_file_path: 
                            if move_files:
                                shutil.move(source_file_path, final_target_file_path)
                            else:
                                shutil.copy2(source_file_path, final_target_file_path)
                            self.log_message(f"{action_verb} '{filename}' to '{os.path.relpath(final_target_file_path, dest_dir)}'")
                            processed_count += 1

                    except Exception as e:
                        self.log_message(f"Error processing '{filename}': {e}")
                        error_count += 1
                    
                    if (processed_count + skipped_count + error_count) % 20 == 0: 
                        self.root.update_idletasks()
        finally:
            self.process_button.config(state=tk.NORMAL) 
            self.root.update_idletasks()


        self.log_message(f"\n--- Processing Complete ({action_gerund.lower()}) ---")
        self.log_message(f"Files successfully {action_verb.lower()}: {processed_count}")
        self.log_message(f"Files skipped: {skipped_count}")
        self.log_message(f"Errors encountered: {error_count}")
        messagebox.showinfo("Complete", f"Processing finished.\n\n{action_verb}: {processed_count}\nSkipped: {skipped_count}\nErrors: {error_count}", parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoSorterApp(root)
    root.mainloop()
