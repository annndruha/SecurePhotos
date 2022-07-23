import os
from image_engine import encrypt_image, decrypt_image

keyphrase = 'mypassword'
encrypt_image(os.path.join('Sell', 'space.jpg'), keyphrase)
decrypt_image(os.path.join('Sell', 'space.cipher'), keyphrase)
