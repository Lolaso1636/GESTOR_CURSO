# Gestor de Cursos

Aplicación web desarrollada con Django para administrar cursos y sus lecciones, con autenticación de usuarios, administración de grupos y control de permisos por grupo.

## Funcionalidades

### Cursos y lecciones
- Listado de cursos con nivel y número de lecciones.
- Creación y eliminación de cursos (Principiante, Intermedio, Avanzado).
- Detalle del curso con sus lecciones.
- Creación, edición y eliminación de lecciones (estado Borrador / Publicado).

### Usuarios, grupos y permisos
- Inicio y cierre de sesión.
- Registro de nuevos usuarios con validación de contraseña.
- Administración de grupos (solo usuarios *staff*): crear, renombrar, eliminar, agregar y quitar miembros.
- Pantalla de permisos (solo *staff*): tabla por modelo con las acciones Ver / Crear / Editar / Eliminar para asignar a cada grupo.
- Todas las vistas de cursos exigen sesión iniciada y el permiso correspondiente; los botones se ocultan si el usuario no tiene permiso.

| Acción | Permiso requerido |
| --- | --- |
| Ver lista y detalle de cursos | `cursos.view_curso` |
| Crear curso | `cursos.add_curso` |
| Eliminar curso | `cursos.delete_curso` |
| Crear lección | `cursos.add_leccion` |
| Editar lección | `cursos.change_leccion` |
| Eliminar lección | `cursos.delete_leccion` |

## Tecnologías

- Python
- Django 5.2
- SQLite
- Tailwind CSS y Font Awesome mediante CDN

## Instalación

```bash
git clone https://github.com/Lolaso1636/GESTOR_CURSO.git
cd GESTOR_CURSO
python -m venv venv
```

Activa el entorno virtual:

- Windows PowerShell: `venv\Scripts\Activate.ps1`
- macOS/Linux: `source venv/bin/activate`

Instala dependencias y aplica migraciones:

```bash
pip install -r requirements.txt
python manage.py migrate
```

Crea un superusuario (tendrá acceso a Grupos y Permisos):

```bash
python manage.py createsuperuser
```

## Ejecución

```bash
python manage.py runserver
```

Abre [http://127.0.0.1:8000/](http://127.0.0.1:8000/) e inicia sesión.

### Flujo sugerido

1. Inicia sesión con el superusuario.
2. En **Grupos**, crea por ejemplo `Docentes` y `Estudiantes`.
3. En **Permisos**, asigna a `Docentes` todos los permisos de Curso y Lección, y a `Estudiantes` solo *Ver*.
4. Los usuarios que se registren desde `/registro/` se agregan a un grupo desde **Grupos → Editar**.

## Rutas principales

| Ruta | Descripción |
| --- | --- |
| `/` | Lista de cursos |
| `/curso/nuevo/` | Crear curso |
| `/curso/<id>/` | Detalle del curso |
| `/curso/<id>/eliminar/` | Eliminar curso |
| `/curso/<id>/nueva-leccion/` | Crear lección |
| `/leccion/<id>/editar/` | Editar lección |
| `/leccion/<id>/eliminar/` | Eliminar lección |
| `/login/` | Iniciar sesión |
| `/registro/` | Registro de usuario |
| `/grupos/` | Administración de grupos |
| `/permisos/` | Permisos por grupo |
| `/admin/` | Administración de Django |

## Pruebas

```bash
python manage.py test
```

## Estructura del proyecto

```text
.
├── manage.py
├── requirements.txt
├── core/                  # Configuración del proyecto
├── cursos/                # App de cursos y lecciones
│   ├── models.py          # Curso y Leccion
│   ├── views.py           # Vistas protegidas con login y permisos
│   └── templates/         # Plantillas (incluye layouts/base.html)
└── accounts/              # App de autenticación, grupos y permisos
    ├── views.py
    ├── urls.py
    ├── static/img/        # Logo y favicon
    └── templates/         # login, registro, grupos, permisos
```
