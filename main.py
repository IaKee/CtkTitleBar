from tkinter import Tk
from tkinter.ttk import Frame, Style, Label
from PIL import ImageTk, Image


class CustomTitleBar(Frame):
	def __init__(
		self, 
		title, 
		icon_path = None, 
		*args, 
		**kwargs):
			# initializes super
			Frame.__init__(*args, **kwargs)

			self.master = master
			self.icon_path = icon_path
			self.title = title
			self.initUI()
			
			# Define a paleta de cores
			self.color_pallete = {
				"fg": "#ffffff",
				"bg": "#333333",
				"disabledfg": "#aaaaaa",
				"disabledbg": "#737373",
				"selectfg": "#ffffff",
				"selectbg": "#fe731f"
			}

			# Abre os sprites
			self.__minisize_active_img = Image.open("assets/minisize_active.png")
			self.__minisize_inactive_img = Image.open("assets/minisize_inactive.png")
			self.__togglefull_active_img = Image.open("assets/togglefull_active.png")
			self.__togglefull_inactive_img = Image.open("assets/togglefull_inactive.png")
			self.__close_active_img = Image.open("assets/close_active.png")
			self.__close_inactive_img = Image.open("assets/close_inactive.png")
			self.__fullwin_active_img = Image.open("assets/fullwin_active.png")
			self.__fullwin_inactive_img = Image.open("assets/fullwin_inactive.png")

			# Converte as imagens para o formato do Tkinter
			self.__minisize_active = ImageTk.PhotoImage(self.__minisize_active_img)
			self.__minisize_inactive = ImageTk.PhotoImage(self.__minisize_inactive_img)
			self.__togglefull_active = ImageTk.PhotoImage(self.__togglefull_active_img)
			self.__togglefull_inactive = ImageTk.PhotoImage(self.__togglefull_inactive_img)
			self.__close_active = ImageTk.PhotoImage(self.__close_active_img)
			self.__close_inactive = ImageTk.PhotoImage(self.__close_inactive_img)
			self.__fullwin_active = ImageTk.PhotoImage(self.__fullwin_active_img)
			self.__fullwin_inactive = ImageTk.PhotoImage(self.__fullwin_inactive_img)

			# Define o ícone da janela
			self.__icon_img = ImageTk.PhotoImage(Image.open("assets/tk.ico"))

			# constants
			self.TITLE_BAR_HEIGHT = 30
	
	def initUI(self):
		self.config(height=32, background="#333333")

		# Define a posição dos botões de controle da janela
		self.btn_close = ttk.Button(self, style="TitlebarButton.TButton")
		self.btn_close.place(x=575, y=4, width=20, height=20)
		self.btn_minimize = ttk.Button(self, style="TitlebarButton.TButton")
		self.btn_minimize.place(x=550, y=4, width=20, height=20)
		self.btn_maximize = ttk.Button(self, style="TitlebarButton.TButton")
		self.btn_maximize.place(x=525, y=4, width=20, height=20)

		# Carrega o ícone da janela
		icon = Image.open(self.icon_path)
		icon = icon.resize((16, 16), Image.ANTIALIAS)
		icon = ImageTk.PhotoImage(icon)
		self.icon_label = tk.Label(self, image=icon, bg="#333333")
		self.icon_label.image = icon
		self.icon_label.place(x=8, y=8)

		# Define o título da janela
		self.title_label = tk.Label(self, text=self.title, font=("Segoe UI", 9), bg="#333333", fg="#ffffff")
		self.title_label.place(x=30, y=8)

		# Faz com que a barra de título possa ser arrastada para mover a janela
		self.bind("<ButtonPress-1>", self.start_move)
		self.bind("<ButtonRelease-1>", self.stop_move)
		self.bind("<B1-Motion>", self.on_motion)

    # Inicia o movimento da janela
	def start_move(self, event):
		self.x = event.x
		self.y = event.y

    # Finaliza o movimento da janela
	def stop_move(self, event):
		self.x = None
		self.y = None

    # Realiza o movimento da janela
	def on_motion(self, event):
		deltax = event.x - self.x
		deltay = event.y - self.y
		x = self.master.winfo_x() + deltax
		y = self.master.winfo_y() + deltay
		self.master.geometry(f"+{x}+{y}")