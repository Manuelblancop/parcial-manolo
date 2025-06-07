class Producto:
    nombre = ""
    precio = 0.0
    descripcion = ""
    stock = 0

producto1 = Producto()
producto1.nombre = "Arepa de queso"
producto1.precio = 3500
producto1.descripcion = "Arepa rellena con queso llanero"
producto1.stock = 10


print("Producto:", producto1.nombre)
print("Precio:", producto1.precio, "Bs")
print("Descripción:", producto1.descripcion)
print("Stock disponible:", producto1.stock)

producto1.stock -= 2
print("Stock luego de la venta:", producto1.stock)