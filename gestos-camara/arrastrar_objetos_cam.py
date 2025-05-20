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
        hand_2 = hands[1] if len(hands) > 1 else None
        if hand and hand_2:
            hand_type = hand["type"] if hand else None # 'Left' o 'Right'
            hand2_type = hand_2["type"] if hand_2 else None
            
            if hand_type == "Left":
                hand_r = hand_2
                hand_l = hand
            else:
                hand_r = hand
                hand_l = hand_2
            
            
            r_list = hand_r["lmList"] 
            l_list = hand_l["lmList"] 
        
            if hand_l:
                # Coordenadas del ÍNDICE (punto 8) y PULGAR (punto 4)
                indexl_x, indexl_y = l_list[8][0], l_list[8][1]
                thumbl_x, thumbl_y = l_list[4][0], l_list[4][1]
                # Convertir coordenadas a pantalla (invertir X por el flip)
                scaledl_x = int((video.shape[1] - indexl_x) / video.shape[1] * screen_w)
                scaledl_y = int(indexl_y  / video.shape[0] * screen_h)
                # Suavizar movimiento
                scaledl_x = prev_x + (scaledl_x - prev_x) // smooth_factor
                scaledl_y = prev_y + (scaledl_y - prev_y) // smooth_factor
                
                distancel = math.dist((indexl_x, indexl_y), (thumbl_x, thumbl_y))
                
                if distancel < click_threshold:
                    # Solo mano derecha
                    if hand_r:
                        # Coordenadas del ÍNDICE (punto 8) y PULGAR (punto 4)
                        indexr_x, indexr_y = r_list[8][0], r_list[8][1]  # Corregido
                        thumbr_x, thumbr_y = r_list[4][0], r_list[4][1]   # Corregido
                        
                        # Convertir coordenadas a pantalla (invertir X por el flip)
                        scaledr_x = int((video.shape[1] - indexr_x) / video.shape[1] * screen_w)
                        scaledr_y = int(indexr_y  / video.shape[0] * screen_h)
                        
                        # Suavizar movimiento
                        scaledr_x = prev_x + (scaledr_x - prev_x) // smooth_factor
                        scaledr_y = prev_y + (scaledr_y - prev_y) // smooth_factor
                        
                        pyautogui.moveTo(scaledr_x, scaledr_y)
                        prev_x, prev_y = scaledr_x, scaledr_y
                        
                        # Calcular distancia entre dedos
                        distancer = math.dist((indexr_x, indexr_y), (thumbr_x, thumbr_y))
                        
                        # Mantener clic presionado
                        if distancer < click_threshold:
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