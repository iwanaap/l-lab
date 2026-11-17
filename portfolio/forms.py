from django import forms


class ContactInquiryForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Nombre"}),
    )
    phone = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "+56 9 ..."}),
    )
    service = forms.ChoiceField(
        choices=[
            ("", "Selecciona una opción"),
            ("Conseguir más consultas", "Conseguir más consultas"),
            ("Ordenar mi operación", "Ordenar mi operación"),
            ("Automatizar tareas", "Automatizar tareas repetitivas"),
            ("Aún no lo sé", "Aún no lo sé, necesito orientación"),
        ]
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Ej.: las consultas llegan por varios canales y se nos pierden...",
                "rows": 4,
            }
        )
    )
