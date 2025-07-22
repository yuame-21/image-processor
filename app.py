from flask import Flask, request
from PIL import Image
import numpy as np

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def calc_avg_intensity(image):
    pixel_array = np.array(image)
    return pixel_array.mean()


@app.route("/calculate-intensity", methods=["POST"])
def calculate_intensity():
    # process image file from the request
    file = request.files["image"]
    image = Image.open(file.stream)

    intensity = calc_avg_intensity(image)
    print(f"Average intensity: {intensity}")
    return {"avg_intensity": intensity}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)