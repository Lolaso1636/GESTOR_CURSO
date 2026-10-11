from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.register, name='register'),
    path('grupos/', views.lista_grupos, name='grupos'),
    path('grupos/<int:id_grupos>/editar/', views.editar_grupo, name='editar_grupo'),
    path('grupos/<int:id_grupos>/agregar-usuario/', views.agregar_usuario_grupo, name='agregar_usuario_grupo'),
    path('grupos/<int:id_grupos>/eliminar-usuario/', views.eliminar_usuario_grupo, name='eliminar_usuario_grupo'),
    path('grupos/<int:id_grupos>/eliminar/', views.eliminar_grupo, name='eliminar_grupo'),
    path('permisos/', views.permisos, name='permisos'),
]
