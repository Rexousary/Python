import tkinter as tk
from tkinter import filedialog, simpledialog, font, messagebox

class SimpleTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.text = tk.Text(root, wrap='word')
        self.text.pack(expand=True, fill=tk.BOTH)
        self.create_menu()
        self.filename = None

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
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menu)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)

        edit_menu.add_command(label="Redo", command=self.redo)

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
        view_menu.add_command(label="Zoom In", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out", command=self.zoom_out)

    def new_file(self):
        self.filename = None
        self.text.delete(1.0, tk.END)

    def open_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".txt")
        if self.filename:
            with open(self.filename, "r") as file:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, file.read())

    def save_file(self):
        if self.filename:
            with open(self.filename, "w") as file:
                file.write(self.text.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if self.filename:
            with open(self.filename, "w") as file:
                file.write(self.text.get(1.0, tk.END))

    def undo(self):
        try:
            self.text.edit_undo()
        except tk.TclError:
            messagebox.showwarning("Warning", "Nothing to undo")

    def redo(self):
        try:
            self.text.edit_redo()
        except tk.TclError:
            messagebox.showwarning("Warning", "Nothing to redo")

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
        font_name = simpledialog.askstring("Input", "Enter font name:")
        font_size = simpledialog.askinteger("Input", "Enter font size:")
        if font_name and font_size:
            self.text.config(font=(font_name, font_size))

    def change_theme(self):
        theme = simpledialog.askstring("Input", "Enter theme (light/dark):")
        if theme == "dark":
            self.text.config(bg="black", fg="white")
        elif theme == "light":
            self.text.config(bg="white", fg="black")
        else:
            messagebox.showwarning("Warning", "Invalid theme")

    def zoom_in(self):
        current_font = font.Font(font=self.text.cget("font"))
        current_size = current_font.actual()["size"]
        self.text.config(font=(current_font.actual()["family"], current_size + 2))

    def zoom_out(self):
        current_font = font.Font(font=self.text.cget("font"))
        current_size = current_font.actual()["size"]
        if current_size > 6:  # Minimum font size limit
            self.text.config(font=(current_font.actual()["family"], current_size - 2))

if __name__ == "__main__":
    root = tk.Tk()
    editor = SimpleTextEditor(root)
    root.mainloop()
