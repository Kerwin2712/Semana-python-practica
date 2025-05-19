import cv2
from cvzone.HandTrackingModule import HandDetector

webcam = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.6, maxHands=1)  # Ajusta detectionCon si es necesario

while True:
    ret, video = webcam.read()
    hands, img_manos = detector.findHands(video, flipType=True)  # ¡FlipType activado!
    
    # Dibuja las manos detectadas (opcional, ya lo hace findHands)
    if hands:
        print(hands)  # Verifica en la consola
        
    cv2.imshow('webcam', img_manos)  # Muestra la imagen procesada
    if cv2.waitKey(1) != -1:
        break

webcam.release()
cv2.destroyAllWindows()