# Alcance del aporte de Jimmy

## Reparto actualizado

Este aporte comprende sistema/servicios.py, sistema/reserva.py y sus pruebas de
contrato. sistema/entidad.py corresponde a Leidy y se retira de los cambios de
esta rama. excepciones.py y logger.py conservan los archivos de Leidy.

## Dependencias pendientes

Al revisar main, en el commit 902ba4f5d8ebdca5abe403f96890a05580ff0280, aun no
estaban publicados entidad.py, cliente.py ni main.py. Los servicios, las reservas
y las pruebas requieren la Entidad que debe incorporar Leidy. Por tanto, esta
rama no es ejecutable por separado hasta integrar esa dependencia.

Servicio y Reserva llaman a super().__init__() sin argumentos. Entidad debe
proporcionar id y los metodos abstractos describir() y validar(). El Cliente real
debe heredar de Entidad y exponer nombre, documento y correo; validar() puede
devolver True o None cuando los datos son correctos, y debe lanzar un error de
la jerarquia SoftwareFJError si falla. Este contrato debe verificarse con los
archivos de Leidy cuando esten disponibles.

## Costos y estados

Tarifa por hora y duracion positivas y finitas; impuestos y descuentos entre 0 y 1.
calcular_costo(2), calcular_costo(2, .19), calcular_costo(2, .19, .10).
Con tarifa 100 los resultados son 200, 238 y 214.20.
Formula: tarifa * horas * (1 - descuento) * (1 + impuesto).
El calculo intermedio usa Decimal y devuelve float tras redondear a dos decimales.

Reserva pasa de pendiente a confirmada y despues a procesada. Se puede cancelar
mientras este pendiente o confirmada. Si falla el procesamiento, el estado y el
costo se conservan; finally registra el cierre. main.py debera controlar las
excepciones propagadas y continuar con las siguientes operaciones.

## Verificacion

Las 19 pruebas aprobaron antes de retirar la Entidad inicialmente aportada por
Jimmy. Ese resultado es historico: no acredita integracion con la Entidad de
Leidy, que aun no estaba publicada. Las pruebas usan ClientePrueba como doble de
prueba. Cuando Leidy publique Entidad, se debe ejecutar de nuevo:

    python -m unittest discover -s tests -v

Tambien falta probar cliente.py, main.py y la simulacion grupal completa de al
menos diez operaciones. La correccion de comentarios conserva el comportamiento
de servicios.py, reserva.py y las pruebas; se comprueba mediante comparacion AST.

## Historial y asistencia

El codigo inicial y esta correccion de documentacion se prepararon con asistencia
de IA. Los tres
commits originales y sus fechas se conservan; su envio desde CMD fue realizado
por Jimmy y verificado en GitHub. Esta correccion registra un cambio real de
alcance y documentacion, sin recrear una secuencia de desarrollo anterior.

La implementacion personal por etapas que solicita la companera requiere el
trabajo y las comprobaciones del estudiante. Estos archivos no se presentan como
evidencia de haber escrito manualmente cada etapa del proyecto.
