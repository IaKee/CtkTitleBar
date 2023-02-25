from tkinter import Tk, PhotoImage, Frame, Label, Button
from tkinter.ttk import Style
from ctypes import WinDLL, windll, wintypes, byref, c_uint
from win32api import GetSystemMetrics
from win32gui import FindWindow, GetWindowRect
from win32con import SM_CXSCREEN, SM_CYSCREEN
from PIL import Image, ImageTk


class CustomTitlebar(Frame):
	def __init__(self, app_title='', icon=None, bg='', hbg='', *args, **kwargs):
		Frame.__init__(self, bd=0, highlightthickness=0, *args, **kwargs)

		# Default color palette
		default_background_color = "#1E1E1E"
		default_highlight_color = "#F8F8F8"
		self.bg = bg if bg else default_background_color
		self.hbg = hbg if hbg else default_highlight_color
		self.configure(bg=self.bg)

		# Sprites
		self.icon_minimize = PhotoImage(file="assets/minisize_inactive.png")
		self.icon_minimize_active = PhotoImage(file="assets/minisize_active.png")
		self.icon_fullscreen = PhotoImage(file="assets/togglefull_inactive.png")
		self.icon_fullscreen_active = PhotoImage(file="assets/togglefull_active.png")
		self.icon_normal_size = PhotoImage(file="assets/fullwin_inactive.png")
		self.icon_normal_size_active = PhotoImage(file="assets/fullwin_active.png")
		self.icon_close = PhotoImage(file="assets/close_inactive.png")
		self.icon_close_active = PhotoImage(file="assets/close_active.png")
		self.default_icon_path = "assets/default.png"

		# Main attributes
		self.taskbar_height = self.get_taskbar_height()
		self.window_size_x, self.window_size_y = self.master.winfo_geometry().rsplit('x')
		self.fullscreen = True if self.master.state() == "zoomed" else False
		
		self.app_title = app_title if app_title else self.master.title()
		hicon = icon if icon else self.default_icon_path
		original_icon = Image.open(hicon).convert("RGBA")
		resized_icon = original_icon.resize((16, 16), resample=Image.LANCZOS)
		#self.resized_icon = PhotoImage(file=original_icon)
		self.icon = ImageTk.PhotoImage(resized_icon, format='png')

		# Create the window title label
		self.icon_lbl = Label(
			master = self, 
			image = self.icon,
			background = self.bg,
			bd = 0, 
			highlightthickness = 0)
		self.icon_lbl.pack(side="left")

		# Create buttons
		self.btn_minimize = Button(
			master = self, 
			image = self.icon_minimize, 
			command = self.master.iconify, 
			background = self.bg,
			bd = 0, 
			highlightthickness = 0,
			takefocus = False)
		self.btn_fullscreen = Button(
			master = self, 
			image = self.icon_normal_size, 
			command = self.toggle_fullscreen, 
			background = self.bg,
			bd = 0, 
			highlightthickness = 0,
			takefocus = False)
		self.btn_close = Button(
			master = self, 
			image = self.icon_close, 
			command = self.master.destroy, 
			background = self.bg,
			bd = 0, 
			highlightthickness = 0,
			takefocus = False)
		self.btn_close.pack(padx=5, side='right')
		self.btn_fullscreen.pack(side='right')
		self.btn_minimize.pack(padx=5, side='right')

		# Create the window title label
		self.title_lbl = Label(
			master = self, 
			text = self.app_title, 
			font=("Segoe UI", 9),
			background = self.bg,
			foreground = self.hbg)
		self.title_lbl.pack(side="left", padx=(8, 0), pady=4, fill='x')

		# Bind mouse events to change button images
		self.btn_minimize.bind("<Enter>", lambda e: self.btn_minimize.config(image=self.icon_minimize_active))
		self.btn_minimize.bind("<Leave>", lambda e: self.btn_minimize.config(image=self.icon_minimize))
		self.btn_fullscreen.bind("<Enter>", lambda e: self.btn_fullscreen.config(image=self.icon_normal_size_active))
		self.btn_fullscreen.bind("<Leave>", lambda e: self.btn_fullscreen.config(image=self.icon_normal_size))
		self.btn_close.bind("<Enter>", lambda e: self.btn_close.config(image=self.icon_close_active))
		self.btn_close.bind("<Leave>", lambda e: self.btn_close.config(image=self.icon_close))

		# Hides parent window title bar
		self.master.overrideredirect(True)
		self.pack(side='top', fill='x')

	def toggle_fullscreen(self, event=None):
		
		if self.fullscreen:
			# Adjusts the sprite of the maximize button
			self.btn_fullscreen.bind("<Enter>", lambda e: self.btn_fullscreen.config(image=self.icon_normal_size_active))
			self.btn_fullscreen.bind("<Leave>", lambda e: self.btn_fullscreen.config(image=self.icon_normal_size))
			self.btn_fullscreen.config(image=self.icon_fullscreen)
	
			# return to normal size
			self.master.geometry(f'{self.window_size_x}x{self.window_size_y}')
		else:
			# Adjusts the sprite of the maximize button
			self.btn_fullscreen.bind("<Enter>", lambda e: self.btn_fullscreen.config(image=self.icon_fullscreen_active))
			self.btn_fullscreen.bind("<Leave>", lambda e: self.btn_fullscreen.config(image=self.icon_fullscreen))
			self.btn_fullscreen.config(image=self.icon_fullscreen_active)

			# Saves current window size to restore later
			self.window_size_x, self.window_size_y = self.master.winfo_geometry().rsplit('x')

			# Gets information about current screenspace
			taskbar_heigh = self.get_taskbar_height()
			taskbar_width = self.get_taskbar_width()
			autohide = self.get_taskbar_autohide()
			taskbar_orient = self.get_taskbar_orientation()
			screen_width, screen_height = self.get_cointaining_screenspace()

			# Adjusts screenspace accordingly to taskbar position
			if(not autohide):
				if(taskbar_orient == 'x'):
					screen_height -= taskbar_heigh
				else:
					screen_width -= taskbar_width

			self.master.geometry(f'{screen_width}x{screen_height}')
			
		self.fullscreen = not self.fullscreen


	def on_map(self, *args):
		self.master.after(10, self.fix_titlebar_position)

	def fix_titlebar_position(self):
		# Fix the titlebar position after the window is mapped
		x, y = self.master.winfo_x(), self.master.winfo_y()
		self.master.geometry(f"+{x}+{y}")
		self.master.after(10, self.fix_titlebar_position)
	def get_taskbar_height(self):
		hWnd = windll.user32.FindWindowW('Shell_TrayWnd', None)
		rect = wintypes.RECT()
		windll.user32.GetWindowRect(hWnd, byref(rect))
		return rect.bottom - rect.top
	def get_taskbar_width(self):
		hWnd = windll.user32.FindWindowW('Shell_TrayWnd', None)
		rect = wintypes.RECT()
		windll.user32.GetWindowRect(hWnd, byref(rect))
		return rect.left - rect.right
	def get_taskbar_orientation(self):
		# Gets screenspace coordinates
		screen_width = GetSystemMetrics(SM_CXSCREEN)
		screen_height = GetSystemMetrics(SM_CYSCREEN)

		# Gets taskbar coordinates
		hwnd = FindWindow("Shell_TrayWnd", None)
		taskbar_rect = GetWindowRect(hwnd)
		if taskbar_rect[1] == 0 and taskbar_rect[3] < screen_height:
			# taskbar is on y coordinate
			return 'y'
		else:
			# taskbar is on x coordinate
			return 'x'
	def get_taskbar_autohide(self):
		SPI_GETFOREGROUNDLOCKTIMEOUT = 0x2000
		user32 = WinDLL('user32')

		timeout = c_uint()
		user32.SystemParametersInfoW(SPI_GETFOREGROUNDLOCKTIMEOUT, 0, byref(timeout), 0)

		if timeout.value == 0:
			# taskbar wont hide
			return False

		else:
			# taskbar will hide
			return True
	def get_cointaining_screenspace(self):
		return self.master.winfo_screenwidth(), self.master.winfo_screenheight()
# test		
if __name__ == '__main__':
	# Create the main window
	root = Tk()
	root['bg'] = 'black'
	root.geometry('600x400')
	root.title('Custom Titlebar Demo')

	# Create the custom title bar
	title_bar = CustomTitlebar(master=root)
	
	print(title_bar.get_taskbar_height())
	# Start the main event loop
	root.mainloop()