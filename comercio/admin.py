from django.contrib import admin
from comercio.models import *


admin.site.register(Rubro)
admin.site.register(Categoria)


class ProductoPedidoAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cantidad', 'total', 'display_ganancia', 'display_preciounit','display_retornounit','display_bulto']
    list_filter = ['producto__proveedor', 'pedido']
    

    def display_bulto(self, obj):
        bulto = obj.producto.cantidad
        return bulto
    display_bulto.short_description = 'Unid x bulto'

    def display_ganancia(self, obj):
        retorno = obj.producto.retorno_total
        cantidad = obj.cantidad
        return retorno*cantidad
    display_ganancia.short_description = 'Ganancia'

    def display_preciounit(self, obj):
        producto = obj.producto
        return producto.precio_unidad
    display_preciounit.short_description = 'Costo unitario'

    def display_retornounit(self, obj):
        producto = obj.producto
        return producto.retorno_unidad
    display_retornounit.short_description = 'Ganancia unitaria'

    

admin.site.register(ProductoPedido, ProductoPedidoAdmin)


class ProductoProveedorInline(admin.StackedInline):
    model = ProductoProveedor
    extra= 0

class ProveedorAdmin(admin.ModelAdmin):
    inlines = [ProductoProveedorInline,]
    list_display = ['empresa', 'contacto']
admin.site.register(Proovedor, ProveedorAdmin)

class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre','cantidad','precio','precio_unidad', 'precio_unidad_comercial', 'retorno_unidad', 'retorno_total']
    list_filter = ['proveedor', 'rubro','categoria']
admin.site.register(ProductoProveedor, ProductoProveedorAdmin)

class ProductoPedidoInline(admin.StackedInline):
    model = ProductoPedido
    extra= 0


class PedidoProveedorAdmin(admin.ModelAdmin):
    inlines = [ProductoPedidoInline,]
    list_display = ['fecha', 'proveedor','total','total_pago','total_retorno']
admin.site.register(PedidoProveedor, PedidoProveedorAdmin)
