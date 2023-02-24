# CtkTitlebar - Custom Tkinter Titlebar

CtkTitlebar is a Python package that provides a customizable title bar for Tkinter windows, with a design that blends seamlessly with a modified Azure theme that allows for customization of the highlight color.

This modified Azure theme can be easily customized to use any color as the highlight color, not just orange. This means that the title bar can be easily tailored to match the color scheme of any application or website.

# Installation
You can install CtkTitlebar using pip:

```python
pip install CtkTitlebar
```

# Usage

Using CtkTitlebar is easy. Simply import it into your Python script and create a CtkTitlebar object, passing in the Tk object that represents your main window:
```python
from ctktitlebar import CtkTitlebar
import tkinter as tk

root = tk.Tk()

# create a CtkTitlebar object
titlebar = CtkTitlebar(root)

# set the title of the main window
root.title('My Application')

# add some widgets to the main window
label = tk.Label(root, text='Hello, world!')
label.pack()

# start the main event loop
root.mainloop()
```
# Credits

CtkTitlebar is based on the [CustomTkinterTitlebar](https://github.com/littlewhitecloud/CustomTkinterTitlebar) project by [littlewhitecloud](https://github.com/littlewhitecloud) and is designed to work seamlessly with the modified [Azure-Ttk-Theme](https://github.com/rdbende/Azure-ttk-theme) by [rdbende](https://github.com/rdbende).

# License

CtkTitlebar, the modified Azure theme and the CustomTitleBar library are all released under the MIT License. See the [LICENSES](https://github.com/IaKee/CtkTitlebar/blob/main/LICENSES) file for more information.
