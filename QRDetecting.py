import cv2
from qreader import QReader
import warnings
import datetime

# Подавление предупреждений о двойной декодировке
warnings.filterwarnings("ignore", message=".*double decoding failed.*")

# Путь к видеофайлу
video_path = "video1.mp4"  # Укажите путь к вашему видеофайлу

# Открытие видеофайла
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"[ERROR] Не удалось открыть видеофайл: {video_path}")
    exit()

# Инициализация QR-ридера
qr_reader = QReader()

while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO] Конец видео.")
        break

    # Считывание QR кодов с кадра
    qr_codes = qr_reader.detect_and_decode(frame, return_detections=True)

    if qr_codes:

        for i in range(len(qr_codes[0])):
            # Выводим название из первого tuple 
            qr = qr_codes[0] 

            if qr[i] is None:
                print('[WARNING] QR-code не прочитан')
            else:
                print(f'[DETECTED] QR-code: {qr[i]}')
            
            # Выводим bbox из второго tuple
            qr = qr_codes[1]  
            barcodeData = qr[i]
            print(f"--- bbox: {barcodeData['bbox_xyxy']}")
            # if len(barcodeData) > 0 and not barcodeData[0] is None:
            try:
                # Если QR-код был считан, выводим его
                
                #  Получаем координаты bbox
                x1 = int(barcodeData['bbox_xyxy'][0])
                y1 = int(barcodeData['bbox_xyxy'][1])
                x2 = int(barcodeData['bbox_xyxy'][2])
                y2 = int(barcodeData['bbox_xyxy'][3])
                # Рисуем прямоугольник
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                # Вы можете записывать данные в CSV или выполнять другие действия
                # Например, сохраняем дату и QR код в файл
            except Exception as e:
                print(f"[ERROR] Ошибка при обработке QR кода: {e}")


    frame_resized = cv2.resize(frame, (1000,1000))
    cv2.imshow("QR Code Scanner", frame_resized )
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Завершение работы
cap.release()
cv2.destroyAllWindows()
