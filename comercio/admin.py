from django.contrib import admin
from comercio.models import *


admin.site.register(Rubro)
admin.site.register(Categoria)


class NotaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha','done']
admin.site.register(Nota, NotaAdmin)


class ProductoPedidoAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cantidad', 'costo_total', 'proveedor', 'ganancia_total', 'costo_unidad','ganancia_unidad','bulto']
    list_filter = ['producto__proveedor', 'pedido']
admin.site.register(ProductoPedido, ProductoPedidoAdmin)

class ProductoEnLocalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock', 'costo_unitario', 'ganancia', 'sugerencia',]
admin.site.register(ProductoEnLocal, ProductoEnLocalAdmin)

class ProductoProveedorInline(admin.StackedInline):
    model = ProductoProveedor
    extra= 0

class ProveedorAdmin(admin.ModelAdmin):
    inlines = [ProductoProveedorInline,]
    list_display = ['empresa', 'contacto']
admin.site.register(Proveedor, ProveedorAdmin)

class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre','cantidad','precio','precio_unidad', 'proveedor','precio_unidad_comercial', 'retorno_unidad', 'retorno_total']
    list_filter = ['proveedor', 'rubro','categoria']
admin.site.register(ProductoProveedor, ProductoProveedorAdmin)

class ProductoPedidoInline(admin.StackedInline):
    model = ProductoPedido
    extra= 0

class PedidoProveedorAdmin(admin.ModelAdmin):
    inlines = [ProductoPedidoInline,]
    list_display = ['fecha', 'proveedor','total','total_retorno']
admin.site.register(PedidoProveedor, PedidoProveedorAdmin)
