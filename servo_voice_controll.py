import aiy.audio
import aiy.cloudspeech
import aiy.voicehat

import aiy.i18n
import sys
import time
import RPi.GPIO as GPIO

OFFSE_DUTY = 0.5
SERVO_MIN_DUTY = 2.5 + OFFSE_DUTY
SERVO_MAX_DUTY = 12.5 + OFFSE_DUTY
servoPin = 24 #same as GPIO 24
LED_PIN = 5

def map(value,fromLow,fromHigh,toLow,toHigh):
	return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

def setup():
	global p
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(servoPin,GPIO.OUT)
	GPIO.output(servoPin,GPIO.LOW)

	p = GPIO.PWM(servoPin,50)
	p.start(0)

	aiy.i18n.set_language_code("es-ES")
	GPIO.setup(LED_PIN,GPIO.OUT)
	global current

def servoWrite(angle):
	if angle < 0:
		angle = 0
	elif angle > 180:
		angle = 180

	p.ChangeDutyCycle(map(angle,0,180,SERVO_MIN_DUTY,SERVO_MAX_DUTY))

def destroy():
	p.stop()
	GPIO.cleanup()


def servo_min():
	servoWrite(0)
	current = 0
	time.sleep(0.3)


def servo_max():
	servoWrite(180)
	current = 180
	time.sleep(0.3)

def servo_mid():
	servoWrite(90)
	current = 90
	time.sleep(0.3)

def saludar():
	for i in range(5):
		for dc in range(0, 181, 1):   #make servo rotate from 0 to 180 deg
			servoWrite(dc)     # Write to servo
			time.sleep(0.001)
		time.sleep(0.5)
		for dc in range(180, -1, -1): #make servo rotate from 180 to 0 deg
			servoWrite(dc)
			time.sleep(0.001)
		time.sleep(0.5)
     

def main():
	
	setup()
	

	recognizer = aiy.cloudspeech.get_recognizer()
	recognizer.expect_phrase("max")
	recognizer.expect_phrase("maximo")
	recognizer.expect_phrase("min")
	recognizer.expect_phrase("minimo")
	recognizer.expect_phrase("centro")
	recognizer.expect_phrase("en medio")
	recognizer.expect_phrase("saludar")
	recognizer.expect_phrase("saluda")
	

	button = aiy.voicehat.get_button()
	aiy.audio.get_recorder().start()

	

	while True:
		print("Presiona el boton y habla")
		button.wait_for_press()
		print("Escuchando")

		text = recognizer.recognize()

		if text is None:
			print("Lo siento, no puedo escucharte")
		else:
			text = text.lower()
			
			print("Dijiste ",text)

			
			

			if "max" in text:
				GPIO.output(LED_PIN,GPIO.HIGH)
				aiy.audio.say("Moviendo al maximo")
				servo_max()
			elif "min" in text:
				GPIO.output(LED_PIN,GPIO.HIGH)
				aiy.audio.say("Moviendo al minimo")
				servo_min()
			elif "centro" in text or "medio" in text:
				GPIO.output(LED_PIN,GPIO.HIGH)
				aiy.audio.say("Moviendo al centro")
				servo_mid()
			elif "tu nombre" in text:
				GPIO.output(LED_PIN,GPIO.HIGH)
				aiy.audio.say("Kendra Guadalupe")
				GPIO.output(LED_PIN,GPIO.LOW)
			elif "saludar" in text:
				GPIO.output(LED_PIN,GPIO.HIGH)
				aiy.audio.say("saludando")
				saludar()
				GPIO.output(LED_PIN,GPIO.LOW)
			elif "salir" in text:
				GPIO.output(LED_PIN,GPIO.HIGH)
				aiy.audio.say("Adios!")
				GPIO.output(LED_PIN,GPIO.LOW)
				destroy()
				sys.exit(0)

			GPIO.output(LED_PIN,GPIO.LOW)

if __name__ == "__main__":
	main()
