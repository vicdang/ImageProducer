# -*- coding: utf-8 -*-
# vim:ts=3:sw=3:expandtab
"""
 Authors: 

 Usage example:
   - <Script>
"""
import tkinter
from tkinter import *
from tkinter import ttk

regionList = open('regions.txt','r')
optionList = open('options.txt','r')
class MainWindow(Frame):
    def __init__(self,master = None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create Window Layout"""
        Boxfont = ('Lucida Grande', 12)

        self.label1 = Label(self, font=Boxfont,
text="Regions").grid(row=2,column=0)
        self.regcombo = ttk.Combobox(self, font = Boxfont, width = 20, textvariable = varRegions)
        self.regcombo.bind("<Return>", self.regcombo_onEnter)
        self.regcombo.bind('<<ComboboxSelected>>',self.regcombo_onEnter)
        self.regcombo['values'] = regionList.readlines()
        self.regcombo.grid(row=2, column=1,sticky = W)

        self.label2 = Label(self, font=Boxfont, text="Options").grid(row=4,column=0)
        self.optcombo = ttk.Combobox(self, font = Boxfont, width = 20, textvariable = varOptions)
        self.optcombo.bind("<Return>", self.optcombo_onEnter)
        self.optcombo.bind('<<ComboboxSelected>>',self.optcombo_onEnter)
        self.optcombo['values'] = optionList.readlines()
        self.optcombo.grid(row=4, column=1,sticky = W)

    def init_window(self):
        self.master.title("User Settings")
        self.pack(fill=BOTH, expand=1)

    def regcombo_onEnter(self,event):
        varRegions.set(varRegions.get().lower())
        mytext = varRegions.get()
        vals = self.regcombo.cget('values')
        self.regcombo.select_range(0,END)
        print(mytext)
        if not vals:
            self.regcombo.configure(values = (mytext.strip,))
        elif mytext not in vals:
            with open('regions.txt','a') as f:
                f.write('\n'+ mytext)
                self.regcombo.configure(values = vals + (mytext,))
                f.close
        return 'break'

    def optcombo_onEnter(self,event):
        varOptions.set(varOptions.get().lower())
        mytext = varOptions.get()
        vals = self.optcombo.cget('values')
        self.optcombo.select_range(0,END)
        print(mytext)
        if not vals:
            self.optcombo.configure(values = (mytext.strip,))
        elif mytext not in vals:
            with open('options.txt','a') as f:
                f.write('\n'+ mytext)
                self.optcombo.configure(values = vals + (mytext,))
                f.close
        return 'break'


root = tkinter.Tk()
root.geometry("800x800")
varRegions = tkinter.StringVar(root, value='')
varOptions = tkinter.StringVar(root, value='')
app = MainWindow(root)
root.mainloop()
# if __name__ == '__main__':
#    main()
