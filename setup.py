from distutils.core import setup
import py2exe

setup(windows=["file_encode_converter.py"] ,
      options = { "py2exe": { "includes": "chardet, Tkinter" } })
