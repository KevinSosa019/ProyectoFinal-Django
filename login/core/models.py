
from django.db import models
from django.contrib.auth.models import User
from datetime import date
import datetime
from django.utils import timezone
from django.contrib.auth.models import User as AuthUser 
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _



class User(AuthUser):
    class Meta:
        proxy = True

class CustomUser(models.Model):
    is_denounced = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='customuser_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_set',
        related_query_name='user',
    )

class Denuncia(models.Model):
    usuario_denunciado = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='denuncias')
    motivo = models.TextField()

    def __str__(self):
        return f"Denuncia de {self.usuario_denunciado.username}: {self.motivo}"

# Create your models here.
def generar_codigo():
    return timezone.now().strftime('%Y%m%d%H%M%S')

class Publicacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='publicaciones_realizadas')
    codigo = models.CharField(max_length=20, unique=True, default=generar_codigo)
    titulo = models.CharField(max_length=100, default='Título Predeterminado')
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cantidad = models.IntegerField(default=0)  
    unidad = models.CharField(max_length=10, choices=[('Kg', 'Kg'), ('g', 'g'), ('L', 'L')], default='Kg')  
    categoria = models.CharField(max_length=100, choices=[('Vegetales', 'Vegetales'), ('Frutas', 'Frutas'), ('Hierbas', 'Hierbas')], default='Vegetales')  # Ejemplo de valor predeterminado
    fechaCosecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(default='Descripción predeterminada')  
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='publicaciones_vendidas')  

    class Meta:
      verbose_name = 'Publicacion'
      verbose_name_plural = 'Publicaciones'
      ordering = ['codigo']

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.titulo, self.precio)
 
class Mensaje(models.Model):
    remite = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De: {self.remite.username}, Para: {self.destinatario.username}, Fecha: {self.fecha_envio}"
    


