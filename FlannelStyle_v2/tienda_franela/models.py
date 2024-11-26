from django.db import models
from django.contrib.auth.models import User


class Camisa(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    tamaño = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    material = models.CharField(max_length=50)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='camisas/', null=True, blank=True)  # Nuevo campo de imagen

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
    estado = models.CharField(
        max_length=50,
        choices=[('Pendiente', 'Pendiente'), ('Enviado', 'Enviado'), ('Entregado', 'Entregado')]
    )
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


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField(max_length=150)
    direccion = models.TextField()
    fecha_contrato = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)  # Calificación de 0 a 5

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])
    numero_camisas = models.IntegerField()
    descuento_aplicable = models.DecimalField(max_digits=5, decimal_places=2)  # Porcentaje de descuento

    def __str__(self):
        return self.nombre



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
