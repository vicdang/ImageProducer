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
import sys
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import colorchooser as tkcolor
import subprocess

TITLE = "Image Producer"
CONF = './config_base.ini'
SEED = 3
HEIGHT = 500
WIDTH = 800

class MainWindow(tk.Frame):
   """docstring for MainWindow"""

   def __init__(self, master=None, conf=None):
      super(MainWindow, self).__init__()
      self.master = master
      self.conf = conf
      self.dict_val = {}
      self.fit = tk.BooleanVar()
      self.font = ('Lucida Grande', 12)
      self.init_window()
      self.create_widgets()

   def init_window(self):
      """
      Init
      """
      self.master.title(TITLE)
      self.pack(fill=tk.BOTH, expand=1)

   def create_widgets(self):
      """
      Create widgets
      """
      lfb = tk.LabelFrame(self, text="", width=50,
                          font=self.font)
      self.textbox = tk.Text(lfb, fg="White", bg="Black", height=10, width=100,
                             wrap="word")
      for sec in self.conf.sections():
         lf = tk.LabelFrame(self, text="%s" % sec.upper(), width=50,
                            font=self.font)
         lf.pack(fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)
         self.create_field(sec, lf)
      # lfb = tk.LabelFrame(self, text="", width=50,
      #                     font=self.font)
      lfb.pack(fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)
      # self.textbox = tk.Text(lfb, fg="White", bg="Black", height=10, width=100,
      #                     wrap="word")
      vsb = tk.Scrollbar(lfb, orient="vertical", command=self.textbox.yview)
      self.textbox.configure(yscrollcommand=vsb.set)
      self.textbox.yview('end')
      vsb.pack(side="right", fill="y")
      self.textbox.pack(fill="both", expand="yes", side="right",
                        padx=5, pady=5, ipadx=5, ipady=5)
      # create instance of file like object
      pl = PrintLogger(self.textbox)
      sys.stdout = pl
      btnrun = tk.Button(lfb, text="Execute", command=self.execute,
                         fg="Black", bg="Green", height=2, width=10)
      btnrun.pack(fill="both", expand="yes", side="right",
                  padx=5, pady=5, ipadx=5, ipady=5)
      btnsave = tk.Button(lfb, text="Save", command=self.save_config,
                          fg="Black", bg="Light green", height=2, width=10)
      btnsave.pack(fill="both", expand="yes", side="right",
                   padx=5, pady=5, ipadx=5, ipady=5)

   def execute(self):
      """
      Execute
      """
      self.textbox.insert(tk.END, '\n'.join([f'{k}:{v[1]}' for k, v in
                                             self.dict_val.items()]))
      self.save_config()
      process = subprocess.Popen('python execute.py -d exec -c',
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 shell=True)
      output, error = process.communicate()
      self.textbox.insert(tk.END, output)

   def select_text(self, event, key):
      """
      change text action
      :param event:
      :param key:
      :return:
      """
      text = event.widget.get()
      self.dict_val[key][1] = text
      return text

   def select_bool(self, key):
      """
      change bool action
      :param key:
      :return:
      """
      text = self.fit.get()
      self.dict_val[key][1] = text
      return text

   def select_folder(self, key):
      """
      Select folder action
      :param key:
      :return:
      """
      text = fd.askdirectory(title="Select a Folder")
      self.dict_val[key][0].config(text=text)
      self.dict_val[key][1] = text
      return text

   def select_file(self, key, file_type=('text files', '*.txt')):
      """
      Change file action
      :param key:
      :param file_type:
      :return:
      """
      text = fd.askopenfilename(title="Select a File",
                                filetypes=[('all files', '.*'),
                                           ('text files', '.txt'),
                                           ('image files', ('.png', '.jpg')),
                                           ])
      self.dict_val[key][0].config(text=text)
      self.dict_val[key][1] = text
      return text

   def select_color(self, key):
      """
      Change color action
      :param key:
      :return:
      """
      text = tkcolor.askcolor()
      self.dict_val[key][0].config(text=text[1])
      self.dict_val[key][1] = text[1]
      return text

   def select_field_type(self, master, sec, key, value, row, col):
      """
      Select field type
      :param master:
      :param sec:
      :param key:
      :param value:
      :param row:
      :param col:
      """
      tb = None
      if re.match(r'^([Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee])$', value):
         self.fit.set(bool(value))
         tb = tk.Checkbutton(master, text=key, height=2,
                             variable=self.fit,
                             command=lambda: self.select_bool('%s_%s' % (
                                sec, key)))
         tb.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
      elif re.match(r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', value):
         tb = tk.Button(master, text=value, width=20,
                        command=lambda: self.select_color(
                           '%s_%s' % (sec, key)))
         tb.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
      elif re.match(r'^(.+)\/([^\/]+)\/$', value):
         tb = tk.Button(master, text=value, width=20,
                        command=lambda: self.select_folder(
                           '%s_%s' % (sec, key)))
         tb.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
      elif re.match(r'^(.+)\/([^\/]+)$', value):
         tb = tk.Button(master, text=value, width=20,
                        command=lambda: self.select_file('%s_%s' % (sec, key)))
         tb.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
      else:
         tb = tk.Entry(master, justify=tk.LEFT,
                       font=self.font, width=20)
         tb.delete(0, tk.END)
         tb.insert(0, "%s" % value)
         tb.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
         tb.bind("<KeyRelease>",
                 lambda event: self.select_text(event,
                                                key='%s_%s' % (sec, key)))
      self.dict_val.update({'%s_%s' % (sec, key): [tb, value]})

   def create_field(self, sec, master):
      """
      Create fields
      :param sec:
      :param master:
      """
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
         self.select_field_type(master, sec, k, v, r, lc + 1)
         r += 1
         if r > m:
            lc += 2
            r = 1

   def save_config(self):
      """
      Save config
      """
      for k, v in self.dict_val.items():
         sec, key = k.split('_')
         self.conf.set(sec, key, self.dict_val[k][1])
      self.export_config(self.conf, './config.ini')

   @staticmethod
   def export_config(conf, file):
      """
      Export config to file
      :param conf:
      :param file:
      """
      with open(file, "w") as file_obj:
         conf.write(file_obj)

class PrintLogger(object):  # create file like object
   """
   show log on simulated terminal
   """
   def __init__(self, textbox):  # pass reference to text widget
      self.textbox = textbox  # keep ref

   def write(self, text):
      """
      write line to term
      :param text:
      """
      self.textbox.insert(tk.END, text)  # write text to textbox
      # could also scroll to end of textbox here to make sure always visible

   def flush(self):  # needed for file like object
      """
      Flush
      """
      pass

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
