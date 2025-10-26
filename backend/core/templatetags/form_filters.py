from django import template

register = template.Library()

@register.filter(name="add_class")
def add_class(field, css_class):
    """
    Filtro para añadir una clase CSS a un campo de formulario.
    Uso: {{ form.campo|add_class:"form-control" }}
    """
    return field.as_widget(attrs={"class": css_class})
