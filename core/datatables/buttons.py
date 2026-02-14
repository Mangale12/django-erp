class ActionButton:
    def __init__(self, label, url, icon=None, css="btn btn-sm btn-primary", attrs=None):
        self.label = label
        self.url = url
        self.icon = icon
        self.css = css
        self.attrs = attrs or {}

    def render(self, obj):
        attrs_html = " ".join(
            f'data-{k}="{v(obj) if callable(v) else v}"'
            for k, v in self.attrs.items()
        )

        icon_html = f'<i data-feather="{self.icon}"></i>' if self.icon else ""

        return f"""
        <a href="{self.url(obj)}" class="{self.css}" {attrs_html}>
            {icon_html} {self.label}
        </a>
        """
