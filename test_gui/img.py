# -*- coding: utf-8 -*-
# vim:ts=3:sw=3:expandtab
"""
 Authors: 

 Usage example:
   - <Script>
"""
import tkinter
import tkinter as tk  # gives tk namespace
from tkinter import *
from tkinter.scrolledtext import *
import tkinter.filedialog
import tkinter.messagebox
import configparser
import string

parser = configparser.ConfigParser()

root = tkinter.Tk(className="Create and Edit Config File")
textPad = ScrolledText(root, width=100, height=30)
task_list = tk.Listbox(root, width=50, height=6)

config = configparser.ConfigParser()
config.read('config.ini')

UserList = (config.get('general', 'interval').split(','))
UserList = [i.strip('[]') for i in UserList]
UserList = [i.strip("{}") for i in UserList]
UserList = [i.strip('"') for i in UserList]
UserList = [i.strip("'") for i in UserList]
print(UserList)

SystemList = (config.get('general', 'backgroundColor').split(','))
SystemList = [i.strip('{}') for i in SystemList]

DeploymentList = (config.get('general', 'backgroundColor').split(','))
List = [i.strip('{}') for i in DeploymentList]

def open_task():
   ##    fin = tkinter.filedialog.askopenfile(mode='rb',title='Select administration Config file')
   ##    if fin is not None:
   ##        task_listread = fin.readlines()
   ##
   for item in UserList:
      task_list.insert(tk.END, item)

##            fin.close()

def exit():
   if tkinter.messagebox.askokcancel("Quit", "Do you really want to quit?"):
      root.destroy()

def about():
   label = tkinter.messagebox.showinfo("About", "To do List py experiment")

def new_task():
   task_list.insert(tk.END, input.get())
   UserList.append(input.get())
   print(UserList)

def delete_item():
   """
   delete a selected line from the listbox
   """
   try:
      # get selected line index
      index = task_list.curselection()[0]
      task_list.delete(index)
   except IndexError:
      pass

def get_list(event):
   """
   function to read the listbox selection
   and put the result in an entry widget
   """
   # get selected line index
   index = task_list.curselection()[0]
   # get the line's text
   seltext = task_list.get(index)
   # delete previous text in input
   input.delete(0, 50)
   # now display the selected text
   input.insert(0, seltext)

def set_list(event):
   """
   insert an edited line from the entry widget
   back into the listbox
   """
   try:
      index = task_list.curselection()[0]
      # delete old listbox line
      task_list.delete(index)
   except IndexError:
      index = tk.END
      # insert edited item back into task_list at index
      task_list.insert(index, input.get())

def save_tasks():
   config.set('VARIABLES', 'USERS', str(UserList))
   with open('Administration.ini', "w") as config_file:
      config.write(config_file, space_around_delimiters=False)

##    """
##    save the current listbox contents to a file
##    """
##    # get a list of listbox lines
##    temp_list = list(task_list.get(0, tk.END))
##    # add a trailing newline char to each line
##    temp_list = [task + '\n' for task in temp_list]
##    # give the file a different name
##
##    if temp_list is not None:
##        fout = tkinter.filedialog.asksaveasfile(mode='w')
##        fout.writelines(temp_list)
##        fout.close()

menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open Task File", command=open_task)
filemenu.add_command(label="Save", command=save_tasks)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About ", command=about)

# create the listbox (note that size is in characters)
# task_list = tk.Listbox(root, width=50, height=6)
task_list.grid(row=0, column=0)

# create a vertical scrollbar to the right of the listbox
yscroll = tk.Scrollbar(command=task_list.yview, orient=tk.VERTICAL)
yscroll.grid(row=0, column=1, sticky=tk.N + tk.S)
task_list.configure(yscrollcommand=yscroll.set)

# task_list.bind("<<ListboxSelect>>", printer)

# use entry widget to display/edit selection
input = tk.Entry(root, width=50)
input.insert(0, 'Write Your Task here')
input.grid(row=1, column=0)
# pressing the enter key will update edited line
input.bind('<Return>', set_list)

# This button is used to add tasks
button_add_task = tk.Button(root, text='Add entry text to listbox',
                            command=new_task)
button_add_task.grid(row=2, column=0, sticky=tk.E)

# This Button is used to call the delete function
button_delete = tk.Button(root, text='Delete selected Task     ',
                          command=delete_item)
button_delete.grid(row=3, column=0, sticky=tk.E)

# left mouse click on a list item to display selection
task_list.bind('<ButtonRelease-1>', get_list)

root.mainloop()
# if __name__ == '__main__':
#    main()
