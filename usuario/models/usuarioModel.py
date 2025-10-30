from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


# ------------------- MANAGER -------------------
class UsuarioManager(BaseUserManager):
    """
    Manager que define cómo se crean usuarios normales y superusuarios.
    Sobrescribe el comportamiento de create_user y create_superuser.
    """

    def create_user(self, gmail, password=None, **extra_fields):
        """
        Crea y guarda un usuario con gmail como identificador único.
        """
        if not gmail:
            raise ValueError("El usuario debe tener un gmail")

        # Normaliza el correo (todo en minúsculas)
        gmail = self.normalize_email(gmail)
        usuario = self.model(gmail=gmail, **extra_fields)
        usuario.set_password(password)  # Encripta la contraseña
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, gmail, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con permisos de administrador.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(gmail, password, **extra_fields)


# ------------------- MODELO -------------------
class UsuarioPersonalizado(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado.
    Reemplaza el User por defecto de Django para usar gmail como login.
    """

    gmail = models.EmailField(unique=True)  # Este será el identificador de login

    # Campos personales
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    apodo = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField()

    # Campos de control para permisos
    is_active = models.BooleanField(default=True)  # Si el usuario está activo
    is_staff = models.BooleanField(default=False)  # Si puede entrar al admin

    # Vinculamos con nuestro manager
    objects = UsuarioManager()

    # Sobrescribimos el identificador único → ahora es gmail
    USERNAME_FIELD = "gmail"
    REQUIRED_FIELDS = ["primer_nombre", "primer_apellido", "fecha_nacimiento"]

    def __str__(self):
        """
        Representación legible del usuario.
        """
        return f"{self.primer_nombre} {self.primer_apellido} ({self.gmail})"
