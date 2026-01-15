import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
import threading
import os
import sys
import site
import datetime
from pathlib import Path
from faster_whisper import WhisperModel

# --- NVIDIA DLL FIX (WINDOWS) ---
# Ensures Python finds CUDA libraries installed via PIP or System
if os.name == 'nt':
    try:
        site_packages = site.getsitepackages()
        for sp in site_packages:
            nvidia_path = Path(sp) / "nvidia"
            if nvidia_path.exists():
                for root, dirs, files in os.walk(nvidia_path):
                    if 'bin' in dirs or 'lib' in dirs:
                        os.add_dll_directory(root)
    except Exception:
        pass  # Silent fail, relying on system PATH if this fails

# --- APP CONSTANTS ---
APP_TITLE = "Kaminski Whisper AI"
APP_VERSION = "v1.0.0 (Portfolio Edition)"
DEFAULT_MODEL = "large-v3"
AVAILABLE_MODELS = ["tiny", "base", "small", "medium", "large-v3"]
AVAILABLE_LANGUAGES = ["auto", "en", "pt", "es", "fr", "de", "it"]

class TranscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_TITLE} [{APP_VERSION}]")
        self.root.geometry("1000x800")
        
        # Apply modern theme if available
        style = ttk.Style()
        try: style.theme_use('clam')
        except: pass
        
        self.file_path = ""
        self.full_transcription = "" 
        self._init_ui()

    def _init_ui(self):
        # 1. Header (Input)
        header_frame = tk.LabelFrame(self.root, text=" 1. Input Source ", font=("Segoe UI", 10, "bold"), padx=15, pady=15)
        header_frame.pack(fill=tk.X, padx=15, pady=10)

        btn_frame = tk.Frame(header_frame)
        btn_frame.pack(fill=tk.X)
        
        self.btn_select = tk.Button(btn_frame, text="📂 Select Media File", command=self.select_file, bg="#e3f2fd", height=1, font=("Segoe UI", 9))
        self.btn_select.pack(side=tk.LEFT, padx=(0, 10))

        self.lbl_file_info = tk.Label(btn_frame, text="No file selected", fg="#666")
        self.lbl_file_info.pack(side=tk.LEFT)

        # 2. Settings (AI Config)
        config_frame = tk.LabelFrame(self.root, text=" 2. Model Settings ", font=("Segoe UI", 10, "bold"), padx=15, pady=15)
        config_frame.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(config_frame, text="Model Size:").pack(side=tk.LEFT)
        self.cb_model = ttk.Combobox(config_frame, values=AVAILABLE_MODELS, state="readonly", width=12)
        self.cb_model.set(DEFAULT_MODEL)
        self.cb_model.pack(side=tk.LEFT, padx=(5, 25))

        tk.Label(config_frame, text="Language:").pack(side=tk.LEFT)
        self.cb_lang = ttk.Combobox(config_frame, values=AVAILABLE_LANGUAGES, state="readonly", width=10)
        self.cb_lang.set("auto")
        self.cb_lang.pack(side=tk.LEFT, padx=(5, 20))

        # Device Indicator
        tk.Label(config_frame, text="Device Target:", fg="gray").pack(side=tk.LEFT, padx=(20, 5))
        tk.Label(config_frame, text="NVIDIA GPU (CUDA)", fg="green", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)

        # 3. Action Control
        action_frame = tk.Frame(self.root, padx=15, pady=10)
        action_frame.pack(fill=tk.X)

        self.btn_start = tk.Button(action_frame, text="▶ START TRANSCRIPTION", command=self.start_thread, 
                                   state=tk.DISABLED, bg="#c8e6c9", font=("Segoe UI", 11, "bold"), height=2)
        self.btn_start.pack(fill=tk.X)
        
        self.lbl_status = tk.Label(action_frame, text="Ready", fg="#333", font=("Segoe UI", 10))
        self.lbl_status.pack(pady=5)

        # 4. Output Log
        log_frame = tk.LabelFrame(self.root, text=" Live Transcript ", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.text_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=("Consolas", 10), state=tk.NORMAL)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # 5. Footer
        footer_frame = tk.Frame(self.root, padx=15, pady=10)
        footer_frame.pack(fill=tk.X)
        
        self.btn_save = tk.Button(footer_frame, text="💾 Save to .TXT", command=self.open_save_dialog, state=tk.DISABLED, width=20)
        self.btn_save.pack(side=tk.RIGHT)

    def select_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Media Files", "*.mp4 *.mp3 *.wav *.m4a *.mkv *.flac"), ("All Files", "*.*")])
        if filename:
            self.file_path = filename
            self.lbl_file_info.config(text=os.path.basename(filename), fg="#000")
            self.btn_start.config(state=tk.NORMAL)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Loaded: {filename}\nWaiting to start...\n")

    def start_thread(self):
        if not self.file_path: return
        self._toggle_inputs(False)
        self.update_status("Initializing GPU...", "orange")
        
        t = threading.Thread(target=self.run_transcription, args=(self.cb_model.get(), self.cb_lang.get()))
        t.daemon = True
        t.start()

    def run_transcription(self, model_size, language):
        lang_param = None if language == "auto" else language
        
        try:
            # 1. Load Model
            try:
                model = WhisperModel(model_size, device="cuda", compute_type="float16")
            except Exception as e:
                self.append_text(f"⚠️ VRAM Warning: {e}\nFallback to int8_float16...\n")
                model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")

            self.update_status("Transcribing... (Please wait)", "blue")
            self.append_text("\n" + "="*40 + "\nTRANSCRIPTION STARTED\n" + "="*40 + "\n")

            # 2. Process
            segments, info = model.transcribe(self.file_path, beam_size=5, language=lang_param)
            
            if lang_param is None:
                self.append_text(f"Detected Language: {info.language.upper()}\n\n")

            buffer = []
            for segment in segments:
                line = f"[{int(segment.start//60):02d}:{segment.start%60:05.2f}] {segment.text}"
                self.append_text(line + "\n")
                buffer.append(line)

            self.full_transcription = "\n".join(buffer)

            # 3. Auto-Save Backup
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"AUTOSAVE_{timestamp}.txt"
            with open(backup_name, "w", encoding="utf-8") as f:
                f.write(self.full_transcription)
            print(f"Auto-save created: {backup_name}")

            self.append_text("\n" + "="*40 + "\nCOMPLETED\n" + "="*40 + "\n")
            
            # 4. Trigger Success on Main Thread
            self.root.after(0, self.on_transcription_complete)

        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"Error: {str(e)}", "red"))
            self.append_text(f"\nCRITICAL ERROR: {e}\n")
        
        finally:
            self.root.after(0, lambda: self._toggle_inputs(True))

    def on_transcription_complete(self):
        """Called by main thread when processing is done."""
        self.update_status("Done! Please save your file.", "green")
        self.btn_save.config(state=tk.NORMAL)
        self.open_save_dialog()

    def open_save_dialog(self):
        if not self.full_transcription: return
        
        default_name = f"Transcript_{os.path.basename(self.file_path)}.txt"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_name,
            title="Save Transcription",
            filetypes=[("Text File", "*.txt")]
        )
        
        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(self.full_transcription)
                self.update_status(f"Saved to: {os.path.basename(save_path)}", "green")
            except Exception as e:
                self.update_status(f"Save Error: {e}", "red")
        else:
            self.update_status("Save cancelled (Backup available in folder)", "#666")

    # --- UI Helpers ---
    def _toggle_inputs(self, enable):
        s = tk.NORMAL if enable else tk.DISABLED
        self.btn_select.config(state=s)
        self.btn_start.config(state=s)
        self.cb_model.config(state="readonly" if enable else tk.DISABLED)

    def update_status(self, text, color):
        self.lbl_status.config(text=text, fg=color)

    def append_text(self, text):
        def _update():
            self.text_area.insert(tk.END, text)
            self.text_area.see(tk.END)
        self.root.after(0, _update)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TranscriberApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Fatal GUI Error: {e}")