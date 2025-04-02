# Example-of-random-forest-algoritm
Example of random forest algoritm 

This Python script will provide an example of random forest algoritm.  Rest of the description will be in spanish (if you find this interesting, use  google translator)


INTRODUCCION:

En este script de python vamos a presentar un ejemplo de algoritmo para random forest. 
Este script analizara los datos de las estaciones meteorologicas españolas proporcionados por AEMET y los datos de precios del mercado electrico proporcionados por ESIOS
Posteriormente tratara de predecir en funcion de esos datos si el precio del mercado electrico en un dia determinado sera cero en algun momento del dia.


El objetivo final en este momento no es tanto lograr una buena prediccion, sino  presentar un ejemplo de script para random forest y poder emplearlo como base en futuros desarrollos.




FUENTES DE DATOS Y PREPARACION PREVIA: 

EL script usa un fichero csv ya preparado.

Se obtuvieron los datos de todas las estaciones meteorologicas de españa, empleando el script disponible aqui:
https://github.com/fenris123/USING-AEMET-API-TO-OBTAIN-WEATHER-DATA-FROM-SPANISH-CITIES

Se descargaron los datos del mercado electrico diario para españa desde aqui.
https://www.esios.ree.es/es/analisis/600?vis=1&start_date=01-01-2022T00%3A00&end_date=31-12-2024T23%3A55&geoids=3&compare_start_date=31-12-2021T00%3A00&groupby=hour

En ambos casos, datos desde el 1/1/2022 hasta el 31/1/2024

Se limpiaron los datos de esios para quedarse solo con la columna valor, organizada en forma de si/no en funcion de si ese dia el precio caia hasta cero o menos y la fecha, y se hizo un merge con los datos de aemet.

La estructura del .csv final sigue esta organizacion:
fecha;indicativo;nombre;provincia;altitud;tmed;prec;tmin;horatmin;tmax;horatmax;dir;velmedia;racha;horaracha;sol;presMax;presMin;hrMedia;hrMax;hrMin;valor

Adjuntamos el archivo con los datos empleados si no se quiere realizar ese trabajo.



LIMIPIEZA Y TRANSFORMACION DE DATOS EJECUTADAS POR EL SCRIPT.

El script realiza una limpieza de los datos previa al algoritmo.  En particular:

- Manejo de las "," y los "." para los decimales.
- Eliminación de algunas columnas que van a aportar poco valor
- Conversion de los datos de la columna valor "SI/NO" en "0/1"
- Eliminacion de algunas filas con valores nulos.
- Transformacion de variables horarias con formato HH:MM  en minutos desde la media noche
- Creacion de la columna "AÑO" para separar los datos de entreno (2022 y 2023) de los de comprobacion (2024).  Eliminacion de dicha columna posteriormente.


Algunas de estas acciones podrian ejecutarse sobre el archivo inicial o en un script aparte, pero hemos preferido mantener los datos basicos originales y que se puedan ver las transformaciones realizadas en el propio script del random forest.




PROBLEMAS DEL ALGORITMO.

A nivel de programacion el script funciona correctamente y da el resultado que se le exije.

No obstante, la precision del algoritmo es MUY mala a la hora de detectar los dias en los que el precio de la electricidad llegara a cero.
En nuestra opinion esto se debe a un mal balance en los datos disponibles para el entrenamiento: Hay muchos dias con los precios por encima de cero, y muy pocos donde se alcance ese dato.
Se han realizado algunas modificaciones al algoritmo no incluidas aqui para tratar de paliar esto, pero no hemos logrado una mejora sustancial.
Ademas, hay demasiados valores nulos o en blanco que perjudican el rendimiento del algoritmo.


FUTUROS DESARROLLOS

El script cumple con su cometido, que era realizar un analisis de random forest sobre unos datos. En este sentido, lo consideramos completado.
Es posible que en el futuro intentemos practicar algunas tecnicas para mejorar la precision en la prediccion de los resultados de la clase menos representada en los datos de entrenamiento.
No obstante esto no es seguro, y no hay una fecha prevista para ello.
Puede que simplemente optemos por probar otro tipo de algoritmo mas adecuado a este tipo de datos.



