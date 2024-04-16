
import cv2
import numpy as np

def detect_formes(img):
    # Convertir l'image de l'espace RGB vers HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    
    # Définir la plage de couleur rouge dans HSV
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask= cv2.inRange(hsv, lower_red, upper_red) # detecte un objet qui contient des pixels inclus dans l'interval 
    
    # Optionnel: appliquer un flou pour réduire le bruit
    mask = cv2.GaussianBlur(mask, (7, 7), 0)
    
    # Trouver les contours dans le masque
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
            
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)  #simplifier le countour cnt en reudisant le nombre de points pour obtenir une forme plus simple pour les analyser
        if len(approx) == 4:  # Chercher des quadrilatères
            area = cv2.contourArea(cnt) #calculer l'aire du contour cnt
            if area > 1000:  # Seuil d'aire pour éliminer les petits contours
                cv2.drawContours(img, [approx], 0, (255, 0, 0), 3)
                x = approx.ravel()[0]
                y = approx.ravel()[1] - 15
                cv2.putText(img, "BOMB", (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
                

    # Définir la plage de couleur bleue dans HSV
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    # Optionnel: appliquer un flou pour réduire le bruit
    mask_blue = cv2.GaussianBlur(mask_blue, (7, 7), 0)

    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt_blue in contours_blue:
        approx_blue = cv2.approxPolyDP(cnt_blue, 0.02 * cv2.arcLength(cnt_blue, True), True)
        if len(approx_blue) == 4:  # Chercher des quadrilatères
            area_blue = cv2.contourArea(cnt_blue)
            if area_blue > 1000:  # Seuil d'aire pour éliminer les petits contours
                cv2.drawContours(img, [approx_blue], 0, (255, 0, 0), 3)
                x_blue = approx_blue.ravel()[0]
                y_blue = approx_blue.ravel()[1] - 15
                cv2.putText(img, "BLUE SQUARE", (x_blue, y_blue), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
    
    # Définir la plage de couleur vert dans HSV
    lower_green = np.array([35, 0, 0])
    upper_green = np.array([75, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    # Optionnel: appliquer un flou pour réduire le bruit
    mask_green = cv2.GaussianBlur(mask_green, (7, 7), 0)

    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt_green in contours_green:
        approx_green = cv2.approxPolyDP(cnt_green, 0.02 * cv2.arcLength(cnt_green, True), True)
        if len(approx_green) == 3:  # Chercher des triangles
            area_green = cv2.contourArea(cnt_green)
            if area_green > 1000:  # Seuil d'aire pour éliminer les petits contours
                cv2.drawContours(img, [approx_green], 0, (0, 255, 255), 3)
                x_green = approx_green.ravel()[0]
                y_green = approx_green.ravel()[1] - 15
                cv2.putText(img, "green TRIANGLE", (x_green, y_green), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))


# Initialiser la webcam
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    detect_formes(frame)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()