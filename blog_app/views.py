from django.shortcuts import render,redirect, get_object_or_404
from .models import Blog, Registrar_Usuario, Avatar
from django.http import HttpResponse
from .forms import BlogForm, RegistrarUsuarioForm, RegistroUsuarioForm, UserEditorForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from django.contrib.auth.decorators import login_required
from os.path import join
from django.conf import settings

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
    avatar=obtener_avatar(request)
    if request.method == "POST":
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data['nombre_usuario']
            contraseña_usuario = form.cleaned_data['contraseña_usuario']
            email_usuario = form.cleaned_data['email_usuario']
            nuevo_usuario = Registrar_Usuario(nombre_usuario=nombre_usuario, contraseña_usuario=contraseña_usuario, email_usuario=email_usuario)
            nuevo_usuario.save()
            mensaje="Nuevo Usuario Creado"
            usuarios_registrados = Registrar_Usuario.objects.all()
        else:
           mensaje="Datos Invalidos"
        formulario_registro = RegistrarUsuarioForm()
        
        return render(request, 'blog_app/registrar_usuario.html', {"mensaje": mensaje, "formulario": formulario_registro, "usuarios_registrados": usuarios_registrados, "avatar":avatar})
    else:
        formulario_registro = RegistrarUsuarioForm()
        usuarios_registrados = Registrar_Usuario.objects.all()
    return render(request, 'blog_app/registrar_usuario.html', {"formulario": formulario_registro, "usuarios_registrados": usuarios_registrados, "avatar":avatar})

@login_required
def eliminar_usuario(request, id):
    avatar=obtener_avatar(request)
    usuario = Registrar_Usuario.objects.get(id=id)
    usuario.delete()
    usuarios = Registrar_Usuario.objects.all()
    formulario_registro = RegistrarUsuarioForm()
    mensaje = "Usuario Eliminado"
    return render(request, 'blog_app/registrar_usuario.html', {"mensaje": mensaje, "formulario": formulario_registro, "usuarios_registrados": usuarios, "avatar":avatar})

@login_required
def editar_usuario(request, id):
    avatar=obtener_avatar(request)
    usuario = get_object_or_404(Registrar_Usuario, id=id)
    formulario_registro = RegistrarUsuarioForm(initial={
        'nombre_usuario': usuario.nombre_usuario,
        'contraseña_usuario': usuario.contraseña_usuario,
        'email_usuario': usuario.email_usuario
    })
    mensaje = ""

    if request.method == "POST":
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            usuario.nombre_usuario = info["nombre_usuario"]
            usuario.contraseña_usuario = info["contraseña_usuario"]
            usuario.email_usuario = info["email_usuario"]
            usuario.save()
            mensaje = "Usuario Editado"
        else:
            mensaje = "Datos Inválidos"

    usuarios_registrados = Registrar_Usuario.objects.all()
    return render(request, 'blog_app/editar_usuario.html', {'mensaje': mensaje, "formulario": formulario_registro, "usuarios_registrados": usuarios_registrados, "avatar":avatar})


def perfil_usuario(request):
    avatar=obtener_avatar(request)
    return render(request,'blog_app/perfil_usuario.html',{"avatar":avatar})

@login_required
def crear_blog(request):
    avatar=obtener_avatar(request)
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            nombre_blog = form.cleaned_data["nombre_blog"]
            tema_blog = form.cleaned_data["tema_blog"]
            blog = Blog(nombre_blog=nombre_blog, tema_blog=tema_blog)
            blog.save()
            return render(request, 'blog_app/crear_blog.html', {"mensaje": "Blog Creado", "avatar":avatar})
        else:
            return render(request, 'blog_app/crear_blog.html', {"mensaje": "Datos Invalidos", "avatar":avatar})
    else:
        formulario_blog = BlogForm()  # Pasar el formulario creado mediante forms.py
        return render(request, 'blog_app/crear_blog.html', {"formulario": formulario_blog, "avatar":avatar})

@login_required
def listar_blog(request):
    blogs= Blog.objects.all()
    respuesta=""
    for blog in blogs:
        respuesta+=f"{blog.nombre_blog} - {blog.tema_blog}"
    return HttpResponse(respuesta)

@login_required
def blog(request):
    avatar=obtener_avatar(request)
    blogs=Blog.objects.all()
    return render(request,'blog_app/blog.html', {'blogs':blogs, "avatar":avatar})

@login_required
def busqueda_temas_blog(request):
    avatar=obtener_avatar(request)
    return render(request, "blog_app/busqueda_temas_blog.html",{"avatar":avatar})

@login_required
def buscar_tema(request):
    avatar=obtener_avatar(request)
    tema = request.GET.get("busqueda_temas", "").strip()  # Obtener el valor del tema del formulario
    mensaje = ""
    if tema:
        blogs = Blog.objects.filter(tema_blog__icontains=tema)  # icontains para buscar algo que contenga lo que escribo en la busqueda
        if blogs.exists():
            return render(request, "blog_app/resultados_busqueda.html", {"blogs": blogs, "avatar":avatar})
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
        mensaje = None  # Puedes definir un mensaje inicial si lo deseas

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
    
@login_required
def editar_perfil(request):
    avatar=obtener_avatar(request)
    usuario=request.user
    if request.method=="POST":
        form=UserEditorForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usuario.email=info["email"]
            usuario.password1=info["password1"]
            usuario.password2=info["password2"]
            usuario.first_name=info["first_name"]
            usuario.last_name=info["last_name"]
            usuario.save()
            return render(request, "blog_app/inicio.html", {"mensaje":f"Usuario {usuario.username} se ha Editado Correctamente", "avatar":avatar})
        else:
            return render(request, "blog_app/editar_perfil.html", {"form": form, "nombreusaurio":usuario.username,"mensaje": "Datos Invalidos", "avatar":avatar})
    else:
        form=UserEditorForm(instance=usuario)
        return render(request, "blog_app/editar_perfil.html", {"form":form, "nombreusuario":usuario.username, "avatar": avatar})
    
    

    
