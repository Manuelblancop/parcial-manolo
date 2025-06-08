from base_de_datos.conexion import Conexion
from clases.producto import Producto

class SistemaGestion:
    def __init__(self):
        self.clientes = []
        self.productos = []
        self.conexion = Conexion()
        self._cargar_productos()

    def _cargar_productos(self):
        productos_db = self.conexion.mostrar_productos()
        for prod in productos_db:
            producto = Producto(prod[0], prod[1], prod[2], prod[3], prod[4])
            self.productos.append(producto)

    def registrar_cliente(self, cliente):
        self.clientes.append(cliente)

    def buscar_cliente(self, id_cliente):
        for c in self.clientes:
            if c.id_cliente == id_cliente:
                return c
        return None

    def registrar_producto(self, producto):
        self.conexion.insertar_producto(
            producto.id_producto,
            producto.nombre,
            producto.precio,
            producto.descripcion,
            producto.stock
        )
        self.productos.append(producto)

    def buscar_producto(self, id_producto):
        for p in self.productos:
            if p.id_producto == id_producto:
                return p
        return None

    def actualizar_stock_producto(self, id_producto, cantidad):
        producto = self.buscar_producto(id_producto)
        if producto:
            if producto.stock >= cantidad:
                producto.stock -= cantidad
                self.conexion.actualizar_stock(id_producto, producto.stock)
            else:
                raise ValueError(f"Stock insuficiente para {producto.nombre}. Stock actual: {producto.stock}, solicitado: {cantidad}")

    def cerrar_conexion(self):
        self.conexion.cerrar_conexion()