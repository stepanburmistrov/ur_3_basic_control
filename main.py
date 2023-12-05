import cv2
import numpy as np
import time
from robot_control import *  # Импорт функций управления роботом из другого модуля
import keyboard  # Библиотека для отслеживания нажатий клавиш
import threading  # Модуль для работы с потоками
import os  # Модуль для работы с операционной системой

# Функция, определяющая задачи для робота
def robot_task():
    # Перемещение робота в рабочую позицию
    move_robot(*robot_positions['work_position'])
    # Возвращение робота в исходное положение
    move_robot(*robot_positions['home_position'])
    # Повторное перемещение робота в рабочую позицию
    move_robot(*robot_positions['work_position'])
    # Вычисление и перемещение робота в новую координату
    x, y = get_robot_cords((175, 175))
    move_robot(x, y, -0.10, 90)
    # Возврат робота в рабочую и затем в исходную позицию
    move_robot(*robot_positions['work_position'])
    move_robot(*robot_positions['home_position'])
    os._exit(0)  # Завершение процесса

# Функция для проверки нажатия клавиши остановки
def check_for_stop_key():
    while True:
        # Проверка, нажата ли клавиша Shift для остановки робота
        if keyboard.is_pressed('shift'):
            robot.stop()  # Остановка робота
            os._exit(0)  # Завершение процесса
            break
        time.sleep(0.01)  # Небольшая задержка для снижения нагрузки на CPU

# Создание потоков для управления роботом и обработки нажатия клавиш
robot_thread = threading.Thread(target=robot_task)
key_thread = threading.Thread(target=check_for_stop_key)

# Запуск потоков
robot_thread.start()
key_thread.start()

# Ожидание завершения работы потоков
robot_thread.join()
key_thread.join()
