import cv2
import numpy as np
import time  # Ajout de la bibliothèque time pour le calcul des FPS
import tensorflow as tf

# Charger le modèle Teachable Machine
model = tf.saved_model.load("model.savedmodel/")

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

# Set window properties
window_name = "Webcam Image"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Create a resizable window
cv2.resizeWindow(window_name, 800, 600)  # Set initial window size

# Constantes
SEUIL_TAILLE = 100  # Seuil de taille en pixels pour les formes
ALERT_THRESHOLD = 10000  # Seuil de taille pour l'alerte 'DANGER PROCHE'

# Plages de couleurs HSV pour le bleu, le vert et le rouge
BLUE_BOUNDS = (np.array([90, 50, 50]), np.array([130, 255, 255]))
GREEN_BOUNDS = (np.array([35, 50, 50]), np.array([85, 255, 255]))
RED_BOUNDS1 = (np.array([0, 50, 50], np.uint8), np.array([10, 255, 255], np.uint8))
RED_BOUNDS2 = (np.array([170, 50, 50], np.uint8), np.array([180, 255, 255], np.uint8))

# Initialisation des variables pour le calcul des FPS
prev_time = 0
fps = 0

def detect_and_draw_contours(mask, img, shape_name, color, expected_corners, aspect_ratio_range, alert_threshold=None):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > SEUIL_TAILLE:
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if len(approx) == expected_corners:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)
                if aspect_ratio_range[0] <= aspect_ratio <= aspect_ratio_range[1]:
                    cv2.drawContours(img, [approx], 0, color, 3)
                    cv2.putText(img, shape_name, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, color)
                    if shape_name == 'RED SQUARE' and area >= alert_threshold:
                        cv2.putText(img, 'DANGER PROCHE', (x, y - 25), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

def detect_formes(img, hsv):
    # Détecter les formes pour chaque couleur
    for bounds, color, shape_name, corners, aspect_ratio in (
        (BLUE_BOUNDS, (255, 0, 0), 'BLUE SQUARE', 4, (0.9, 1.1)),
        (GREEN_BOUNDS, (0, 255, 0), 'GREEN TRIANGLE', 3, (0.9, 1.1)),
        (RED_BOUNDS1, (0, 0, 255), 'RED SQUARE', 4, (0.7, 1.1)),
        (RED_BOUNDS2, (0, 0, 255), 'RED SQUARE', 4, (0.7, 1.1))
    ):
        mask = cv2.inRange(hsv, *bounds)
        mask = cv2.GaussianBlur(mask, (7, 7), 0)
        detect_and_draw_contours(mask, img, shape_name, color, corners, aspect_ratio, ALERT_THRESHOLD)

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Inverse the image
    image = cv2.flip(image, 1)

    # Resize the raw image into (224-height,224-width) pixels
    image_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the models input shape.
    image_input = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image_input = (image_input / 127.5) - 1

    # Predicts the model
    prediction = model(image_input)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Choose color based on class
    color = (0, 255, 0)  
    if "Gentil" in class_name:
        color = (255, 0, 0)  
    elif "Ennemi" in class_name:
        color = (0, 0, 255)  

    # Draw prediction on the image
    text = f"{class_name[1:]}"
    cv2.putText(image, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    text = f"{str(np.round(confidence_score * 100))[:-2]}%"
    cv2.putText(image, text, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Convert BGR to HSV for shape detection
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    detect_formes(image, hsv)

    # Calculate FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Display FPS
    cv2.putText(image, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Show the image with prediction and rectangle
    cv2.imshow(window_name, image)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
