from django.contrib import admin
from .models import Camisa
from .models import Carrito, ProductoCarrito

@admin.register(Camisa)
class CamisaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'tamaño', 'precio', 'material', 'stock')


class ProductoCarritoInline(admin.TabularInline):
    model = ProductoCarrito
    extra = 0  # No mostrar filas vacías por defecto
    fields = ['camisa', 'cantidad']  # Los campos que quieres mostrar
    readonly_fields = ['camisa', 'cantidad']  # Si no quieres que puedan editarlos directamente, usa readonly_fields

class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ver_productos')  # Muestra el usuario y los productos asociados
    inlines = [ProductoCarritoInline]  # Muestra los productos en línea dentro del carrito
    search_fields = ['usuario__username']  # Permite buscar por nombre de usuario

    def ver_productos(self, obj):
        # Accede a los productos del carrito y obtiene los nombres de las camisas
        productos = ProductoCarrito.objects.filter(carrito=obj)
        return ", ".join([producto.camisa.nombre for producto in productos])
    
    ver_productos.short_description = 'Productos'

admin.site.register(Carrito, CarritoAdmin)
admin.site.register(ProductoCarrito)  # Registra ProductoCarrito si no lo has hecho ya

