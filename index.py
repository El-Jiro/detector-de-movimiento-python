"""
Además de procesar imágenes, opencv también nos permite procesar vídeos, ya sea tomados directamente de nuestra webcam
o usando archivos de vídeo guardados en la computadora. Para esto utilizaremos el método videoCapture, el cual recibe como parámetros
un número entero que va desde 0 a n-1, siendo n la cantidad de cámaras conectadas a nuestro equipo (por ejemplo, si sólo tenemos una 
laptop con webcam integrada le pasaremos un 0), o la ruta de un archivo de vídeo en forma de string, como en este caso queremos usar
la cámara default le pasamos un 0.
"""

import cv2, time

video = cv2.VideoCapture(0)

"""
Para comprobar que el script de verdad está grabando, simplemente llamamos al método read de nuestro objeto video, este no recibe ningún argumento
y devuelve dos valores: Un booleano que nos indica si se ha efectuado la grabación y un array numpy 3D con todos los frames del vídeo
"""

a = 0
#Para mostrar el vídeo completo en vez de sólo el primer frame, metemos el código dentro de un bucle while:


while True:
    a+=1
    check, frame = video.read()
    print(check)
    print(frame)

    #Convertimos la imagen a escala de grises:
    gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #mostramos la imagen en gris
    cv2.imshow("Capturing", gray)
    #Reemplazamos el 0 por, no sé, 500 milisegundos y guardamos el evento en el objeto key
    key = cv2.waitKey(1)

    #Ponemos una tecla especifica para detener el bucle:
    if key == ord("q"):
        break

#Esto nos dará el número total de frames en el vídeo
print(a)
    
#Cuando hayamos terminado de grabar llamamos al método release de nuestro objeto video y destruimos las ventanas
video.release()
cv2.destroyAllWindows()