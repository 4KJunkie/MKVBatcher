import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import difflib


class MKVBatcherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MKVBatcher")
        self.geometry("650x400")

        # Variables
        self.mkvmerge_path_var = tk.StringVar()
        self.input_folder_var = tk.StringVar()
        self.output_folder_var = tk.StringVar()
        self.delete_originals_var = tk.BooleanVar(value=True)

        # Row 1 : mkvmerge.exe
        row = 0
        tk.Label(self, text="Path to mkvmerge.exe:").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self, textvariable=self.mkvmerge_path_var, width=55).grid(row=row, column=1, padx=5, pady=5, sticky="we")
        tk.Button(self, text="Browse...", command=self.browse_mkvmerge).grid(row=row, column=2, padx=5, pady=5)

        # Row 2 : Input folder
        row += 1
        tk.Label(self, text="Input folder (video + SRT):").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self, textvariable=self.input_folder_var, width=55).grid(row=row, column=1, padx=5, pady=5, sticky="we")
        tk.Button(self, text="Select folder...", command=self.browse_input_folder).grid(row=row, column=2, padx=5, pady=5)

        # Row 3 : Output folder
        row += 1
        tk.Label(self, text="Output folder (optional):").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self, textvariable=self.output_folder_var, width=55).grid(row=row, column=1, padx=5, pady=5, sticky="we")
        tk.Button(self, text="Select folder...", command=self.browse_output_folder).grid(row=row, column=2, padx=5, pady=5)

        # Row 4 : Delete originals
        row += 1
        tk.Checkbutton(
            self,
            text="Delete original VIDEO + SRT after successful processing",
            variable=self.delete_originals_var
        ).grid(row=row, column=0, columnspan=3, sticky="w", padx=10, pady=5)

        # Row 5 : Run
        row += 1
        tk.Button(self, text="Run batch", command=self.run_batch, height=2).grid(
            row=row, column=0, columnspan=3, pady=10
        )

        # Row 6 : Log
        row += 1
        tk.Label(self, text="Log:").grid(row=row, column=0, sticky="w", padx=10)
        row += 1
        self.log = scrolledtext.ScrolledText(self, width=80, height=10, state="normal")
        self.log.grid(row=row, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        self.grid_rowconfigure(row, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def browse_mkvmerge(self):
        path = filedialog.askopenfilename(
            title="Select mkvmerge.exe",
            filetypes=[("mkvmerge.exe", "mkvmerge.exe"), ("All files", "*.*")]
        )
        if path:
            self.mkvmerge_path_var.set(path)

    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="Select input folder")
        if folder:
            self.input_folder_var.set(folder)

    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder_var.set(folder)

    def log_line(self, text):
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.update_idletasks()

    # Smart matching function
    def find_best_srt(self, video_name, srt_files):
        match = difflib.get_close_matches(video_name, srt_files, n=1, cutoff=0.6)
        return match[0] if match else None

    def run_batch(self):
        mkvmerge_path = self.mkvmerge_path_var.get().strip()
        input_folder = self.input_folder_var.get().strip()
        output_folder = self.output_folder_var.get().strip()

        if not mkvmerge_path or not os.path.isfile(mkvmerge_path):
            messagebox.showerror("Error", "Invalid mkvmerge.exe path.")
            return

        if not input_folder or not os.path.isdir(input_folder):
            messagebox.showerror("Error", "Invalid input folder.")
            return

        if not output_folder:
            output_folder = input_folder
        elif not os.path.isdir(output_folder):
            messagebox.showerror("Error", "Invalid output folder.")
            return

        delete_originals = self.delete_originals_var.get()

        self.log.delete("1.0", tk.END)
        self.log_line(f"mkvmerge : {mkvmerge_path}")
        self.log_line(f"Input folder : {input_folder}")
        self.log_line(f"Output folder : {output_folder}")
        self.log_line(f"Delete originals : {'Yes' if delete_originals else 'No'}")
        self.log_line("Starting batch...\n")

        valid_exts = (".mkv", ".mp4", ".avi", ".mov", ".webm")
        srt_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".srt")]

        count_ok = 0
        count_fail = 0

        for filename in os.listdir(input_folder):

            if filename.lower().endswith(".final.mkv"):
                continue

            if not filename.lower().endswith(valid_exts):
                continue

            video_full = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]

            best_srt = self.find_best_srt(base_name, srt_files)

            if not best_srt:
                self.log_line(f"[SKIPPED] No matching SRT found for {filename}")
                continue

            srt_full = os.path.join(input_folder, best_srt)
            output_name = base_name + ".final.mkv"
            output_full = os.path.join(output_folder, output_name)

            if os.path.exists(output_full):
                self.log_line(f"[SKIPPED] {output_name} already exists")
                continue

            self.log_line(f"[PROCESSING] {filename} + {best_srt} -> {output_name}")

            try:
                result = subprocess.run(
                    [mkvmerge_path, "-o", output_full, video_full, srt_full],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )

                self.log_line(result.stdout.strip())

                if result.returncode == 0:
                    self.log_line(f"[OK] Finished {output_name}")
                    count_ok += 1

                    if delete_originals:
                        try:
                            os.remove(video_full)
                            os.remove(srt_full)
                            self.log_line("   Original video + SRT deleted")
                        except Exception as e:
                            self.log_line(f"   [WARNING] Could not delete originals: {e}")

                else:
                    self.log_line(f"[ERROR] mkvmerge failed for {filename}")
                    count_fail += 1

            except Exception as e:
                self.log_line(f"[ERROR] Exception for {filename}: {e}")
                count_fail += 1

            self.log_line("")

        self.log_line("Batch finished.")
        self.log_line(f"Success: {count_ok}, Failed: {count_fail}")
        messagebox.showinfo("Done", f"Batch finished.\nSuccess: {count_ok}\nFailed: {count_fail}")


if __name__ == "__main__":
    app = MKVBatcherApp()
    app.mainloop()
