import os
import threading
import cv2
import numpy as np
from deepface import DeepFace

os.environ["HOME"] = "./models"

# Capture the video from the webcam.
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cpt = 0
face_match = False
# Charger les images de référence depuis le dossier.
reference_list = []
directory = "./ennemy"
for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        img_path = os.path.join(directory, filename)
        img = cv2.imread(img_path)
        if img is not None:
            reference_list.append(img)

verification_in_progress = False
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def check_face_match(frame):
    global face_match, verification_in_progress
    verification_in_progress = True
    face_match = False
    try:
        for reference_img in reference_list:
            result = DeepFace.verify(frame, reference_img, model_name='VGG-Face', enforce_detection=True)
            if result["verified"]:
                face_match = True
                break
    except Exception as e:
        print("Erreur lors de la vérification :", e)
    finally:
        verification_in_progress = False

def detect_formes(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Red detection
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            area = cv2.contourArea(cnt)
            if area > 1000:
                cv2.drawContours(img, [approx], 0, (255, 0, 0), 3)
                x = approx.ravel()[0]
                y = approx.ravel()[1] - 15
                cv2.putText(img, "RED SQUARE", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255))

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


while True:
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.2, 5)
        detect_formes(frame)  # Appel de la fonction de détection de formes

        if cpt % 30 == 0 and not verification_in_progress:
            threading.Thread(target=check_face_match, args=(frame.copy(),)).start()
        cpt += 1

        if verification_in_progress:
            cv2.putText(frame, "Scanning...", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        elif face_match:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, "Ennemy spotted !!!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Sector clear", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Frame', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
