import sqlite3
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Función para conectar a la base de datos
def conectar_db():
    conn = sqlite3.connect('inventario_libros.db')  # Archivo de la base de datos
    return conn


# Función para registrar un libro
def registrar_libro():
    nombre = input(Fore.CYAN + "Nombre del libro: ")
    autor = input(Fore.CYAN + "Autor del libro: ")
    año = int(input(Fore.CYAN + "Año de publicación: "))
    genero = input(Fore.CYAN + "Género: ")
    cantidad = int(input(Fore.CYAN + "Cantidad: "))
    precio = float(input(Fore.CYAN + "Precio: "))

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO libros (nombre, autor, año, genero, cantidad, precio)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre, autor, año, genero, cantidad, precio))
    
    conn.commit()  # Esto asegura que los cambios se guarden permanentemente
    conn.close()   # Cerramos la conexión
    print(Fore.GREEN + "Libro registrado correctamente.")

# Función para mostrar los libros registrados
def mostrar_libros():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()

    if libros:
        print(Fore.YELLOW + "\nLista de libros registrados:")
        for libro in libros:
            print(f"ID: {libro[0]} | Nombre: {libro[1]} | Autor: {libro[2]} | Año: {libro[3]} | Género: {libro[4]} | Cantidad: {libro[5]} | Precio: {libro[6]}")
    else:
        print(Fore.RED + "No hay libros registrados.")

    conn.close()

# Función para mostrar los detalles del libro antes de actualizarlo
def mostrar_detalles_libro(id_libro):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM libros WHERE id = ?', (id_libro,))
    libro = cursor.fetchone()
    conn.close()
    
    if libro:
        print(Fore.YELLOW + "\nDetalles del libro seleccionado:")
        print(f"ID: {libro[0]} | Nombre: {libro[1]} | Autor: {libro[2]} | Año: {libro[3]} | Género: {libro[4]} | Cantidad: {libro[5]} | Precio: {libro[6]}")
        return libro
    else:
        print(Fore.RED + "No se encontró el libro con ese ID.")
        return None

# Función para actualizar un solo campo de un libro
def actualizar_libro():
    mostrar_libros()
    try:
        id_libro = int(input(Fore.CYAN + "Ingrese el ID del libro a actualizar: "))
        libro = mostrar_detalles_libro(id_libro)
        
        if libro:
            print(Fore.CYAN + "¿Qué campo te gustaría actualizar?")
            print("1. Precio")
            print("2. Cantidad")
            opcion = input(Fore.CYAN + "Selecciona una opción (1/2): ")

            if opcion == '1':
                nuevo_precio = float(input(Fore.CYAN + f"Ingrese el nuevo precio (actual: {libro[6]}): "))
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute('''
                UPDATE libros 
                SET precio = ? 
                WHERE id = ?
                ''', (nuevo_precio, id_libro))
                
                conn.commit()  # Guardar los cambios
                conn.close()
                print(Fore.GREEN + "Precio actualizado correctamente.")

            elif opcion == '2':
                nueva_cantidad = int(input(Fore.CYAN + f"Ingrese la nueva cantidad (actual: {libro[5]}): "))
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute('''
                UPDATE libros 
                SET cantidad = ? 
                WHERE id = ?
                ''', (nueva_cantidad, id_libro))
                
                conn.commit()  # Guardar los cambios
                conn.close()
                print(Fore.GREEN + "Cantidad actualizada correctamente.")

            else:
                print(Fore.RED + "Opción no válida. No se ha actualizado el libro.")
        else:
            print(Fore.RED + "No se pudo actualizar el libro.")
    except Exception as e:
        print(Fore.RED + f"Error al actualizar el libro: {e}")

# Función para eliminar un libro
def eliminar_libro():
    mostrar_libros()
    try:
        id_libro = int(input(Fore.CYAN + "Ingrese el ID del libro a eliminar: "))

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM libros WHERE id = ?', (id_libro,))
        
        conn.commit()  # Guardar los cambios
        conn.close()

        print(Fore.GREEN + "Libro eliminado correctamente.")
    except Exception as e:
        print(Fore.RED + f"Error al eliminar el libro: {e}")

# Función para verificar si la tabla existe
def verificar_tabla():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='libros';")
    if cursor.fetchone():
        print(Fore.GREEN + "La tabla 'libros' existe.")
    else:
        print(Fore.RED + "La tabla 'libros' no existe.")
    conn.close()

# Función para volver al menú principal
def volver_menu_principal():
    respuesta = input(Fore.CYAN + "¿Volver al menú principal? (Y/N): ").upper()
    if respuesta == 'Y':
        menu()

# Función para mostrar el menú principal
def menu():
    while True:
        print(Fore.GREEN + "\n--- Menú de Inventario de Libros ---")
        print("1. Registrar libro")
        print("2. Mostrar libros")
        print("3. Actualizar libro")
        print("4. Eliminar libro")
        print("5. Verificar existencia de tabla")
        print("6. Salir")

        opcion = input(Fore.CYAN + "Seleccione una opción: ")

        if opcion == '1':
            registrar_libro()
            volver_menu_principal()
        elif opcion == '2':
            mostrar_libros()
            volver_menu_principal()
        elif opcion == '3':
            actualizar_libro()
            volver_menu_principal()
        elif opcion == '4':
            eliminar_libro()
            volver_menu_principal()
        elif opcion == '5':
            verificar_tabla()
            volver_menu_principal()
        elif opcion == '6':
            print(Fore.YELLOW + "¡Hasta luego!")
            break
        else:
            print(Fore.RED + "Opción no válida. Intenta de nuevo.")

# Función para inicializar el programa
def inicializar_programa():
    print(Fore.GREEN + "\nBienvenid@ al inventario de libros.")
    menu()

# Ejecutar el programa
if __name__ == '__main__':
    inicializar_programa()
