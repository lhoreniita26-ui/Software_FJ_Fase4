"""Programa principal de Software FJ.

Simula operaciones válidas e inválidas de clientes, servicios y reservas.
Cada operación va en su propio try/except, así el programa nunca se detiene.
"""

# Importa la clase Cliente
from sistema.cliente import Cliente
# Importa los tres servicios especializados
from sistema.servicios import ReservaSala, AlquilerEquipo, Asesoria
# Importa la clase Reserva
from sistema.reserva import Reserva
# Importa la excepción base: captura todos los errores propios del sistema
from sistema.excepciones import SoftwareFJError
# Importa las funciones para escribir en el archivo de log
from sistema.logger import registrar_evento, registrar_error

# Lista donde se guardan los clientes creados
clientes = []
# Lista donde se guardan los servicios creados
servicios = []
# Lista donde se guardan las reservas creadas
reservas = []

# Contador de operaciones que terminaron bien
exitosas = 0
# Contador de operaciones que terminaron con un error controlado
fallidas = 0

# Deja constancia en el log de que empezó la simulación
registrar_evento("=== Inicio de la simulación ===")

# Muestra el título del programa en pantalla
print("=== Simulación Software FJ ===")

# Operación 1: cliente válido
print("\n--- Operación 1: Cliente válido ---")
try:
    # Crea el cliente con datos correctos
    cliente1 = Cliente("Ana Pérez", "1012345678", "ana@correo.com")
    # Lo agrega a la lista de clientes
    clientes.append(cliente1)
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 1 exitosa: cliente creado -> {cliente1.describir()}")
    # Muestra el resultado
    print("OK:", cliente1.describir())
# Captura el error del sistema y el programa sigue
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 1 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)

# Operación 2: segundo cliente válido
print("\n--- Operación 2: Segundo cliente válido ---")
try:
    # Crea el cliente con datos correctos
    cliente2 = Cliente("Luis Gómez", "79876543", "luis@correo.com")
    # Lo agrega a la lista de clientes
    clientes.append(cliente2)
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 2 exitosa: cliente creado -> {cliente2.describir()}")
    # Muestra el resultado
    print("OK:", cliente2.describir())
# Captura el error del sistema y el programa sigue
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 2 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)

# Operación 3: cliente inválido (correo sin arroba)
print("\n--- Operación 3: Cliente inválido (correo sin arroba) ---")
try:
    # Intenta crear el cliente con un correo incorrecto (debe fallar)
    cliente3 = Cliente("Pedro Ruiz", "12345678", "correo-sin-arroba")
    # Solo llega aquí si no falló
    clientes.append(cliente3)
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 3 exitosa: cliente creado -> {cliente3.describir()}")
    # Muestra el resultado
    print("OK:", cliente3.describir())
# Captura el error del cliente inválido
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 3 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)

# Operación 4: cliente inválido (nombre vacío)
print("\n--- Operación 4: Cliente inválido (nombre vacío) ---")
try:
    # Intenta crear el cliente con el nombre vacío (debe fallar)
    cliente4 = Cliente("   ", "12345678", "x@correo.com")
    # Solo llega aquí si no falló
    clientes.append(cliente4)
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 4 exitosa: cliente creado -> {cliente4.describir()}")
    # Muestra el resultado
    print("OK:", cliente4.describir())
# Captura el error del cliente inválido
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 4 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)