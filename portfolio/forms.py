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
                    ("", "Selecciona un plan o servicio"),
                    ("Plan Web Esencial", "Plan Web Esencial"),
                    ("Plan Empresa", "Plan Empresa"),
                    ("Plan Automatización", "Plan Automatización"),
                    ("Desarrollo a medida", "Desarrollo a medida"),
                    ("Mantención web", "Mantención web"),
                ]
            ),
            "message": forms.Textarea(attrs={"placeholder": "Cuéntame qué necesitas construir, mejorar o automatizar.", "rows": 5}),
        }
