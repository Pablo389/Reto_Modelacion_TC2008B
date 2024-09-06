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

    # Definición de propiedades de datos
    class RiskLevel(DataProperty):
        domain = [KnownObject]
        range = [float]

    class RecommendedAction(DataProperty):
        domain = [KnownObject]
        range = [str]


# Añadir ejemplos a la ontología
car = SafeObject("car")
dog = SafeObject("dog")
person = SuspiciousObject("person")

car.RiskLevel.append(0.1)
car.RecommendedAction.append("ignore")

dog.RiskLevel.append(0.2)
dog.RecommendedAction.append("ignore")

person.RiskLevel.append(0.8)
person.RecommendedAction.append("investigate")

# Guardar la ontología
onto.save(file="ontology.owl")
