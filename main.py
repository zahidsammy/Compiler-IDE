import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

ide = tk.Tk()
ide.title('Magicbox IDE')
file_path = ''
bg_color = 'white'
fg_color = 'black'

def set_file_path(path):
    global file_path
    file_path = path

def set_bg_color(color):
    global bg_color, fg_color
    bg_color = color
    if color == 'black':
        fg_color = 'white'
    else:
        fg_color = 'black'
    ide.config(bg=bg_color)
    editor.config(bg=bg_color, fg=fg_color)
    code_output.config(bg=bg_color, fg=fg_color)

def open_file():
    path = filedialog.askopenfilename(filetypes=[('Python Files', '*.py')])
    if path:
        try:
            with open(path, 'r') as file:
                code = file.read()
                editor.delete('1.0', tk.END)
                editor.insert('1.0', code)
                set_file_path(path)
        except Exception as e:
            error_message('Error opening file: ' + str(e))

def save_file():
    if not file_path:
        path = filedialog.asksaveasfilename(filetypes=[('Python Files', '*.py')])
        if not path:
            return
    else:
        path = file_path
    try:
        with open(path, 'w') as file:
            code = editor.get('1.0', tk.END)
            file.write(code)
            set_file_path(path)
    except Exception as e:
        error_message('Error saving file: ' + str(e))

def run_code():
    if not file_path:
        error_message('Please save your code')
        return
    command = f'python "{file_path}"'
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        code_output.config(state='normal')
        code_output.delete('1.0', tk.END)
        code_output.insert(tk.END, output)
        code_output.insert(tk.END, error)
        code_output.config(state='disabled')
    except Exception as e:
        error_message('Error running code: ' + str(e))

def error_message(msg):
    messagebox.showerror('Error', msg)

menubar = tk.Menu(ide)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Open', command=open_file)
filemenu.add_command(label='Save', command=save_file)
filemenu.add_command(label='Save As', command=save_file)
filemenu.add_command(label='Exit', command=ide.quit)
menubar.add_cascade(label='File', menu=filemenu)

runmenu = tk.Menu(menubar, tearoff=0)
runmenu.add_command(label='Run', command=run_code)
menubar.add_cascade(label='Run', menu=runmenu)

themesmenu = tk.Menu(menubar, tearoff=0)
themesmenu.add_command(label='Light', command=lambda: set_bg_color('white'))
themesmenu.add_command(label='Dark', command=lambda: set_bg_color('black'))
menubar.add_cascade(label='Themes', menu=themesmenu)

ide.config(menu=menubar)

editor = tk.Text(ide)
editor.pack()

code_output = tk.Text(ide, height=10, state='disabled')
code_output.pack(pady=10)

ide.mainloop()
