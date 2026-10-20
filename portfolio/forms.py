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
            ("", "Selecciona una solución"),
            ("Diagnóstico general", "Diagnóstico general (15 min)"),
            ("Web profesional", "Web profesional"),
            ("Catálogo web", "Catálogo web"),
            ("ERP para pymes", "ERP para pymes"),
            ("Automatización", "Automatización de procesos"),
            ("Desarrollo a medida", "Desarrollo a medida"),
        ]
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "¿Qué proceso quieres ordenar, vender mejor o dejar de hacer manualmente?",
                "rows": 5,
            }
        )
    )
