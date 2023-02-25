import tkinter as tk
from main import CustomTitlebar

# Cria a janela principal
root = tk.Tk()
root.geometry('400x400')
root.configure(bg='#333333')

# Cria a barra de título personalizada
title_bar = CustomTitlebar(root, 'Minha Janela', '#333333', '#ffffff', '#fe731f', icon_path='path/to/icon.png')

# Adiciona widgets à janela principal
tk.Label(root, text='Exemplo de Janela', bg='#333333', fg='#ffffff', font=('Arial', 20)).pack(pady=20)

# Empacota a barra de título personalizada
title_bar.pack(fill='x')

# Inicia o loop principal da janela
root.mainloop()
