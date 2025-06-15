from flask import Flask, request, render_template, jsonify
# Monkey-patch InputLayer to accept legacy batch_shape kwarg
from tensorflow.keras.layers import InputLayer
orig_init = InputLayer.__init__
def patched_init(self, *args, batch_shape=None, **kwargs):
    if batch_shape is not None:
        kwargs['batch_input_shape'] = tuple(batch_shape)
    return orig_init(self, *args, **kwargs)
InputLayer.__init__ = patched_init

from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os

# Initialize Flask app, explicitly pointing to templates directory
app = Flask(__name__, template_folder="templates")
from flask_cors import CORS
# Allow health and upload endpoints cross-origin
CORS(app, resources={r"/health": {"origins": "*"}, r"/upload": {"origins": "*"}})

# Load your Keras .h5 model without compiling optimizer
model = load_model("asl_alphabet_cnn.h5", compile=False)


def predict_from_video(path):
    """
    Reads all frames from video, preprocesses each to model input size,
    predicts per-frame classes, and returns the full sequence with spaces.
    """
    cap = cv2.VideoCapture(path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize/grayscale per CNN's training configuration
        img = cv2.resize(frame, (32, 32))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        frames.append(gray)
    cap.release()

    if not frames:
        return ""

    # Prepare batch: (N,32,32,1)
    x = np.stack(frames, axis=0)[..., np.newaxis] / 255.0
    preds = model.predict(x)
    frame_classes = np.argmax(preds, axis=1)
    # Map indices: letters A-Z, then del, nothing, space
    labels = [chr(c) for c in range(65, 91)] + ['del', 'nothing', ' ']
    seq = [labels[c] for c in frame_classes]

    # Collapse repeats (keep spaces) and remove 'del'/'nothing' tokens
    result_chars = []
    prev = None
    for ch in seq:
        if ch in ('del', 'nothing'):
            continue
        if ch != prev:
            result_chars.append(ch)
        prev = ch
    return ''.join(result_chars)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# This is your endpoint for video uploads and translation, your asl_alphabet_cnn.h5 is the trained model that helps with the translation 
@app.route("/upload", methods=["POST"])
def upload_video():
    vid = request.files.get("video")
    if not vid:
        return jsonify({"error": "No video file provided"}), 400
    os.makedirs("uploads", exist_ok=True)
    save_path = os.path.join("uploads", vid.filename)
    vid.save(save_path)
    translation = predict_from_video(save_path)
    return jsonify({"translation": translation}), 200

#This endpoint checks the the health of your server , thats how you can see if the server is running on your front end
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)