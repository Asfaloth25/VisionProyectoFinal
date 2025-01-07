import numpy as np
import cv2
from picamera2 import Picamera2

def write_video(video_writer, frame):
    """Escribe un frame en el archivo de video."""
    video_writer.write(frame)

def stream_video():
    picam = Picamera2()
    picam.preview_configuration.main.size = (1280, 720)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    # Nombre del archivo de salida para el video
    output_video = 'output_video.avi'

    # Definir el codec y crear el objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Usamos el códec XVID
    video_writer = cv2.VideoWriter(output_video, fourcc, 30.0, (1280, 720))  # 30 FPS, resolución 1280x720

    print("Grabando video... Presiona 'q' para detener.")

    while True:
        # Capturar un fotograma de la cámara
        frame = picam.capture_array()

        # Mostrar el fotograma en una ventana
        cv2.imshow("PiCamera - Video Stream", frame)

        # Escribir el fotograma en el archivo de video
        write_video(video_writer, frame)

        # Si se presiona 'q', se detiene la grabación
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar el objeto VideoWriter y cerrar las ventanas
    video_writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_video()
    print("Video guardado como 'output_video.avi'.")
