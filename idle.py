import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import subprocess
import re
import os

class PythonIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced IDE with TypeScript and C# Support")
        self.create_widgets()
        self.command_history = []
        self.history_index = -1
        self.current_language = "Python"
        self.project_path = None

    def create_widgets(self):
        # Create a paned window to hold the text area and console
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        # Text area for the code editor
        self.text_area = tk.Text(self.paned_window, wrap=tk.WORD, font=("Consolas", 12), undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=1)
        self.text_area.bind("<KeyRelease>", self.on_key_release)
        self.paned_window.add(self.text_area, weight=3)

        # Configure tags for syntax highlighting
        self.text_area.tag_configure("keyword", foreground="blue")
        self.text_area.tag_configure("string", foreground="green")
        self.text_area.tag_configure("comment", foreground="gray")
        self.text_area.tag_configure("number", foreground="purple")

        # Frame to hold the console output and command input
        self.console_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.console_frame, weight=1)

        # Console output area
        self.console_output = scrolledtext.ScrolledText(self.console_frame, wrap=tk.WORD, font=("Consolas", 12), height=10, bg="black", fg="white")
        self.console_output.pack(fill=tk.BOTH, expand=1)

        # Command input for the terminal
        self.command_input = tk.Entry(self.console_frame, font=("Consolas", 12), bg="black", fg="white", insertbackground="white")
        self.command_input.pack(fill=tk.X)
        self.command_input.bind("<Return>", self.execute_command)
        self.command_input.bind("<Up>", self.previous_command)
        self.command_input.bind("<Down>", self.next_command)

        # Menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Run menu
        run_menu = tk.Menu(self.menu_bar, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_code)
        self.menu_bar.add_cascade(label="Run", menu=run_menu)

        # Project menu
        project_menu = tk.Menu(self.menu_bar, tearoff=0)
        project_menu.add_command(label="New Project", command=self.new_project)
        project_menu.add_command(label="Open Project", command=self.open_project)
        self.menu_bar.add_cascade(label="Project", menu=project_menu)

        # Language menu
        language_menu = tk.Menu(self.menu_bar, tearoff=0)
        language_menu.add_command(label="Python", command=lambda: self.set_language("Python"))
        language_menu.add_command(label="JavaScript", command=lambda: self.set_language("JavaScript"))
        language_menu.add_command(label="TypeScript", command=lambda: self.set_language("TypeScript"))
        language_menu.add_command(label="C#", command=lambda: self.set_language("C#"))
        self.menu_bar.add_cascade(label="Language", menu=language_menu)

    def set_language(self, language):
        self.current_language = language
        self.highlight_syntax()

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.root.title("Untitled - Enhanced IDE")
        
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("JavaScript Files", "*.js"), ("TypeScript Files", "*.ts"), ("C# Files", "*.cs"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.INSERT, code)
                self.root.title(f"{file_path} - Enhanced IDE")
                if file_path.endswith('.py'):
                    self.current_language = "Python"
                elif file_path.endswith('.js'):
                    self.current_language = "JavaScript"
                elif file_path.endswith('.ts'):
                    self.current_language = "TypeScript"
                elif file_path.endswith('.cs'):
                    self.current_language = "C#"
                self.highlight_syntax()
            self.file_path = file_path
    
    def save_file(self):
        if hasattr(self, 'file_path'):
            with open(self.file_path, 'w') as file:
                code = self.text_area.get(1.0, tk.END)
                file.write(code)
        else:
            self.save_as_file()
    
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("JavaScript Files", "*.js"), ("TypeScript Files", "*.ts"), ("C# Files", "*.cs"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                code = self.text_area.get(1.0, tk.END)
                file.write(code)
                self.root.title(f"{file_path} - Enhanced IDE")
            self.file_path = file_path
    
    def exit(self):
        self.root.quit()

    def new_project(self):
        project_path = filedialog.askdirectory()
        if project_path:
            self.project_path = project_path
            os.makedirs(os.path.join(self.project_path, 'src'), exist_ok=True)
            self.new_file()
            self.root.title(f"New Project - {self.project_path} - Enhanced IDE")

    def open_project(self):
        project_path = filedialog.askdirectory()
        if project_path:
            self.project_path = project_path
            file_path = filedialog.askopenfilename(initialdir=self.project_path, filetypes=[("Python Files", "*.py"), ("JavaScript Files", "*.js"), ("TypeScript Files", "*.ts"), ("C# Files", "*.cs"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, 'r') as file:
                    code = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.INSERT, code)
                    self.root.title(f"{file_path} - Enhanced IDE")
                    if file_path.endswith('.py'):
                        self.current_language = "Python"
                    elif file_path.endswith('.js'):
                        self.current_language = "JavaScript"
                    elif file_path.endswith('.ts'):
                        self.current_language = "TypeScript"
                    elif file_path.endswith('.cs'):
                        self.current_language = "C#"
                    self.highlight_syntax()
                self.file_path = file_path

    def run_code(self):
        code = self.text_area.get(1.0, tk.END)
        temp_file_path = "temp_code"
        if self.current_language == "Python":
            temp_file_path += ".py"
            command = ['python', temp_file_path]
        elif self.current_language == "JavaScript":
            temp_file_path += ".js"
            command = ['node', temp_file_path]
        elif self.current_language == "TypeScript":
            temp_file_path += ".ts"
            command = ['ts-node', temp_file_path]
        elif self.current_language == "C#":
            temp_file_path += ".cs"
            output_exe = os.path.splitext(temp_file_path)[0] + ".exe"
            command = ['csc', '/out:' + output_exe, temp_file_path]

        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(code)
        
        if self.current_language == "C#":
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                result = subprocess.run([output_exe], capture_output=True, text=True, shell=True)
        else:
            result = subprocess.run(command, capture_output=True, text=True)
        
        self.console_output.delete(1.0, tk.END)
        self.console_output.insert(tk.INSERT, result.stdout if result.stdout else result.stderr)
        self.console_output.see(tk.END)

    def execute_command(self, event):
        command = self.command_input.get()
        if command:
            self.command_history.append(command)
            self.history_index = -1
            self.command_input.delete(0, tk.END)
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.console_output.insert(tk.INSERT, f"\n$ {command}\n{result.stdout if result.stdout else result.stderr}")
            self.console_output.see(tk.END)
    
    def previous_command(self, event):
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_input.delete(0, tk.END)
            self.command_input.insert(0, self.command_history[-(self.history_index + 1)])
    
    def next_command(self, event):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.command_input.delete(0, tk.END)
            self.command_input.insert(0, self.command_history[-(self.history_index + 1)])
        elif self.history_index == 0:
            self.history_index -= 1
            self.command_input.delete(0, tk.END)

    def on_key_release(self, event):
        self.highlight_syntax()

    def highlight_syntax(self):
        '''Simple syntax highlighting for Python, JavaScript, TypeScript, and C#'''
        self.text_area.tag_remove("keyword", "1.0", tk.END)
        self.text_area.tag_remove("string", "1.0", tk.END)
        self.text_area.tag_remove("comment", "1.0", tk.END)
        self.text_area.tag_remove("number", "1.0", tk.END)

        if self.current_language == "Python":
            keywords = r'\b(class|def|return|if|else|elif|for|while|break|continue|pass|try|except|finally|import|from|as|with|lambda|yield|in|is|not|or|and)\b'
            comments = r'#[^\n]*'
        elif self.current_language == "JavaScript":
            keywords = r'\b(function|return|if|else|for|while|break|continue|try|catch|finally|import|from|as|with|yield|in|is|not|or|and|var|let|const)\b'
            comments = r'//[^\n]*|/\*[\s\S]*?\*/'
        elif self.current_language == "TypeScript":
            keywords = r'\b(function|return|if|else|for|while|break|continue|try|catch|finally|import|from|as|with|yield|in|is|not|or|and|var|let|const|interface|type|namespace)\b'
            comments = r'//[^\n]*|/\*[\s\S]*?\*/'
        elif self.current_language == "C#":
            keywords = r'\b(class|struct|enum|void|int|double|float|bool|string|if|else|for|while|do|switch|case|break|continue|return|try|catch|finally|using|namespace|public|private|protected|static|new|virtual|override|abstract|sealed)\b'
            comments = r'//[^\n]*|/\*[\s\S]*?\*/'

        strings = r'(\".*?\"|\'.*?\')'
        numbers = r'\b\d+\b'

        content = self.text_area.get(1.0, tk.END)

        for match in re.finditer(keywords, content):
            start, end = match.span()
            self.text_area.tag_add("keyword", f"1.0+{start}c", f"1.0+{end}c")
        
        for match in re.finditer(strings, content):
            start, end = match.span()
            self.text_area.tag_add("string", f"1.0+{start}c", f"1.0+{end}c")
        
        for match in re.finditer(comments, content):
            start, end = match.span()
            self.text_area.tag_add("comment", f"1.0+{start}c", f"1.0+{end}c")
        
        for match in re.finditer(numbers, content):
            start, end = match.span()
            self.text_area.tag_add("number", f"1.0+{start}c", f"1.0+{end}c")

if __name__ == "__main__":
    root = tk.Tk()
    ide = PythonIDE(root)
    root.mainloop()
