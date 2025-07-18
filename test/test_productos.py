import unittest
import os
import gc
from clases.producto import Producto
from clases.sistema_gestion import SistemaGestion
from base_de_datos.conexion import Conexion

class TestProductos(unittest.TestCase):
    def setUp(self):
        
        self.conexion = Conexion(path_bd="base_de_datos/test_tienda.db")
        self.sistema = SistemaGestion()
        self.producto1 = Producto(101, "Arepa", 2.5, "Arepa de queso", 10)
        self.producto2 = Producto(102, "Empanada", 1.5, "Empanada de carne", 15)

    def tearDown(self):
       
        self.sistema.cerrar_conexion()
        self.conexion.cerrar_conexion()  
        gc.collect()  
        if os.path.exists("base_de_datos/test_tienda.db"):
            try:
                os.remove("base_de_datos/test_tienda.db")
            except PermissionError:
                pass  
    def test_registrar_producto(self):
        self.sistema.registrar_producto(self.producto1)
        producto_encontrado = self.sistema.buscar_producto(101)
        self.assertIsNotNone(producto_encontrado)
        self.assertEqual(producto_encontrado.nombre, "Arepa")
        self.assertEqual(producto_encontrado.precio, 2.5)
        self.assertEqual(producto_encontrado.stock, 10)
    
        productos_db = self.sistema.conexion.mostrar_productos()
        self.assertEqual(len(productos_db), 1)
        self.assertEqual(productos_db[0][1], "Arepa")

    def test_buscar_producto_inexistente(self):
        producto_encontrado = self.sistema.buscar_producto(999)
        self.assertIsNone(producto_encontrado)

    def test_actualizar_stock_suficiente(self):
        self.sistema.registrar_producto(self.producto1)
        self.sistema.actualizar_stock_producto(101, 5)
        producto_encontrado = self.sistema.buscar_producto(101)
        self.assertEqual(producto_encontrado.stock, 5)
        
        productos_db = self.sistema.conexion.mostrar_productos()
        self.assertEqual(productos_db[0][4], 5)

    def test_actualizar_stock_insuficiente(self):
        self.sistema.registrar_producto(self.producto1)
        with self.assertRaises(ValueError) as context:
            self.sistema.actualizar_stock_producto(101, 15)
        self.assertTrue("Stock insuficiente" in str(context.exception))

    def test_mostrar_productos(self):
        self.sistema.registrar_producto(self.producto1)
        self.sistema.registrar_producto(self.producto2)
        productos_db = self.sistema.conexion.mostrar_productos()
        self.assertEqual(len(productos_db), 2)
        nombres = [prod[1] for prod in productos_db]
        self.assertIn("Arepa", nombres)
        self.assertIn("Empanada", nombres)

if __name__ == '__main__':
    unittest.main()