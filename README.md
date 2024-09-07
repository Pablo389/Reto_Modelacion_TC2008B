# Surveillance System with Multi-Agent Simulation

## Descripción

Este proyecto es un sistema de vigilancia que utiliza un enfoque de simulación multi-agente para patrullar y responder a objetos sospechosos en un entorno simulado. El sistema se basa en tres componentes principales:

Unity: Modela el entorno en 3D, incluyendo cámaras y drones. Las cámaras envían imágenes al servidor para su análisis.
AgentPy: Maneja la lógica de los agentes, incluyendo cámaras y drones. Utiliza ontologías para tomar decisiones basadas en las alertas recibidas y coordinar la investigación de objetos sospechosos.
Servidor: Coordina la comunicación entre Unity y AgentPy utilizando WebSockets. Procesa las imágenes recibidas, envía alertas y gestiona el estado de los agentes.

1. Clone the repository to your local machine:

```bash
git clone https://github.com/Pablo389/Reto_Modelacion_TC2008B
```

### Inicialización del Servidor

Para iniciar el servidor, utiliza el siguiente comando:

```bash
uvicorn server.app:app --host 0.0.0.0 --port 8000 --reload
```

Este comando ejecutará el servidor en el puerto 8000 y habilitará la recarga automática de código durante el desarrollo.

### Requisitos

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

server/: Contiene la lógica del servidor y el archivo principal app.py para ejecutar el servidor FastAPI.

agentpy/: Contiene la implementación de los agentes y la lógica de simulación.

unity/: Contiene los archivos relacionados con la integración de Unity (esto puede ser opcional dependiendo de tu estructura).

## Contribuciones

Si deseas contribuir al proyecto, por favor realiza un fork del repositorio y envía un pull request con tus cambios. Asegúrate de que tus cambios estén bien documentados y prueban el código antes de enviarlo.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## Link a el drive con el ZIP de unity, proyecto con Assets y Packages folder

https://drive.google.com/drive/folders/1y3Lph-4Z3eNWo5LYAxwvCAacWwRIZmdX?usp=sharing
