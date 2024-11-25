from django.db import models
from django.contrib.auth.models import User

class Camisa(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    tamaño = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    material = models.CharField(max_length=50)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo_electronico = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('Enviado', 'Enviado'), ('Entregado', 'Entregado')])
    metodo_pago = models.CharField(max_length=50)
    direccion_envio = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    camisa = models.ForeignKey(Camisa, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id} - Pedido {self.pedido.id}"


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Camisa, through='ProductoCarrito')

    def __str__(self):
        return f'Carrito de {self.usuario.username}'

class ProductoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    camisa = models.ForeignKey(Camisa, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} x {self.camisa.nombre}'