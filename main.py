import os
from encrypt_code.image_engine import encrypt_image, decrypt_image

keyphrase = 'mypassword'
encrypt_image(os.path.join('space.jpg'), keyphrase)
decrypt_image(os.path.join('space.cipher'), keyphrase)