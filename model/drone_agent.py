import agentpy as ap
import numpy as np
import heapq
from owlready2 import *
from ultralytics import YOLO
import json
from model.YoloVision import YoloVision

class DroneAgent(ap.Agent):
    def setup(self):
        """
        self.path = []  # Posición inicial del dron UNITY DARA LA POSICION DESDE LA QUE SE TIENE QUE LLEGAR
        self.reached_destination = False
        """
        self.state = 'patrolling'  # Estados: 'patrolling', 'investigating', 'returning'
        self.target_position = None
        self.object_name = None

        self.vision = YoloVision()

    def receive_alert(self, alert):
        if self.state == 'patrolling':
            print(f"Drone received alert: {alert['object']} detected at {alert['position']} by camera {alert['camera_id']}")
            self.state = 'investigating'
            self.target_position = alert['position']
            self.object_name = alert['object']
            self.model.stage = 'investigating'
    
    def detect_objects(self, image_path, object_position):
        suspicious_detected = self.vision.detect_objects(image_path)

        for obj in suspicious_detected:
            if obj['confidence'] > 0.5:
                self.send_alert(obj, object_position)

        return suspicious_detected
    
    def send_alert(self, object, position):
        alert = {
            'camera_id': self.id,
            'object': object,
            'position': position
        }
        self.model.drone_alerts.append(alert)
        print(f"Camera {self.id} sent an alert: {object['name']} detected at {position}")

    def step(self):
        if self.model.alerts:
            alert = self.model.alerts.pop(0)
            self.receive_alert(alert)

    