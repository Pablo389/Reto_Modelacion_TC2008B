import agentpy as ap
from model.camera_agent import CameraAgent
from model.drone_agent import DroneAgent
from model.guard_agent import SecurityGuard

class SurveillanceModel(ap.Model):
    def setup(self):
        self.alerts = []
        self.cameras = ap.AgentList(self, 4, CameraAgent)
        self.guard = ap.AgentList(self, 1, SecurityGuard)
        self.drone = ap.AgentList(self, 1, DroneAgent)

    def step(self, camera_id: int, img: str, object_position):
        for camera in self.cameras:
            if camera.id == camera_id:
                print(f"Camera {camera_id} is active")
                camera.step(img, object_position)

        self.drone[0].step()
