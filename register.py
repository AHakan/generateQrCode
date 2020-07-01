import random
import string
import requests
import click
import qrcode
from PIL import Image


def get_random_alphaNumeric_string(randomLength):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(randomLength)))

def generateQrCode(token):
    face = Image.open('icon.png')
    qr_big = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr_big.add_data(token)
    qr_big.make()
    img_qr_big = qr_big.make_image(fill_color="#0f3891", back_color="#e8e8e8").convert('RGB')
    pos = ((img_qr_big.size[0] - face.size[0]) // 2, (img_qr_big.size[1] - face.size[1]) // 2)
    img_qr_big.paste(face, pos)
    img_qr_big.save(token+'.png')

@click.command()  
@click.option("--yyy", prompt="yyy", help="yyy değerini giriniz.") 
@click.option("--length", default=32, prompt="String Length", help="Random string uzunluğunu giriniz.") 
def postRequest(yyy, length):
    newHeaders = {'Content-type': 'application/json', 'User-agent': 'xxx'}

    xxx = get_random_alphaNumeric_string(length)
    body={"xxx": xxx, "yyy": yyy}

    response = requests.post('xxx',
                            json=body,
                            headers=newHeaders)

    response_Json = response.json()

    if response_Json['message']=="1":
        generateQrCode(token)

postRequest()
