from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase
from django.urls import reverse


class LoginRegistroTests(TestCase):

    def test_login_correcto_redirige_a_cursos(self):
        User.objects.create_user('ana', password='ClaveSegura123')
        respuesta = self.client.post(reverse('login'), {'username': 'ana', 'password': 'ClaveSegura123'})
        self.assertRedirects(respuesta, reverse('lista_cursos'), fetch_redirect_response=False)

    def test_login_incorrecto_muestra_error(self):
        respuesta = self.client.post(reverse('login'), {'username': 'nadie', 'password': 'x'})
        self.assertContains(respuesta, 'Usuario o contraseña incorrectos')

    def test_logout(self):
        User.objects.create_user('ana', password='ClaveSegura123')
        self.client.login(username='ana', password='ClaveSegura123')
        respuesta = self.client.post(reverse('logout'))
        self.assertRedirects(respuesta, reverse('login'))

    def test_registro_crea_usuario(self):
        respuesta = self.client.post(reverse('register'), {
            'username': 'nuevo', 'email': 'nuevo@correo.com', 'first_name': 'Nuevo', 'last_name': 'Usuario',
            'password1': 'ClaveSegura123', 'password2': 'ClaveSegura123',
        })
        self.assertRedirects(respuesta, reverse('lista_cursos'), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username='nuevo').exists())

    def test_registro_contrasenas_distintas(self):
        respuesta = self.client.post(reverse('register'), {
            'username': 'nuevo', 'email': 'nuevo@correo.com', 'first_name': 'Nuevo', 'last_name': 'Usuario',
            'password1': 'ClaveSegura123', 'password2': 'OtraClave456',
        })
        self.assertContains(respuesta, 'Las contraseñas no coinciden.')
        self.assertFalse(User.objects.filter(username='nuevo').exists())


class GruposPermisosTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user('admin', password='ClaveSegura123', is_staff=True)
        self.normal = User.objects.create_user('normal', password='ClaveSegura123')

    def test_usuario_no_staff_no_entra_a_grupos(self):
        self.client.login(username='normal', password='ClaveSegura123')
        self.assertEqual(self.client.get(reverse('grupos')).status_code, 302)
        self.assertEqual(self.client.get(reverse('permisos')).status_code, 302)

    def test_admin_crea_grupo_y_agrega_usuario(self):
        self.client.login(username='admin', password='ClaveSegura123')
        self.client.post(reverse('grupos'), {'nombre_grupo': 'Docentes'})
        grupo = Group.objects.get(name='Docentes')
        self.client.post(reverse('agregar_usuario_grupo', args=[grupo.id]), {'id_user': self.normal.id})
        self.assertIn(self.normal, grupo.user_set.all())
        self.client.post(reverse('eliminar_usuario_grupo', args=[grupo.id]), {'id_user': self.normal.id})
        self.assertNotIn(self.normal, grupo.user_set.all())

    def test_permisos_del_grupo_aplican_al_usuario(self):
        grupo = Group.objects.create(name='Estudiantes')
        grupo.user_set.add(self.normal)
        ver_curso = Permission.objects.get(codename='view_curso')

        self.client.login(username='admin', password='ClaveSegura123')
        respuesta = self.client.get(reverse('permisos'), {'grupo': grupo.id})
        self.assertContains(respuesta, 'Cursos')
        self.client.post(reverse('permisos'), {'grupo': grupo.id, 'permisos': [ver_curso.id]})
        self.assertIn(ver_curso, grupo.permissions.all())

        self.client.login(username='normal', password='ClaveSegura123')
        self.assertEqual(self.client.get(reverse('lista_cursos')).status_code, 200)
        self.assertEqual(self.client.get(reverse('crear_curso')).status_code, 403)

    def test_admin_elimina_grupo(self):
        grupo = Group.objects.create(name='Temporal')
        self.client.login(username='admin', password='ClaveSegura123')
        self.client.post(reverse('eliminar_grupo', args=[grupo.id]))
        self.assertFalse(Group.objects.filter(id=grupo.id).exists())
