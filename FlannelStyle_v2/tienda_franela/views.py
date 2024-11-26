from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Camisa, Carrito, ProductoCarrito
from django.contrib.auth.decorators import login_required

# Vista de inicio
def inicio(request):
    camisas = Camisa.objects.all()
    return render(request, 'index.html', {'camisas': camisas})

# Vista de productos
def productos(request):
    camisas = Camisa.objects.all()  # Obtener todas las camisas
    return render(request, 'productos.html', {'camisas': camisas})


# Vista para registro de usuario
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')  # Redirige al inicio después de registrarse
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

#Vista para login de usuario
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')  # Redirige a la página de inicio después de iniciar sesión
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Vista para ver el carrito de un usuario autenticado
@login_required
def carrito(request):
    # Usamos get_or_create() para asegurarnos de que el carrito exista
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    # Obtenemos los productos en el carrito
    productos_carrito = ProductoCarrito.objects.filter(carrito=carrito)
    
    # Calculamos el total
    total = sum(item.camisa.precio * item.cantidad for item in productos_carrito)
    
    return render(request, 'carrito.html', {'productos_carrito': productos_carrito, 'total': total})

# Agregar un producto al carrito
@login_required
def agregar_al_carrito(request, camisa_id):
    camisa = Camisa.objects.get(id=camisa_id)
    
    # Obtiene o crea un carrito para el usuario
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    # Si ya existe el producto en el carrito, aumentamos la cantidad
    producto_carrito, created = ProductoCarrito.objects.get_or_create(carrito=carrito, camisa=camisa)
    if not created:
        producto_carrito.cantidad += 1
    producto_carrito.save()

    return redirect('carrito')

# Eliminar un producto del carrito
@login_required
def eliminar_del_carrito(request, item_id):
    producto_carrito = ProductoCarrito.objects.get(id=item_id)
    producto_carrito.delete()
    return redirect('carrito')