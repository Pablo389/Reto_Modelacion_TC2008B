from fastapi import FastAPI, WebSocket
from model.camera_agent import CameraAgent
from model.construction_model import SurveillanceModel
import numpy as np
import base64
import cv2
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Warehouse Simulation API"}

@app.websocket("/ws/test/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    model = SurveillanceModel()
    model.setup()
    while True:
        data = await websocket.receive_text()  # Espera mensaje del cliente
        if data:
            try:
                # Parsear el string JSON recibido
                json_data = json.loads(data)
                #print(f"JSON recibido: {json_data}")
                
                # Acceder a la imagen en base64 del JSON
                base64_str = json_data.get("image_base64", "")
                
                # Decodificar la cadena base64 a bytes
                img_data = base64.b64decode(base64_str)
                
                # Convertir los bytes a un arreglo NumPy
                nparr = np.frombuffer(img_data, np.uint8)
                
                # Decodificar el arreglo NumPy a una imagen OpenCV
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                camera_id = json_data.get("id", "")
                print(f"Id de la camara: {camera_id}")

                #model.step(camera_id, img)

                camera_agent = CameraAgent(SurveillanceModel())
                suspicious_objects = camera_agent.detect_objects(img)
                print(f"Objetos sospechosos detectados: {suspicious_objects}")
                print("Id de la camara: ", json_data.get("id", ""))
                
                await websocket.send_json({"status": "vision completed", 'suspicious_objects': 'Hola'})
            
            except json.JSONDecodeError:
                print("Error al decodificar el JSON recibido")
            except KeyError:
                print("El JSON recibido no contiene la clave 'image_base64'")
            except Exception as e:
                print(f"Error procesando la imagen: {e}")
            
        elif data == "close":
            await websocket.close()
            break