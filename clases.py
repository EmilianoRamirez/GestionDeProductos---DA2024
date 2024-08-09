import json

class Producto:
    def __init__(self, id, nombre, precio, stock):
        self.__id = id
        self.__nombre = nombre
        self.__precio = self.validar_precio(precio)
        self.__stock = self.validar_cantidad(stock)

    @property
    def id(self):
        return self.__id
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def precio(self):
        return self.__precio
    
    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)
    
    @property
    def stock(self):
        return self.__stock
    

    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num <= 0:
                raise ValueError("El precio debe ser un número positivo.")
            return precio_num
        except ValueError:
            raise ValueError("El precio debe ser un número válido.")

    def validar_cantidad(self, stock):
        try:
            cantidad_num = int(stock)
            if cantidad_num < 0:
                raise ValueError("La stock debe ser un número entero no negativo.")
            return cantidad_num
        except ValueError:
            raise ValueError("La stock debe ser un número entero válido.")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock
        }

    def __str__(self):
        return f"{self.nombre} - Precio: ${self.precio:.2f} - Stock: {self.stock}"

class ProductoElectronico(Producto):
    def __init__(self, id, nombre, precio, stock, marca):
        super().__init__(id, nombre, precio, stock)
        self.__marca = marca

    @property
    def marca(self):
        return self.__marca

    def to_dict(self):
        data = super().to_dict()
        data["marca"] = self.marca
        data["tipo"] = "Electronico"
        return data

    def __str__(self):
        return f"Electronico >> {super().__str__()} - Marca: {self.marca}"

class ProductoAlimenticio(Producto):
    def __init__(self, id, nombre, precio, stock, fecha_caducidad, forma):
        super().__init__(id, nombre, precio, stock)
        self.__fecha_caducidad = fecha_caducidad
        self.__forma = self.validar_forma(forma)

    @property
    def fecha_caducidad(self):
        return self.__fecha_caducidad
    
    @property
    def forma(self):
        return self.__forma
    
    def validar_forma(self, f):
        opciones_validas = ['unidad', 'docena', 'kilo']
        if f not in opciones_validas:
            raise ValueError("Las unicas palabras aceptadas son 'unidad', 'docena', 'kilo' ")
        return f

    def to_dict(self):
        data = super().to_dict()
        data["fecha_caducidad"] = self.fecha_caducidad
        data["forma"] = self.forma
        data["tipo"] = "Alimenticio"
        return data

    def __str__(self):
        return f"Alimenticio >> {super().__str__()} - Forma: {self.forma} - Fecha de caducidad: {self.fecha_caducidad}"

class ProductoIndumentaria(Producto):
    def __init__(self, id, nombre, precio, stock, nom_marca, talle):
        super().__init__(id, nombre, precio, stock)
        self.__nom_marca = nom_marca
        self.__talle = self.validar_talle(talle)

    @property
    def nom_marca(self):
        return self.__nom_marca
    
    @property
    def talle(self):
        return self.__talle
    
    def validar_talle(self, t):
        talles_validos = ['xs', 's', 'm', 'l', 'xl', 'xxl']
        if t not in talles_validos:
            raise ValueError("Los talles validos son XS, S, M, L, XL o XXL ")
        return t
    
    def to_dict(self):
        data = super().to_dict()
        data["nombre_marca"] = self.nom_marca
        data["talle"] = self.talle
        data["tipo"] = "Indumentaria"
        return data
    
    def __str__(self):
        return f"Indumentaria >> {super().__str__()} - Marca: {self.marca} - Talle: {self.talle}"


class GestionProductos:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_producto(self, producto):
        try:
            datos = self.leer_datos()
            id = producto.id
            if id in datos:
                print(f"Ya existe un producto con ID '{id}'.")
            else:
                datos[id] = producto.to_dict()
                self.guardar_datos(datos)
                print(f"Producto {producto.nombre} creado correctamente.")
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')

    def leer_producto(self, id):
        try:
            datos = self.leer_datos()
            if id in datos:
                producto_data = datos[id]
                if 'marca' in producto_data:
                    producto = ProductoElectronico(**producto_data)
                else:
                    producto = ProductoAlimenticio(**producto_data)
                print(f'Producto encontrado: {producto}')
            else:
                print(f'No se encontró producto con ID {id}')

        except Exception as e:
            print(f'Error al leer producto: {e}')

    def actualizar_producto(self, id, nuevo_precio):
        try:
            datos = self.leer_datos()
            if id in datos:
                    datos[id]['precio'] = nuevo_precio
                    self.guardar_datos(datos)
                    print(f'Precio actualizado para el producto ID:{id}')
            else:
                print(f'No se encontró producto con ID:{id}')
        except Exception as e:
            print(f'Error al actualizar el producto: {e}')

    def eliminar_producto(self, id):
        try:
            datos = self.leer_datos()
            if id in datos:
                    del datos[id]
                    self.guardar_datos(datos)
                    print(f'Producto ID:{id} eliminado correctamente')
            else:
                print(f'No se encontró producto con ID:{id}')
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')