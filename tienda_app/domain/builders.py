from ..models import Orden
from .logic import CalculadorImpuestos


class OrdenBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._usuario = None
        self._items = []
        self._direccion = ""

    def con_usuario(self, usuario):
        self._usuario = usuario
        return self  # Permite Fluent Interface

    def con_productos(self, productos):
        self._items = productos
        return self

    def para_envio(self, direccion):
        self._direccion = direccion
        return self

    def build(self) -> Orden:
        # el usuario puede ser None porque la tienda todavia no tiene login
        if not self._items:
            raise ValueError("Datos insuficientes para crear la orden.")

        # el calculo queda encapsulado aca y no en la vista
        subtotal = sum(p.precio for p in self._items)
        total_con_iva = round(CalculadorImpuestos.obtener_total_con_iva(subtotal), 2)

        orden = Orden.objects.create(
            usuario=self._usuario,
            libro=self._items[0],  # por ahora el modelo Orden solo guarda un libro
            total=total_con_iva,
            direccion_envio=self._direccion
        )
        self.reset()
        return orden
