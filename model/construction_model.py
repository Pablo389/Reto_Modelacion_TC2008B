import agentpy as ap
import numpy as np
from model.camera_agent import CameraAgent
from model.drone_agent import DroneAgent
from model.guard_agent import SecurityGuard

class SurveillanceModel(ap.Model):
    def setup(self): #FALTA VER COMO ESTAN LOS OBSTACULOS EN UNITY TAL CUAL Y VER LO DE LAS POSICIONES ESPECIFICAS, PARA EL ESPACIO

        self.cameras = ap.AgentList(self, 4, CameraAgent)
        #self.guard = ap.AgentList(self, 1, SecurityGuard)

        camera_positions = [tuple(np.random.randint(0, 15, 3)) for _ in range(4)]  # Números enteros
        drone_position = tuple(np.random.randint(0, 15, 3))  # Convertir a tuple con números enteros
        #guard_position = [tuple(np.random.randint(0, 15, 3))]  # Convertir a tuple en una lista con números enteros
        self.drone = [DroneAgent(self, initial_position=drone_position)]
        print(f"Camera positions: {camera_positions}")
        print(f"Drone position: {drone_position}")
        #print(f"Guard position: {guard_position}")

        self.space = ap.Space(self, shape=[250, 70, 250])

        self.space.add_agents(self.cameras, positions=camera_positions, random=False)
        self.space.add_agents(self.drone, positions=[drone_position], random=False)  # Pasar como lista de tuplas
        #self.space.add_agents(self.guard, positions=guard_position, random=False)

        self.grid = np.ones((250, 70, 250))

        num_obstacles = 5
        for _ in range(num_obstacles):
            obs_pos = tuple(np.random.randint(0, 15, 3))  # Números enteros
            print(f"Obstacle position: {obs_pos}")
            self.grid[obs_pos] = 0

        #print(f"Grid shape: {self.grid.shape}")
        #print(f"Grid: {self.grid}")


    def update(self):
        pass

    def step(self, camera_id, img, object_position):
        self.suspicious_position = object_position
        for camera in self.cameras:
            #print(camera.id)
            if camera.id == int(camera_id):
                print(f"Camera {camera_id} is active")
                suspicious = camera.detect_objects(img)
                if suspicious:
                    return "suspicious"
        
        return "safe"
    
    def create_path(self, start): #Falta hacer que funcione con el drone
        path = self.drone[0].a_star_search(self.grid, start, self.suspicious_position)
        return path