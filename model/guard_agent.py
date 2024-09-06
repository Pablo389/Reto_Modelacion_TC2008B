import agentpy as ap

class SecurityGuard(ap.Agent):
    def setup(self):
        pass

    def receive_alert(self, position, object_name):
        print(f"Guard received alert about {object_name} at {position}. Investigating...")

        # Explorar la zona usando el dron
        self.explore_area(position, object_name)

    def explore_area(self, position, object_name):
        exploration_time = 0
        certainty_sum = 0
        checks = 3

        for _ in range(checks):
            certainty = self.model.drone[0].vision.detect_certainty(object_name)
            certainty_sum += certainty
            exploration_time += 1
            print(f"Exploration {exploration_time}, certainty {certainty}")

        avg_certainty = certainty_sum / checks
        if avg_certainty > 0.6 and exploration_time > 2:
            print("General alert! Suspicious object confirmed.")
        else:
            print("False alarm. Object seems safe.")
