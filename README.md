# Codes
En todos los códigos hay una primera lectura de los argumentos con los que se va a trabajar (inserte csv). Debido a que el csv contiene un encabezado a la hora de leerlo se añade la opción para eliminarlo del conjunto de datos.
En todos los códigos que generan gráficas (color.py, colorMasUsado.py y  horasMasActividad.py) se ha utilizado un parámetro extra que sirve para seleccionar el bucket en el que se desea que se guarde los resultados. Esto ha sido necesario ya que Matplotlib que es la librería que usamos para generar las imágenes no podía guardarlas directamente en el bucket. Para lo anterior se usa la función upload_blob.
Debido a que ciertas casillas del csv están vacías (en la columna del timestamp) se realiza un filtro para eliminar la fila entera.

color.py: Trabaja con la columna color que se muestra con su valor en hexadecimal, de la cual saca la suma de cada uno. Con estos datos el código procede a hacer una gráfica de barras en la cual se muestra en el eje Y el número de veces que se ha usado ese color. Para darle un caracter más visual a la gráfica se han presentado las barras del color correspondiente al modificado. Esto se guarda en un png en local (/tmp) el cual se transpasa al GCS (Google Cloud Storage) en la carpeta y bucket seleccionados.

horasMasActividad.py: Trabaja con el timestamp en el que se ha puesto el dato (tanto dia como hora). Estos datos los ordena por timestamp de modificación, sumando para cada día y cada hora cuantos píxeles han sido modificados. Para cada día genera una gráfica de barras en las que aparecen las 24 horas del día en el eje X y el número de píxeles modificados en el Y.

userMasActivo.py: Trabaja con las columnas del id, contando cuantas veces aparece cada uno de ellos y ordenandolos de manera descendiente. De esta forma con la función limit podemos sacar los 10 usuarios con más actividad y sacar un fichero con el id del usuario y las veces que escribe. El resultado se guarda en el GCS directamente.

pixelesMasMovidos.py: Utiliza la columna de coordenadas y al igual que userMasActivo, cuenta cuantas veces aparece cada coordenada, ordenandolas de manera decreciente y mostrandose mediante la función limit las 10 coordenadas que más se han modificado. El fichero que se guarda directamente en el GCS contiene la coordenada y las veces que se ha modificado.

colorMasUsadoHora.py: Utiliza de nuevo la columna timestampt y por cada hora de cada día muestra en forma de gráfico de lineas los 10 colores que más se han utilizado (En el caso del blanco se ha utilizado el color negro pero en vez de puntos se han utilizado asteriscos para diferenciarlo). Hemos establecido el límite superior de la gráfica a 1500000 elementos para poder apreciar la diferencia entre los valores debido a que el valor #FFFFFF al final de la gráfica toma un valor exorbitado.

https://yef4n.github.io/rPlaceAnalysis/
