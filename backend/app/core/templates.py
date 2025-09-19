import os
from jinja2 import Environment, FileSystemLoader

# Path to the templates folder
templates_path = os.path.join(os.path.dirname(__file__), "..", "templates")

env = Environment(loader=FileSystemLoader(templates_path))

def render_template(template_name: str, **kwargs) -> str:
    """Render an HTML template with variables."""
    template = env.get_template(template_name)
    return template.render(**kwargs)
