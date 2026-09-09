from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso, Leccion


NIVELES_VALIDOS = ['Principiante', 'Intermedio', 'Avanzado']
ESTADOS_VALIDOS = ['Borrador', 'Publicado']


def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'cursos.html', {'cursos': cursos})


def detalle_curso(request, pk):
    # get_object_or_404 se usa aquí porque la actividad lo exige puntualmente:
    # si el curso no existe, Django debe responder 404.
    curso = get_object_or_404(Curso, pk=pk)
    lecciones = Leccion.objects.filter(curso=curso).order_by('fecha_creacion')
    return render(request, 'detalle_curso.html', {'curso': curso, 'lecciones': lecciones})


def crear_curso(request):
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        nivel = request.POST.get('nivel')

        if not titulo or not descripcion or nivel not in NIVELES_VALIDOS:
            error = "Este campo es obligatorio"
            return render(request, 'crear_curso.html', {
                'error': error,
                'titulo': titulo,
                'descripcion': descripcion,
                'nivel': nivel,
            })

        curso = Curso(
            titulo=titulo,
            descripcion=descripcion,
            nivel=nivel
        )
        curso.save()
        return redirect('lista_cursos')

    return render(request, 'crear_curso.html')


def eliminar_curso(request, id):
    curso = Curso.objects.get(id=id)
    curso.delete()
    return redirect('lista_cursos')


def crear_leccion(request, curso_pk):
    curso = get_object_or_404(Curso, pk=curso_pk)

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        duracion = request.POST.get('duracion')
        estado = request.POST.get('estado')

        if not titulo or not contenido or not duracion or estado not in ESTADOS_VALIDOS:
            error = "Este campo es obligatorio"
            return render(request, 'crear_leccion.html', {
                'curso': curso,
                'error': error,
                'titulo': titulo,
                'contenido': contenido,
                'duracion': duracion,
                'estado': estado,
            })

        leccion = Leccion(
            curso=curso,
            titulo=titulo,
            contenido=contenido,
            duracion=duracion,
            estado=estado
        )
        leccion.save()
        return redirect('detalle_curso', pk=curso.pk)

    return render(request, 'crear_leccion.html', {'curso': curso})


def editar_leccion(request, pk):
    leccion = Leccion.objects.get(id=pk)

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        duracion = request.POST.get('duracion')
        estado = request.POST.get('estado')

        if not titulo or not contenido or not duracion or estado not in ESTADOS_VALIDOS:
            error = "Este campo es obligatorio"
            return render(request, 'editar_leccion.html', {
                'leccion': leccion,
                'error': error,
                'titulo': titulo,
                'contenido': contenido,
                'duracion': duracion,
                'estado': estado,
            })

        leccion.titulo = titulo
        leccion.contenido = contenido
        leccion.duracion = duracion
        leccion.estado = estado
        leccion.save()
        return redirect('detalle_curso', pk=leccion.curso.pk)

    # GET: se precargan los valores actuales de la lección en el formulario
    return render(request, 'editar_leccion.html', {
        'leccion': leccion,
        'titulo': leccion.titulo,
        'contenido': leccion.contenido,
        'duracion': leccion.duracion,
        'estado': leccion.estado,
    })


def eliminar_leccion(request, pk):
    leccion = Leccion.objects.get(id=pk)

    if request.method == "POST":
        curso_pk = leccion.curso.pk
        leccion.delete()
        return redirect('detalle_curso', pk=curso_pk)

    return render(request, 'eliminar_leccion.html', {'leccion': leccion})
