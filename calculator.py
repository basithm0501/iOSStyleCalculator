import customtkinter as ctk
from buttons import Button
import darkdetect
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class Calculator(ctk.CTk):
    def __init__(self, is_dark):

        # setup
        super().__init__(fg_color=(WHITE, BLACK))
        ctk.set_appearance_mode(f'{'dark' if is_dark else 'light'}')
        self.title('iOS Style Calculator')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.iconbitmap('') # Does not function since on Mac
        self.resizable(False, False)

        # layout
        self.rowconfigure(list(range(MAIN_ROWS)), weight=1, uniform='a')
        self.columnconfigure(list(range(MAIN_COLUMNS)), weight=1, uniform='a')

        # data
        self.result_string = ctk.StringVar(value = '0')
        self.formula_string = ctk.StringVar(value = '')

        # widgets
        self.create_widgets()

        self.mainloop()

    def create_widgets(self):
        # fonts
        main_font = ctk.CTkFont(family=FONT, size=NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family=FONT, size=OUTPUT_FONT_SIZE)

        # output labels
        OutputLabel(self, 0, 'se', main_font, self.formula_string)
        OutputLabel(self, 1, 'e', result_font, self.result_string)

        # AC Button
        Button(
            parent=self, 
            func=self.clear,
            text=OPERATORS['clear']['text'], 
            col=OPERATORS['clear']['col'], 
            row=OPERATORS['clear']['row'],
            font=main_font
        )

        # Invert Button
        Button(
            parent=self, 
            func=self.invert,
            text=OPERATORS['invert']['text'], 
            col=OPERATORS['invert']['col'], 
            row=OPERATORS['invert']['row'],
            font=main_font
        )

        # Percentage Button
        Button(
            parent=self, 
            func=self.percent,
            text=OPERATORS['percent']['text'], 
            col=OPERATORS['percent']['col'], 
            row=OPERATORS['percent']['row'],
            font=main_font
        )

        # number butttons
        for num, data in NUM_POSITIONS.items():
            Button(
                parent=self,
                text=num,
                func=self.number,
                col=data['col'],
                row=data['row'],
                font=main_font,
                color='light-gray',
                colspan=data['span']
            )

        # math buttons
        for math, data in MATH_POSITIONS.items():
            Button(
                parent=self,
                text=data['character'],
                func=self.math,
                col=data['col'],
                row=data['row'],
                font=main_font,
                color='orange',
            )

    def clear(self, text):
        print('clear')

    def invert(self, text):
        print('invert')

    def percent(self, text):
        print('percent')

    def number(self, number):
        print(number)

    def math(self, math_operator):
        print(math_operator)

    def title_bar_color(self, is_dark):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLORS['dark'] if is_dark else TITLE_BAR_HEX_COLORS['light']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(master=parent, font=font, textvariable=string_var)
        self.grid(column=0, columnspan=4, row=row, sticky=anchor, padx=10)

if __name__ == '__main__':
    Calculator(darkdetect.isDark())