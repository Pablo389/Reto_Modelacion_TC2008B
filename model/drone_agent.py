import agentpy as ap
from model.YoloVision import YoloVision
from owlready2 import get_ontology

class DroneAgent(ap.Agent):
    def setup(self):
        self.state = 'patrolling'
        self.target_position = None
        self.object_name = None
        self.vision = YoloVision()
        self.ontology = get_ontology("ontology.owl").load()

    def receive_alert(self, alert):
        if self.state == 'patrolling':
            print(f"Drone received alert: {alert['object']} at {alert['position']} by camera {alert['camera_id']}")
            self.state = 'investigating'
            self.target_position = alert['position']
            self.object_name = alert['object']
    
    def step(self):
        if self.model.alerts:
            alert = self.model.alerts.pop(0)
            self.receive_alert(alert)

        if self.state == 'investigating':
            self.investigate_object()

    def investigate_object(self):
        certainty = self.vision.detect_certainty(self.object_name)
        detected_obj = self.ontology.search_one(iri=f"*{self.object_name}")

        if detected_obj:
            risk_level = detected_obj.riskLevel
            print(f"Drone investigating {self.object_name}. Risk level: {risk_level}, Certainty: {certainty}")

            if risk_level > 0.5 and certainty > 0.7:
                print(f"Drone confirms {self.object_name} as high risk. Calling guard.")
                self.call_guard()
            else:
                print(f"Drone dismisses {self.object_name} as low risk or uncertain.")
                self.state = 'patrolling'
    
    def call_guard(self):
        guard = self.model.guard[0]
        guard.receive_alert(self.target_position, self.object_name)
        self.state = 'returning'