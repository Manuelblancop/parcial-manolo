class Producto:
    def __init__(self, id_producto, nombre, precio, descripcion, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock

    def actualizar_stock(self, cantidad, sistema_gestion):
        sistema_gestion.actualizar_stock_producto(self.id_producto, cantidad)