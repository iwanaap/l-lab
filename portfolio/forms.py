from django import forms

from .models import ContactInquiry


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ["name", "email", "phone", "service", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Nombre"}),
            "email": forms.EmailInput(attrs={"placeholder": "correo@empresa.cl"}),
            "phone": forms.TextInput(attrs={"placeholder": "+56 9 ..."}),
            "service": forms.Select(
                choices=[
                    ("", "Selecciona una solución"),
                    ("Diagnóstico general", "Diagnóstico general (15 min)"),
                    ("Web profesional", "Web profesional"),
                    ("Catálogo web", "Catálogo web"),
                    ("ERP para pymes", "ERP para pymes"),
                    ("Automatización", "Automatización de procesos"),
                    ("Desarrollo a medida", "Desarrollo a medida"),
                ]
            ),
            "message": forms.Textarea(attrs={"placeholder": "¿Qué proceso quieres ordenar, vender mejor o dejar de hacer manualmente?", "rows": 5}),
        }
