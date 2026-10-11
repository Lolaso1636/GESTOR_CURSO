from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.apps import apps
from django.contrib.auth import login
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def register(request):
    datos = {}
    errors = []

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        datos = request.POST

        if not username or not email or not first_name or not last_name or not password1:
            errors.append('Todos los campos son obligatorios.')

        if password1 != password2:
            errors.append('Las contraseñas no coinciden.')

        if User.objects.filter(username=username).exists():
            errors.append('El nombre de usuario ya existe.')

        if User.objects.filter(email=email).exists():
            errors.append('El correo electrónico ya está registrado.')

        if not errors:
            try:
                validate_password(password1, User(username=username, email=email,
                                                  first_name=first_name, last_name=last_name))
            except ValidationError as e:
                errors.extend(e.messages)

        if not errors:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return redirect('lista_cursos')

    return render(request, 'registro.html', {'errors': errors, 'datos': datos})


def es_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(es_admin)
def lista_grupos(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre_grupo')
        if nombre and not Group.objects.filter(name=nombre).exists():
            Group.objects.create(name=nombre)
        return redirect('grupos')

    grupos = Group.objects.all()
    return render(request, 'grupos.html', {'grupos': grupos})


@user_passes_test(es_admin)
def eliminar_grupo(request, id_grupos):
    if request.method == "POST":
        grupo = get_object_or_404(Group, id=id_grupos)
        grupo.delete()

    return redirect('grupos')


def dar_miembros(grupo):
    return grupo.user_set.all()


def dar_no_miembros(grupo):
    miembros = dar_miembros(grupo)
    return User.objects.exclude(id__in=miembros.values_list('id', flat=True))


@user_passes_test(es_admin)
def editar_grupo(request, id_grupos):
    grupo = get_object_or_404(Group, id=id_grupos)
    if request.method == "POST":
        nuevo_nombre = request.POST.get('name')
        if nuevo_nombre:
            grupo.name = nuevo_nombre
            grupo.save()
        return redirect('grupos')

    return render(request, 'editar_grupo.html', {
        'grupo': grupo,
        'miembros': dar_miembros(grupo),
        'no_miembros': dar_no_miembros(grupo),
    })


@user_passes_test(es_admin)
def agregar_usuario_grupo(request, id_grupos):
    grupo = get_object_or_404(Group, id=id_grupos)
    if request.method == "POST":
        usuario = get_object_or_404(User, id=request.POST.get('id_user'))
        grupo.user_set.add(usuario)

    return redirect('editar_grupo', id_grupos=grupo.id)


@user_passes_test(es_admin)
def eliminar_usuario_grupo(request, id_grupos):
    grupo = get_object_or_404(Group, id=id_grupos)
    if request.method == "POST":
        usuario = get_object_or_404(User, id=request.POST.get('id_user'))
        grupo.user_set.remove(usuario)

    return redirect('editar_grupo', id_grupos=grupo.id)


# Columnas de la tabla de permisos, en el orden en que se muestran
ACCIONES = ['view', 'add', 'change', 'delete']

# Apps internas de Django que no vale la pena mostrar
APPS_OCULTAS = ['admin', 'contenttypes', 'sessions']


def dar_tabla_permisos():
    """Agrupa los permisos por app y por modelo para mostrarlos como tabla."""
    secciones = {}
    permisos = (Permission.objects
                .select_related('content_type')
                .exclude(content_type__app_label__in=APPS_OCULTAS)
                .order_by('content_type__app_label', 'content_type__model', 'codename'))

    for permiso in permisos:
        tipo = permiso.content_type
        if tipo.app_label not in secciones:
            secciones[tipo.app_label] = {
                'nombre': apps.get_app_config(tipo.app_label).verbose_name,
                'modelos': {},
            }
        modelos = secciones[tipo.app_label]['modelos']
        if tipo.id not in modelos:
            modelo = tipo.model_class()
            modelos[tipo.id] = {
                'nombre': modelo._meta.verbose_name.capitalize() if modelo else tipo.model,
                'acciones': {},
                'otros': [],
            }

        accion = permiso.codename.split('_')[0]
        if accion in ACCIONES and permiso.codename == f'{accion}_{tipo.model}':
            modelos[tipo.id]['acciones'][accion] = permiso
        else:
            modelos[tipo.id]['otros'].append(permiso)

    tabla = []
    for seccion in secciones.values():
        filas = []
        for fila in seccion['modelos'].values():
            fila['celdas'] = [fila['acciones'].get(accion) for accion in ACCIONES]
            filas.append(fila)
        tabla.append({'nombre': seccion['nombre'], 'filas': filas})
    return tabla


@user_passes_test(es_admin)
def permisos(request):
    grupos = Group.objects.order_by('name')
    id_grupo = request.POST.get('grupo') or request.GET.get('grupo')
    grupo = get_object_or_404(Group, id=id_grupo) if id_grupo else grupos.first()

    if request.method == "POST" and grupo:
        ids = request.POST.getlist('permisos')
        grupo.permissions.set(Permission.objects.filter(id__in=ids))
        return redirect(f"{reverse('permisos')}?grupo={grupo.id}&guardado=1")

    permisos_grupo = set(grupo.permissions.values_list('id', flat=True)) if grupo else set()

    return render(request, 'permisos.html', {
        'grupos': grupos,
        'grupo': grupo,
        'tabla': dar_tabla_permisos(),
        'permisos_grupo': permisos_grupo,
        'guardado': request.GET.get('guardado'),
    })
