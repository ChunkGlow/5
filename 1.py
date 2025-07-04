# Notepad Professional
# A simple text editor with advanced features
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename



app = Tk()
app.title("Notepad Professional")
app.geometry("600x400")
app.rowconfigure(0, minsize=800, weight=1)
app.columnconfigure(1, minsize=800, weight=1)

txt_edit = Text(app)
txt_edit.grid(row=0, column=1, sticky="nsew")

def open_file():
    filepath = askopenfilename(
        title="Open A Text File / Files",
        filetypes=[("Text Files", "*.txt"),("RTF Files", "*.rtf"),("JSON Files", "*.json"),("Advanced Text Formats", "*.atf"),("Markdown Files", "*.md"),("All Files", "*.*")]
    )

    if not filepath:
        messagebox.showwarning("Warning", "You did not select a file. Please select a file to open.")
        return

    txt_edit.delete(1.0, END)

    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(END, text)

    
def save_file():
    filepath = asksaveasfilename(
        title="Save A Text File / Files",
        defaultextension=".txt, .rtf, .json, .atf, .md",
        filetypes=[("Text Files", "*.txt"),("RTF Files", "*.rtf"),("JSON Files", "*.json"),("Advanced Text Formats", "*.atf"),("Markdown Files", "*.md"),("All Files", "*.*")]
    )

    if not filepath:
        messagebox.showwarning("Warning", "You did not select a file. Please select a file to save.")
        return
    
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, END)
        output_file.write(text)
        app.title(f"Notepad Professional  - {filepath}")
        messagebox.showinfo("Success", "File saved successfully!")

def on_closing():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        app.destroy()
        txt_edit = Text(app)

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()