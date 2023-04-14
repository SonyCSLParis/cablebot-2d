from time import sleep
from picamera import PiCamera

# Ce programme prend une photo avec la picamera, les enregistre dans le path indique dans le programme.
# Le detail du nom doit etre precise en argv1 de sorte a ce que une nouvelle photo soit cree au lieu de modifier celle d'avant

file_path = '/home/leonard/Documents/Projet indus/récupération_image/photo_picamera' + sys.argv[1] + '.png'
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
sleep(0.5)
camera.capture(file_path)
