from django.shortcuts import render,redirect, get_object_or_404
from .models import Page, Registrar_Usuario, Avatar, UserProfile
from django.http import HttpResponse
from .forms import PageForm, RegistroUsuarioForm, UserProfileForm
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from django.contrib.auth.decorators import login_required
from os.path import join
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages

def inicio (request):
    avatar=obtener_avatar(request)
    return render(request, "blog_app/inicio.html", {"avatar":avatar})

def obtener_avatar(request):
    avatares=Avatar.objects.filter(user=request.user.id)
    if len(avatares)!=0:
        return avatares[0].img.url
    else:
        return"media/avatars/avatar_por_defecto.png"

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario en la base de datos
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            # Almacenar un mensaje de éxito
            messages.success(request, 'Nuevo Usuario Creado')

            return redirect('login')  # Redirige al usuario a la vista 'login'
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'blog_app/registrar_usuario.html', {'formulario': form})

def eliminar_perfil(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.delete()
    logout(request)
    messages.success(request, 'Usuario Eliminado Satisfactoriamente.')
    return redirect('inicio')

@login_required
def editar_perfil(request):
    print("Estoy dentro de la vista editar_perfil")  # Agrega esta línea para verificar si la vista se ejecuta
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('perfil_usuario')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'blog_app/editar_perfil.html', {'form': form, 'user': user})

@login_required
def perfil_usuario(request):
    usuario = request.user  
    avatar = Avatar.objects.filter(user=usuario).first()  # Obtén el avatar del usuario
    return render(request, 'blog_app/perfil_usuario.html', {'usuario': usuario, 'avatar': avatar})

@login_required
def crear_blog(request):
    avatar = obtener_avatar(request)
    mensaje = ""  
    if request.method == "POST":
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            blog_page = form.save(commit=False)
            blog_page.autor_page = request.user
            blog_page.save()
            mensaje = "Blog Creado"  
            return redirect('page', page_id=blog_page.id)
        else:
            return render(request, 'blog_app/crear_blog.html', {"formulario": form, "avatar": avatar, "mensaje": mensaje})
    else:
        form = PageForm()

    return render(request, 'blog_app/crear_blog.html', {"formulario": form, "avatar": avatar, "mensaje": mensaje})


@login_required
def page(request, page_id):                     #BLOG
    avatar = obtener_avatar(request)
    pages = Page.objects.all()
    return render(request, 'blog_app/page.html', {'pages': pages, "avatar": avatar})

@login_required
def busqueda_temas_blog(request):
    avatar=obtener_avatar(request)
    return render(request, "blog_app/busqueda_temas_blog.html",{"avatar":avatar})

@login_required
def buscar_tema(request):
    avatar=obtener_avatar(request)
    tema = request.GET.get("busqueda_temas", "").strip()  # Obtiene el valor del tema del formulario
    mensaje = ""
    if tema:
        pages = Page.objects.filter(tema_blog__icontains=tema)  # icontains para buscar algo que contenga lo que escribo en la busqueda
        if pages.exists():
            return render(request, "blog_app/resultados_busqueda.html", {"pages": pages, "avatar":avatar})
        else:
            mensaje = "No se encontraron blogs con ese tema."
    else:
        mensaje = "Por favor, ingresa un tema para buscar."
    return render(request, "blog_app/busqueda_temas_blog.html", {"mensaje": mensaje, "avatar":avatar})

def mi_login(request):
    avatar = obtener_avatar(request)
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            info = form.cleaned_data
            user = info["username"]
            clave = info["password"]
            usuario = authenticate(username=user, password=clave)
            if usuario is not None:
                login(request, usuario)
                return redirect('inicio')  # Redirige al usuario a la vista 'inicio'
            else:
                mensaje = "Username o Password Incorrectas. Intentelo Nuevamente"
        else:
            mensaje = "Username o Password Incorrectas. Intentelo Nuevamente"
    else:
        form = AuthenticationForm()
        mensaje = None
    return render(request, 'blog_app/login.html', {"form": form, "mensaje": mensaje, "avatar": avatar})
    
def register(request):
    avatar=obtener_avatar(request)
    if request.method=="POST":
        form=RegistroUsuarioForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            nombre_user=info["username"]
            form.save()
            return render(request, "blog_app/inicio.html", {"mensaje": f"Usuario {nombre_user} Registrado Exitosamente", "avatar": avatar})
        else:
            return render(request, "blog_app/register.html", {"form":form, "mensaje": "Datos Invalidos", "avatar":avatar})

    else:
        form=RegistroUsuarioForm()
        return render(request, "blog_app/register.html", {"form":form, "avatar":avatar})
    
@ login_required    
def about(request):
    avatar=obtener_avatar(request)
    return render(request,'blog_app/about.html', {"avatar":avatar})

@login_required
def page_view(request, page_id=None):
    avatar = obtener_avatar(request)
    all_pages = Page.objects.all()   # Obtengo todas las entradas de blog
    paginator = Paginator(all_pages, 10)  # Configuro la cantidad de entradas con un máximo de 10 blogs por página
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)

    return render(request, 'blog_app/page.html', {'pages': pages, 'avatar': avatar})

@login_required
def detalle_blog(request, page_id):
    blog = get_object_or_404(Page, pk=page_id)
    return render(request, 'blog_app/detalle_blog.html', {'page': blog})

