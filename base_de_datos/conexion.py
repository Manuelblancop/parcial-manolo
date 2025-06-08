import sqlite3
import os

class Conexion:
    def __init__(self, path_bd="base_de_datos/tienda.db"):
        os.makedirs(os.path.dirname(path_bd), exist_ok=True)
        self.conexion = sqlite3.connect(path_bd)
        self.cursor = self.conexion.cursor()
        self.crear_tabla_productos()

    def crear_tabla_productos(self):
        # Eliminar la tabla si existe para evitar duplicados
        self.cursor.execute('DROP TABLE IF EXISTS productos')
        # Crear la tabla
        self.cursor.execute('''
            CREATE TABLE productos (
                id_producto INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                descripcion TEXT,
                stock INTEGER NOT NULL
            )
        ''')
        self.conexion.commit()

    def insertar_producto(self, id_producto, nombre, precio, descripcion, stock):
        self.cursor.execute('''
            INSERT INTO productos (id_producto, nombre, precio, descripcion, stock)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_producto, nombre, precio, descripcion, stock))
        self.conexion.commit()

    def mostrar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        return productos

    def eliminar_producto(self, id_producto):
        self.cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
        self.conexion.commit()

    def actualizar_stock(self, id_producto, stock):
        self.cursor.execute("UPDATE productos SET stock = ? WHERE id_producto = ?", (stock, id_producto))
        self.conexion.commit()

    def cerrar_conexion(self):
        self.conexion.close()