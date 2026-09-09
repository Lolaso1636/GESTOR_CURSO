from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('curso/nuevo/', views.crear_curso, name='crear_curso'),
    path('curso/<int:pk>/', views.detalle_curso, name='detalle_curso'),
    path('curso/<int:id>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
    path('curso/<int:curso_pk>/nueva-leccion/', views.crear_leccion, name='crear_leccion'),
    path('leccion/<int:pk>/editar/', views.editar_leccion, name='editar_leccion'),
    path('leccion/<int:pk>/eliminar/', views.eliminar_leccion, name='eliminar_leccion'),
]
