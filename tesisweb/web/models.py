from enum import unique
from django.db import models  
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
class usuarios(models.Model):
    cedula = models.CharField(max_length=150,primary_key=False)
    nombre = models.CharField(max_length=150)
    id_usuario = models.CharField(max_length=150, blank=True) 
    
    class Meta:
        verbose_name_plural = "Usuarios"

class interacciones(models.Model):
    nombre = models.CharField(max_length=150)
    fecha = models.DateField()
    hora = models.TimeField()
    razon = models.CharField(max_length=150)
    contrato = models.CharField(max_length=100)
    cedula = models.CharField(max_length=150)
    class Meta:
        verbose_name_plural = "Interacciones"

class horariospermitidos(models.Model):

    class dias(models.TextChoices):
        LUNES = 'Lunes', 'Lunes'
        MARTES = 'Martes', 'Martes'
        MIERCOLES = 'Miercoles','Miercoles'
        JUEVES = 'Jueves', 'Jueves'
        VIERNES = 'Viernes', 'Viernes'
        SABADO = 'Sabado', 'Sabado'
        DOMINGO = 'Domingo', 'Domingo'
        SIEMPRE = 'Siempre', 'Siempre'

    # en este campo se debe poner el "id" del usuario, no la cedula
    dia=models.CharField(max_length=20, choices=dias.choices, default=dias.LUNES)
    entrada=models.TimeField()
    salida=models.TimeField()
    cedula = models.CharField(max_length=150)
    class Meta:
        verbose_name_plural = "Horarios"

# class apertura(models.Model):
#     acceso = models.CharField(max_length=50)
#     id_usuario = models.CharField(max_length=150)
#     cedula = serializers.CharField()
#     id_usuario = serializers.CharField()



class UserManager(BaseUserManager):
    def create_user(self, cedula, email, password):
        
        if not email or not cedula:
            raise ValueError('El usuario debe tener un correo valido y una cedula')

        user = self.model(
            cedula=cedula,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, email, password):
        
        if not email or not cedula:
            raise ValueError('El usuario debe tener un correo valido y una cedula')

        user = self.create_user (
            cedula,
            email,
            password=password
        )
        user.staff = True
        user.admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    cedula = models.CharField(max_length=200, unique = True)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'cedula'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email','password']
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
    
    objects = UserManager()