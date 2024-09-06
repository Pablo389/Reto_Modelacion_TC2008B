import agentpy as ap
from model.YoloVision import YoloVision
from owlready2 import *

class DroneAgent(ap.Agent):
    def setup(self):
        self.state = 'patrolling'  # Estados: 'patrolling', 'investigating', 'returning'
        self.target_position = None
        self.vision = YoloVision() 
        self.ontology = get_ontology("ontology.owl").load()
        self.investigating_steps = 0 

    def receive_alert(self, alert):
        if self.state == 'patrolling':
            print(f"Drone received alert: {alert['object']} detected at {alert['position']} by camera {alert['camera_id']}")
            self.state = 'investigating'
            self.target_position = alert['position']
            self.model.stage = 'investigating'
    
    def investigate_area(self, img):

        if self.investigating_steps > 7:
            print(f"Drone finished investigating the area at position {self.target_position}")
            self.state = 'patrolling'
            self.model.stage = 'patrolling'
            self.investigating_steps = 0
            self.target_position = None
            return
        if self.state == 'investigating':
            self.investigating_steps += 1
            print(f"Drone is investigating the area at position {self.target_position}")

            detected_objects = self.vision.detect_objects(img)

            # Consultar la ontología para obtener información del objeto
            for obj in detected_objects:
                if obj['confidence'] > 0.5:
                    print(f"Drone detected object: {obj['name']} with confidence {obj['confidence']}")
                    detected_obj = self.ontology.search_one(iri=f"*{obj['name']}")
                    
                    if detected_obj:
                        risk_level = detected_obj.RiskLevel[0] if detected_obj.RiskLevel else 0
                        recommended_action = detected_obj.RecommendedAction[0] if detected_obj.RecommendedAction else "ignore"

                        # Enviar la alerta al guardia si es relevante
                        if risk_level > 0.5:
                            print(f"Drone detected a suspicious object: {obj['name']} with risk level {risk_level}.")
                            self.send_alert(obj, self.target_position)
                            self.model.stage = "guard_investigating"
                        else:
                            print(f"Drone detected {obj['name']} but it is not considered a risk.")
                    else:
                        print(f"Drone detected an object {obj['name']} that is not in the ontology.")

    def send_alert(self, object, position):
        alert = {
            'object': object,
            'position': position
        }
        self.model.drone_alerts.append(alert)
        print(f"Drone {self.id} sent an alert: {object['name']} detected at {position}")

    def step(self):
        if self.model.alerts:
            print("Drone is checking for alerts")
            alert = self.model.alerts.pop(0)
            print(f"Drone received alert: {alert['object']} detected at {alert['position']} by camera {alert['camera_id']}")
            self.receive_alert(alert)

