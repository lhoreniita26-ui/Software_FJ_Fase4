# Integración de los servicios y las reservas de Jimmy

## Reparto y base utilizada

El aporte de Jimmy comprende sistema/servicios.py, sistema/reserva.py y sus pruebas.
Entidad corresponde a Leidy. Su archivo se incorporó desde main mediante Fetch y
Pull, conservando sus commits y sin modificar su contenido. La base de main
verificada es edb0f505802ca5a013e53b8cb864d429dee396c4.

excepciones.py y logger.py también conservan los archivos de Leidy. La versión
individual de respaldo no forma parte de esta integración.

## Contrato confirmado de Entidad

Entidad tiene un constructor sin parámetros, una propiedad id de solo lectura y
los métodos abstractos describir() y validar(). Servicio y Reserva invocan
super().__init__() sin argumentos e implementan ambos métodos. Servicio mantiene
además calcular_costo() y validar_parametros() como contratos abstractos para sus
clases concretas ReservaSala, AlquilerEquipo y Asesoria.

La Entidad de Leidy asigna un id entero mediante un contador compartido. Las
reservas lo incorporan a sus mensajes con formato de texto. Se adaptó una prueba
para convertir el id mediante str() antes de buscarlo dentro de la descripción;
esto evita imponer que la propiedad id tenga que devolver una cadena.

## Costos y estados

Tarifa por hora y duración positivas y finitas; impuestos y descuentos entre 0 y 1.
calcular_costo(2), calcular_costo(2, .19), calcular_costo(2, .19, .10).
Con tarifa 100 los resultados son 200, 238 y 214.20.
Fórmula: tarifa * horas * (1 - descuento) * (1 + impuesto).
El cálculo intermedio usa Decimal y devuelve float tras redondear a dos decimales.

Reserva pasa de pendiente a confirmada y después a procesada. Puede cancelarse
mientras está pendiente o confirmada. Si falla el procesamiento, se conservan el
estado y el costo; finally registra el cierre. main.py deberá controlar las
excepciones propagadas y continuar con las siguientes operaciones.

## Verificación

Se ejecutan las 19 pruebas con la Entidad publicada por Leidy y sus módulos de
excepciones y registro:

    python -m unittest discover -s tests -v

Resultado: 19 pruebas aprobadas. Las pruebas usan ClientePrueba como doble de
prueba; no sustituyen al Cliente real. Todavía falta integrar cliente.py y main.py,
que no estaban publicados en main al revisar la base indicada, y verificar la
simulación grupal completa de al menos diez operaciones.

## Historial y asistencia

El aporte inicial y sus revisiones se prepararon con asistencia de IA. Los tres
commits originales y sus fechas se conservan; Jimmy realizó su envío desde CMD
y se verificó la rama en GitHub. Después se registraron correcciones reales de
alcance, integración y compatibilidad, sin recrear una secuencia de desarrollo
anterior. Los commits de Entidad conservan la autoría de Leidy.

La implementación personal por etapas solicitada por la compañera requiere el
trabajo y las comprobaciones del estudiante. Estos archivos no se presentan como
evidencia de haber escrito manualmente cada etapa del proyecto.
