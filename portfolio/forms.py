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
                    ("", "Selecciona un servicio"),
                    ("Sitio web corporativo", "Sitio web corporativo"),
                    ("Landing page", "Landing page"),
                    ("Tienda online", "Tienda online"),
                    ("Aplicación web", "Aplicación web"),
                    ("Sistema interno", "Sistema interno"),
                    ("Dashboard", "Dashboard"),
                    ("Automatización / API", "Automatización / API"),
                    ("Mantención web", "Mantención web"),
                ]
            ),
            "message": forms.Textarea(attrs={"placeholder": "Cuéntame qué necesitas construir, mejorar o automatizar.", "rows": 5}),
        }
