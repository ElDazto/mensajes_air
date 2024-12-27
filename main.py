import cv2
import numpy as np
import pyautogui
import time
import logging
from PIL import ImageGrab

# Imágenes de referencia
SERVER_NOTIFICATION_ICON = "Image/notificacion.png"
CHANNEL_MENTION_ICON = "Image/mencion_nueva.png"
MESSAGE_BOX_ICON = "Image/notificacion.png"

# Coordenadas de áreas de escaneo (x1, y1, x2, y2)
SERVER_ICON_AREA = (35, 1107, 71, 1802)  # Ajustar según el área de icono de servidor
MENTION_TEXT_AREA = (73, 1643, 311, 1818)  # Ajustar según el área de mención en canal
MENTION_TEXT_AREA_2 = (73, 1007, 311, 1070)  # Ajustar según el área de mención en canal
CHANNEL_ICON_AREA = (271, 1008, 310, 1817)  # Ajustar según el área de icono en el canal

# Coordenadas del area de mensajes
CUADRO_DE_TEXTO = (539, 1827)

# Mensaje generico
MENSAJE = ["Yo", False]

# Configuración del logging
logging.basicConfig(
    filename="detector_notificaciones.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def detect_and_click(image_path, scan_area):
    """ Detecta la imagen en un área de la pantalla y hace clic si encuentra una coincidencia. """
    # Captura la región de la pantalla especificada y convierte a escala de grises
    screenshot = np.array(ImageGrab.grab(bbox=scan_area))
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Cargar la imagen de referencia, eliminar canal alfa y convertirla a escala de grises
    template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if template.shape[2] == 4:  # Si tiene canal alfa
        template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    h_template, w_template = template_gray.shape

    # Verifica que el área de escaneo sea más grande que la plantilla
    if screenshot_gray.shape[0] < h_template or screenshot_gray.shape[1] < w_template:
        print(f"El área de escaneo es más pequeña que la plantilla para {image_path}")
        return False

    # Realizar la coincidencia de plantillas en escala de grises
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9  # Ajusta el umbral según la precisión deseada
    locations = np.where(result >= threshold)

    # Si encuentra una coincidencia, hace clic en el centro del área coincidente
    for pt in zip(*locations[::-1]):
        click_x = scan_area[0] + pt[0] + w_template // 2
        click_y = scan_area[1] + pt[1] + h_template // 2
        pyautogui.click(click_x, click_y)
        return True  # Detener después del primer clic
    return False

def detect_and_click2(image_path, scan_area):
    """ Detecta la imagen en un área de la pantalla y hace clic si encuentra una coincidencia. """
    # Captura la región de la pantalla especificada
    screenshot = np.array(ImageGrab.grab(bbox=scan_area))
    h_screenshot, w_screenshot, _ = screenshot.shape

    # Cargar la imagen de referencia (en color)
    template = cv2.imread(image_path)
    h_template, w_template, _ = template.shape

    # Verifica que el área de escaneo sea más grande que la plantilla
    if h_screenshot < h_template or w_screenshot < w_template:
        print(f"El área de escaneo es más pequeña que la plantilla para {image_path}")
        return False

    # Realizar la coincidencia de plantillas en color
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.45  # Ajusta el umbral según la precisión deseada
    locations = np.where(result >= threshold)

    # Si encuentra una coincidencia, hace clic en el centro del área coincidente
    for pt in zip(*locations[::-1]):
        click_x = scan_area[0] + pt[0] + w_template // 2
        click_y = scan_area[1] + pt[1] + h_template // 2
        pyautogui.click(click_x, click_y)
        return True  # Detener después del primer clic
    return False

def detect_and_click3(image_path, scan_area):
    """ Detecta la imagen en un área de la pantalla y hace clic si encuentra una coincidencia. """
    # Captura la región de la pantalla especificada y convierte a escala de grises
    screenshot = np.array(ImageGrab.grab(bbox=scan_area))
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Cargar la imagen de referencia, eliminar canal alfa y convertirla a escala de grises
    template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if template.shape[2] == 4:  # Si tiene canal alfa
        template = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    h_template, w_template = template_gray.shape

    # Verifica que el área de escaneo sea más grande que la plantilla
    if screenshot_gray.shape[0] < h_template or screenshot_gray.shape[1] < w_template:
        print(f"El área de escaneo es más pequeña que la plantilla para {image_path}")
        return False

    # Realizar la coincidencia de plantillas en escala de grises
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6  # Ajusta el umbral según la precisión deseada
    locations = np.where(result >= threshold)

    # Si encuentra una coincidencia, hace clic en el centro del área coincidente
    for pt in zip(*locations[::-1]):
        click_x = scan_area[0] + pt[0] + w_template // 2 - 100  # Ajuste hacia la izquierda
        click_y = scan_area[1] + pt[1] + h_template // 2
        pyautogui.click(click_x, click_y)
        return True  # Detener después del primer clic
    return False

def enviar_mensaje(mensaje, bool):
    time.sleep(0.5)
    pyautogui.write(mensaje)
    if(bool):
        pyautogui.press("enter")
    print("Mensaje escrito.")

def scroll_down(y_pos, pixels):
    pyautogui.moveTo(CUADRO_DE_TEXTO[0], y_pos - pixels)
    pyautogui.scroll(-(pixels * 4))

while True:
    try:
        # Paso 1: Detecta y haz clic en el icono de notificación del servidor o en la mención en canal
        if detect_and_click(SERVER_NOTIFICATION_ICON, SERVER_ICON_AREA):
            logging.info("Icono de notificación del servidor detectado y clic realizado.")
            time.sleep(1)  # Pausa para cargar la siguiente pantalla

            if detect_and_click2(CHANNEL_MENTION_ICON, MENTION_TEXT_AREA):
                logging.info("Mención en canal detectada y clic realizado en área principal.")
                time.sleep(0.7)

                if detect_and_click3(MESSAGE_BOX_ICON, CHANNEL_ICON_AREA):
                    logging.info("Caja de texto encontrada, realizando acciones.")
                    time.sleep(0.2)
                    scroll_down(CUADRO_DE_TEXTO[1], 200)
                    pyautogui.click(CUADRO_DE_TEXTO)
                    enviar_mensaje(MENSAJE[0], MENSAJE[1])

            elif detect_and_click2(CHANNEL_MENTION_ICON, MENTION_TEXT_AREA_2):
                logging.info("Mención en canal detectada y clic realizado en área secundaria.")
                time.sleep(0.7)

                if detect_and_click3(MESSAGE_BOX_ICON, CHANNEL_ICON_AREA):
                    logging.info("Caja de texto encontrada en segunda mención, realizando acciones.")
                    time.sleep(0.2)
                    scroll_down(CUADRO_DE_TEXTO[1], 200)
                    pyautogui.click(CUADRO_DE_TEXTO)
                    enviar_mensaje(MENSAJE[0], MENSAJE[1])

            elif detect_and_click3(MESSAGE_BOX_ICON, CHANNEL_ICON_AREA):
                logging.info("Caja de texto detectada directamente, realizando acciones.")
                time.sleep(0.2)
                scroll_down(CUADRO_DE_TEXTO[1], 200)
                pyautogui.click(CUADRO_DE_TEXTO)
                enviar_mensaje(MENSAJE[0], MENSAJE[1])

        # Si no detecta nada, espera un poco antes de revisar nuevamente
        time.sleep(1)

    except Exception as e:
        logging.error(f"Error en el bucle principal: {e}")
