import tkinter as tk
from tkinter import ttk, messagebox
from clases.cliente import Cliente
from clases.producto import Producto
from clases.detalle_pedido import DetallePedido
from clases.pedido import Pedido
from clases.venta import Venta
from clases.sistema_gestion import SistemaGestion

class TiendaApp:
    def __init__(self, root):
        self.sistema = SistemaGestion()
        self.root = root
        self.root.title("Sistema de Tienda")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        # Inicializar datos
        cliente1 = Cliente(1, "Manuel Blanco", "manuel@gmail.com")
        self.sistema.registrar_cliente(cliente1)
        producto1 = Producto(101, "Arepa", 2.5, "Arepa de queso", 10)
        producto2 = Producto(102, "Empanada", 1.5, "Empanada de carne", 15)
        self.sistema.registrar_producto(producto1)
        self.sistema.registrar_producto(producto2)

        self.pedido = Pedido(1001, cliente1)
        detalle1 = DetallePedido(producto1, 2)
        detalle2 = DetallePedido(producto2, 3)
        self.pedido.agregar_detalle(detalle1)
        self.pedido.agregar_detalle(detalle2)

        # Formulario para agregar productos
        tk.Label(root, text="Agregar Nuevo Producto", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        frame_form = tk.Frame(root, bg="#f0f0f0")
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="ID Producto:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(frame_form)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Nombre:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_form)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Precio:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
        self.entry_precio = tk.Entry(frame_form)
        self.entry_precio.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Descripción:", bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5)
        self.entry_descripcion = tk.Entry(frame_form)
        self.entry_descripcion.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Stock:", bg="#f0f0f0").grid(row=4, column=0, padx=5, pady=5)
        self.entry_stock = tk.Entry(frame_form)
        self.entry_stock.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(frame_form, text="Agregar Producto", command=self.agregar_producto, bg="#4CAF50", fg="white").grid(row=5, columnspan=2, pady=10)

        # Interfaz para pedidos
        tk.Label(root, text="Seleccione un producto", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        self.combo = ttk.Combobox(root, values=[
            f"{d.producto.nombre} (Cantidad: {d.cantidad}, Subtotal: {d.subtotal})"
            for d in self.pedido.detalles
        ])
        self.combo.pack(pady=10)
        tk.Button(root, text="Generar Comprobante", command=self.generar_comprobante, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(root, text="Mostrar Productos en BD", command=self.mostrar_productos_bd, bg="#2196F3", fg="white").pack(pady=10)
        self.resultado = tk.Text(root, height=10, width=50)
        self.resultado.pack(pady=10)

    def agregar_producto(self):
        try:
            id_producto = int(self.entry_id.get())
            nombre = self.entry_nombre.get()
            precio = float(self.entry_precio.get())
            descripcion = self.entry_descripcion.get()
            stock = int(self.entry_stock.get())

            if not nombre:
                raise ValueError("El nombre del producto es obligatorio.")
            if precio <= 0:
                raise ValueError("El precio debe ser mayor que 0.")
            if stock < 0:
                raise ValueError("El stock no puede ser negativo.")

            # Verificar si el ID ya existe
            if self.sistema.buscar_producto(id_producto):
                raise ValueError("El ID del producto ya existe.")

            producto = Producto(id_producto, nombre, precio, descripcion, stock)
            self.sistema.registrar_producto(producto)

            # Verificar que el producto se guardó en la base de datos
            productos_db = self.sistema.conexion.mostrar_productos()
            producto_guardado = any(p[0] == id_producto for p in productos_db)
            if not producto_guardado:
                raise ValueError("Error al guardar el producto en la base de datos.")

            messagebox.showinfo("Éxito", f"Producto {nombre} agregado y guardado en la base de datos.")
            self.entry_id.delete(0, tk.END)
            self.entry_nombre.delete(0, tk.END)
            self.entry_precio.delete(0, tk.END)
            self.entry_descripcion.delete(0, tk.END)
            self.entry_stock.delete(0, tk.END)
            self.actualizar_combobox(producto)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def actualizar_combobox(self, nuevo_producto=None):
        # Mantener los detalles existentes y agregar el nuevo producto si se proporciona
        if nuevo_producto:
            detalle_nuevo = DetallePedido(nuevo_producto, 1)
            if not any(d.producto.id_producto == nuevo_producto.id_producto for d in self.pedido.detalles):
                self.pedido.agregar_detalle(detalle_nuevo)
        
        self.combo['values'] = [
            f"{d.producto.nombre} (Cantidad: {d.cantidad}, Subtotal: {d.subtotal})"
            for d in self.pedido.detalles
        ]
        if self.pedido.detalles:
            self.combo.current(0)  # Seleccionar el primer elemento por defecto

    def generar_comprobante(self):
        try:
            seleccion = self.combo.current()
            if seleccion >= 0:
                detalle_seleccionado = self.pedido.detalles[seleccion]
            else:
                detalle_seleccionado = None
            venta = Venta(self.pedido)
            self.resultado.delete(1.0, tk.END)
            self.resultado.insert(tk.END, "----- COMPROBANTE -----\n")
            self.resultado.insert(tk.END, f"Cliente: {self.pedido.cliente.nombre}\n")
            self.resultado.insert(tk.END, "Producto:\n")
            if detalle_seleccionado:
                self.resultado.insert(tk.END, f"{detalle_seleccionado.producto.nombre} x{detalle_seleccionado.cantidad} = {detalle_seleccionado.subtotal}\n")
            else:
                self.resultado.insert(tk.END, "No se seleccionó ningún producto.\n")
            self.resultado.insert(tk.END, f"Total: {venta.total}\n")
            self.resultado.insert(tk.END, "-----------------------")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def mostrar_productos_bd(self):
        productos = self.sistema.conexion.mostrar_productos()
        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, "----- Productos en Base de Datos -----\n")
        if productos:
            for prod in productos:
                self.resultado.insert(tk.END, f"ID: {prod[0]}, Nombre: {prod[1]}, Precio: {prod[2]}, Stock: {prod[4]}\n")
        else:
            self.resultado.insert(tk.END, "No hay productos en la base de datos.\n")
        self.resultado.insert(tk.END, "-------------------------------------\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TiendaApp(root)
    root.mainloop()