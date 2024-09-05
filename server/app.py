from fastapi import FastAPI, WebSocket
from model.camera_agent import CameraAgent
from model.construction_model import SurveillanceModel
import numpy as np
import base64
import cv2
import json

app = FastAPI()

model = SurveillanceModel()
model.setup()

@app.get("/")
def read_root():
    return {"message": "Warehouse Simulation API"}

@app.websocket("/ws/test/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()  # Espera mensaje del cliente
        if data:
            try:
                # Decodificar el JSON recibido
                json_data = json.loads(data)
                action = json_data.get("action", "")  # Identificar la acción solicitada
            except json.JSONDecodeError:
                await websocket.send_json({"status": "error", "message": "JSON decode error"})
                continue

            try:
                if action == "send_image":
                    
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

                    object_position = json_data.get("coordinates", "")
                    print(f"Posicion del objeto: {object_position}")

                    suspicious = model.step(camera_id, img, object_position)
                    if suspicious == "suspicious":
                        await websocket.send_json({"status": "suspicious", "camera_id": camera_id})
                    else:
                        await websocket.send_json({"status": "safe", "camera_id": camera_id})

                elif action == "send_drone_position":
                    drone_position = list(json_data.get("coordinates", ""))
                    print(f"Posicion del dron: {drone_position}")

                    path = model.create_path(drone_position)

                    await websocket.send_json({"status": "path sent", "path": "path"})

                elif action == "close":
                    await websocket.close()
                    break
            
            except KeyError:
                print("El JSON recibido no contiene la clave solicitada")
            except Exception as e:
                print(f"Error procesando la peticion: {e}")