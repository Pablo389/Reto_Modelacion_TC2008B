from owlready2 import *

# Crear un nuevo archivo de ontología en memoria
onto = get_ontology("http://example.org/onto.owl")

with onto:
    class KnownObject(Thing):
        pass

    class SuspiciousObject(KnownObject):
        pass

    class SafeObject(KnownObject):
        pass

    class RiskLevel(KnownObject >> float, FunctionalProperty):
        pass

    class RecommendedAction(KnownObject >> str, FunctionalProperty):
        pass

# Añadir ejemplos a la ontología
car = SafeObject("car")
toilet = SafeObject("toilet")
traffic_light = SuspiciousObject("traffic_light")

car.riskLevel = 0.1
car.recommendedAction = "ignore"

toilet.riskLevel = 0.2
toilet.recommendedAction = "monitor"

traffic_light.riskLevel = 0.8
traffic_light.recommendedAction = "investigate"

# Guardar la ontología
onto.save(file="ontology.owl")
