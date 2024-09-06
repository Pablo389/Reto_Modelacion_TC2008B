import agentpy as ap
from model.YoloVision import YoloVision
from model.Ontology import Ontology  

class DroneAgent(ap.Agent):
    def setup(self):
        self.state = 'patrolling'  # Estados: 'patrolling', 'investigating', 'returning'
        self.target_position = None
        self.vision = YoloVision() 
        self.ontology = Ontology()  

    def receive_alert(self, alert):
        if self.state == 'patrolling':
            print(f"Drone received alert: {alert['object']} detected at {alert['position']} by camera {alert['camera_id']}")
            self.state = 'investigating'
            self.target_position = alert['position']
    
    def investigate_area(self):
        if self.state == 'investigating':
            print(f"Drone is investigating the area at position {self.target_position}")

            # El dron toma una nueva imagen y hace un análisis en esa posición
            image_path = "path_to_image_taken_by_drone"  # Aquí iría la lógica real de tomar la imagen
            detected_objects = self.vision.detect_objects(image_path)

            # Consultar la ontología para obtener información del objeto
            for obj in detected_objects:
                if obj['confidence'] > 0.5:
                    # Acceder a la ontología para obtener información del objeto
                    detected_obj = self.ontology.search_one(iri=f"*{obj['name']}")
                    risk_level = detected_obj.riskLevel if detected_obj else 0
                    recommended_action = detected_obj.recommendedAction if detected_obj else "ignore"

                    # Enviar la alerta al guardia si es relevante
                    if risk_level > 0.5:
                        print(f"Drone detected a suspicious object: {obj['name']} with risk level {risk_level}.")
                        self.model.guard[0].receive_alert(self.target_position, obj)
                    else:
                        print(f"Drone detected {obj['name']} but it is not considered a risk.")

            self.state = 'returning'

    def step(self):
        if self.model.alerts:
            alert = self.model.alerts.pop(0)
            self.receive_alert(alert)
            self.investigate_area()  # El dron procede a investigar el área cuando recibe una alerta

