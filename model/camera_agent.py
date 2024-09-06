import agentpy as ap
from owlready2 import *
import json
from model.YoloVision import YoloVision
 
class CameraAgent(ap.Agent):
    
    def setup(self):
        self.is_moving = True
        self.vision = YoloVision()
    
    def detect_objects(self, image_path, object_position):
        suspicious_detected = self.vision.detect_objects(image_path)
        #print(f"Camera {self.id} detected: {suspicious_detected}")
        
        for obj in suspicious_detected:
            self.send_alert(obj, object_position)

        return suspicious_detected
    
    def send_alert(self, object, position):
        alert = {
            'camera_id': self.id,
            'object': object,
            'position': position
        }
        self.model.alerts.append(alert)
        print(f"Camera {self.id} sent an alert: {object['name']} detected at {position}")

    def step(self, img, object_position):
        self.detect_objects(img, object_position)