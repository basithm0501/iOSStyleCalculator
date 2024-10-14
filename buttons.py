from customtkinter import CTkButton
from settings import *

class Button(CTkButton):
    def __init__(self, parent, text, func, col, row, font, colspan = 1, color='dark-gray'):
        super().__init__(
            master=parent,
            command = lambda: func(text),
            corner_radius=STYLING['corner-radius'],
            text=text,
            font=font,
            fg_color=COLORS[color]['fg'],
            hover_color=COLORS[color]['hover'],
            text_color=COLORS[color]['text'],
        )
        self.grid(column=col, row=row, columnspan=colspan, sticky='news', padx=STYLING['gap'], pady=STYLING['gap'])