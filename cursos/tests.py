from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from .models import Curso, Leccion


class PermisosCursosTests(TestCase):

    def setUp(self):
        self.curso = Curso.objects.create(titulo='Python', descripcion='Básico', nivel='Principiante')
        self.leccion = Leccion.objects.create(curso=self.curso, titulo='Intro', contenido='Hola', duracion=10)
        self.usuario = User.objects.create_user('lector', password='ClaveSegura123')

    def dar_permisos(self, *codenames):
        self.usuario.user_permissions.add(*Permission.objects.filter(codename__in=codenames))

    def test_sin_login_redirige_al_login(self):
        respuesta = self.client.get(reverse('lista_cursos'))
        self.assertRedirects(respuesta, f"{reverse('login')}?next={reverse('lista_cursos')}")

    def test_sin_permiso_responde_403(self):
        self.client.login(username='lector', password='ClaveSegura123')
        self.assertEqual(self.client.get(reverse('lista_cursos')).status_code, 403)

    def test_con_permiso_de_ver_lista_cursos(self):
        self.dar_permisos('view_curso')
        self.client.login(username='lector', password='ClaveSegura123')
        respuesta = self.client.get(reverse('lista_cursos'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Python')
        # Sin permiso de crear/eliminar no se muestran esos botones
        self.assertNotContains(respuesta, reverse('crear_curso'))
        self.assertNotContains(respuesta, reverse('eliminar_curso', args=[self.curso.pk]))

    def test_solo_ver_no_puede_crear_ni_eliminar(self):
        self.dar_permisos('view_curso')
        self.client.login(username='lector', password='ClaveSegura123')
        self.assertEqual(self.client.get(reverse('crear_curso')).status_code, 403)
        self.assertEqual(self.client.get(reverse('eliminar_curso', args=[self.curso.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('editar_leccion', args=[self.leccion.pk])).status_code, 403)
        self.assertTrue(Curso.objects.filter(pk=self.curso.pk).exists())

    def test_con_permiso_de_crear(self):
        self.dar_permisos('view_curso', 'add_curso')
        self.client.login(username='lector', password='ClaveSegura123')
        respuesta = self.client.post(reverse('crear_curso'), {
            'titulo': 'Django', 'descripcion': 'Web', 'nivel': 'Intermedio',
        })
        self.assertRedirects(respuesta, reverse('lista_cursos'))
        self.assertTrue(Curso.objects.filter(titulo='Django').exists())

    def test_con_permiso_de_editar_leccion(self):
        self.dar_permisos('view_curso', 'change_leccion')
        self.client.login(username='lector', password='ClaveSegura123')
        self.client.post(reverse('editar_leccion', args=[self.leccion.pk]), {
            'titulo': 'Intro editada', 'contenido': 'Hola', 'duracion': 15, 'estado': 'Publicado',
        })
        self.leccion.refresh_from_db()
        self.assertEqual(self.leccion.titulo, 'Intro editada')
