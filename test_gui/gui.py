# -*- coding: utf-8 -*-
# vim:ts=3:sw=3:expandtab
"""
 Authors: 

 Usage example:
   - <Script>
"""

import tkinter as tk

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("this is a variable")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.entrythingy.bind('<Key-Return>',
                             self.print_contents)
        self.entrythingy.option_add("*Button.Background", "black")
        self.entrythingy.option_add("*Button.Foreground", "red")

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())

def startgame():
   pass

root = tk.Tk()
# root.geometry("500x500") #You want the size of the app to be 500x500
# root.resizable(0, 0)
# root.title('The game')
# #You can set the geometry attribute to change the root windows size
# root.geometry("500x500") #You want the size of the app to be 500x500
# root.resizable(0, 0) #Don't allow resizing in the x or y direction
#
# back = tk.Frame(master=root,bg='black')
# back.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
# back.pack(fill=tk.BOTH, expand=1) #Expand the frame to fill the root window
#
# #Changed variables so you don't have these set to None from .pack()
# go = tk.Button(master=back, text='Start Game', command=startgame)
# go.pack()
# close = tk.Button(master=back, text='Quit', command=root.destroy)
# close.pack()
# info = tk.Label(master=back, text='Made by me!', bg='red', fg='black')
# info.pack()


img_app = App(root)
img_app.master.title("Image producer")
img_app.master.geometry('700x700')
img_app.master.resizable(0, 0)

# myapp.mainloop()

root.mainloop()
# if __name__ == '__main__':
#    main()
