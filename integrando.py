#Libraries
import RPi.GPIO as GPIO
import time
import requests


# GPIO Mode (BOARD / BCM).
GPIO.setmode(GPIO.BCM)

# Set GPIO Pins.
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# Set GPIO direction (IN / OUT).
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def distance():
    # Set Trigger to HIGH.
    GPIO.output(GPIO_TRIGGER, True)

    # Set Trigger after 0.01ms to LOW.
    # Emit the echo!
    time.sleep(0.00001)  # 0.01ms
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # Save start_time.
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # Save time of arrival.
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Time difference between start and arrival.
    time_elapsed = stop_time - start_time
    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back.
    distance = (time_elapsed * 34300) / 2

    return distance

def enviar_distancia(tacho_id, distancia):
    ENDPOINT = 'https://reciclo.herokuapp.com/api/levels/'
    ACCESS_TOKEN = 'ce5c8302adb16aa7258a8d6b003dbc9ec3b0e9ea'
    payload = {
        'distance': distancia,
        'trash_can': tacho_id,
    }
    headers = {
        'Authorization': ' '.join(['Token', ACCESS_TOKEN]),
    }
    return requests.post(ENDPOINT, data=payload, headers=headers)


if __name__ == '__main__':
    distancia = distance()
    tacho_id = 2
    response = enviar_distancia(tacho_id, distancia)
    print(response)
