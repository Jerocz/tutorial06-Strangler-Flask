from django.shortcuts import get_object_or_404
from .models import Libro, Inventario, Orden
from .domain.logic import CalculadorImpuestos
from .domain.builders import OrdenBuilder

class CompraService:
    """
    SERVICE LAYER: Orquesta la interacción entre el dominio, 
    la infraestructura y la base de datos.
    """
    def __init__(self, procesador_pago):
        # Inyectamos la dependencia (DIP)
        self.procesador = procesador_pago
        self.builder = OrdenBuilder()

    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {"libro": libro, "total": total}

    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
        # Uso del Builder: semantica clara y validacion interna
        orden = (self.builder
                 .con_usuario(usuario)
                 .con_productos(lista_productos)
                 .para_envio(direccion)
                 .build())

        # Uso del Factory (inyectado): cambia el comportamiento sin cambiar codigo
        if self.procesador.pagar(orden.total):
            return orden

        orden.delete()
        raise Exception("Error en la pasarela de pagos.")

    def ejecutar_compra(self, libro_id, cantidad=1, direccion="", usuario=None):
        libro = get_object_or_404(Libro, id=libro_id)
        inv = get_object_or_404(Inventario, libro=libro)

        if inv.cantidad < cantidad:
            raise ValueError("No hay suficiente stock para completar la compra.")

        orden = self.ejecutar_proceso_compra(usuario, [libro] * cantidad, direccion)

        inv.cantidad -= cantidad
        inv.save()
        return orden.total


class CompraRapidaService:
    """
    Servicio para la compra rapida.
    Saca de la vista toda la logica (inventario, impuestos y pago).
    """
    def __init__(self, procesador_pago):
        # el procesador se inyecta, el servicio no sabe que banco es (DIP)
        self.procesador_pago = procesador_pago

    def obtener_detalle(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {'libro': libro, 'total': total}

    def procesar(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        inv = get_object_or_404(Inventario, libro=libro)

        if inv.cantidad <= 0:
            raise ValueError("No hay existencias.")

        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)

        if self.procesador_pago.pagar(total):
            inv.cantidad -= 1
            inv.save()
            Orden.objects.create(libro=libro, total=total)
            return total

        raise ValueError("El pago fue rechazado.")
