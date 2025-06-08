import tkinter as tk
from tkinter import ttk, messagebox
from clases.cliente import Cliente
from clases.producto import Producto
from clases.detalle_pedido import DetallePedido
from clases.pedido import Pedido
from clases.venta import Venta
from clases.sistema_gestion import SistemaGestion  
from base_de_datos.conexion import Conexion


class TiendaApp:
    def __init__(self, root):
        self.sistema = SistemaGestion()  
        self.root = root
        self.root.title("Sistema de Tienda")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

      
        cliente1 = Cliente(1, "Pedro Pérez", "pedro@gmail.com")
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

       
        tk.Label(root, text="Seleccione un producto", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        self.combo = ttk.Combobox(root, values=[
            f"{d.producto.nombre} (Cantidad: {d.cantidad}, Subtotal: {d.subtotal})"
            for d in self.pedido.detalles
        ])
        self.combo.pack(pady=10)
        tk.Button(root, text="Generar Comprobante", command=self.generar_comprobante, bg="#4CAF50", fg="white").pack(pady=10)
        self.resultado = tk.Text(root, height=5, width=50)
        self.resultado.pack(pady=10)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = TiendaApp(root)
    root.mainloop()