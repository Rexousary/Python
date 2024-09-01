import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from features import EditorFeatures  # Updated import statement to match features.py

class SimpleTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.text = tk.Text(root, wrap='word', undo=True)
        self.text.pack(expand=1, fill='both')

        self.filename = None
        self.modified = False

        self.features = EditorFeatures(self)
        self.create_menu()

        self.text.bind("<<Modified>>", self.on_modify)

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_close)

        edit_menu = tk.Menu(menu)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Word Count", command=self.features.word_count)
        edit_menu.add_command(label="Find and Replace", command=self.features.find_replace)

        format_menu = tk.Menu(menu)
        menu.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Align Left", command=self.align_left)
        format_menu.add_command(label="Align Center", command=self.align_center)
        format_menu.add_command(label="Align Right", command=self.align_right)
        format_menu.add_separator()
        format_menu.add_command(label="Change Font", command=self.change_font)
        format_menu.add_command(label="Change Theme", command=self.change_theme)

        view_menu = tk.Menu(menu)
        menu.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Insert Table", command=self.features.insert_table)

        tools_menu = tk.Menu(menu)
        menu.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Numbered List", command=self.features.set_numbered_list)
        tools_menu.add_command(label="Bulleted List", command=self.features.set_bulleted_list)
        tools_menu.add_command(label="Alphabetical List", command=self.features.set_alphabetical_list)
        tools_menu.add_separator()
        tools_menu.add_command(label="Export to PDF", command=self.features.export_pdf)

    def new_file(self):
        self.text.delete(1.0, tk.END)
        self.filename = None
        self.modified = False

    def open_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".txt",
                                                  filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filename:
            with open(self.filename, "r") as file:
                content = file.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, content)
            self.modified = False

    def save_file(self):
        if self.filename:
            with open(self.filename, "w") as file:
                content = self.text.get(1.0, tk.END)
                file.write(content)
            self.modified = False
        else:
            self.save_as_file()

    def save_as_file(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filename:
            self.save_file()

    def undo(self):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass

    def align_left(self):
        self.text.tag_configure("left", justify='left')
        self.text.tag_add("left", 1.0, tk.END)

    def align_center(self):
        self.text.tag_configure("center", justify='center')
        self.text.tag_add("center", 1.0, tk.END)

    def align_right(self):
        self.text.tag_configure("right", justify='right')
        self.text.tag_add("right", 1.0, tk.END)

    def change_font(self):
        font_name = simpledialog.askstring("Font", "Enter font name (e.g., Arial):")
        font_size = simpledialog.askinteger("Font Size", "Enter font size:")
        if font_name and font_size:
            self.text.config(font=(font_name, font_size))

    def change_theme(self):
        theme = simpledialog.askstring("Theme", "Enter theme (light or dark):")
        if theme == "dark":
            self.text.config(bg="black", fg="white")
        elif theme == "light":
            self.text.config(bg="white", fg="black")

    def on_modify(self, event):
        self.modified = True

    def on_close(self):
        if self.modified:
            if messagebox.askyesno("Save changes?", "You have unsaved changes. Do you want to save them?"):
                self.save_file()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    editor = SimpleTextEditor(root)
    root.mainloop()
