from django.db import models


class Curso(models.Model):
    '''
    Modelo que representa un curso
    '''
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    nivel = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'

    def __str__(self):
        return self.titulo


class Leccion(models.Model):
    '''
    Modelo que representa una lección dentro de un curso
    '''
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    duracion = models.IntegerField()
    estado = models.CharField(max_length=20, default='Borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'lección'
        verbose_name_plural = 'lecciones'

    def __str__(self):
        return f"{self.titulo} ({self.curso.titulo})"
