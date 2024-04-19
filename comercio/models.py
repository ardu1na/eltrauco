from django.db import models


class Rubro(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__ (self):      
        return self.nombre
    
"""a rubro y categoria se le puede añadir una variable de porcentaje de marcado"""

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__ (self):      
        return self.nombre
    
class Proovedor(models.Model):
    class Meta:
        verbose_name_plural = "proveedores"

    empresa = models.CharField(max_length=100)
    
    contacto = models.CharField(max_length=100, null=True, blank=True)
    contacto_tel = models.CharField(max_length=100, null=True, blank=True)

    whatsapp = models.CharField(max_length=100, null=True, blank=True)
    tel =  models.CharField(max_length=100, null=True, blank=True)
    web =  models.CharField(max_length=100, null=True, blank=True)
    ig =  models.CharField(max_length=100, null=True, blank=True)
    fb =  models.CharField(max_length=100, null=True, blank=True)


    def __str__ (self):
        if self.contacto:
            return f'{self.contacto} - {self.empresa}'
        return self.empresa
    

class ProductoProveedor(models.Model):
    class Meta:
        verbose_name_plural = "productos de lista"
        verbose_name = "producto de lista"


    """
    # cómo manejar las promos?
    """
    proveedor = models.ForeignKey(Proovedor, on_delete=models.CASCADE, related_name="productos")
    rubro = models.ForeignKey(Rubro, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos")
    codigo_prod = models.CharField(max_length=10, null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)

    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveSmallIntegerField(default=1)
    precio = models.PositiveSmallIntegerField(default=1)
    
    precio_unidad_comercial = models.PositiveSmallIntegerField(default=1, help_text="Dejar en 1 para un marcado automático de 50 porciento")

    def __str__ (self):      
        return self.nombre

    @property
    def precio_unidad(self):
        p = self.precio/self.cantidad
        return p
    

    @property
    def retorno_unidad(self):
        p = self.precio_unidad_comercial - self.precio_unidad 
        return p

    @property
    def retorno_total(self):
        p = self.retorno_unidad * self.cantidad
        return p
    
    def save(self, *args, **kwargs):
        if self.precio_unidad_comercial < 2:
            self.precio_unidad_comercial = self.precio_unidad*1.5

        super().save(*args, **kwargs)

class PedidoProveedor(models.Model):

    class Meta:
        verbose_name_plural = "pedidos a proveedores"
        verbose_name = "pedido a proveedor"

    fecha = models.DateField()
    comentarios = models.TextField()

    def __str__ (self):      
        return f'Pedido a {self.proveedor} {self.fecha} - inversion ${self.total} - ganancia ${self.total_retorno}' 
    
    @property
    def total(self):
        t = 0
        productos_pedido = ProductoPedido.objects.filter(pedido=self)
        for producto_p in productos_pedido:
            s = producto_p.cantidad * producto_p.producto.precio
            t += s
        return t


    @property
    def total_retorno(self):
        t = 0
        productos_pedido = ProductoPedido.objects.filter(pedido=self)
        for producto_p in productos_pedido:
            s = producto_p.cantidad * producto_p.producto.retorno_total
            t += s
        return t

    @property
    def total_pago(self):
        return (self.total + self.total_retorno)

    @property
    def proveedor(self):
        p = ProductoPedido.objects.filter(pedido=self).first()
        pro = p.producto.proveedor
        return pro.empresa


class ProductoPedido(models.Model):
    class Meta:
        verbose_name_plural = "productos pedidos"

    producto = models.ForeignKey(
        ProductoProveedor, on_delete=models.CASCADE, related_name="pedidos"
        )
    cantidad = models.PositiveSmallIntegerField(
        default=1
        )
    pedido = models.ForeignKey(
        PedidoProveedor, on_delete=models.CASCADE, related_name="productos"
        )

    def __str__ (self):      
        return f'{self.producto.nombre} ${self.producto.precio} x {self.producto.cantidad}'
                  

    @property
    def total(self):
        p = self.producto.precio*self.cantidad
        return p


    @property
    def proovedor(self):
        p = ProductoPedido.objects.filter(pedido=self)
        p = self.producto.producto.proovedor
        return p
