
# Web
https://yef4n.github.io/rPlaceAnalysis/

## Descripción
El proyecto trata sobre el análisis del mural de r/place 2022. El r/place es un evento que se creó en el April Fools’ Day del 2017 en Reddit.

El lienzo inicialmente es de 1000 x 1000 píxeles, aunque a lo largo de la duración del evento, su tamaño aumenta hasta los 2000 x 2000 píxeles. Los usuarios pueden cambiar el color de un píxel cada 5 minutos.

Comunidades de distintos ámbitos se organizan para crear imágenes a gran escala como por ejemplo banderas de sus países, monumentos, logos, comida o incluso personajes de series o películas.

En este proyecto se van a estudiar las zonas que más actividad han tenido a través de un mapa de calor, así como los colores más usados y a qué hora hay más actividad. Viendo los dibujos dónde más gente participa se podrá ver qué comunidades son más activos, las zonas más disputadas, cuántos píxeles ha puesto la persona con más actividad en el mural, o si hay zonas que hayan sobrevivido desde el inicio.

## Necesidad de Big Data
Con más de 100 millones de píxeles colocados sobre el mural y más de 10 millones de usuarios únicos, es imposible procesar esta información sin la ayuda de Big Data.

## Descripción de los datos
El formato de los datos es csv, han sido obtenidos de la página de Kaggle. La información se divide en: la hora en la que se ha introducido el píxel en formato UTC, el hash del usuario, el color del píxel en formato hexadecimal y las coordenadas. El conjunto de los datos asciende a casi 22 GB.

El link a los datos es el siguiente: https://www.kaggle.com/datasets/antoinecarpentier/redditrplacecsv

## Descripción de códigos, herramientas e infraestructuras

### Codigos
Se han desarrollado los siguientes scripts en Python, para ver los contenidos o descargarlos, dirigirse a la carpeta [scripts](/scripts).

En todos los códigos hay una primera lectura de los argumentos con los que se va a trabajar (inserte csv). Debido a que el csv contiene un encabezado a la hora de leerlo se añade la opción para eliminarlo del conjunto de datos.
En todos los códigos que generan gráficas (color.py, colorMasUsado.py y  horasMasActividad.py) se ha utilizado un parámetro extra que sirve para seleccionar el bucket en el que se desea que se guarde los resultados. Esto ha sido necesario ya que Matplotlib que es la librería que usamos para generar las imágenes no podía guardarlas directamente en el bucket. Para lo anterior se usa la función upload_blob.
Debido a que ciertas casillas del csv están vacías (en la columna del timestamp) se realiza un filtro para eliminar la fila entera.

[color.py](/scripts/color.py): Trabaja con la columna color que se muestra con su valor en hexadecimal, de la cual saca la suma de cada uno. Con estos datos el código procede a hacer una gráfica de barras en la cual se muestra en el eje Y el número de veces que se ha usado ese color. Para darle un caracter más visual a la gráfica se han presentado las barras del color correspondiente al modificado. Esto se guarda en un png en local (/tmp) el cual se transpasa al GCS (Google Cloud Storage) en la carpeta y bucket seleccionados.

[horasMasActividad.py](scripts/horasMasActividad.py): Trabaja con el timestamp en el que se ha puesto el dato (tanto dia como hora). Estos datos los ordena por timestamp de modificación, sumando para cada día y cada hora cuantos píxeles han sido modificados. Para cada día genera una gráfica de barras en las que aparecen las 24 horas del día en el eje X y el número de píxeles modificados en el Y.

[userMasActivo.py](scripts/userMasActivo.py): Trabaja con las columnas del id, contando cuantas veces aparece cada uno de ellos y ordenandolos de manera descendiente. De esta forma con la función limit podemos sacar los 10 usuarios con más actividad y sacar un fichero con el id del usuario y las veces que escribe. El resultado se guarda en el GCS directamente.

[pixelesMasMovidos.py](scripts/pixelesMasMovidos.py): Utiliza la columna de coordenadas y al igual que userMasActivo, cuenta cuantas veces aparece cada coordenada, ordenandolas de manera decreciente y mostrandose mediante la función limit las 10 coordenadas que más se han modificado. El fichero que se guarda directamente en el GCS contiene la coordenada y las veces que se ha modificado.

[colorMasUsadoHora.py](scripts/colorMasUsadoHora.py): Utiliza de nuevo la columna timestampt y por cada hora de cada día muestra en forma de gráfico de lineas los 10 colores que más se han utilizado (En el caso del blanco se ha utilizado el color negro pero en vez de puntos se han utilizado asteriscos para diferenciarlo). Hemos establecido para que la gráfica resultante se muestre de manera logarítmica ya que los valores se disparan a partir de cierto punto, cambiando además el color Blanco (#FFFFFF) por otro que se aprecie mejor en la gráfica. Como apunte, el primer dia tiene algunos valores muy pequeños que deforman la gráfica por lo que es un caso especial con datos no útiles y por ende no los mostramos.

### Infraestructura
Para el desarrollo del proyecto hemos utilizado las siguientes herramientas:

_Github_: Control de versiones, almacenamiento de datos y setup de la página web (github pages).

_Google Cloud_: Almacenamiento del csv y los códigos y ejecución de los códigos.

_Matplotlib_: Librería de Python para la creación de los gráficos que generan los códigos.

_Python_: Lenguaje de programación usado para generar los códigos.

_HTML/Javascript_: Programación del frontend de la página web.

_Pyspark_: Biblioteca de Python que se utiliza como interfaz para Apache Spark. Con PySpark, podemos realizar operaciones en datasets y aprovechar la programación funcional paralela.

_Visual Code_: Editor de código fuente para la depuración, control integrado de Git, resaltado de sintaxis, finalización inteligente de código, fragmentos y refactorización de código.

# Como ejecutar el proyecto
Antes de nada necesitaremos una cuenta de Google Cloud con saldo, un proyecto de Cloud (el predeterminado sirve), un bucket que contenga una carpeta llamada input con el csv anteriormente mencionado y los .py descargados en el bucket, en el mismo directorio que la carpeta input.

## Ejecuta PySpark por  Local
### 1. Instalación de Python y pip
Aplicamos estos comandos para actualizar la lista de paquetes disponibles, instalar Python 3 y luego instalar el administrador de paquetes de Python (pip) en un sistema basado en Debian, como Ubuntu.


```
$ sudo apt update
$ sudo apt install python3
$ sudo apt install python3-pip
```
### 2. Instalación de Java Runtime Enviorment(JRE)
Este comando instala el entorno de ejecución de Java (Java Runtime Environment, JRE) predeterminado en un sistema basado en Debian, como Ubuntu. El JRE es necesario para ejecutar aplicaciones Java en el sistema.

```$ sudo apt install default-jre```
### 3. Instalación de PySpark
Este código instala la biblioteca PySpark utilizando el administrador de paquetes de Python, pip. Este comando descarga e instala la biblioteca PySpark y sus dependencias necesarias en tu entorno de Python.

```$ pip install pyspark```
### 4. Ejecuta los Python Scripts
Este comando ejecuta un script de Apache Spark usando el programa spark-submit. En este caso, pondremos en <script>  el nombre del script de Spark que deseas ejecutar.

```$ spark-submit <script>```
## Ejecuta PySpark por Cloud
Este comando crea un clúster de Google Cloud Dataproc en la región "europe-west6" con un nodo maestro y nodos de trabajo, y establece el tamaño de los discos de arranque tanto para el nodo maestro como para los nodos de trabajo en 50 GB.

```
$ gcloud dataproc clusters create example-cluster --region europe-west6 --enable-component-gateway --master-boot-disk-size 50GB --worker-boot-disk-size 50GB
```
A continuación, ejecutamos el siguiente comando para establecer BUCKET como el bucket que creamos con anterioridad,

```$ BUCKET=gs://<your bucket name> ```

Y ahora, para ejecutar cada uno de los códigos tendríamos que realizar lo siguiente (Nos liamos un poco con los códigos debido a que _Matplotlib_ no podía guardar directamente las gráficas en el bucket):
Los tres primeros al generar gráficas con _Matplotlib_ necesitamos pasarle como parámetro el ID del bucket donde queremos que lo guarde.

Ejecutar color.py:  ```spark-submit <numero workers> <numero ejecutores> $BUCKET/color.py $BUCKET/input <nombre archivo salida> <ID bucket>```

Ejecutar colorMasUsadoHora.py: ```spark-submit <numero workers> <numero ejecutores> $BUCKET/colorMasUsadoHora.py $BUCKET/input $BUCKET/<nombre archivo salida> <ID bucket>```

Ejecutar horasMasActividad.py: ```spark-submit <numero workers> <numero ejecutores> $BUCKET/horasMasActividad.py $BUCKET/input $BUCKET/<nombre archivo salida> <ID bucket>```

Los últimos dos códigos generan un txt que será procesado para mostrar una tabla con los valores.

Ejecutar pixelesMasMovidos.py: ```spark-submit <numero workers> <numero ejecutores> $BUCKET/pixelesMasMovidos.py $BUCKET/input $BUCKET/<nombre archivo salida>```

Ejecutar userMasActivo.py: ```spark-submit  <numero workers> <numero ejecutores> $BUCKET/userMasActivo.py $BUCKET/input $BUCKET/<nombre archivo salida>```

# Comparaciones de tiempos

![Gráficas_tiempos](https://github.com/YeF4n/rPlaceAnalysis/assets/100349938/43e63a15-7eb1-41d5-beab-85e8d4aee1ed)

Los tiempos y speed-ups han sido los siguientes:

[color.py](/scripts/color.py): 

          -Master: 264
  
          -2 W 2 C: 96   -Speedup = 264/96 = 2,75
  
          -2 W 4 C: 96   -Speedup = 264/96 = 2,75
  
          -2 W 8 C: 59   -Speedup = 264/59 = 4,47
  
          -4 W 2 C: 66   -Speedup = 264/66 = 4
  
          -4 W 3 C: 60   -Speedup = 264/60 = 4,4
  
          -4 W 4 C: 60   -Speedup = 264/60 = 4,4

[horasMasActividad.py](scripts/horasMasActividad.py): 

          -Master: 462   
  
          -2 W 2 C: 150   -Speedup = 462/150 = 3,08
  
          -2 W 4 C: 156   -Speedup = 462/156 = 2,96
  
          -2 W 8 C: 84   -Speedup = 462/84 = 5,5
          
          -4 W 2 C: 90   -Speedup = 462/90 = 5,133
          
          -4 W 3 C: 96   -Speedup = 462/96 = 4,81
          
          -4 W 4 C: 96   -Speedup = 462/96 = 4,81
  
[pixelesMasMovidos.py](scripts/pixelesMasMovidos.py): 

          -Master: 342   
          
          -2 W 2 C: 114   -Speedup = 342/114 = 3
          
          -2 W 4 C: 120   -Speedup = 342/120 = 2,85
          
          -2 W 8 C: 66   -Speedup = 342/66 = 5,18
          
          -4 W 2 C: 72   -Speedup = 342/72 = 4,75
          
          -4 W 3 C: 78   -Speedup = 342/78 = 4,38
          
          -4 W 4 C: 78   -Speedup = 342/78 = 4,38

[userMasActivo.py](scripts/userMasActivo.py): 

          -Master: 600 
          
          -2 W 2 C: 144   -Speedup = 600/144 = 4,16
          
          -2 W 4 C: 150   -Speedup = 600/150 = 4
          
          -2 W 8 C: 84   -Speedup = 600/84 = 7,14
          
          -4 W 2 C: 90   -Speedup = 600/90 = 6,67
          
          -4 W 3 C: 90   -Speedup = 600/90 = 6,67
          
          -4 W 4 C: 90   -Speedup = 600/90 = 6,67
          
[colorMasUsadoHora.py](scripts/colorMasUsadoHora.py): 

          -Master: 900  
          
          -2 W 2 C: 252   -Speedup = 900/252 = 3,571
          
          -2 W 4 C: 252   -Speedup = 900/252 = 3,571
          
          -2 W 8 C: 132   -Speedup = 900/132 = 6,82
          
          -4 W 2 C: 144   -Speedup = 900/144 = 6,25
          
          -4 W 3 C: 144   -Speedup = 900/144 = 6,25
          
          -4 W 4 C: 150   -Speedup = 900/150 = 6
