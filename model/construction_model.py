import agentpy as ap
import numpy as np
from model.camera_agent import CameraAgent
from model.drone_agent import DroneAgent
from model.guard_agent import SecurityGuard

class SurveillanceModel(ap.Model):
    def setup(self):

        self.alerts = []
        self.suspicious_obj_pos = None
        self.stage = 'patrolling'

        self.cameras = ap.AgentList(self, 4, CameraAgent)
        self.guard = ap.AgentList(self, 1, SecurityGuard)
        self.drone = ap.AgentList(self, 1, DroneAgent)

        camera_positions = [(3, 7, 12), (1, 14, 9), (8, 0, 13), (5, 10, 2)]  # Poner las posiciones de unity parametrizadas de donde estan las camaras
        drone_position = [(0, 15, 3)]  # Igual que las camaras, pero con la posicion inicial del dron
        guard_position = [(0, 15, 3)]  # Posicion arbitraria del guardia de seguridad

        print(f"Camera positions: {camera_positions}")
        print(f"Drone position: {drone_position}")
        print(f"Guard position: {guard_position}")

        self.space = ap.Space(self, shape=[250, 70, 250])

        self.space.add_agents(self.cameras, positions=camera_positions, random=False)
        self.space.add_agents(self.drone, positions=drone_position, random=False)  # Pasar como lista de tuplas
        self.space.add_agents(self.guard, positions=guard_position, random=False)

        #Ver para que nos funciona el grid y como lo usamos
        """
        self.grid = np.ones((250, 70, 250))

        num_obstacles = 5
        for _ in range(num_obstacles):
            obs_pos = tuple(np.random.randint(0, 15, 3))  # Números enteros
            print(f"Obstacle position: {obs_pos}")
            self.grid[obs_pos] = 0

        """ 
        
    def step(self, camera_id: int, img: str, object_position):
        #Nueva logica: siempre las camaras van a ver si ven algo, sii no, el dron ejecuta su camino

        for camera in self.cameras:
            if camera.id == camera_id:
                print(f"Camera {camera_id} is active")
                camera.step(img, object_position)
                
        self.drone[0].step()