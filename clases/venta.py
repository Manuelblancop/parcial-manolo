class Venta:
    def __init__(self, pedido):
        self.pedido = pedido
        self.total = pedido.calcular_total()

    def generar_comprobante(self, detalle_seleccionado=None):
        print("----- COMPROBANTE -----")
        print("Cliente:", self.pedido.cliente.nombre)
        print("Producto:")
        if detalle_seleccionado:
            print(f"{detalle_seleccionado.producto.nombre} x{detalle_seleccionado.cantidad} = {detalle_seleccionado.subtotal}")
        else:
            print("No se seleccionó ningún producto.")
        print("Total:", self.total)
        print("-----------------------")
