from django import forms
from django.contrib.auth.forms import AuthenticationForm
from usuario.models import UsuarioDocente


# ------------------- FORMULARIO DE REGISTRO -------------------
class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmar contraseña", widget=forms.PasswordInput
    )

    class Meta:
        model = UsuarioDocente
        fields = [
            "gmail",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "apodo",
            "fecha_nacimiento",
        ]

    def clean_password2(self):
        """
        Valida que ambas contraseñas coincidan.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        """
        Guarda el usuario con la contraseña encriptada.
        """
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password1"])
        if commit:
            usuario.save()
        return usuario


# ------------------- FORMULARIO DE LOGIN -------------------
class LoginForm(AuthenticationForm):
    """
    Sobrescribimos username → ahora es gmail
    """

    username = forms.EmailField(label="Gmail")
