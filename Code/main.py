from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import random
import os
import time
from datetime import date
from main import code_editor
from application import text_editor



def screenMenu():
    menu = Menu(root)
    root.config(menu=menu)
    file = Menu(menu)
    menu.add_cascade(label="File", menu=file)
    file.add_command(label='New', command=new)
    file.add_command(label='Save', command=save)
    file.add_command(label='Save As', command=save_as)
    file.add_command(label='Exit', command=app_quit)

    edit = Menu(menu)
    menu.add_cascade(label="Edit", menu=edit)
    edit.add_command(label='Cut', command=cut)
    edit.add_command(label='Copy', command=copy)
    edit.add_command(label='Paste', command=paste)
    edit.add_separator()
    edit.add_command(label='Select All', command=select_all)
    edit.add_command(label='Undo', command=Undo)
    edit.add_command(label='Redo', command=Redo)
    edit.add_command(label='Clear', command=Clear)
    edit.add_separator()
    edit.add_command(label="Find", command=find_text)
    edit.add_separator()
    edit.add_command(label='Insert Date', command=insertDate)
    edit.add_command(label='Insert Time', command=insertTime)
    edit.add_command(label='Insert date and time', command=insertDateTime)

    font = Menu(menu)
    menu.add_cascade(label="Font", menu=font)

    font.add_command(label='Arial', command=Arial)
    font.add_command(label='Arial Bold', command=ArialBold)
    font.add_command(label='Arial Italic', command=ArialItalic)
    font.add_separator()

    font.add_command(label='Roman', command=Roman)
    font.add_command(label='Roman Bold', command=RomanBold)
    font.add_command(label='Roman Italic', command=RomanItalic)
    font.add_separator()

    font.add_command(label='Courier', command=Courier)
    font.add_command(label='Courier Bold', command=CourierBold)
    font.add_command(label='Courier Italic', command=CourierItalic)
    font.add_separator()

    font.add_command(label='Verdana', command=Verdana)
    font.add_command(label='Verdana Bold', command=VerdanaBold)
    font.add_command(label='Verdana Italic', command=VerdanaItalic)
    font.add_separator()

    font_color = Menu(menu)
    menu.add_cascade(label='Font Color', menu=font_color)
    font_color.add_command(label='Red', command=foreground_red)
    font_color.add_command(label='Black', command=foreground_black)
    font_color.add_command(label="Blue", command=foreground_blue)
    font_color.add_command(label='Green', command=foreground_green)
    font_color.add_command(label='White', command=foreground_white)

    text_background = Menu(menu)
    menu.add_cascade(label='Text Background', menu=text_background)
    text_background.add_command(label='Black', command=background_black)
    text_background.add_command(label='White', command=background_white)
    text_background.add_command(label='Red', command=background_red)
    text_background.add_command(label='Blue', command=background_blue)
    text_background.add_command(label='Green', command=background_green)

    theme_menu = Menu(menu)
    menu.add_cascade(label='Themes', menu=theme_menu)
    theme_menu.add_command(label='Dark', command=dark_theme)
    theme_menu.add_command(label='Light', command=light_theme)
    theme_menu.add_command(label='Default', command=default_theme)

    help_menu = Menu(menu)
    menu.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=about)
    help_menu.add_command(label='Help', command=EditorHelp)

def code_edit():
    root.destroy()
    code_editor()


def find_text():
    search_top_level = Toplevel(root)
    search_top_level.title('Find Text')
    search_top_level.transient(root)
    search_top_level.resizable(False, False)
    Label(search_top_level, text="Find:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_top_level, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_top_level, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e',
                                                                                       padx=2, pady=2)
    Button(search_top_level, text="Find", underline=0,
           command=lambda: search_output(
               search_entry_widget.get(), ignore_case_value.get(),
               txt, search_top_level, search_entry_widget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)


def search_output(needle, if_ignore_case, content_text, search_top_level, search_box):
    content_text.tag_remove('match', '1.0', END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle, start_pos, nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break

            end_pos = '{} + {}c'.format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config('match', background='yellow', foreground='blue')
    search_box.focus_set()
    matches_found_text = '{} matches found'.format(matches_found)
    search_top_level.title(matches_found_text)


def new():
    save_dialog = tkinter.messagebox.askokcancel(
        "Are you sure?",
        "Do you want to save this file before creating a new one?",
        icon='warning'
    )

    if save_dialog:
        save_as()

    txt.delete("1.0", END)


def WriteToFile(file):
    try:
        content = txt.get(1.0, 'end')
        with open(file, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass


global filename


def save_as():
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt"),
                                                                      ("HTML", "*.html"), ("CSS", "*.css"),
                                                                      ("JavaScript", "*.js")])

    if input_file_name:
        global filename
        filename = input_file_name
        x = ('{} - {}'.format(os.path.basename(filename), root.title()))
        root.title(x)

    return "break"


def save():
    global filename
    if not filename:
        save_as()

    else:
        WriteToFile(filename)

    return 'break'


def insertDate():
    today = date.today().strftime("%A, %d.%B %Y")
    txt.insert("1.0", today)


def insertTime():
    today = time.strftime("%H:%M Uhr ")
    txt.insert("1.0", today)


def insertDateTime():
    insertDate()
    insertTime()


def about():
    tkinter.messagebox.showinfo("About ATS Office: ",
                                "ATS Office is Made by Amey V, a programmer")


def EditorHelp():
    tkinter.messagebox.showinfo("ATS Help",
                                """
                                \nTo type, just type in the Text box\n
                                \nDifferent Image each time you open the App!\n
                                \nYou can save your work, so you can view it any time!\n
                                \nText features like changing the font, font color, background, etc\n
                                \nApp features like App themes, beautiful interface, etc\n
                               """)


def app_quit():
    quit_message_box = tkinter.messagebox.askokcancel(
        "Are you sure?",
        "Do you want to quit ATS Office?",
        icon='question'
    )

    if quit_message_box:
        root.destroy()


def underline():
    txt.config(underline=True)


def Undo():
    try:
        txt.edit_undo()

    except TclError:
        tkinter.messagebox.showerror(
            "Nothing to Undo!",
            "You have not entered any text to undo!",
            icon="error"
        )


def Redo():
    try:
        txt.edit_redo()

    except TclError:
        tkinter.messagebox.showerror(
            "Nothing to Redo!",
            "You have not done an Undo! Please do an undo and try again.",
            icon='error'
        )


def Clear():
    txt.delete("1.0", "end")


def Courier():
    txt.config(font='Courier')


def CourierBold():
    txt.config(font=('Courier', 12, "bold"))


def CourierItalic():
    txt.config(font=('Courier', 12, "italic"))


def Arial():
    txt.config(font='Arial')


def ArialBold():
    txt.config(font=('arial', 12, 'bold'))


def ArialItalic():
    txt.config(font=('Arial', 12, 'italic'))


def Verdana():
    txt.config(font='verdana')


def VerdanaBold():
    txt.config(font=('verdana', 12, 'bold'))


def VerdanaItalic():
    txt.config(font=('verdana', 12, 'italic'))


def Roman():
    txt.config(font=('Roman', 12))


def RomanBold():
    txt.config(font=('Roman', 12, 'bold'))


def RomanItalic():
    txt.config(font=('Roman', 12, 'italic'))


def default_theme():
    light_theme()


def dark_theme():
    txt.config(background='black', foreground='white')


def light_theme():
    txt.config(background='white', fg='black')


def background_green():
    txt.config(bg='green')


def background_black():
    txt.config(bg='black')


def background_white():
    txt.config(bg='white')


def background_red():
    txt.config(bg='red')


def background_blue():
    txt.config(bg='blue')


def foreground_white():
    txt.config(fg='white')


def foreground_blue():
    txt.config(fg='blue')


def foreground_green():
    txt.config(fg='green')


def foreground_red():
    txt.config(foreground='red')


def foreground_black():
    txt.config(fg='black')


# Select all the text in textbox
def select_all():
    txt.tag_add(SEL, "1.0", END)
    txt.mark_set(INSERT, "1.0")
    txt.see(INSERT)
    return 'break'


def cut():
    txt.event_generate("<<Cut>>")


def copy():
    txt.event_generate("<<Copy>>")


def paste():
    txt.event_generate("<<Paste>>")


root = Tk()
root.geometry("770x521")
root.resizable(False, False)
root.title("ATS office - ATS Word")
# -------
backgroundImage1 = PhotoImage(file='nature.png')
background2 = PhotoImage(file='tree.png')
backgrounds3 = PhotoImage(file='sun.png')

backgrounds = [backgroundImage1, background2, backgrounds3]
background = random.choice(backgrounds)


backgroundLabel = Label(root, image=background)
backgroundLabel.place(relwidth=1, relheight=1)

select_all_button = Button(root, text="Select All", relief=FLAT, bg='white', fg='black', command=select_all)
select_all_button.place(x=10, y=12)

cut_button = Button(root, text='Cut', relief=FLAT, bg='white', fg='black', width=6, command=cut)
cut_button.place(x=80, y=12)

copy_button = Button(root, text='Copy', relief=FLAT, bg='white', fg='black', width=6, command=copy)
copy_button.place(x=145, y=12)

paste_button = Button(root, text='Paste', relief=FLAT, bg='white', fg='black', width=6, command=paste)
paste_button.place(x=210, y=12)

clear_button = Button(root, text='Clear', relief=FLAT, bg='white', fg='black', width=6, command=Clear)
clear_button.place(x=275, y=12)

undo_button = Button(root, text='Undo', relief=FLAT, bg='white', fg='black', width=6, command=Undo)
undo_button.place(x=340, y=12)

redo_button = Button(root, text='Redo', relief=FLAT, bg='white', fg='black', width=6, command=Redo)
redo_button.place(x=405, y=12)

frame = Frame(root, bd=3, bg="grey")
frame.place(relx=0.5, rely=0.1, relwidth=0.85, relheight=0.85, anchor='n')

txt = Text(frame, font="Arial", undo=True)
txt.place(relx=0.5, rely=0.01, relwidth=0.95, relheight=0.95, anchor='n')

scrollbar = Scrollbar(txt)
txt.configure(yscrollcommand=scrollbar.set)
scrollbar.config(command=txt.yview)
scrollbar.pack(side='right', fill='y')

screenMenu()
root.protocol("WM_DELETE_WINDOW", app_quit)
root.mainloop()
