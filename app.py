import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import shutil
import csv
from datetime import datetime


# ============================================================
# DEFAULT FILE CATEGORIES
# ============================================================

DEFAULT_CATEGORIES = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif",
        ".webp", ".svg", ".bmp", ".ico"
    },

    "Documents": {
        ".pdf", ".doc", ".docx", ".txt",
        ".rtf", ".odt"
    },

    "Spreadsheets": {
        ".xls", ".xlsx", ".csv", ".ods"
    },

    "Presentations": {
        ".ppt", ".pptx", ".odp"
    },

    "Videos": {
        ".mp4", ".mkv", ".mov",
        ".avi", ".webm"
    },

    "Audio": {
        ".mp3", ".wav", ".m4a",
        ".flac", ".aac", ".ogg"
    },

    "Archives": {
        ".zip", ".rar", ".7z",
        ".tar", ".gz"
    },

    "Code": {
        ".py", ".js", ".ts",
        ".html", ".css", ".java",
        ".cpp", ".c", ".json"
    }
}


# ============================================================
# MAIN APPLICATION
# ============================================================

class SmartFileAutomation:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Smart File Automation"
        )

        self.root.geometry(
            "900x680"
        )

        self.root.minsize(
            800, 600
        )

        # Copy categories so we can customize them
        self.categories = {
            name: set(extensions)
            for name, extensions
            in DEFAULT_CATEGORIES.items()
        }

        self.folder = tk.StringVar()

        self.preview_mode = tk.BooleanVar(
            value=True
        )

        self.status = tk.StringVar(
            value="Ready"
        )

        self.total_files = 0
        self.total_size = 0
        self.errors = 0

        self.report_data = []

        self.create_style()
        self.create_interface()


    # ========================================================
    # STYLE
    # ========================================================

    def create_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11)
        )

        style.configure(
            "Card.TFrame",
            padding=15
        )

        style.configure(
            "Action.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )


    # ========================================================
    # USER INTERFACE
    # ========================================================

    def create_interface(self):

        # ---------- HEADER ----------

        header = ttk.Frame(
            self.root
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(25, 10)
        )

        ttk.Label(
            header,
            text="Smart File Automation",
            style="Title.TLabel"
        ).pack()

        ttk.Label(
            header,
            text="Organize, analyze and manage files automatically",
            style="Subtitle.TLabel"
        ).pack(
            pady=(5, 0)
        )


        # ---------- FOLDER CARD ----------

        folder_card = ttk.LabelFrame(
            self.root,
            text=" Folder Selection "
        )

        folder_card.pack(
            fill="x",
            padx=35,
            pady=10
        )

        folder_frame = ttk.Frame(
            folder_card
        )

        folder_frame.pack(
            fill="x",
            padx=15,
            pady=15
        )

        ttk.Label(
            folder_frame,
            text="Folder:"
        ).pack(
            side="left"
        )

        self.folder_entry = ttk.Entry(
            folder_frame,
            textvariable=self.folder
        )

        self.folder_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        ttk.Button(
            folder_frame,
            text="Browse",
            command=self.select_folder
        ).pack(
            side="right"
        )


        # ---------- CONTROL BAR ----------

        controls = ttk.Frame(
            self.root
        )

        controls.pack(
            fill="x",
            padx=35,
            pady=10
        )

        ttk.Checkbutton(
            controls,
            text="Preview only (recommended)",
            variable=self.preview_mode
        ).pack(
            side="left"
        )

        ttk.Button(
            controls,
            text="Customize Categories",
            command=self.customize_categories
        ).pack(
            side="left",
            padx=15
        )

        ttk.Button(
            controls,
            text="Organize Files",
            style="Action.TButton",
            command=self.organize_files
        ).pack(
            side="right"
        )


        # ---------- STATISTICS ----------

        stats = ttk.LabelFrame(
            self.root,
            text=" Statistics "
        )

        stats.pack(
            fill="x",
            padx=35,
            pady=10
        )

        self.files_label = ttk.Label(
            stats,
            text="Files: 0",
            font=("Segoe UI", 10, "bold")
        )

        self.files_label.pack(
            side="left",
            padx=20,
            pady=12
        )

        self.size_label = ttk.Label(
            stats,
            text="Size: 0 B",
            font=("Segoe UI", 10, "bold")
        )

        self.size_label.pack(
            side="left",
            padx=20
        )

        self.error_label = ttk.Label(
            stats,
            text="Errors: 0",
            font=("Segoe UI", 10, "bold")
        )

        self.error_label.pack(
            side="left",
            padx=20
        )


        # ---------- PROGRESS ----------

        self.progress = ttk.Progressbar(
            self.root,
            mode="determinate"
        )

        self.progress.pack(
            fill="x",
            padx=35,
            pady=(10, 5)
        )


        # ---------- STATUS ----------

        ttk.Label(
            self.root,
            textvariable=self.status
        ).pack(
            anchor="w",
            padx=35
        )


        # ---------- LOG ----------

        log_frame = ttk.LabelFrame(
            self.root,
            text=" Activity Log "
        )

        log_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        self.log = tk.Text(
            log_frame,
            height=15,
            font=("Consolas", 9),
            wrap="word"
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.log.configure(
            state="disabled"
        )


        # ---------- BOTTOM BUTTONS ----------

        bottom = ttk.Frame(
            self.root
        )

        bottom.pack(
            fill="x",
            padx=35,
            pady=(0, 20)
        )

        ttk.Button(
            bottom,
            text="Clear Log",
            command=self.clear_log
        ).pack(
            side="left"
        )

        ttk.Button(
            bottom,
            text="Export Report",
            command=self.export_report
        ).pack(
            side="right"
        )


    # ========================================================
    # SELECT FOLDER
    # ========================================================

    def select_folder(self):

        folder = filedialog.askdirectory(
            title="Select Folder"
        )

        if not folder:
            return

        self.folder.set(
            folder
        )

        self.status.set(
            "Folder selected"
        )

        self.write_log(
            f"Selected folder: {folder}"
        )


    # ========================================================
    # WRITE LOG
    # ========================================================

    def write_log(self, message):

        self.log.configure(
            state="normal"
        )

        self.log.insert(
            "end",
            message + "\n"
        )

        self.log.see(
            "end"
        )

        self.log.configure(
            state="disabled"
        )

        self.root.update_idletasks()


    # ========================================================
    # CLEAR LOG
    # ========================================================

    def clear_log(self):

        self.log.configure(
            state="normal"
        )

        self.log.delete(
            "1.0",
            "end"
        )

        self.log.configure(
            state="disabled"
        )

        self.status.set(
            "Log cleared"
        )


    # ========================================================
    # FIND CATEGORY
    # ========================================================

    def get_category(self, file):

        extension = file.suffix.lower()

        for category, extensions in self.categories.items():

            if extension in extensions:

                return category

        return "Others"


    # ========================================================
    # SAFE DUPLICATE HANDLING
    # ========================================================

    def get_unique_path(self, path):

        if not path.exists():

            return path

        counter = 1

        while True:

            new_path = path.with_name(
                f"{path.stem}_{counter}{path.suffix}"
            )

            if not new_path.exists():

                return new_path

            counter += 1


    # ========================================================
    # FORMAT FILE SIZE
    # ========================================================

    def format_size(self, size):

        units = [
            "B",
            "KB",
            "MB",
            "GB",
            "TB"
        ]

        value = float(size)

        for unit in units:

            if value < 1024:

                return f"{value:.2f} {unit}"

            value /= 1024

        return f"{value:.2f} PB"


    # ========================================================
    # ORGANIZE FILES
    # ========================================================

    def organize_files(self):

        folder = Path(
            self.folder.get()
        ).expanduser()

        if not folder.is_dir():

            messagebox.showerror(
                "Invalid Folder",
                "Please select a valid folder."
            )

            return


        files = [
            file
            for file in folder.iterdir()
            if file.is_file()
        ]


        if not files:

            messagebox.showinfo(
                "No Files",
                "No files were found in this folder."
            )

            return


        self.total_files = len(files)

        self.total_size = sum(
            file.stat().st_size
            for file in files
        )

        self.errors = 0

        self.report_data = []


        # Reset statistics

        self.files_label.config(
            text=f"Files: {len(files)}"
        )

        self.size_label.config(
            text=f"Size: {self.format_size(self.total_size)}"
        )

        self.error_label.config(
            text="Errors: 0"
        )


        # Progress

        self.progress["maximum"] = len(files)

        self.progress["value"] = 0


        self.write_log("")

        self.write_log(
            "=" * 75
        )

        if self.preview_mode.get():

            self.write_log(
                "PREVIEW MODE — Files will NOT be moved"
            )

        else:

            self.write_log(
                "LIVE MODE — Files WILL be moved"
            )

        self.write_log(
            f"Processing {len(files)} file(s)"
        )

        self.write_log(
            "=" * 75
        )


        # Process

        for number, file in enumerate(
            files,
            start=1
        ):

            category = self.get_category(
                file
            )

            destination_folder = (
                folder / category
            )

            destination = self.get_unique_path(
                destination_folder / file.name
            )


            try:

                size = file.stat().st_size

                self.write_log(
                    f"[{number}/{len(files)}] "
                    f"{file.name}  →  "
                    f"{category}/{destination.name}"
                )


                self.report_data.append({

                    "file": file.name,

                    "category": category,

                    "size": self.format_size(size),

                    "status":
                        "Preview"
                        if self.preview_mode.get()
                        else "Moved"

                })


                if not self.preview_mode.get():

                    destination_folder.mkdir(
                        exist_ok=True
                    )

                    shutil.move(
                        str(file),
                        str(destination)
                    )


            except OSError as error:

                self.errors += 1

                self.report_data.append({

                    "file": file.name,

                    "category": category,

                    "size": "Unknown",

                    "status": "Error"

                })

                self.write_log(
                    f"ERROR: {error}"
                )


            self.progress["value"] = number

            self.status.set(
                f"Processing {number} of {len(files)}..."
            )


        # Final statistics

        self.error_label.config(
            text=f"Errors: {self.errors}"
        )


        self.write_log("")

        self.write_log(
            "=" * 75
        )

        self.write_log(
            "PROCESSING COMPLETE"
        )

        self.write_log(
            "=" * 75
        )


        categories_count = {}

        for item in self.report_data:

            category = item["category"]

            categories_count[category] = (
                categories_count.get(category, 0) + 1
            )


        for category, count in sorted(
            categories_count.items()
        ):

            self.write_log(
                f"{category}: {count} file(s)"
            )


        self.write_log(
            f"Total files: {len(files)}"
        )

        self.write_log(
            f"Total size: {self.format_size(self.total_size)}"
        )

        self.write_log(
            f"Errors: {self.errors}"
        )

        self.write_log(
            "=" * 75
        )


        self.status.set(
            "Completed successfully"
        )


        if self.preview_mode.get():

            messagebox.showinfo(
                "Preview Complete",
                f"{len(files)} files analyzed.\n\n"
                "No files were moved.\n\n"
                "If everything looks correct, "
                "uncheck Preview mode and run again."
            )

        else:

            messagebox.showinfo(
                "Organization Complete",
                f"{len(files)} files processed.\n\n"
                f"Errors: {self.errors}"
            )


    # ========================================================
    # CUSTOM CATEGORIES
    # ========================================================

    def customize_categories(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Customize Categories"
        )

        window.geometry(
            "650x500"
        )

        ttk.Label(
            window,
            text="Custom File Categories",
            font=("Segoe UI", 18, "bold")
        ).pack(
            pady=20
        )

        ttk.Label(
            window,
            text="Add extensions to categories. Example: .psd, .ai, .sql"
        ).pack()


        frame = ttk.Frame(
            window
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )


        listbox = tk.Listbox(
            frame,
            font=("Consolas", 10)
        )

        listbox.pack(
            fill="both",
            expand=True
        )


        def refresh():

            listbox.delete(
                0,
                "end"
            )

            for category, extensions in sorted(
                self.categories.items()
            ):

                ext_text = ", ".join(
                    sorted(extensions)
                )

                listbox.insert(
                    "end",
                    f"{category}: {ext_text}"
                )


        refresh()


        input_frame = ttk.Frame(
            window
        )

        input_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )


        category_entry = ttk.Entry(
            input_frame
        )

        category_entry.insert(
            0,
            "Category"
        )

        category_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )


        extension_entry = ttk.Entry(
            input_frame
        )

        extension_entry.insert(
            0,
            ".extension"
        )

        extension_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )


        def add_category():

            category = category_entry.get().strip()

            extension = extension_entry.get().strip().lower()

            if not category or not extension:

                messagebox.showwarning(
                    "Missing information",
                    "Enter both a category and extension.",
                    parent=window
                )

                return

            if not extension.startswith("."):

                extension = "." + extension

            if category not in self.categories:

                self.categories[category] = set()

            self.categories[category].add(
                extension
            )

            refresh()

            category_entry.delete(
                0,
                "end"
            )

            extension_entry.delete(
                0,
                "end"
            )


        ttk.Button(
            input_frame,
            text="Add",
            command=add_category
        ).pack(
            side="right",
            padx=(5, 0)
        )


        ttk.Button(
            window,
            text="Close",
            command=window.destroy
        ).pack(
            pady=15
        )


    # ========================================================
    # EXPORT REPORT
    # ========================================================

    def export_report(self):

        if not self.report_data:

            messagebox.showinfo(
                "No Report",
                "Run the organizer first."
            )

            return


        filename = (
            f"file_automation_report_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )


        path = filedialog.asksaveasfilename(

            title="Save Report",

            initialfile=filename,

            defaultextension=".csv",

            filetypes=[
                ("CSV files", "*.csv")
            ]
        )


        if not path:

            return


        try:

            with open(
                path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.DictWriter(

                    file,

                    fieldnames=[
                        "file",
                        "category",
                        "size",
                        "status"
                    ]
                )

                writer.writeheader()

                writer.writerows(
                    self.report_data
                )


            messagebox.showinfo(
                "Report Exported",
                f"Report saved successfully:\n{path}"
            )

            self.status.set(
                "Report exported"
            )


        except OSError as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    application = SmartFileAutomation(
        root
    )

    root.mainloop()