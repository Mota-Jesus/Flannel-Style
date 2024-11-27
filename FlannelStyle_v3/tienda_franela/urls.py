from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar/<int:camisa_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    
    # URL para login y registro
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': 'inicio'}, name='logout'),
    path('registro/', views.registro, name='registro'),
]

