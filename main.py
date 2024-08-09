import os
import platform

from clases import (
    ProductoElectronico,
    ProductoAlimenticio,
    ProductoIndumentaria,
    GestionProductos,
)

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') 

def mostrar_menu():
    print("========== Menú de Gestión de Productos ==========")
    print('1. Agregar Producto Electrónico')
    print('2. Agregar Producto Alimenticio')
    print('3. Agregar Producto Indumentaria')
    print('4. Buscar Producto por ID')
    print('5. Actualizar Producto')
    print('6. Eliminar Producto por ID')
    print('7. Mostrar Todos los Productos')
    print('8. Salir')
    print('==================================================')

def agregar_producto(gestion, tipo_producto):
    try:
        id = int(input('Ingrese ID del producto: '))
        nombre = input('Ingrese nombre del producto: ')
        precio = float(input('Ingrese precio del producto: '))
        cantidad = int(input('Ingrese cantidad en stock: '))

        if tipo_producto == '1':
            marca = input('Ingrese marca del producto: ')
            producto = ProductoElectronico(id, nombre, precio, cantidad, marca)
        elif tipo_producto == '2':
            fecha_caducidad = input('Ingrese fecha de caducidad del producto (dd/mm/aaaa): ')
            forma = input('Ingrese la forma de cobro (unidad, docena, kilo): ').lower()
            producto = ProductoAlimenticio(id, nombre, precio, cantidad, fecha_caducidad, forma)
        elif tipo_producto == '3':
            nom_marca = input('Ingrese nombre de la marca: ')
            talle = input('ingrese talle (XS, S, M, L, XL, XXL): ').lower()
            producto = ProductoIndumentaria(id, nombre, precio, cantidad, nom_marca, talle)
        else:
            print('Opción inválida')
            return

        gestion.crear_producto(producto)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_producto_por_id(gestion):
    id = input('Ingrese el ID del producto a buscar: ')
    gestion.leer_producto(id)
    input('Presione enter para continuar...')

def actualizar_precio_producto(gestion):
    id = input('Ingrese el ID del producto para actualizar precio: ')
    precio = float(input('Ingrese el nuevo precio del producto: '))
    gestion.actualizar_producto(id, precio)
    input('Presione enter para continuar...')

def eliminar_producto_por_id(gestion):
    id = input('Ingrese el ID del producto a eliminar: ')
    gestion.eliminar_producto(id)
    input('Presione enter para continuar...')

def mostrar_todos_los_productos(gestion):
    productos = gestion.leer_datos()
    if len(productos) > 0:
        print('=============== Listado completo de los Productos ==============')
        for producto in productos.values():
            if 'marca' in producto:
                print(f"{producto['nombre']} - Marca: {producto['marca']} - Precio: {producto['precio']}")
            elif 'forma' in producto:
                print(f"{producto['nombre']} - Se vende por {producto['forma']} - Precio: {producto['precio']} - Caducidad: {producto['fecha_expiracion']}")
            elif 'talle' in producto:
                print(f"{producto['nombre']} - Marca: {producto['nombre_marca']} - Precio: {producto['precio']} - Talle: {producto['talle']}")
            else:
                print(f"{producto['nombre']} - Precio: {producto['precio']}")
        print('================================================================')
    else:
        print("No hay productos en el inventario.")
    input('Presione enter para continuar...')

if __name__ == "__main__":
    archivo_productos = 'productos_db.json'
    gestion = GestionProductos(archivo_productos)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2' or opcion == '3':
            agregar_producto(gestion, opcion)
        
        elif opcion == '4':
            buscar_producto_por_id(gestion)

        elif opcion == '5':
            actualizar_precio_producto(gestion)

        elif opcion == '6':
            eliminar_producto_por_id(gestion)

        elif opcion == '7':
            mostrar_todos_los_productos(gestion)

        elif opcion == '8':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-7)')