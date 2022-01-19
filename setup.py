import sys
from cx_Freeze import setup, Executable


setup(name="Nesne Tanima",
      version="0.1",
      description="This software detects objects in realtime",
      executables=[Executable("anadosya4.py")]
      )

