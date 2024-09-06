import agentpy as ap
from owlready2 import *

class SecurityGuard(ap.Agent):
    def setup(self):
        self.is_in_control_of_drone = False
        self.ontology = get_ontology("ontology.owl").load() 
        self.investigating_steps = 0
        self.exploration_time = 0

    def take_control_of_drone(self):
        self.is_in_control_of_drone = True


    def explore_area_with_drone(self, image_path):
        if self.investigating_steps > 7:
            print(f"Guard finished investigating the area")
            self.model.stage = 'patrolling'
            self.model.drone[0].state = 'patrolling'
            self.investigating_steps = 0
            return
        
        self.is_in_control_of_drone = True
        if self.is_in_control_of_drone:
            print("Guard is exploring the area with the drone")
            self.investigating_steps += 1
            detected_objects = self.model.drone[0].vision.detect_objects(image_path)

            # Si se detectan objetos, el guardia los evalúa
            for obj in detected_objects:
                certainty = obj['confidence']
                self.exploration_time += 1
                print(f"Guard observing through drone. Check {self.exploration_time}, certainty {certainty} for object {obj['name']}")

                # Acceder a la ontología para obtener el nivel de riesgo y la acción recomendada
                detected_obj = self.ontology.search_one(iri=f"*{obj['name']}")
                risk_level =  detected_obj.RiskLevel[0] if detected_obj else 0
                recommended_action = detected_obj.RecommendedAction[0] if detected_obj else "ignore"

                # Evaluar el objeto con base en riesgo, certeza y tiempo
                self.evaluate_object(obj, certainty, risk_level, recommended_action)

        if self.exploration_time > 5:
            self.release_control_of_drone()

    def evaluate_object(self, obj, certainty, risk_level, recommended_action):
        # Decisión basada en nivel de riesgo, certeza y tiempo
        if recommended_action == "investigate" and certainty > 0.6 and self.exploration_time > 3 and risk_level > 0.5:
            print(f"General alert! {obj['name']} is confirmed as suspicious with risk level {risk_level} and certainty {certainty}.")
            self.model.stage = "final_alert"
            self.exploration_time = 0
            self.release_control_of_drone()
        elif self.exploration_time > 5:
            print(f"False alarm or low certainty for {obj['name']}. No action required.")
            self.model.stage = "patrolling"
            self.exploration_time = 0
            self.release_control_of_drone()

    def release_control_of_drone(self):
        self.is_in_control_of_drone = False
        print("Guard released control of the drone.")

    def receive_alert(self, alert):
        print(f"Guard received alert: {alert['object']} detected at {alert['position']}")
        self.take_control_of_drone()

    def step(self):
        if self.model.drone_alerts:
            alert = self.model.drone_alerts.pop(0)
            self.receive_alert(alert)
