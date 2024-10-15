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
        self.display_nums = []
        self.full_operation = []

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
        # clear output
        self.result_string.set(0)
        self.formula_string.set('')

        # clear data
        self.display_nums.clear()
        self.full_operation.clear()

    def invert(self, text):
        current_number = ''.join(self.display_nums)
        if current_number:
            if float(current_number) > 0:
                self.display_nums.insert(0, '-')
            else:
                del self.display_nums[0]

            self.result_string.set(''.join(self.display_nums))

    def percent(self, text):
        if self.display_nums:
            current_number = float(''.join(self.display_nums))
            percent_number = current_number / 100

            # update data
            self.display_nums = list(str(percent_number))
            self.result_string.set(''.join(self.display_nums))

    def number(self, number):
        self.display_nums.append(str(number))
        full_number = ''.join(self.display_nums)
        self.result_string.set(full_number )

    def math(self, math_operator):
        if math_operator == '÷':
            math_operator = '/'
        elif math_operator == 'x':
            math_operator = '*'

        current_number = ''.join(self.display_nums)
        if current_number:
            self.full_operation.append(current_number)
            if math_operator != '=':
                # update data
                self.full_operation.append(math_operator)
                self.display_nums.clear()

                # update output
                self.result_string.set('')
                self.formula_string.set(' '.join(self.full_operation))
            else:
                formula = ' '.join(self.full_operation)
                result = eval(formula)

                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 3)

                # update data
                self.full_operation.clear()
                self.display_nums = [str(result)]

                # update output
                self.result_string.set(result)
                self.formula_string.set(formula)

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