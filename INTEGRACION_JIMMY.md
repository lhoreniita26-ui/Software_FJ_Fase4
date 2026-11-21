# Aporte grupal de Jimmy

Base: main de lhoreniita26-ui/Software_FJ_Fase4, commit
902ba4f5d8ebdca5abe403f96890a05580ff0280.

Se agregan entidad.py, servicios.py y reserva.py, con comentarios de las
lineas y pruebas de contrato. excepciones.py y logger.py conservan el
contenido publicado por Leidy. No se incluye la alternativa individual.

## Contrato de integracion

Cliente debe heredar de Entidad, llamar a super().__init__() o pasar un
identificador y exponer nombre, documento y correo como textos no vacios.
Debe implementar describir() y validar(). La validacion correcta puede devolver
True o None y los datos incorrectos deben lanzar ClienteInvalidoError.

Los imports admiten sistema como paquete y ejecucion desde su carpeta.
Los atributos y los estados de Reserva se consultan con propiedades de lectura.
Servicio.disponible puede modificarse con un valor booleano.

## Costos

Tarifa por hora positiva; duracion positiva y finita. Tasas entre cero y uno.
calcular_costo(2), calcular_costo(2, .19), calcular_costo(2, .19, .10).
Con tarifa 100 los resultados son 200, 238 y 214.20.
Formula: tarifa * horas * (1 - descuento) * (1 + impuesto).
Se redondea al final a dos decimales. No se agregan cargos no acordados.

## Estados y excepciones

Pendiente -> confirmada -> procesada. Se puede cancelar desde pendiente o confirmada.
Procesada y cancelada son estados finales. Si falla un calculo, el estado y el costo
no se modifican; puede corregirse el parametro y reintentarse.
procesar() usa try/except/else/finally. Los errores se registran y se propagan con
su tipo original; los calculos no representables encadenan la causa aritmetica.
El controlador grupal debera aislar cada operacion y registrar los errores de
creacion de clientes y servicios para completar la simulacion del anexo.

## Verificacion y trabajo pendiente

python -m unittest discover -s tests -v

Las 19 pruebas usan ClientePrueba como doble de prueba, no como cliente de produccion.
Se prueban valores invalidos, costos, estados, disponibilidad, reintentos, logs y causas.
Todavia no estan publicados cliente.py ni main.py: falta integrar esos archivos,
la simulacion completa de al menos 10 operaciones y el informe grupal final.

## Publicacion y autoria

Este aporte se prepara para Jimmy1295 con asistencia de IA. Se publica mediante la
integracion de GitHub y commits de la cuenta conectada. Esta publicacion no es
evidencia de un git push ejecutado desde CMD; esa evidencia local queda pendiente.
Los tres commits locales anteriores se conservan en la copia original y no se
reescribe el historial de main. El pull request presenta el aporte para revision.
