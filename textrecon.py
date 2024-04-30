from PIL import image
import pytesseract
import cv2

def detect_texte(frame):
	img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	text = pytesseract.image_to_string(img, output_type=Output.DICT) #stockage des informations
	print(text)
	boites = len(d['level'])
	for i in range(NbBox):
		(x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    # display rectangle
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
# Initialiser la webcam
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    detect_texte(frame)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
