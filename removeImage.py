#2024.03.26 00:35 완성

from flask import Flask, render_template, request
import cv2
import numpy as np
import base64
from rembg import remove

app = Flask(__name__)

# 이미지 처리 함수
def remove_background(image):
    input = image # load image
    output = remove(input) # remove background
    return output

# Flask 라우트
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                nparr = np.fromstring(image_file.read(), np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                result_image = remove_background(image)
                _, buffer = cv2.imencode('.png', result_image)
                result_base64 = base64.b64encode(buffer).decode('utf-8')
                return render_template('index.html', result=result_base64)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

