# sor_agent/tools/helpers/print_style.py
class PrintStyle:
    def __init__(self, font_color="blue", background_color="white", bold=False, padding=False):
        self.font_color = font_color
        self.background_color = background_color
        self.bold = bold
        self.padding = padding

    def print(self, message):
        style = f"color: {self.font_color}; background: {self.background_color};"
        if self.bold:
            style += " font-weight: bold;"
        if self.padding:
            style += " padding: 5px;"
        print(f"<span style='{style}'>{message}</span>")
