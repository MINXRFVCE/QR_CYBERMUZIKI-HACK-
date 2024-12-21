# QR_CYBERMUZIKI-HACK-
Hakatone 2024 Task: Detecting QR-Codes On Video (AI)

# Техническое задание: Определение нужного QR-кода

## Цель
Разработать систему для распознавания нужного QR-кода среди различных QR-кодов на видео, валидации остальных и сохранения их в файл.

## Шаги выполнения

### 1. Сбор данных
- У нас будет видео с QR-кодами. Среди них необходимо найти нужный QR-код, который был заранее определен.
- Все остальные QR-коды будут валидироваться и сохраняться в файл.

### 2. Выбор инструментов
- Использовать qreader для поиска QR-кодов на изображении.
- Использовать OpenCV для отображения видео в реальном времени, разбивания его на кадры и отображения границ QR-кодов с помощью прямоугольников.

### 3. Предобработка изображения
- Разбить видео на фреймы.
- Применить методы предобработки изображений, такие как преобразование в оттенки серого и фильтрация шума для улучшения качества распознавания.

### 4. Распознавание QR-кодов
- Использовать qreader для распознавания QR-кодов на кадрах.
- Определить местоположение каждого QR-кода на изображении.
- Отобразить границы найденных QR-кодов с помощью прямоугольников в OpenCV.

### 5. Сравнение данных
- Сравнить извлеченные данные с заранее определенным содержимым "нужного" QR-кода.
- Если данные совпадают, отметить этот код как нужный.

### 6. Вывод результата
- Вывести информацию о найденном QR-коде, например, его содержимое и позицию на изображении.
- Все остальные QR-коды будут валидироваться и сохраняться в файл.
- Если нужный QR-код не найден, вывести сообщение об этом.

## Видео презентация проекта

- видео готовое

## Почему выбрали QReader и python, а не другие библиотеки и среду

прикрепить https://github.com/Eric-Canas/QReader?ysclid=m4xlaifikw917679933 отсюда гифку почему qreader эффективнее чем OPENcv и PyzBar

## Benchmark

### Rotation Test
<div>
  <img alt="Rotation Test" title="Rotation Test" src="https://raw.githubusercontent.com/Eric-Canas/QReader/main/documentation/benchmark/rotation_benchmark.gif" width="40%">
</div>

<div style="clear: both;">
<div align="center">
  
| Method  | Max Rotation Degrees  |
|---------|-----------------------|
| Pyzbar  | 17º                   |
| OpenCV  | 46º                   |
| QReader | 79º                   |

  </div>
</div>

## Сравнительный анализ использовать необратанное видео или обработанное видео.

 - написать код для предобработки видео








