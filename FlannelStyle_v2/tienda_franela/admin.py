from django.contrib import admin
from .models import Camisa

@admin.register(Camisa)
class CamisaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'tamaño', 'precio', 'material', 'stock')
