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
dog = SafeObject("dog")
person = SuspiciousObject("person")

car.riskLevel = 0.1
car.recommendedAction = "ignore"

dog.riskLevel = 0.2
dog.recommendedAction = "monitor"

person.riskLevel = 0.8
person.recommendedAction = "investigate"

# Guardar la ontología
onto.save(file="ontology.owl")
