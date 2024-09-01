import tkinter as tk
from tkinter import simpledialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class EditorFeatures:
    def __init__(self, editor):
        self.editor = editor
        self.current_list_type = None
        self.col_width = 15  # Default column width

        # Bind Enter key to continue list
        self.editor.text.bind("<Return>", self.continue_list)

    def word_count(self):
        text = self.editor.text.get(1.0, tk.END)
        words = text.split()
        num_words = len(words)
        messagebox.showinfo("Word Count", f"Total words: {num_words}")

    def find_replace(self):
        find_text = simpledialog.askstring("Find", "Enter text to find:")
        if not find_text:
            return
        replace_text = simpledialog.askstring("Replace", "Enter replacement text:")
        if replace_text is None:
            return

        content = self.editor.text.get(1.0, tk.END)
        if find_text in content:
            content = content.replace(find_text, replace_text)
            self.editor.text.delete(1.0, tk.END)
            self.editor.text.insert(tk.END, content)
        else:
            messagebox.showinfo("Find and Replace", "Text not found.")

    def export_pdf(self):
        filename = simpledialog.askstring("Export PDF", "Enter filename (without extension):")
        if filename:
            c = canvas.Canvas(filename + ".pdf", pagesize=letter)
            text = self.editor.text.get(1.0, tk.END).strip().replace("\n", " ")
            c.drawString(100, 750, text)
            c.save()
            messagebox.showinfo("Export PDF", f"PDF saved as {filename}.pdf")

    def clear_list_format(self):
        content = self.editor.text.get(1.0, tk.END).strip()
        if content:
            lines = content.split('\n')
            cleared_lines = []
            for line in lines:
                if line.strip():
                    if self.current_list_type == "numbered" and line.strip()[0].isdigit():
                        line = line.lstrip("0123456789. ").strip()
                    elif self.current_list_type == "bulleted" and line.strip().startswith("•"):
                        line = line.lstrip("• ").strip()
                    elif self.current_list_type == "alphabetical" and line.strip()[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        line = line.lstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ. ").strip()
                cleared_lines.append(line)
            self.editor.text.delete(1.0, tk.END)
            self.editor.text.insert(tk.END, "\n".join(cleared_lines))

    def apply_new_list_format(self):
        self.clear_list_format()
        content = self.editor.text.get(1.0, tk.END).strip()
        if content:
            self._apply_list_format()
        else:
            if self.current_list_type == "numbered":
                self.editor.text.insert(tk.END, "1. ")
            elif self.current_list_type == "bulleted":
                self.editor.text.insert(tk.END, "• ")
            elif self.current_list_type == "alphabetical":
                self.editor.text.insert(tk.END, "A. ")

    def set_numbered_list(self):
        self.current_list_type = "numbered"
        self.apply_new_list_format()

    def set_bulleted_list(self):
        self.current_list_type = "bulleted"
        self.apply_new_list_format()

    def set_alphabetical_list(self):
        self.current_list_type = "alphabetical"
        self.apply_new_list_format()

    def continue_list(self, event):
        if self.current_list_type:
            content = self.editor.text.get(1.0, tk.END).strip()
            lines = content.split('\n')
            if lines:
                last_line = lines[-1]
                if self.current_list_type == "numbered":
                    if last_line.strip().isdigit():
                        self.editor.text.insert(tk.END, f"\n{int(last_line.strip()) + 1}. ")
                elif self.current_list_type == "bulleted":
                    if last_line.strip().startswith("•"):
                        self.editor.text.insert(tk.END, "\n• ")
                elif self.current_list_type == "alphabetical":
                    if last_line.strip()[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        last_char = last_line.strip()[0]
                        next_char = chr(ord(last_char) + 1)
                        if next_char > 'Z':
                            next_char = 'A'
                        self.editor.text.insert(tk.END, f"\n{next_char}. ")
        return "break"  # Prevents the default behavior of inserting a newline

    def insert_table(self):
        # Ask for number of rows and columns
        num_rows = simpledialog.askinteger("Insert Table", "Enter number of rows:")
        num_cols = simpledialog.askinteger("Insert Table", "Enter number of columns:")
        if num_rows and num_cols:
            # Ask for column width
            new_col_width = simpledialog.askinteger("Column Width", "Enter column width in characters:", initialvalue=self.col_width)
            if new_col_width:
                self.col_width = new_col_width

            # Generate table header separator
            header_separator = "+".join(["-" * self.col_width for _ in range(num_cols)])
            header_separator = "+" + header_separator + "+"

            # Generate table rows
            table_text = header_separator + "\n"
            for _ in range(num_rows):
                row = "|" + "|".join([" " * self.col_width for _ in range(num_cols)]) + "|"
                table_text += row + "\n" + header_separator + "\n"

            self.editor.text.insert(tk.END, table_text)
