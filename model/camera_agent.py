import agentpy as ap
from model.YoloVision import YoloVision
from owlready2 import get_ontology

class CameraAgent(ap.Agent):
    
    def setup(self):
        self.is_moving = True
        self.vision = YoloVision()
        self.ontology = get_ontology("ontology.owl").load()
    
    def detect_objects(self, image_path, object_position):
        detected_objects = self.vision.detect_objects(image_path)

        for obj in detected_objects:
            self.send_alert(obj, object_position)

    def send_alert(self, object, position):
        alert = {
            'camera_id': self.id,
            'object': object['name'],
            'position': position
        }
        print(f"Camera {self.id}: Detected {object['name']}. Sending alert.")
        self.model.alerts.append(alert)

    def step(self, img, object_position):
        self.detect_objects(img, object_position)