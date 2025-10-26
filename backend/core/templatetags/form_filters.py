from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    """
    Filtro para añadir clases CSS a los campos del formulario.
    Ejemplo en template:
    {{ form.titulo|add_class:"form-control" }}
    """
    return field.as_widget(attrs={"class": css})
