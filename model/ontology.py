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

# Añadir ejemplos a la ontología
car = SafeObject("car")
toilet = SafeObject("toilet")
traffic = SuspiciousObject("traffic light")

onto.save(file="ontology.owl")