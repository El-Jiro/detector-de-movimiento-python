import cv2

video = cv2.VideoCapture(0)

#Definimos una variable para guardar el primer frame del vídeo y le asignamos el valor de None
first_frame = None

while True:
    
    check, frame = video.read()
        
    #Convertimos la imagen a escala de grises:
    gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    """
    Aplicamos un desenfoque gaussiano para suavizar los bordes y mejorar la detección, este método recibe
    tres parámetros obligatorios: la imagen que queremos procesar, el kernel, una tupla con dos números impares que determinará
    el tamaño de una matriz generada automáticamente por opencv, la cual que tanto peso tendrá un determinado píxel 
    sobre sus vecinos, y un número entero conocido como desviación x o sigma, el cual define el ancho de la camapana de Gauss, 
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
    

    #mostramos la imagen en gris
    cv2.imshow("Gray frame", gray)
    #mostramos la diferencia ente ambos
    
    
    #Se mostrará un frame por milisegundo
    key = cv2.waitKey(1)

    #Ponemos una tecla especifica para detener el bucle:
    if key == ord("q"):
        break

    
#Cuando hayamos terminado de grabar llamamos al método release de nuestro objeto video y destruimos las ventanas
video.release()
cv2.destroyAllWindows()