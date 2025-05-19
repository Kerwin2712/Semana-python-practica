import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import math

# Configuración
webcam = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.6, maxHands=2)
screen_w, screen_h = pyautogui.size()
click_threshold = 30  # Ajusta según necesidad
smooth_factor = 2   # Para movimientos más suaves

# Variables de control
prev_x, prev_y = 0, 0
is_dragging = False  # Nuevo estado para arrastre

while True:
    ret, video = webcam.read()
    hands, img_manos = detector.findHands(video, flipType=True)
    
    if hands:
        hand = hands[0]
        hand_type = hand["type"]  # 'Left' o 'Right'
        lm_list = hand["lmList"]
        
        # Solo mano derecha
        if hand_type == "Right":
            # Coordenadas del ÍNDICE (punto 8) y PULGAR (punto 4)
            index_x, index_y = lm_list[8][0], lm_list[8][1]  # Corregido
            thumb_x, thumb_y = lm_list[4][0], lm_list[4][1]   # Corregido
            
            # Convertir coordenadas a pantalla (invertir X por el flip)
            scaled_x = int((video.shape[1] - index_x) / video.shape[1] * screen_w)
            scaled_y = int(index_y  / video.shape[0] * screen_h)
            
            # Suavizar movimiento
            scaled_x = prev_x + (scaled_x - prev_x) // smooth_factor
            scaled_y = prev_y + (scaled_y - prev_y) // smooth_factor
            
            pyautogui.moveTo(scaled_x, scaled_y)
            prev_x, prev_y = scaled_x, scaled_y
            
            # Calcular distancia entre dedos
            distance = math.dist((index_x, index_y), (thumb_x, thumb_y))
            
            # Mantener clic presionado
            if distance < click_threshold:
                if not is_dragging:
                    pyautogui.mouseDown()
                    is_dragging = True
            else:
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False

    cv2.imshow('webcam', img_manos)
    if cv2.waitKey(1) != -1:
        break

# Liberar clic al finalizar por si queda activo
if is_dragging:
    pyautogui.mouseUp()
webcam.release()
cv2.destroyAllWindows()