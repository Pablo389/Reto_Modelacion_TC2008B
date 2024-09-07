from owlready2 import *
from ultralytics import YOLO
import json

class YoloVision():

    def __init__(self):
        self.safe_objects = set()  # Conjunto para objetos seguros
        self.suspicious_objects = set()  # Conjunto para objetos sospechosos
        self.load_ontology()
        self.model = YOLO("yolov8n_beto.pt")  # Cargar el modelo YOLO solo una vez

    def load_ontology(self):
            # Cargar la ontología creada
            self.ontology = get_ontology("ontology.owl").load()
            for obj in self.ontology.SafeObject.instances():
                self.safe_objects.add(obj.name)
            for obj in self.ontology.SuspiciousObject.instances():
                self.suspicious_objects.add(obj.name)
        
    def detect_objects(self, image_path, show_image=False):
        """ Método para procesar objetos detectados """
        # Cargar y procesar la imagen usando el modelo YOLO
        results = self.model(image_path)
        if show_image:
            results[0].show()
        
        # Extraer objetos detectados
        detected_objects = []
        json_result = results[0].tojson()
        
        json_result = json.loads(json_result)
        #print(type(json_result[0]))
        #print(json_result)
        for obj in json_result:
            detected_objects.append(obj)
        
        # Analizar los objetos detectados
        suspicious_detected = []
        for obj in detected_objects:
            if obj['name'] in self.suspicious_objects:
                suspicious_detected.append(obj)
                print(f"Alerta: Objeto sospechoso detectado - {obj['name']}")
            elif obj['name'] in self.safe_objects:
                print(f"Objeto seguro detectado - {obj['name']}")
            else:
                #suspicious_detected.append(obj)
                print(f"Alerta: Objeto desconocido detectado - {obj['name']}")

        return suspicious_detected