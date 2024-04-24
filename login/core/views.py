from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from .models import Publicacion
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .forms import MensajeForm, DenunciaForm
from .models import Mensaje
from django.contrib.auth.models import User
from decimal import Decimal, InvalidOperation
from .forms import ActualizarDatosForm, CustomUserCreationForm, CambiarContraseñaForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from .forms import DenunciaForm
from .models import Denuncia
from .models import CustomUser

# Create your views here.
#inicio_admin
def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:  
                    return redirect('administrador')  
                else:
                    return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def administrador(request):
    nombre_admin = request.user.username 
    usuarios_denunciados = CustomUser.objects.filter(is_denounced=True)
    return render(request, 'superestrella/administrador.html', {'nombre_admin': nombre_admin, 'usuarios_denunciados': usuarios_denunciados})

@login_required
def juicio(request, usuario_id):
    usuario_denunciado = get_object_or_404(User, pk=usuario_id)
    return render(request, 'superestrella/juicio.html', {'usuario_denunciado': usuario_denunciado})

@login_required
def denunciar(request, vendedor_id):
    #fallo
    vendedor = get_object_or_404(User, id=vendedor_id)
    
    
    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        if form.is_valid():
            motivo = form.cleaned_data['motivo']
            print("Motivo de la denuncia:", motivo)
            
            denuncia = Denuncia(usuario_denunciado=vendedor, motivo=motivo)
            denuncia.save()
            messages.success(request, 'Denuncia enviada correctamente.')
            return redirect('ver_perfil_vendedor', vendedor_id=vendedor_id)
    else:
        form = DenunciaForm(initial={'usuario_denunciado': vendedor_id})
    return render(request, 'core/denunciar.html', {'form': form, 'vendedor': vendedor})



#Mostrar las publicaiones al inicio 
def home(request):
    publicacionesListados = Publicacion.objects.all()
    return render(request, "core/home.html", {"publicaciones": publicacionesListados})

def detalle_publicacion(request, codigo):
    publicacion = get_object_or_404(Publicacion, codigo=codigo)
    vendedor = publicacion.vendedor
    return render(request, 'core/detalle_publicacion.html', {'publicacion': publicacion, 'vendedor': vendedor})

def ver_perfil_vendedor(request, vendedor_id):
    vendedor = get_object_or_404(User, id=vendedor_id)
    publicaciones = Publicacion.objects.filter(vendedor=vendedor)
    return render(request, 'core/ver_perfil_vendedor.html', {'vendedor': vendedor, 'publicaciones': publicaciones})
@login_required
def enviar_mensaje(request, vendedor_id):
    vendedor = get_object_or_404(User, id=vendedor_id)
    mensajes = Mensaje.objects.filter(destinatario=vendedor)

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            destinatario_id = form.cleaned_data['destinatario']
            destinatario = get_object_or_404(User, id=destinatario_id)
            mensaje_texto = form.cleaned_data['mensaje']
            mensaje_enviado = Mensaje.objects.create(remite=request.user, destinatario=destinatario, mensaje=mensaje_texto)
            mensaje_recibido = Mensaje.objects.create(remite=destinatario, destinatario=request.user, mensaje=mensaje_texto)
            messages.success(request, 'Mensaje enviado correctamente.')
            return redirect(reverse('mensajes_enviados'))
    else:
        form = MensajeForm()
    
    return render(request, 'core/enviar_mensaje.html', {'form': form})

@login_required
def mensajes_enviados(request):
    mensajes = Mensaje.objects.filter(remite=request.user)
    return render(request, 'core/mensajes_enviados.html', {'mensajes': mensajes})

@login_required
def mensajes_recibidos(request):
    mensajes = Mensaje.objects.filter(destinatario=request.user)
    return render(request, 'core/mensajes_recibidos.html', {'mensajes': mensajes})



def nosotros(request):
    return render(request, 'core/nosotros.html')

def perfil(request):
    return render(request, 'core/perfil.html')


"""@login_required
def products(request):
    return render(request, 'core/products.html')"""

def exit(request):
    logout(request)
    return redirect('home')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)


#Publicaciones
@login_required
def publicar(request):
    publicacionesListados = Publicacion.objects.filter(usuario=request.user)
    messages.success(request, 'Publicacion listada!')
    return render(request, "Venta/PublicarVenta.html", {"publicaciones": publicacionesListados})

#2da
@login_required
def registrarPublicacion(request):
    if request.method == 'POST':
        #codigo = request.POST['txtCodigo']
        titulo = request.POST['txtTitulo']
        precio = request.POST['numPrecio']
        cantidad = request.POST['numCantidad']
        unidad = request.POST['txtUnidad']
        categoria = request.POST['txtCategoria']
        fechaCosecha = request.POST['fechaCosecha']
        descripcion = request.POST['txtDescripcion']
        
        vendedor = request.user

        
        fechaCosecha_str = str(fechaCosecha)

        
        usuario = request.user

        publicacion = Publicacion.objects.create(
            usuario=usuario,
            #codigo=codigo, 
            titulo=titulo, 
            precio=precio,
            cantidad=cantidad,
            unidad=unidad,
            categoria=categoria,
            fechaCosecha=fechaCosecha_str,
            descripcion=descripcion,
            vendedor=vendedor,
            )
        
  
    messages.success(request, 'Publicacion registrada!')
    return redirect('/publicar')

def edicionPublicacion(request, codigo):
    publicacion = Publicacion.objects.get(codigo=codigo)
    return render(request, "Venta/edicionPublicacion.html", {"publicacion": publicacion})


def editarPublicacion(request):
    codigo = request.POST['txtCodigo']
    titulo = request.POST['txtTitulo']
    precio = request.POST['numPrecio']
    cantidad = request.POST['numCantidad']
    unidad = request.POST['txtUnidad']
    categoria = request.POST['txtCategoria']
    fechaCosecha = request.POST['fechaCosecha']
    descripcion = request.POST['txtDescripcion']
    
    precio_str = request.POST['numPrecio']  # Obtener el valor del precio como cadena

    try:
        precio = Decimal(precio_str)  # Intentar convertir a Decimal
    except InvalidOperation:
        # Manejar el error si el valor no es un número decimal válido
        print("Error al convertir el precio a Decimal:", precio_str)
        messages.error(request, 'El precio debe ser un número decimal válido.')
        return redirect('/publicar')

    publicacion = Publicacion.objects.get(codigo=codigo)
    publicacion.titulo = titulo
    publicacion.precio = precio
    publicacion.cantidad = cantidad
    publicacion.unidad = unidad
    publicacion.categoria = categoria
    publicacion.fechaCosecha_str = fechaCosecha
    publicacion.descripcion = descripcion
    publicacion.save()

    messages.success(request, 'Publicacion actualizada!')
    return redirect('/publicar')


def eliminarPublicacion(request, codigo):
    publicacion = Publicacion.objects.get(codigo=codigo)
    publicacion.delete()

    messages.success(request, 'Publicacion eliminada!')
    return redirect('/publicar')

def listarPublicacion(request):
    if request.method == "POST":
        busqueda = request.POST.get("buscar")
        publicaciones = Publicacion.objects.all()

        if busqueda:
            publicaciones = Publicacion.objects.filter(
                Q(titulo__icontains=busqueda) | 
                Q(categoria__icontains=busqueda)
            ).distinct()

        return render(request, 'core/buscar.html', {'publicaciones': publicaciones})

    elif request.method == "GET":
        orden = request.GET.get("orden", "titulo")  
        publicaciones = Publicacion.objects.all()

        # Ordenar las publicaciones según el parámetro de ordenamiento
        publicaciones = publicaciones.order_by(orden)
             
        return render(request, 'core/buscar.html', {'publicaciones': publicaciones})

def actualizar_datos_usuario(request):
    data = {
        'form': ActualizarDatosForm(instance=request.user)
    }

    if request.method == 'POST':
        form = ActualizarDatosForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
        else:
            data['form'] = form

    return render(request, 'registration/editarPerfil.html', data)


def cambiar_contraseña(request):
    data = {
        'form': CambiarContraseñaForm(user=request.user)
    }

    if request.method == 'POST':
        form = CambiarContraseñaForm(data=request.POST, user=request.user)

        if form.is_valid():
            nueva_contraseña = form.cleaned_data['nueva_contraseña']
            request.user.set_password(nueva_contraseña)
            request.user.save()
            return redirect('perfil')
        else:
            data['form'] = form

    return render(request, 'core/cambiarcontraseña.html', data)

def editarperfil(request):
    return render(request,'registration/editarPerfil.html')


