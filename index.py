import cv2
from datetime import datetime

#Llamamos al método VideoCapture que recibe como único argumento un número entero, el cuál representa una webcam del PC,
#para usar la webcam default que viene integrada en nuestro equipo pasamos un 0
video = cv2.VideoCapture(0)

#Creamos una lista para guardar el status de cada frame, la inicializamos con dos elementos None para no tener un IndexError al
#comparar los status en la primera iteración del bucle while
status_list: list[int] = [None, None]
#Creamos otra lista para guardar las marcas de tiempo en las que se ha detectado un cambio en el movimiento
times: list[datetime] = []

#Definimos una variable para guardar el primer frame del vídeo y le asignamos el valor de None
first_frame = None

while True:
    
    #Empezamos a capturar el vídeo
    check, frame = video.read()

    #Definimos un status 0, que significa que no hay movimiento
    status: int = 0
    #Convertimos la imagen a escala de grises:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    """
    Aplicamos un desenfoque gaussiano para suavizar los bordes y mejorar la detección, este método recibe
    tres parámetros obligatorios: la imagen que queremos procesar, el kernel; una tupla con dos números impares que determinará
    el tamaño de una matriz (generada automáticamente por opencv) la cual controla que tanto peso tendrá un determinado píxel 
    sobre sus vecinos, y un número entero conocido como desviación x o sigma, el cual define el ancho de la campana de Gauss, 
    a mayor ancho más desenfocada estará la imagen. Si lo dejamos en 0, opencv calculará automáticamente una desviación apropiada
    a partir del kernel
    """
    gray = cv2.GaussianBlur(gray, (21,21), 0)
    
    """
    En la primera iteración, first_Frame será igual a None, por lo que le asignaremos el valor del primer
    frame del vídeo convertido a gris. Sin embargo, como no queremos que se ejecute el código debajo, usaremos
    la palabra reservada continue para saltarlo y pasar a la siguiente iteración del while
    """
    if first_frame is None:
        first_frame = gray
        continue

    #Calculamos la diferencia entre el primer frame y los frames subsecuentes y guardamos el resultado en la variable delta_frame
    delta_frame = cv2.absdiff(first_frame, gray)

    """
    A partir del delta_frame, calcularemos el umbral o treshold utilizando la función homónima de cv2, 
    esta función lo que hará será simplificar la imagen asignando un determinado tono dentro de la escala de grises 
    a cada píxel que se encuentre dentro del umbral definido por nosotros, mientras que si está fuera de ese umbral 
    se le asignará negro.
    
    Recibe cuatro argumentos: la imagen con la que trabajará, el umbral, que en este caso es 30, el color que 
    le asignaremos a los píxeles que se encuentren dentro de dicho umbral, en este caso 255 (blanco), y el algoritmo
    de umbralización, en este caso binario. 

    Devolverá una tupla con dos valores, pero en el caso del TRESH_BINARY sólo nos interesa el segundo, el primero
    lo podemos ignorar.
    """
    tresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    """
    Para suavizar un poco el contorno de las zonas blancas y eliminar los enormes huecos negros usamos el método dilate, 
    este recibe sólo tres argumentos, la imagen sobre la cual se aplicará, un array de kernel, que podemos dejar como None 
    en caso de no necesitarlo, y  el argumento de palabra clave iterations, que define el número de veces que se aplicará 
    el algoritmo, en este caso 2.
    """
    tresh_frame = cv2.dilate(tresh_frame, None, iterations=2)

    """
    Ahora detectaremos los contornos de los objetos en movimiento a partir de la imagen umbralizada, para esto utilizamos
    el método  cv2.findContours, este recibe tres argumentos; la imagen con la que se trabajará (en este caso llamaremos al método
    copy de nuestro objeto treshold frame para no modificar la imagen original), la cual debe ser binaria y tener objetos en blanco 
    con fondo negro, el modo de recuperación, que define cuáles contornos se recuperarán y cómo se relacionan jerárquicamente entre ellos, 
    y la aproximación del contorno, esta controla cómo se almacenarán los contornos, sólo puede tomar dos valores; cv2.CHAIN_APPROX_NONE 
    que guarda todos los puntos, o cv2.CHAIN_APPROX_SIMPLE que elimina los puntos redundantes.

    Este método retorna dos valores: contours, una lista de arrays con todas las coordenadas de los contornos encontrados en cada fila 
    de pixeles, y hierarchy, que determina la relación jeráraquica entre contornos, esta última no es relevante para nuestro caso ya que 
    usaremos un modo de recuperación no-jerarquizado, así que almacenaremos el valor en una variable anónima definida por un guión bajo (_)
    """
    contours, _ = cv2.findContours(tresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #A continuación iteraremos sobre la lista de contornos con un bucle for y dejaremos sólo aquellos cuya área sea mayor o igual a 10000
    for c in contours:

        if cv2.contourArea(contour=c) < 10000:
            continue 
        else:
            #En cuanto encontremos un área mayor a 10000 cambiamos el status a 1, es decir que se ha detectado un objeto en movimiento
            status = 1

            #Usamos el método bounding rect para obtener las coordenadas, ancho y alto del rectángulo mínimo que encierra 
            #completamente nuestro objeto en movimiento, recibe como único parámetro el array de contorno
            x, y, w, h = cv2.boundingRect(c)

            """
            Ahora dibujamos el rectángulo en nuestra imagen con el método cv2.rectangle, le pasamos el frame original a color, 
            una tupla con las coordenadas iniciales del rectángulo (x,y), otra tupla con las coordenadas finales (x+w,y+h), una
            tercera tupla con el color del rectángulo en formato BGR, y un número entero que representa el ancho de la línea del
            rectángulo
            """
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)
        
    #Antes de mostrar los vídeos añadimos a la lista el valor de status para el frame actual
    status_list.append(status)

    #Creamos una marca de tiempo para cada momento en que cambió el status de 0 a 1 y viceversa, y la guardamos en la nueva lista
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
    elif status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())

    #mostramos la imagen en gris
    cv2.imshow("Gray frame", gray)
    #mostramos la diferencia ente ambos
    cv2.imshow("Delta frame", delta_frame)
    #mostramos la imagen umbralizada
    cv2.imshow("Treshold frame", tresh_frame)
    #mostramos el frame original a color son sus respectivos rectángulos
    cv2.imshow("Color frame", frame)
    
    #Se mostrará un frame por milisegundo
    key = cv2.waitKey(1)

    #Especificamos una tecla para detener el bucle:
    if key == ord("q"):
        #Verificamos si el último status fue 1, en cuyo caso su timestamp del final será el momento en el que terminó la grabación
        if status == 1:
            times.append(datetime.now())
        break
    

#imprimimos la lista al finalizar la captura de vídeo
print(status_list)
print(times)

#Cuando hayamos terminado de grabar llamamos al método release de nuestro objeto video y destruimos las ventanas
video.release()
cv2.destroyAllWindows()