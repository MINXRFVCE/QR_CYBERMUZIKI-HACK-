import cv2
from qreader import QReader
import warnings
import datetime

def bbox_show(frame, point1 : tuple[int, int] , point2: tuple[int, int], name: str | None, is_valid: bool) -> None:
    '''
    Отрисовка QR-code
    '''
    text = ('None' if name is None else name)
    point_text = (point1[0], point1[1] - 10)
    color = (0, 0, 255)
    if is_valid: 
        color = (0, 255, 0)
    #Отрисовка текста
    cv2.putText(img=frame, 
                text=text, 
                point=point_text,
                font=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=0.5, 
                color=color, 
                thickness=2)
    #Отрисовка прямоугольника
    cv2.rectangle(frame, point1, point2, color, 2)


def realtime_scanning(video_path: str, valid_text: list, filter_warnings: bool=True) -> None:
    # Подавление предупреждений о двойной декодировке
    if filter_warnings: 
        warnings.filterwarnings("ignore", message=".*double decoding failed.*")

    # Открытие видеофайла
    cap = cv2.VideoCapture(video_path)

    # Проверка открытия файла
    if not cap.isOpened():
        print(f"[ERROR] Не удалось открыть видеофайл: {video_path}")
        exit()

    #
    qr_reader = QReader()

    while True:

        ret, frame = cap.read() # Чтение кадра видео
        
        # Проверка на конец видео
        if not ret:
            print("[INFO] Конец видео.")
            break

        qr_codes = qr_reader.detect_and_decode(frame, return_detections=True)

        if qr_codes:

            for i in range(len(qr_codes[0])):

                # Выводим название из первого tuple 
                # qr = qr_codes[0] 
                name = qr_codes[0][i]

                # Если QR-код был считан, выводим его
                if name is None:
                    print('[WARNING] QR-code не прочитан')
                else:
                    print(f'[DETECTED] QR-code: {name}')
                
                # Выводим bbox из второго tuple 
                barcodeData = qr_codes[1][i]

                print(f"--- bbox: {barcodeData['bbox_xyxy']}")

                # if len(barcodeData) > 0 and not barcodeData[0] is None:

                try:
                    #  Получаем координаты bbox
                    x1 = int(barcodeData['bbox_xyxy'][0])
                    y1 = int(barcodeData['bbox_xyxy'][1])
                    x2 = int(barcodeData['bbox_xyxy'][2])
                    y2 = int(barcodeData['bbox_xyxy'][3])

                    # Рисуем прямоугольник
                    #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    bbox_show(frame, (x1,y1), (x2,y2), name, name in valid_text)

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


def scanning(video_path: str, valid_text: list, output_path: str, filter_warnings: bool=True):
    # Подавление предупреждений о двойной декодировке
    if filter_warnings: 
        warnings.filterwarnings("ignore", message=".*double decoding failed.*")

    # Открытие видеофайла
    cap = cv2.VideoCapture(video_path)

    # Проверка открытия файла
    if not cap.isOpened():
        print(f"[ERROR] Не удалось открыть видеофайл: {video_path}")
        exit()

    #
    qr_reader = QReader()

    #
    
    new_video = cv2.VideoWriter(output_path, -1, 1, (1920, 1080))
    
    while True:

        ret, frame = cap.read() # Чтение кадра видео
        
        # Проверка на конец видео
        if not ret:
            print("[INFO] Конец видео.")
            break

        qr_codes = qr_reader.detect_and_decode(frame, return_detections=True)

        if qr_codes:

            for i in range(len(qr_codes[0])):

                # Выводим название из первого tuple 
                # qr = qr_codes[0] 
                name = qr_codes[0][i]

                # Если QR-код был считан, выводим его
                if name is None:
                    print('[WARNING] QR-code не прочитан')
                else:
                    print(f'[DETECTED] QR-code: {name}')
                
                # Выводим bbox из второго tuple 
                barcodeData = qr_codes[1][i]

                print(f"--- bbox: {barcodeData['bbox_xyxy']}")

                # if len(barcodeData) > 0 and not barcodeData[0] is None:

                try:
                    #  Получаем координаты bbox
                    x1 = int(barcodeData['bbox_xyxy'][0])
                    y1 = int(barcodeData['bbox_xyxy'][1])
                    x2 = int(barcodeData['bbox_xyxy'][2])
                    y2 = int(barcodeData['bbox_xyxy'][3])

                    # Рисуем прямоугольник
                    #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    bbox_show(frame, (x1,y1), (x2,y2), name, name in valid_text)

                except Exception as e:
                    print(f"[ERROR] Ошибка при обработке QR кода: {e}")

        new_video.write(frame)
        
    cap.release()
    new_video.release()

valid_text = 'БЭК'

# Путь к видеофайлу
video_path = "video1.mp4"  # Укажите путь к вашему видеофайлу


