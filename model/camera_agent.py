import agentpy as ap
from model.YoloVision import YoloVision
from owlready2 import get_ontology

class CameraAgent(ap.Agent):
    
    def setup(self):
        self.is_moving = True
        self.vision = YoloVision()
        # Cargar ontología
        self.ontology = get_ontology("ontology.owl").load()
    
    def detect_objects(self, image_path, object_position):
        suspicious_detected = self.vision.detect_objects(image_path)

        for obj in suspicious_detected:
            self.evaluate_object(obj, object_position)

    def evaluate_object(self, obj, position):
        object_name = obj['name']
        detected_obj = self.ontology.search_one(iri=f"*{object_name}")
        
        if detected_obj:
            risk_level = detected_obj.riskLevel
            action = detected_obj.recommendedAction
            
            print(f"Camera {self.id}: Detected {object_name} (Risk: {risk_level})")

            if risk_level > 0.5:
                print(f"Sending alert: {object_name} is suspicious.")
                self.send_alert(obj, position)
        else:
            print(f"Camera {self.id}: {object_name} not found in ontology.")
    
    def send_alert(self, object, position):
        alert = {
            'camera_id': self.id,
            'object': object['name'],
            'position': position
        }
        self.model.alerts.append(alert)
        print(f"Camera {self.id} sent an alert for {object['name']} at {position}")

    def step(self, img, object_position):
        self.detect_objects(img, object_position)
