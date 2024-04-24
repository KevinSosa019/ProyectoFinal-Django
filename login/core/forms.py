from django import forms
from .models import Mensaje
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm



class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Este correo electrónico ya está registrado')
		return email
	
class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['destinatario', 'mensaje']

class DenunciaForm(forms.Form):
       motivo = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Describe el motivo de la denuncia'}))
    
    
class CambiarContraseñaForm(forms.Form):
    password_actual = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput)
    nueva_contraseña = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CambiarContraseñaForm, self).__init__(*args, **kwargs)

    def clean_password_actual(self):
        password_actual = self.cleaned_data.get('password_actual')
        if not self.user.check_password(password_actual):
            raise forms.ValidationError('La contraseña actual es incorrecta')
        return password_actual

    def clean_confirmar_contraseña(self):
        nueva_contraseña = self.cleaned_data.get('nueva_contraseña')
        confirmar_contraseña = self.cleaned_data.get('confirmar_contraseña')
        if nueva_contraseña and confirmar_contraseña and nueva_contraseña != confirmar_contraseña:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return confirmar_contraseña
    
class ActualizarDatosForm(UserChangeForm):
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email']  
