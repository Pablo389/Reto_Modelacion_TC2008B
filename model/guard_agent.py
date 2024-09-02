import agentpy as ap

class SecurityGuard(ap.Agent): #FALTA HACERLO BASICAMENTE
    def setup(self):
        pass

    def receive_alert(self, position, object_name):
        print(f"Guard received alert about suspicious activity at position: {position}, of {object_name}")