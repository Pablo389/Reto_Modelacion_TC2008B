import agentpy as ap
from owlready2 import *

class SecurityGuard(ap.Agent):
    def setup(self):
        self.is_in_control_of_drone = False
        self.ontology = get_ontology("ontology.owl").load() 

    def receive_alert(self, position, suspicious_obj):
        print(f"Guard received alert. Taking control of the drone to investigate the area at {position}...")

        # Tomar el control del dron
        self.take_control_of_drone(position)

    def take_control_of_drone(self, position):
        self.is_in_control_of_drone = True
        self.explore_area_with_drone(position)

    def explore_area_with_drone(self, position):
        exploration_time = 0
        certainty_sum = 0
        checks = 3  # El guardia "mira" a través del dron varias veces

        for _ in range(checks):
            # Aquí el guardia hace un nuevo análisis de los objetos usando la cámara del dron
            image_path = "path_to_image_taken_by_drone"  # Simular la captura de imagen del dron
            detected_objects = self.model.drone[0].vision.detect_objects(image_path)

            # Si se detectan objetos, el guardia los evalúa
            for obj in detected_objects:
                certainty = obj['confidence']
                certainty_sum += certainty
                exploration_time += 1
                print(f"Guard observing through drone. Check {exploration_time}, certainty {certainty} for object {obj['name']}")

                # Acceder a la ontología para obtener el nivel de riesgo y la acción recomendada
                detected_obj = self.ontology.search_one(iri=f"*{obj['name']}")
                risk_level = detected_obj.riskLevel if detected_obj else 0
                recommended_action = detected_obj.recommendedAction if detected_obj else "ignore"

                # Evaluar el objeto con base en riesgo, certeza y tiempo
                self.evaluate_object(obj, certainty, exploration_time, risk_level, recommended_action)

        avg_certainty = certainty_sum / checks
        self.release_control_of_drone()

    def evaluate_object(self, obj, certainty, exploration_time, risk_level, recommended_action):
        # Decisión basada en nivel de riesgo, certeza y tiempo
        if recommended_action == "investigate" and certainty > 0.6 and exploration_time > 2 and risk_level > 0.5:
            print(f"General alert! {obj['name']} is confirmed as suspicious with risk level {risk_level} and certainty {certainty}.")
        else:
            print(f"False alarm or low certainty for {obj['name']}. No action required.")

    def release_control_of_drone(self):
        self.is_in_control_of_drone = False
        print("Guard released control of the drone.")

    def receive_alert(self, alert):
        print(f"Guard received alert: {alert['object']} detected at {alert['position']}")

    def step(self):
        if self.model.drone_alerts:
            alert = self.model.drone_alerts.pop(0)
            self.receive_alert(alert)
