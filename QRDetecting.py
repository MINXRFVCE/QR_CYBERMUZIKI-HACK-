import cv2
from qreader import QReader
import warnings
import datetime
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from tkinter.filedialog import asksaveasfilename


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
    frame = cv2.putText(img=frame, 
                text=text, 
                org=point_text,
                fontFace=cv2.FONT_HERSHEY_COMPLEX, 
                fontScale=1, 
                color=color, 
                thickness=3)
    #Отрисовка прямоугольника
    frame = cv2.rectangle(frame, point1, point2, color, 2)


def realtime_scanning(video_path: str, valid_text: list, skip_frame: int, PredProc: int, filter_warnings: bool=True) -> set:
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
    
    #executor = ThreadPoolExecutor(max_workers=8)

    # Функция для обработки QR-кодов
    #def process_frame(frame):
        #return qr_reader.detect_and_decode(frame, return_detections=True)
    SearchQRcode = set()
    dic = {}
    frame_count = 0
    while True:
        frame_count += 1
        ret, frame = cap.read()
        
           
        # Проверка на конец видео
        if not ret:
            print("[INFO] Конец видео.")
            break
        if PredProc == 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #frame = cv2.GaussianBlur(frame, (9,9), 0)
            #frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            #brightness = 10 
            # Adjusts the contrast by scaling the pixel values by 2.3 
            #contrast = 2.3  
            #frame = cv2.addWeighted(frame, contrast, np.zeros(frame.shape, frame.dtype), 0, brightness) 
            #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
            #frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel, iterations=2)
            # frame = cv2.medianBlur(frame, 1)
            #brightness = -100
            #contrast = 1
            #frame = cv2.addWeighted(frame, contrast, np.zeros(frame.shape, frame.dtype), 0, brightness)
            #_, frame = cv2.threshold(frame, 0, 0, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        qr_codes=False

        #future = executor.submit(process_frame, frame)
        #qr_codes = future.result()
        if frame_count % skip_frame == 0:  # Обрабатываем только каждый второй кадр
            qr_codes = qr_reader.detect_and_decode(frame, return_detections=True)            
            for key in list(dic.keys()):
                if not key in valid_text:
                    del dic[key]
            #dic.clear()
            #array.clear()
        else:
            for key, value in dic.items():
                bbox_show(frame, (value[0], value[1]), (value[2], value[3]), key, value[4])
        
        #qr_codes = qr_reader.detect_and_decode(frame, return_detections=True)
            
        #qr_codes = qr_reader.detect_and_decode(frame)
        #qr_codes = False

        if qr_codes:
            for i in range(len(qr_codes[0])):
                # Выводим название из первого tuple 
                # qr = qr_codes[0] 
                name = qr_codes[0][i]

                # Если QR-код был считан, выводим его

                if name is None:
                    print('[WARNING] QR-code не прочитан')
                    continue
                else:
                    print(f'[DETECTED] QR-code: {name}') 
                    SearchQRcode.add(name)             
                # Выводим bbox из второго tuple 
                barcodeData = qr_codes[1][i]

                #print(f"--- bbox: {barcodeData['bbox_xyxy']}")

                # if len(barcodeData) > 0 and not barcodeData[0] is None:

                try:
                    #  Получаем координаты bbox
                    x1 = int(barcodeData['bbox_xyxy'][0])
                    y1 = int(barcodeData['bbox_xyxy'][1])
                    x2 = int(barcodeData['bbox_xyxy'][2])
                    y2 = int(barcodeData['bbox_xyxy'][3])
                    dic[name] = [x1,y1,x2,y2, name in valid_text]
                    # Рисуем прямоугольник
                    #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    bbox_show(frame, (x1,y1), (x2,y2), name, name in valid_text)

                except Exception as e:
                    print(f"[ERROR] Ошибка при обработке QR кода: {e}")
    
        print(frame_count)
        frame_resized = cv2.resize(frame, (640, 480))
        cv2.imshow("QR Code Scanner", frame_resized)
        # cv2.imshow("QR Code Scanner", frame )
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    # Завершение работы
    cap.release()
    cv2.destroyAllWindows()
    return SearchQRcode
    


def scanning(video_path: str, valid_text: list, output_path: str, skip_frame:int, PredProc: int, filter_warnings: bool=True) -> set:
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
    
    file_path = asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    new_video = cv2.VideoWriter(file_path, fourcc=cv2.VideoWriter.fourcc(*'mp4v'), fps=30, frameSize=(1920, 1080))
    SearchQRcode = set()
    lastQR = {}
    frame_count=0
    while True:
        frame_count += 1
        ret, frame = cap.read() # Чтение кадра видео
        

        # Проверка на конец видео
        if not ret:
            print("[INFO] Конец видео.")
            break
        if PredProc == 1:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        qr_codes=False
        if frame_count % skip_frame == 0:  # Обрабатываем только каждый второй кадр
            qr_codes = qr_reader.detect_and_decode(frame, return_detections=True)
            for key in list(lastQR.keys()):
                if not key in valid_text:
                    del lastQR[key]
        else:
            for key, value in lastQR.items():
                
                bbox_show(frame, (value[0], value[1]), (value[2], value[3]), key, value[4])

        #qr_codes = qr_reader.detect_and_decode(frame, return_detections=True)

        if qr_codes:

            for i in range(len(qr_codes[0])):

                # Выводим название из первого tuple 
                # qr = qr_codes[0] 
                name = qr_codes[0][i]

                # Если QR-код был считан, выводим его
                if name is None:
                    print('[WARNING] QR-code не прочитан')
                    continue
                else:
                    print(f'[DETECTED] QR-code: {name}')
                    SearchQRcode.add(name)    
                
                # Выводим bbox из второго tuple 
                barcodeData = qr_codes[1][i]

                # print(f"--- bbox: {barcodeData['bbox_xyxy']}")

                # if len(barcodeData) > 0 and not barcodeData[0] is None:

                try:
                    #  Получаем координаты bbox
                    x1 = int(barcodeData['bbox_xyxy'][0])
                    y1 = int(barcodeData['bbox_xyxy'][1])
                    x2 = int(barcodeData['bbox_xyxy'][2])
                    y2 = int(barcodeData['bbox_xyxy'][3])

                    lastQR[name] = [x1,y1,x2,y2, name in valid_text]
                    # Рисуем прямоугольник
                    #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    bbox_show(frame, (x1,y1), (x2,y2), name, name in valid_text)

                except Exception as e:
                    print(f"[ERROR] Ошибка при обработке QR кода: {e}")
        
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        print(frame_count)
        new_video.write(frame)
    cap.release()
    new_video.release()
    return SearchQRcode


