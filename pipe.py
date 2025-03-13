import cv2
import mediapipe as mp 

# Instalasi MediaPipe Hand
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

#mengenali gerakan tangan(mengambil posisi ujung jari)
def mengenali_tangan(hand_landmarks):
    ujung_jempol = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    ujung_telunjuk = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    ujung_jaritengah = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ujung_jarimanis = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ujung_kelingking = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

# poee jika diangkat
    if (ujung_jempol.y < ujung_telunjuk.y and
        ujung_jempol.y < ujung_jaritengah.y and
        ujung_jempol.y < ujung_jarimanis.y and
        ujung_jempol.y < ujung_kelingking.y and
        ujung_telunjuk.y > ujung_jempol.y and
        ujung_jaritengah.y > ujung_jempol.y and
        ujung_jarimanis.y > ujung_jempol.y and
        ujung_kelingking.y > ujung_jempol.y):
        return "Thumbs Up"

    if (ujung_telunjuk.y < ujung_jempol.y and
        ujung_telunjuk.y < ujung_jaritengah.y and
        ujung_telunjuk.y < ujung_jarimanis.y and
        ujung_telunjuk.y < ujung_kelingking.y):
        return "one"


    if (ujung_telunjuk.y < ujung_jempol.y and
        ujung_jaritengah.y < ujung_jempol.y and
        ujung_jarimanis.y > ujung_telunjuk.y and
        ujung_kelingking.y > ujung_telunjuk.y):
        return "Peace Sign"


    if (ujung_jempol.y < ujung_telunjuk.y and
        ujung_telunjuk.y < ujung_jaritengah.y and
        ujung_jaritengah.y < ujung_jarimanis.y and
        ujung_jarimanis.y < ujung_kelingking.y and
        ujung_jempol.y >  ujung_kelingking.y):
        return "Stop"


    if (ujung_jempol.y > ujung_telunjuk.y and
        ujung_telunjuk.y > ujung_jaritengah.y and
        ujung_jaritengah.y > ujung_jarimanis.y and
        ujung_jarimanis.y > ujung_kelingking.y):
        return "kepalan"

    if (abs(ujung_jempol.x - ujung_telunjuk.x) < 0.05 and 
        abs(ujung_jempol.y - ujung_telunjuk.y) < 0.05 and  
        ujung_jaritengah.y < ujung_jempol.y and  
        ujung_jarimanis.y < ujung_jempol.y and  
        ujung_kelingking.y < ujung_jempol.y):
        return "OK Sign"

    if (ujung_jempol.y < ujung_telunjuk.y and
        ujung_kelingking.y < ujung_telunjuk.y and
        ujung_telunjuk.y > ujung_jempol.y and
        ujung_jaritengah.y > ujung_jempol.y and
        ujung_jarimanis.y > ujung_jempol.y):
        return "Call Me"

    if (ujung_telunjuk.y < ujung_jempol.y and
        ujung_jaritengah.y > ujung_telunjuk.y and
        ujung_jarimanis.y > ujung_telunjuk.y and
        ujung_kelingking.y > ujung_telunjuk.y):
        return "Pointing"

    return 'Gesture tidak dikenali'

# Fungsi untuk mendeteksi tangan
def detect_hand(image, hands): 
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
    results = hands.process(image_rgb) 

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:  
#mendeteksi gesture
            gesture = mengenali_tangan(hand_landmarks)
# Menggambar landmark tangan
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
#memuat tulisan
            cv2.putText(image, gesture,(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,140,0),2,cv2.LINE_AA)
    
    return image

# Membuka kamera
foto = cv2.VideoCapture(0)

if not foto.isOpened():
    print('Tidak dapat membuka kamera')
    exit()

while foto.isOpened():
    ret, frame = foto.read()
    if not ret:
        print('kamera gagal dimuat')
        break

    frame = detect_hand(frame, hands)

    cv2.imshow('pose tangan memakai MediaPipe dan OpenCV', frame)

    # Menutup kamera jika tekan 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

foto.release()
cv2.destroyAllWindows()