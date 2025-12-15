import cv2

video = cv2.VideoCapture(0)

while True:
    
    check, frame = video.read()
    
    #Convertimos la imagen a escala de grises:
    gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #mostramos la imagen en gris
    cv2.imshow("Capturing", gray)
    #Reemplazamos el 0 por, no sé, 500 milisegundos y guardamos el evento en el objeto key
    key = cv2.waitKey(1)

    #Ponemos una tecla especifica para detener el bucle:
    if key == ord("q"):
        break

    
#Cuando hayamos terminado de grabar llamamos al método release de nuestro objeto video y destruimos las ventanas
video.release()
cv2.destroyAllWindows()