from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class FormularioAcceso(forms.Form):
    gmail = forms.EmailField(
        label="Correo electronico",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Ingresa tu correo"}
        ),
    )
    contrasena = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Ingresa tu contraseña"}
        ),
    )

    def clean(self):
        """
        Valida las credenciales del usuario
        """
        cleaned_data = super().clean()
        gmail = cleaned_data.get("gmail")
        contrasena = cleaned_data.get("contrasena")

        if gmail and contrasena:
            usuario = authenticate(username=gmail, password=contrasena)
            if usuario is None:
                raise ValidationError("Correo o contraseña incorrectos")

        return cleaned_data
