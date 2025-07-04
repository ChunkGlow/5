from tkinter import *
from tkinter import messagebox, font, colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename
import re

app = Tk()
app.title("Notepad Professional")
app.geometry("800x600")
try:
    app.iconbitmap("icon.ico")
except Exception:
    pass

# Font settings
available_fonts = list(font.families())
current_font_family = StringVar(value="Times New Roman")
current_font_size = IntVar(value=12)
text_font = font.Font(family=current_font_family.get(), size=current_font_size.get())

# Toolbar Frame (styled to look like Windows XP/Word 2003)
toolbar = Frame(app, bg="#ece9d8", height=32, bd=2, relief=RAISED)
toolbar.pack(side=TOP, fill=X)

# Font family dropdown
font_family_menu = OptionMenu(toolbar, current_font_family, *available_fonts, command=lambda e: update_font())
font_family_menu.config(width=15, font=("Tahoma", 9), bg="#f7f7f7", relief=GROOVE)
font_family_menu.pack(side=LEFT, padx=(6,2), pady=4)

# Font size dropdown
font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 32, 36, 40, 48, 56, 64, 72]
font_size_menu = OptionMenu(toolbar, current_font_size, *font_sizes, command=lambda e: update_font())
font_size_menu.config(width=3, font=("Tahoma", 9), bg="#f7f7f7", relief=GROOVE)
font_size_menu.pack(side=LEFT, padx=2, pady=4)

# Supported languages for highlighting
LANGUAGES = [
    "Plain Text", "Python", "Java", "C", "C++", "C#", "HTML", "CSS", "JavaScript"
]
current_language = StringVar(value="Plain Text")

# Add language selector to toolbar
language_menu = OptionMenu(toolbar, current_language, *LANGUAGES, command=lambda e: highlight_code())
language_menu.config(width=10, font=("Tahoma", 9), bg="#f7f7f7", relief=GROOVE)
language_menu.pack(side=LEFT, padx=(8,2), pady=4)

# Set default font to monospaced for code
def update_font():
    lang = current_language.get()
    if lang == "Plain Text":
        text_font.config(family=current_font_family.get(), size=current_font_size.get())
    else:
        text_font.config(family="Consolas", size=current_font_size.get())
    txt_edit.configure(font=text_font)
    highlight_code()

# Formatting buttons (styled)
Button(toolbar, text="B", command=lambda: toggle_tag("bold"), width=2, relief=RAISED, font=("Arial", 10, "bold"), bg="#f7f7f7").pack(side=LEFT, padx=2, pady=2)
Button(toolbar, text="I", command=lambda: toggle_tag("italic"), width=2, relief=RAISED, font=("Arial", 10, "italic"), bg="#f7f7f7").pack(side=LEFT, padx=2, pady=2)
Button(toolbar, text="U", command=lambda: toggle_tag("underline"), width=2, relief=RAISED, font=("Arial", 10, "underline"), bg="#f7f7f7").pack(side=LEFT, padx=2, pady=2)

# Separator
Frame(toolbar, width=2, bd=0, bg="#b6b3aa").pack(side=LEFT, fill=Y, padx=4, pady=4)

# Text color button
Button(toolbar, text="A", command=lambda: choose_color(), relief=RAISED, font=("Arial", 10, "bold"), fg="#c00000", bg="#f7f7f7", width=2).pack(side=LEFT, padx=2, pady=2)

# Separator
Frame(toolbar, width=2, bd=0, bg="#b6b3aa").pack(side=LEFT, fill=Y, padx=4, pady=4)

# Alignment buttons (styled)
Button(toolbar, text="🡸", command=lambda: align_text("left"), width=2, font=("Tahoma", 10), relief=RAISED, bg="#f7f7f7").pack(side=LEFT, padx=2, pady=2)
Button(toolbar, text="⯀", command=lambda: align_text("center"), width=2, font=("Tahoma", 10), relief=RAISED, bg="#f7f7f7").pack(side=LEFT, padx=2, pady=2)
Button(toolbar, text="🡺", command=lambda: align_text("right"), width=2, font=("Tahoma", 10), relief=RAISED, bg="#f7f7f7").pack(side=LEFT, padx=2, pady=2)

# Main text area (styled)
txt_edit = Text(app, font=text_font, wrap=WORD, undo=True,
                bg="white", fg="black", insertbackground="black",
                relief=FLAT, borderwidth=0)
txt_edit.pack(fill=BOTH, expand=1, padx=2, pady=(0,2))

# Tag configuration for formatting
txt_edit.tag_configure("bold", font=font.Font(txt_edit, txt_edit.cget("font"), weight="bold"))
txt_edit.tag_configure("italic", font=font.Font(txt_edit, txt_edit.cget("font"), slant="italic"))
txt_edit.tag_configure("underline", font=font.Font(txt_edit, txt_edit.cget("font"), underline=1))
txt_edit.tag_configure("left", justify=LEFT)
txt_edit.tag_configure("center", justify=CENTER)
txt_edit.tag_configure("right", justify=RIGHT)

def toggle_tag(tag):
    try:
        start, end = txt_edit.index("sel.first"), txt_edit.index("sel.last")
    except TclError:
        return  # No selection
    if tag in txt_edit.tag_names("sel.first"):
        txt_edit.tag_remove(tag, start, end)
    else:
        txt_edit.tag_add(tag, start, end)

def choose_color():
    color = colorchooser.askcolor()[1]
    if color:
        try:
            start, end = txt_edit.index("sel.first"), txt_edit.index("sel.last")
            tag_name = f"color_{color}"
            txt_edit.tag_add(tag_name, start, end)
            txt_edit.tag_configure(tag_name, foreground=color)
        except TclError:
            txt_edit.configure(fg=color)

def align_text(align_type):
    try:
        start, end = txt_edit.index("sel.first"), txt_edit.index("sel.last")
    except TclError:
        return
    for tag in ("left", "center", "right"):
        txt_edit.tag_remove(tag, start, end)
    txt_edit.tag_add(align_type, start, end)

# --- Syntax Highlighting ---
def highlight_code(event=None):
    lang = current_language.get()
    txt_edit.tag_remove("keyword", "1.0", END)
    txt_edit.tag_remove("string", "1.0", END)
    txt_edit.tag_remove("comment", "1.0", END)
    txt_edit.tag_remove("tag", "1.0", END)
    code = txt_edit.get("1.0", END)

    if lang == "Python":
        keywords = r"\b(False|class|finally|is|return|None|continue|for|lambda|try|True|def|from|nonlocal|while|and|del|global|not|with|as|elif|if|or|yield|assert|else|import|pass|break|except|in|raise)\b"
        strings = r"(\".*?\"|\'.*?\')"
        comments = r"#[^\n]*"
    elif lang in ("C", "C++", "C#", "Java"):
        keywords = r"\b(int|float|double|char|void|if|else|for|while|do|switch|case|break|continue|return|public|private|protected|class|static|final|new|try|catch|finally|throw|throws|import|package|using|namespace|struct|enum|bool|true|false|null|this|super|extends|implements)\b"
        strings = r"(\".*?\"|\'.*?\')"
        comments = r"(//[^\n]*|/\*.*?\*/)"
    elif lang == "HTML":
        tags = r"(<[^>]+>)"
        for match in re.finditer(tags, code, re.DOTALL):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            txt_edit.tag_add("tag", start, end)
        txt_edit.tag_configure("tag", foreground="#1a1aa6")
        return
    elif lang == "CSS":
        keywords = r"\b(color|background|font|border|margin|padding|display|position|float|width|height|content|align|justify|flex|grid|block|inline|none|auto|relative|absolute|fixed|sticky)\b"
        strings = r"(\".*?\"|\'.*?\')"
        comments = r"/\*.*?\*/"
    elif lang == "JavaScript":
        keywords = r"\b(var|let|const|function|if|else|for|while|do|switch|case|break|continue|return|true|false|null|undefined|this|new|class|extends|super|import|export|from|as|try|catch|finally|throw)\b"
        strings = r"(\".*?\"|\'.*?\'|\`.*?\`)"

    # Highlight keywords
    if lang != "HTML":
        for match in re.finditer(keywords, code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            txt_edit.tag_add("keyword", start, end)
        txt_edit.tag_configure("keyword", foreground="#0000cc", font=(text_font.actual("family"), text_font.actual("size"), "bold"))

    # Highlight strings
    if 'strings' in locals():
        for match in re.finditer(strings, code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            txt_edit.tag_add("string", start, end)
        txt_edit.tag_configure("string", foreground="#a31515")

    # Highlight comments
    if 'comments' in locals():
        for match in re.finditer(comments, code, re.DOTALL):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            txt_edit.tag_add("comment", start, end)
        txt_edit.tag_configure("comment", foreground="#008000", font=(text_font.actual("family"), text_font.actual("size"), "italic"))

# Bind highlighting to key release
txt_edit.bind("<KeyRelease>", highlight_code)

# --- File operations ---
def open_file():
    filepath = askopenfilename(
        title="Open A Text File / Files",
        filetypes=[
            ("Text Files", "*.txt"),
            ("RTF Files", "*.rtf"),
            ("JSON Files", "*.json"),
            ("Advanced Text Formats", "*.atf"),
            ("Markdown Files", "*.md"),
            ("All Files", "*.*")
        ]
    )
    if not filepath:
        messagebox.showwarning("Warning", "You did not select a file. Please select a file to open.")
        return
    txt_edit.delete(1.0, END)
    with open(filepath, "r", encoding="utf-8") as input_file:
        txt_edit.insert(END, input_file.read())
    app.title(f"{filepath} - Notepad Professional")
    highlight_code()

def save_file():
    filepath = asksaveasfilename(
        title="Save A Text File / Files",
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("RTF Files", "*.rtf"),
            ("JSON Files", "*.json"),
            ("Advanced Text Formats", "*.atf"),
            ("Markdown Files", "*.md"),
            ("All Files", "*.*")
        ]
    )
    if not filepath:
        messagebox.showwarning("Warning", "You did not select a file. Please select a file to save.")
        return
    with open(filepath, "w", encoding="utf-8") as output_file:
        output_file.write(txt_edit.get(1.0, "end-1c"))
    app.title(f"{filepath} - Notepad Professional")
    messagebox.showinfo("Success", "File saved successfully!")

# --- About dialog ---
def show_about():
    about_win = Toplevel(app)
    about_win.title("About Notepad Professional")
    try:
        about_win.iconbitmap("icon.ico")
    except Exception:
        pass
    about_win.resizable(False, False)
    about_win.configure(bg="#ece9d8")
    Label(
        about_win,
        text="Notepad Professional - Version 1.1a",
        font=("Tahoma", 12, "bold"),
        bg="#ece9d8",
        fg="#333"
    ).pack(padx=30, pady=20)
    Button(
        about_win,
        text="OK",
        command=about_win.destroy,
        width=10,
        bg="#f7f7f7"
    ).pack(pady=(0, 15))

# --- Menubar ---
menubar = Menu(app)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)
menubar.add_cascade(label="File", menu=file_menu)

theme_menu = Menu(menubar, tearoff=0)
theme_menu.add_command(label="Classic Theme", command=lambda: txt_edit.configure(bg="white", fg="black", insertbackground="black"))
theme_menu.add_command(label="Dark Theme", command=lambda: txt_edit.configure(bg="#2e2e2e", fg="white", insertbackground="white"))
menubar.add_cascade(label="Theme", menu=theme_menu)

help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)

app.config(menu=menubar)

# --- Exit confirmation ---
def on_closing():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
