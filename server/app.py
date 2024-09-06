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
                    
                    # Decodificar la imagen para poder mandarla a YOLO
                    img_data = base64.b64decode(base64_str)
                    nparr = np.frombuffer(img_data, np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    ### Ver que hacemos aqui por que el modelo debe entrar el step con toda la info que necesite, sería intersante ver como se hace esto
                    ## Osea no pasarle esos parametros maybe? entonces darle el json?

                    camera_id = int(json_data.get("id", ""))
                    print(f"Id de la camara: {camera_id}")

                    object_position = json_data.get("coordinates", "") #Que tipo de dato es esto?
                    print(f"Posicion del objeto: {object_position}")

                    model.step(camera_id, img, object_position)

                    if model.stage == "investigating":
                        await websocket.send_json({"status": "suspicious", "camera_id": camera_id})
                    else:
                        await websocket.send_json({"status": "safe", "camera_id": camera_id})

                elif action == "send_drone_position":
                    drone_position = list(json_data.get("coordinates", ""))
                    print(f"Posicion del dron: {drone_position}")

                    object_position = model.drone[0].target_position

                    await websocket.send_json({"status": "path sent", "path": object_position})

                elif action == "close":
                    await websocket.close()
                    break
            
            except KeyError:
                print("El JSON recibido no contiene la clave solicitada")
            except Exception as e:
                print(f"Error procesando la peticion: {e}")