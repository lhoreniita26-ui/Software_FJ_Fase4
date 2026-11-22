# Servicios y reservas de Jimmy

## Base y responsabilidades

Se trabaja sobre main, commit 50e641778a7a3cc3d29bfd82d7361b4e8ae72c4c, que incluye
el PR anterior y el Cliente de Leidy. Entidad, Cliente, excepciones y logger
conservan sus archivos y autoria. Jimmy modifica servicios, reservas y sus pruebas.
main.py y la simulacion completa del grupo siguen pendientes de integracion.

## Calculos especializados

Todas las tarifas y duraciones deben ser positivas y finitas. Impuesto y descuento
son proporciones entre 0 y 1. Los booleanos, el texto, NaN e infinitos se rechazan.
Se calcula con Decimal y se devuelve float tras redondear a dos decimales con
ROUND_HALF_UP. Se redondea una sola vez, al final.

- ReservaSala: subtotal = tarifa * horas + cargo_limpieza.
- AlquilerEquipo: subtotal = tarifa * horas * (1 + tasa_seguro).
- Asesoria: subtotal = tarifa * horas.

Total = subtotal * (1 - descuento) * (1 + impuesto).
Los cargos adicionales tambien reciben el descuento y el impuesto.
El cargo de limpieza es un importe fijo no negativo aplicado una vez por reserva.
El seguro es una proporcion de 0 a 1: 0.05 significa el 5 % del alquiler.

Las llamadas anteriores con nombre, tarifa y disponible mantienen su resultado:
los cargos opcionales valen cero por defecto. Los cargos se pasan por nombre:

    ReservaSala('Sala', 100, cargo_limpieza=20)
    AlquilerEquipo('Equipo', 100, tasa_seguro=0.05)

calcular_costo conserva las variantes con horas, horas e impuesto, u horas,
impuesto y descuento. describir() informa la regla particular del servicio.

## Reservas

Reserva empieza pendiente, puede confirmarse y procesarse, o cancelarse desde
pendiente o confirmada. Los errores conservan el estado anterior; else guarda
el costo solo si el calculo termina correctamente y finally registra el cierre.
El id entero pertenece a la Entidad de Leidy; se convierte a texto al describirlo.

## Verificacion

    python -m unittest discover -s tests -v

Etapa equipo: 29 pruebas aprobadas (19 anteriores, 5 de sala y 5 de equipo).
Las pruebas nuevas verifican cargos, redondeo, encapsulacion y reservas con el
Cliente real publicado por Leidy. Falta la simulacion completa de al menos diez
operaciones mediante main.py para dar por terminado el proyecto grupal.

## Historial y asistencia

Los cambios y las pruebas se preparan con asistencia de IA y se registran en
commits funcionales, conservando el historial previo y la autoria de Leidy.
Cada resultado de pruebas corresponde a la etapa efectivamente ejecutada.
