import agentpy as ap
from owlready2 import *
from ultralytics import YOLO
import json

class CameraAgent(ap.Agent):
    
    def setup(self):
        self.safe_objects = set()  # Conjunto para objetos seguros
        self.suspicious_objects = set()  # Conjunto para objetos sospechosos
        self.load_ontology()
        self.model = YOLO("yolov8s.pt")  # Cargar el modelo YOLO solo una vez
        self.is_moving = True
    
    def load_ontology(self):
        # Cargar la ontología creada
        self.ontology = get_ontology("ontology.owl").load()
        for obj in self.ontology.SafeObject.instances():
            self.safe_objects.add(obj.name)
        for obj in self.ontology.SuspiciousObject.instances():
            self.suspicious_objects.add(obj.name)
    
    def detect_objects(self, image_path):
        """ Método para procesar objetos detectados """
        # Cargar y procesar la imagen usando el modelo YOLO
        results = self.model(image_path)
        #results[0].show()
        
        # Extraer objetos detectados
        detected_objects = []
        json_result = results[0].tojson()
        
        json_result = json.loads(json_result)
        #print(type(json_result[0]))
        print(json_result)
        for obj in json_result:
            detected_objects.append(obj["name"])
        
        # Analizar los objetos detectados
        suspicious_detected = []
        for obj in detected_objects:
            if obj in self.suspicious_objects:
                suspicious_detected.append(obj)
                print(f"Alerta: Objeto sospechoso detectado - {obj}")
            elif obj in self.safe_objects:
                print(f"Objeto seguro detectado - {obj}")
            else:
                suspicious_detected.append(obj)
                print(f"Alerta: Objeto desconocido detectado - {obj}")
        
        return suspicious_detected
    
    def detect_objects_dummy(self):
        suspicious_detected = [{'name': 'car', 'class': 2, 'confidence': 0.93602, 'box': {'x1': 254.27472, 'y1': 318.5394, 'x2': 804.0683, 'y2': 593.53308}}]
        positions = [10,2,6]
        obj = {'object':'traffic light', 'position': positions}
        #detecta una objeto sospechoso y manda a llamar donde esta el dron en ese momento
        #osea aqui debería retornar algo 
    
    def alert_drone(self, obj): #Ver como tengo que mandar obj para que lo reciba el drone QUITAR!!!
        #Esta funcion no debe exisitir, debemos usa ralgo de tipo mensajería en boradcast y ya el dron lo recibe
        if self.model.drone:
            drone = self.model.drone[0]
            drone.investigate(obj['position'], obj['object'])
    
    def stop_moving(self):
        self.is_moving = False