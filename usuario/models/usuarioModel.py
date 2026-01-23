from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

# ------------------- MANAGER -------------------
class UsuarioDocenteManager(BaseUserManager):
    """
    Manager que define cómo se crean los docentes (usuarios normales) 
    y superusuarios usando el gmail como identificador.
    """

    def create_user(self, gmail, password=None, **extra_fields):
        if not gmail:
            raise ValueError("El usuario debe tener un gmail")

        gmail = self.normalize_email(gmail)
        user = self.model(gmail=gmail, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, gmail, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(gmail, password, **extra_fields)


# ------------------- MODELO -------------------
class UsuarioDocente(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado para Docentes.
    Usa 'gmail' como identificador único de inicio de sesión.
    """

    gmail = models.EmailField(unique=True, verbose_name="Correo Electrónico (Gmail)")

    # Campos personales
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    apodo = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField()

    # Campos de estado y permisos
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Vinculamos con el nuevo manager
    objects = UsuarioDocenteManager()

    # Configuración de Login
    USERNAME_FIELD = "gmail"
    # Campos obligatorios al crear por consola (createsuperuser)
    REQUIRED_FIELDS = ["primer_nombre", "primer_apellido", "fecha_nacimiento"]

    class Meta:
        verbose_name = "Usuario Docente"
        verbose_name_plural = "Usuarios Docentes"

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} ({self.gmail})"