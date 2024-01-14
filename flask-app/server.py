
from flask import Flask, Response, request
from flask_cors import CORS
from flask_socketio import SocketIO


import numpy as np
import cv2

##

import inference
import supervision as sv
import os
os.environ['ROBOFLOW_API_KEY'] = 'iO1raAWZcPu5LL6vhwrA'

annotator = sv.BoxAnnotator(color=sv.Color(0, 255, 0))

scene, detections, labels = None, None, None
annotated = None

def on_prediction(predictions, image):
    global scene, detections, labels, annotated

    scene = image
    labels = [p["class"] for p in predictions["predictions"]]
    detections = sv.Detections.from_roboflow(predictions)

    
inference.Stream(
    source=0,  # or rtsp stream or camera id
    model="disease-detection-uc0x4/1",  # from Universe
    output_channel_order="BGR",
    use_main_thread=False,  # for opencv display
    on_prediction=on_prediction,
)


###

# Initialize Roboflow model
API_KEY = 'iO1raAWZcPu5LL6vhwrA'

# Assuming this file is located at my_project/flask_app/app.py
app = Flask(__name__, static_folder='dist')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

show_disease = False
show_detections = True
threshold = 50

def ProcessImage(frame, processing_factor):
    # Using vectorized operations for faster processing
    b, g, r = cv2.split(frame)
    disease = r - g
    alpha = GetAlpha(frame)

    # Simplified disease processing
    mask = g > processing_factor
    disease[mask] = 255

    disease_rgb = cv2.merge([disease, disease, disease])

    # Return processed images for later use
    return frame, disease, disease_rgb, alpha

def GetAlpha(frame):
    # Using vectorized operations for Alpha calculation
    high_values = (frame[:, :, 0] > 200) & (frame[:, :, 1] > 200) & (frame[:, :, 2] > 200)
    alpha = np.zeros(frame.shape[:2], dtype=np.uint8)
    alpha[high_values] = 255
    return alpha


def gen_frames():  
    global show_disease, show_detections, scene, detections, labels

    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # uhhhhhhhhhhhhhhhhhhhh
            if (show_disease):
                frame, disease, disease_rgb, alpha = ProcessImage(frame, threshold)
                frame = disease_rgb
            else:
                frame = scene
     
            if (show_detections):
                frame = annotator.annotate(
                    scene=frame,
                    detections=detections,
                    labels=labels,
                )

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# post request to toggle disease
# content header type must be application/json
# and has {toggle: boolean} in the body
@app.route('/toggle_disease', methods=['POST'])
def toggle_disease():
    global show_disease
    
    # get the toggle value from the request body
    toggle = request.get_json()['toggle']
    show_disease = toggle

    return 'OK'

@app.route('/toggle_detections', methods=['POST'])
def toggle_detections():
    global show_detections
    
    # get the toggle value from the request body
    toggle = request.get_json()['toggle']
    show_detections = toggle

    return 'OK'

# post request to threshold
# content header type must be application/json
# and has {value: number} in the body
@app.route('/set_threshold', methods=['POST'])
def set_threshold():
    global threshold
    
    # get the toggle value from the request body
    toggle = request.get_json()['threshold']
    threshold = toggle

    return 'OK'

# on socket connect, print something
@socketio.on('connect')
def test_connect():
    print('Client connected')


# if /video_feed, send the frames
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')


from sensor import emit_sensor_data

if __name__ == '__main__':
    socketio.start_background_task(emit_sensor_data, socketio)
    socketio.run(app, debug=True)