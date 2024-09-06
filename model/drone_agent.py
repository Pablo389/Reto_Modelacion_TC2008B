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
            print(f"Drone received alert: {alert['object_name']} detected at {alert['position']} by camera {alert['camera_id']}")
            self.state = 'investigating'
            self.target_position = alert['position']
            self.object_name = alert['object_name']
            self.model.stage = 'investigating'
    
    def detect_objects(self, image_path):
        suspicious_detected = self.vision.detect_objects(image_path)

        return suspicious_detected

    def step(self):
        if self.model.alerts:
            alert = self.model.alerts.pop(0)
            self.receive_alert(alert)

    