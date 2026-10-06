import sqlite3

# Conexión con la base de datos
base_datos = sqlite3.connect("universidad.db")
db = base_datos.cursor()

# Crear la tabla si todavía no existe
db.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    carrera TEXT
)
""")

base_datos.commit()


def obtener_entero(texto):
    while True:
        dato = input(texto)

        try:
            numero = int(dato)
            return numero
        except ValueError:
            print("Ingrese un valor numérico válido.")


def agregar_estudiante():
    print("\n--- REGISTRO DE ESTUDIANTE ---")

    nombre = input("Ingrese el nombre: ")
    edad = obtener_entero("Ingrese la edad: ")
    carrera = input("Ingrese la carrera: ")

    db.execute(
        "INSERT INTO estudiantes (nombre, edad, carrera) VALUES (?, ?, ?)",
        (nombre, edad, carrera)
    )

    base_datos.commit()

    print("El estudiante fue registrado.")


def mostrar_estudiantes():
    print("\n--- LISTA DE ESTUDIANTES ---")

    db.execute("SELECT id, nombre, edad, carrera FROM estudiantes")
    registros = db.fetchall()

    if not registros:
        print("Actualmente no existen estudiantes registrados.")
        return

    for registro in registros:
        identificador = registro[0]
        nombre = registro[1]
        edad = registro[2]
        carrera = registro[3]

        print(
            "ID:", identificador,
            "| Nombre:", nombre,
            "| Edad:", edad,
            "| Carrera:", carrera
        )


def modificar_estudiante():
    print("\n--- ACTUALIZAR ESTUDIANTE ---")

    identificador = obtener_entero("Ingrese el ID del estudiante: ")

    db.execute(
        "SELECT * FROM estudiantes WHERE id = ?",
        (identificador,)
    )

    estudiante = db.fetchone()

    if estudiante is None:
        print("No existe un estudiante con ese ID.")
        return

    nombre = input("Nuevo nombre: ")
    edad = obtener_entero("Nueva edad: ")
    carrera = input("Nueva carrera: ")

    db.execute("""
        UPDATE estudiantes
        SET nombre = ?, edad = ?, carrera = ?
        WHERE id = ?
    """, (nombre, edad, carrera, identificador))

    base_datos.commit()

    print("Los datos fueron actualizados correctamente.")


def borrar_estudiante():
    print("\n--- ELIMINAR ESTUDIANTE ---")

    identificador = obtener_entero("Ingrese el ID que desea eliminar: ")

    db.execute(
        "SELECT * FROM estudiantes WHERE id = ?",
        (identificador,)
    )

    estudiante = db.fetchone()

    if estudiante is None:
        print("No se encontró ningún estudiante con ese ID.")
        return

    db.execute(
        "DELETE FROM estudiantes WHERE id = ?",
        (identificador,)
    )

    base_datos.commit()

    print("El estudiante fue eliminado.")


def mostrar_menu():
    print("       SISTEMA UNIVERSIDAD")

    print("1. Agregar estudiante")
    print("2. Mostrar estudiantes")
    print("3. Modificar estudiante")
    print("4. Eliminar estudiante")
    print("5. Cerrar programa")


while True:
    mostrar_menu()

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        agregar_estudiante()

    elif opcion == "2":
        mostrar_estudiantes()

    elif opcion == "3":
        modificar_estudiante()

    elif opcion == "4":
        borrar_estudiante()

    elif opcion == "5":
        print("\nPrograma cerrado correctamente.")
        break

    else:
        print("La opción seleccionada no es válida.")


base_datos.close()
