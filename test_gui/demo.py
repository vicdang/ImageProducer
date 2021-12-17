# -*- coding: utf-8 -*-
# vim:ts=3:sw=3:expandtab
"""
---------------------------
Copyright (C) 2021
@Authors: Vic Dang
@Date: 16-Dec-21
@Version: 1.0
---------------------------
 Usage example:
   - demo1.py <options>

"""
import re
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import colorchooser as tkcolor
import os

TITLE = "Image Producer"
CONF = './config.ini'
SEED = 3
HEIGHT = 500
WIDTH = 800

class MainWindow(tk.Frame):
   """docstring for MainWindow"""

   def __init__(self, master=None, conf=None):
      super(MainWindow, self).__init__()
      self.master = master
      self.conf = conf
      self.font = ('Lucida Grande', 12)
      self.init_window()
      self.create_widgets()

   def init_window(self):
      self.master.title(TITLE)
      self.pack(fill=tk.BOTH, expand=1)

   def create_widgets(self):
      for sec in self.conf.sections():
         lf = tk.LabelFrame(self, text="%s" % sec.upper(), width=50,
                         font=self.font)
         lf.pack(fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)
         # lf.grid(row=0, column=0, sticky=NW,
         #         padx=5, pady=5, ipadx=5, ipady=5)
         self.create_field(sec, lf)
      lfb = tk.LabelFrame(self, text="", width=50,
                          font=self.font)
      lfb.pack(fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)
      btnsave = tk.Button(lfb, text="Save", command=self.save_config,
                         fg="Black", bg="Light green", height=2)
      btnsave.pack(fill="both", expand="yes", side="right")
      btnrun = tk.Button(lfb, text="Execute", command=self.execute,
                         fg="Black", bg="Light green", height=2)
      btnrun.pack(fill="both", expand="yes", side="right")

   def execute(self):
      return

   def select_folder(self, master):
      text = fd.askdirectory(title="Select a Folder")
      master.config(text=text)
      return text

   def select_file(self, master, file_type=('text files', '*.txt')):
      text = fd.askopenfilename(title="Select a File",
                                filetype=(file_type, ('all files', '*.*')))
      master.config(text=text)
      return text

   def select_color(self, master):
      text = tkcolor.askcolor()
      master.config(text=text)
      return text

   def select_field_type(self, master, value, row, col):
      tb = None
      if re.match(r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', value):
         tb = tk.Button(master, text=value, command=self.select_color)
         tb.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
      elif re.match(r'^(.+)\/([^\/]+)\/$', value):
         tb = tk.Button(master, text=value, command=self.select_folder)
         tb.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
      elif re.match(r'^(.+)\/([^\/]+)$', value):
         tb = tk.Button(master, text=value, command=self.select_file)
         tb.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
      else:
         tb = tk.Entry(master, justify=tk.LEFT,
                       font=self.font, width=20)
         tb.insert(0, "%s" % value)
         tb.grid(row=row, column=col, ipadx=5, sticky=tk.EW)

   def create_field(self, sec, master):
      item = dict(self.conf.items(sec))
      n = len(item)
      m = n / SEED
      if n % SEED > 0:
         m += 1
      r = lc = 1
      for k, v in item.items():
         lb = tk.Label(master, text="%s" % k, justify=tk.LEFT, padx=5,
                       font=self.font, width=10)
         lb.grid(row=r, column=lc, ipadx=10, sticky=tk.EW)
         self.select_field_type(master, v, r, lc+1)
         r += 1
         if r > m:
            lc += 2
            r = 1

   def save_config(self):
      self.conf.add_section("ORDERDATA")
      self.conf.set("ORDERDATA", "REKVIRENT", "111")


def export_config(conf, file):
   with open(file, "w") as file_obj:
      conf.write(file_obj)

def get_config():
   """
   Using to get the configuration
   :return:
   """
   try:
      from configparser import ConfigParser
   except ImportError:
      from ConfigParser import ConfigParser  # ver. < 3.0
   # instantiate
   conf = ConfigParser()
   # parse existing file
   conf.read(CONF)
   return conf

def main():
   """
   Main process
   """
   root = tk.Tk()
   # root.geometry("%dx%d" % (WIDTH, HEIGHT))
   root.resizable(0, 0)
   app = MainWindow(root, get_config())
   root.mainloop()

if __name__ == '__main__':
   main()
