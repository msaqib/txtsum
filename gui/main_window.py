import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading

class TextSummarizerGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.setup_layout()
        
        # Callbacks - to be set by main app
        self.on_summarize = None
        self.on_check_connection = None
        self.on_load_models = None

        self.load_available_models()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Text Summarizer with Local LLM")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Configure grid weights for resizing
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame with padding
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # Model Settings Frame
        self.settings_frame = ttk.LabelFrame(self.main_frame, text="Model Settings", padding="10")
        
        ttk.Label(self.settings_frame, text="Model:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(self.settings_frame, textvariable=self.model_var, 
                                         values=["Loading..."], 
                                         state="readonly", width=15)
        
        # Max length input
        ttk.Label(self.settings_frame, text="Max Length:").grid(row=0, column=2, sticky="w", padx=(20, 5))
        self.max_length_var = tk.StringVar(value="500")
        self.max_length_entry = ttk.Entry(self.settings_frame, textvariable=self.max_length_var, width=10)
        
        # Connection test button
        self.connection_button = ttk.Button(self.settings_frame, text="Check Connection", 
                                          command=self.check_connection_clicked)
        self.refresh_models_button = ttk.Button(self.settings_frame, text="Refresh Models", 
                                              command=self.load_available_models)
        
        # Input section
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Input Text", padding="5")
        
        # Input text area with scrollbar
        self.input_text = scrolledtext.ScrolledText(self.input_frame, height=12, width=80,
                                                   wrap=tk.WORD, font=("Arial", 10))
        self.input_text.insert("1.0", "Paste your long text here...")
        self.input_text.bind("<FocusIn>", self.clear_placeholder)
        
        # Input buttons frame
        self.input_buttons_frame = ttk.Frame(self.input_frame)
        self.clear_input_btn = ttk.Button(self.input_buttons_frame, text="Clear Input", 
                                        command=self.clear_input)
        self.summarize_btn = ttk.Button(self.input_buttons_frame, text="Summarize Text", 
                                      command=self.summarize_clicked)
        self.load_file_btn = ttk.Button(self.input_buttons_frame, text="Load from File", 
                                      command=self.load_file)
        
        # Output section
        self.output_frame = ttk.LabelFrame(self.main_frame, text="Summary Output", padding="5")
        
        # Output text area with scrollbar
        self.output_text = scrolledtext.ScrolledText(self.output_frame, height=8, width=80,
                                                    wrap=tk.WORD, font=("Arial", 10),
                                                    state=tk.DISABLED)
        
        # Output buttons frame
        self.output_buttons_frame = ttk.Frame(self.output_frame)
        self.copy_btn = ttk.Button(self.output_buttons_frame, text="Copy Summary", 
                                 command=self.copy_summary)
        self.save_btn = ttk.Button(self.output_buttons_frame, text="Save to File", 
                                 command=self.save_to_file)
        self.clear_output_btn = ttk.Button(self.output_buttons_frame, text="Clear Output", 
                                         command=self.clear_output)
        
        # Status bar
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_var = tk.StringVar(value="● Ready")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, 
                                    relief=tk.SUNKEN, anchor="w")
        
        # Progress bar (initially hidden)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_frame, variable=self.progress_var, 
                                          mode='indeterminate')
        
    def setup_layout(self):
        """Arrange widgets using grid layout"""
        # Main frame
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.main_frame.grid_rowconfigure(1, weight=2)  # Input section gets more space
        self.main_frame.grid_rowconfigure(2, weight=1)  # Output section
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Settings frame layout
        self.settings_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.settings_frame.grid_columnconfigure(4, weight=1)
        
        self.model_dropdown.grid(row=0, column=1, sticky="w", padx=(0, 20))
        self.max_length_entry.grid(row=0, column=3, sticky="w", padx=(0, 20))
        self.connection_button.grid(row=0, column=4, sticky="e")
        self.refresh_models_button.grid(row=0, column=5, sticky="e")
        
        # Input frame layout
        self.input_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.input_frame.grid_rowconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_text.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self.input_buttons_frame.grid(row=1, column=0, sticky="ew")
        
        self.clear_input_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.summarize_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.load_file_btn.pack(side=tk.LEFT)
        
        # Output frame layout
        self.output_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)
        
        self.output_text.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        self.output_buttons_frame.grid(row=1, column=0, sticky="ew")
        
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.clear_output_btn.pack(side=tk.LEFT)
        
        # Status bar layout
        self.status_frame.grid(row=3, column=0, sticky="ew")
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
    def clear_placeholder(self, event):
        """Clear placeholder text when input field gets focus"""
        if self.input_text.get("1.0", "end-1c") == "Paste your long text here...":
            self.input_text.delete("1.0", tk.END)
            
    def clear_input(self):
        """Clear the input text area"""
        self.input_text.delete("1.0", tk.END)
        
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        
    def load_file(self):
        """Load text from a file"""
        file_path = filedialog.askopenfilename(
            title="Select text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {str(e)}")
                
    def copy_summary(self):
        """Copy summary to clipboard"""
        summary = self.output_text.get("1.0", "end-1c")
        if summary.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(summary)
            self.update_status("Summary copied to clipboard")
        else:
            messagebox.showwarning("Warning", "No summary to copy")
            
    def save_to_file(self):
        """Save summary to a file"""
        summary = self.output_text.get("1.0", "end-1c")
        if not summary.strip():
            messagebox.showwarning("Warning", "No summary to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save summary",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(summary)
                self.update_status(f"Summary saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
                
    def summarize_clicked(self):
        """Handle summarize button click"""
        input_text = self.input_text.get("1.0", "end-1c").strip()
        if not input_text or input_text == "Paste your long text here...":
            messagebox.showwarning("Warning", "Please enter text to summarize")
            return
            
        if self.on_summarize:
            # Disable button during processing
            self.summarize_btn.config(state="disabled")
            self.show_progress(True)
            self.update_status("Processing...")
            
            # Run in separate thread to prevent GUI freezing
            thread = threading.Thread(target=self._run_summarize, args=(input_text,))
            thread.daemon = True
            thread.start()
            
    def _run_summarize(self, input_text):
        """Run summarization in background thread"""
        try:
            if self.on_summarize:
                result = self.on_summarize(input_text, self.model_var.get(), 
                                         int(self.max_length_var.get()))
                # Update GUI in main thread
                self.root.after(0, self._update_result, result)
        except Exception as e:
            self.root.after(0, self._handle_error, str(e))
            
    def _update_result(self, result):
        """Update GUI with summarization result"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", result)
        self.output_text.config(state=tk.DISABLED)
        
        self.summarize_btn.config(state="normal")
        self.show_progress(False)
        self.update_status("● Ready")
        
    def _handle_error(self, error_msg):
        """Handle errors from background thread"""
        messagebox.showerror("Error", f"Summarization failed: {error_msg}")
        self.summarize_btn.config(state="normal")
        self.show_progress(False)
        self.update_status("● Error occurred")

    def load_available_models(self):
        """Load available models from Ollama"""
        if self.on_load_models:
            self.model_dropdown.config(state="disabled")
            self.update_status("Loading models...")
            
            # Run in background thread
            thread = threading.Thread(target=self._run_load_models)
            thread.daemon = True
            thread.start()
        else:
            # Fallback to default models if no callback is set
            self.model_dropdown['values'] = ["No model is installed"]
            if self.model_dropdown['values']:
                self.model_var.set(self.model_dropdown['values'][0])

    def _run_load_models(self):
        """Load models in background thread"""
        try:
            if self.on_load_models:
                models = self.on_load_models()
                self.root.after(0, self._update_models_list, models)
        except Exception as e:
            self.root.after(0, self._handle_models_error, str(e))

    def _update_models_list(self, models):
        """Update the models dropdown with loaded models"""
        self.model_dropdown.config(state="readonly")
        
        if models:
            self.model_dropdown['values'] = models
            self.model_var.set(models[0])  # Select first model by default
            self.update_status(f"● Loaded {len(models)} models")
        else:
            self.model_dropdown['values'] = ["No models found"]
            self.model_var.set("No models found")
            self.update_status("● No models installed")
            
    def _handle_models_error(self, error_msg):
        """Handle errors when loading models"""
        self.model_dropdown.config(state="readonly")
        self.model_dropdown['values'] = ["Error loading models"]
        self.model_var.set("Error loading models")
        self.update_status(f"● Error loading models: {error_msg}")
        
    def check_connection_clicked(self):
        """Handle connection test button click"""
        if self.on_check_connection:
            self.update_status("Checking connection...")
            # Run in background thread
            thread = threading.Thread(target=self._run_connection_check)
            thread.daemon = True
            thread.start()
            
    def _run_connection_check(self):
        """Run connection check in background thread"""
        try:
            if self.on_check_connection:
                is_connected = self.on_check_connection()
                status = "● Connected to Ollama" if is_connected else "● Connection failed"
                self.root.after(0, self.update_status, status)
        except Exception as e:
            self.root.after(0, self.update_status, f"● Connection error: {str(e)}")
            
    def update_status(self, message):
        """Update the status bar"""
        self.status_var.set(message)
        
    def show_progress(self, show):
        """Show or hide progress bar"""
        if show:
            self.progress_bar.grid(row=0, column=1, sticky="e", padx=(10, 0))
            self.progress_bar.start(10)
        else:
            self.progress_bar.stop()
            self.progress_bar.grid_remove()
            
    def get_input_text(self):
        """Get text from input area"""
        return self.input_text.get("1.0", "end-1c")
        
    def set_output_text(self, text):
        """Set text in output area"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", text)
        self.output_text.config(state=tk.DISABLED)