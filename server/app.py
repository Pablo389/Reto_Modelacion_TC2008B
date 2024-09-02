from fastapi import FastAPI, WebSocket
from model.camera_agent import CameraAgent
from model.construction_model import MyModel
import numpy as np
import base64
import cv2

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Warehouse Simulation API"}

@app.websocket("/ws/test/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()  # Espera mensaje del cliente
        if data:

            img_data = base64.b64decode(data)
    
            # Convertir los bytes en un arreglo NumPy
            nparr = np.frombuffer(img_data, np.uint8)
            
            # Decodificar la imagen usando OpenCV
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            camera_agent = CameraAgent(MyModel())
            suspicious_objects = camera_agent.detect_objects(img)
            print(f"Objetos sospechosos detectados: {suspicious_objects}")
            
            await websocket.send_json({"status": "vision completed", 'info': 'Vision completed'})
        
        elif data == "close":
            await websocket.close()
            break