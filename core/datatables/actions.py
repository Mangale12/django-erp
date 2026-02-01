class ActionGroup:
    def __init__(self, *buttons):
        self.buttons = buttons

    def render(self, obj):
        rendered = "".join(btn.render(obj) for btn in self.buttons)
        return f'<div class="btn-group btn-group-sm">{rendered}</div>'
