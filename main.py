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
# Operación 5: sala válida
print("\n--- Operación 5: Servicio válido (sala) ---")
try:
    # Crea la sala con nombre y precio por hora
    sala = ReservaSala("Sala Ejecutiva", 50000)
    # La agrega a la lista de servicios
    servicios.append(sala)
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 5 exitosa: servicio creado -> {sala.describir()}")
    # Muestra el resultado
    print("OK:", sala.describir())
# Captura el error del sistema y el programa sigue
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 5 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)

# Operación 6: equipo y asesoría válidos
print("\n--- Operación 6: Servicios válidos (equipo y asesoría) ---")
try:
    # Crea el equipo con nombre y precio por hora
    equipo = AlquilerEquipo("Proyector 4K", 20000)
    # Crea la asesoría con nombre y precio por hora
    asesoria = Asesoria("Asesoría en Datos", 80000)
    # Agrega ambos a la lista de servicios
    servicios.extend([equipo, asesoria])
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 6 exitosa: servicios creados -> {equipo.describir()} y {asesoria.describir()}")
    # Muestra ambos resultados
    print("OK:", equipo.describir())
    print("OK:", asesoria.describir())
# Captura el error del sistema y el programa sigue
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 6 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)

# Operación 7: servicio inválido (precio negativo)
print("\n--- Operación 7: Servicio inválido (precio negativo) ---")
try:
    # Intenta crear la sala con precio negativo (debe fallar)
    sala_mala = ReservaSala("Sala Falsa", -100)
    # Solo llega aquí si no falló
    servicios.append(sala_mala)
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 7 exitosa: servicio creado -> {sala_mala.describir()}")
    # Muestra el resultado
    print("OK:", sala_mala.describir())
# Captura el error del servicio inválido
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 7 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)

# Operación 8: servicio inválido (nombre vacío)
print("\n--- Operación 8: Servicio inválido (nombre vacío) ---")
try:
    # Intenta crear la asesoría con el nombre vacío (debe fallar)
    asesoria_mala = Asesoria("", 60000)
    # Solo llega aquí si no falló
    servicios.append(asesoria_mala)
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 8 exitosa: servicio creado -> {asesoria_mala.describir()}")
    # Muestra el resultado
    print("OK:", asesoria_mala.describir())
# Captura el error del servicio inválido
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 8 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)
# Operación 9: reserva exitosa (crear, confirmar y procesar)
print("\n--- Operación 9: Reserva exitosa ---")
try:
    # Crea la reserva: primer cliente, primer servicio, 3 horas
    reserva1 = Reserva(clientes[0], servicios[0], 3)
    # La agrega a la lista de reservas
    reservas.append(reserva1)
    # Cambia el estado de pendiente a confirmada
    reserva1.confirmar()
    # Procesa con 19% de impuesto y 10% de descuento
    total = reserva1.procesar(0.19, 0.10)
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 9 exitosa: reserva {reserva1.id} procesada, total {total}")
    # Muestra el total y el estado final
    print("OK, total:", total, "| estado:", reserva1.estado)
# Captura el error del sistema y el programa sigue
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 9 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)

# Operación 10: reserva fallida (horas = 0)
print("\n--- Operación 10: Reserva fallida (horas = 0) ---")
try:
    # Intenta crear la reserva con 0 horas (debe fallar)
    reserva_mala = Reserva(clientes[1], servicios[1], 0)
    # Solo llega aquí si no falló
    reservas.append(reserva_mala)
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 10 exitosa: reserva creada -> {reserva_mala.describir()}")
    # Muestra el resultado
    print("OK:", reserva_mala.describir())
# Captura el error de la reserva inválida
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 10 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)

# Operación 11: reserva fallida (servicio no disponible)
print("\n--- Operación 11: Reserva fallida (servicio no disponible) ---")
try:
    # Marca el equipo como no disponible
    servicios[1].disponible = False
    # Crea la reserva (se permite: queda pendiente)
    reserva_no_disp = Reserva(clientes[1], servicios[1], 2)
    # La agrega a la lista de reservas
    reservas.append(reserva_no_disp)
    # Confirma: aquí falla porque el servicio no está disponible
    reserva_no_disp.confirmar()
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 11 exitosa: reserva confirmada -> {reserva_no_disp.describir()}")
    # Muestra el resultado
    print("OK:", reserva_no_disp.describir())
# Captura el error del servicio no disponible
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 11 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)
# Se ejecuta siempre: deja el servicio disponible otra vez
finally:
    # Restablece la disponibilidad para las siguientes operaciones
    servicios[1].disponible = True

# Operación 12: procesar una reserva sin confirmar
print("\n--- Operación 12: Procesar una reserva sin confirmar ---")
try:
    # Crea una reserva nueva (queda pendiente)
    reserva2 = Reserva(clientes[1], servicios[2], 2)
    # La agrega a la lista de reservas
    reservas.append(reserva2)
    # Procesa sin confirmar (debe fallar)
    reserva2.procesar()
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 12 exitosa: reserva procesada -> {reserva2.describir()}")
    # Muestra el resultado
    print("OK:", reserva2.describir())
# Captura el error de operación no permitida
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 12 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)

# Operación 13: confirmar una reserva cancelada
print("\n--- Operación 13: Confirmar una reserva cancelada ---")
try:
    # Cancela la reserva de la operación 12
    reserva2.cancelar()
    # Confirma una reserva cancelada (debe fallar)
    reserva2.confirmar()
    # Suma una operación exitosa
    exitosas += 1
    # Registra el éxito en el log
    registrar_evento(f"Operación 13 exitosa: reserva confirmada -> {reserva2.describir()}")
    # Muestra el resultado
    print("OK:", reserva2.describir())
# Captura el error de operación no permitida
except SoftwareFJError as error:
    # Suma una operación fallida
    fallidas += 1
    # Registra el error en el log
    registrar_error(f"Operación 13 fallida: {error}")
    # Muestra el error
    print("Error controlado:", error)        