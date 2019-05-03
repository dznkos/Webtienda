from django.contrib import admin
from .models import Producto, Comentario, ImagenesProducto, CarritoCompras

@admin.register(Producto, Comentario, ImagenesProducto, CarritoCompras)
class ProductoAdmin(admin.ModelAdmin):
    pass



