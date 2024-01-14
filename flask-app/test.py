import cv2
import inference
import supervision as sv
import os
os.environ['ROBOFLOW_API_KEY'] = 'iO1raAWZcPu5LL6vhwrA'

annotator = sv.BoxAnnotator()

scene, detections, labels = None, None, None

def on_prediction(predictions, image):
    global scene, detections, labels

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

while True:
    if scene is not None:
      cv2.imshow(
              "Prediction",
              annotator.annotate(
                  scene=scene,
                  detections=detections,
                  labels=labels
              )
          ),
      cv2.waitKey(1)