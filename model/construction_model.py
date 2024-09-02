import agentpy as ap
import numpy as np

class SurveillanceModel(ap.Model):
    def setup(self): #FALTA VER COMO ESTAN LOS OBSTACULOS EN UNITY TAL CUAL Y VER LO DE LAS POSICIONES ESPECIFICAS, PARA EL ESPACIO
        self.space = ap.Space(self, shape=[15, 15, 15])

        self.cameras = [Camera(self) for _ in range(4)]
        self.guard = [SecurityGuard(self) for _ in range(1)]

        for camera in self.cameras:
            camera.unique_id = self.cameras.index(camera) + 1
            print(f"Camera {camera.unique_id} created")

        camera_positions = [tuple(np.random.randint(0, 15, 3)) for _ in range(4)]  # Números enteros
        drone_position = tuple(np.random.randint(0, 15, 3))  # Convertir a tuple con números enteros
        guard_position = [tuple(np.random.randint(0, 15, 3))]  # Convertir a tuple en una lista con números enteros

        print(f"Camera positions: {camera_positions}")
        print(f"Drone position: {drone_position}")
        print(f"Guard position: {guard_position}")

        self.drone = [Drone(self, initial_position=drone_position)]

        self.space.add_agents(self.cameras, positions=camera_positions, random=False)
        self.space.add_agents(self.drone, positions=[drone_position], random=False)  # Pasar como lista de tuplas
        self.space.add_agents(self.guard, positions=guard_position, random=False)

        self.grid = np.ones((15, 15, 15))

        num_obstacles = 5
        for _ in range(num_obstacles):
            obs_pos = tuple(np.random.randint(0, 15, 3))  # Números enteros
            print(f"Obstacle position: {obs_pos}")
            self.grid[obs_pos] = 0

        #print(f"Grid shape: {self.grid.shape}")
        #print(f"Grid: {self.grid}")


    def update(self):
        pass

    def step(self):
        for camera in self.cameras:
            camera.process_detection()
        for drone in self.drone:
            print(f"Drone position: {drone.position}")