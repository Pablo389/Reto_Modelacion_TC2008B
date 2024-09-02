import agentpy as ap
import numpy as np
import heapq
from owlready2 import *

class Drone(ap.Agent):
    def setup(self, initial_position):
        self.path = []
        self.position = initial_position   # Posición inicial del dron UNITY DARA LA POSICION DESDE LA QUE SE TIENE QUE LLEGAR
        self.reached_destination = False

    def investigate(self, position, object_name):
        start = self.position
        print(f"Sus position: {position}")
        modified_position = (position[0], position[1] + 2, position[2])
        self.path = self.a_star_search(self.model.grid, start, modified_position) #MANDARLA A UNITY PARA SPLINES
        print(f"Path found: {self.path}")
        if self.path:
            while self.path:
                next_position = self.path.pop(0)
                #print(f"Moving to next position: {next_position}")
                self.move_to(next_position) #AQUI NO SE VA A MOVER TAL CUAL, PERO POR MERA REPRESENTACION ESTA AQUI
                # Esperar un poco o permitir el avance del paso podría ser necesario
                #time.sleep(1)  # Agregar un retraso para observar el movimiento
            self.reached_destination = True #ESTO NOS LO MANDARA UNITY
        else:
            print("No path found")

        if self.reached_destination:
            self.perform_additional_moves(modified_position, object_name)


    def perform_additional_moves(self, target_position, object_name):
        # Realizar movimientos adicionales, como girar o subir/bajar
        print("Performing additional moves around the target position.")
        # Ejemplo de movimiento: Subir y bajar
        up_position = (target_position[0], target_position[1], target_position[2] + 2)
        down_position = (target_position[0], target_position[1], target_position[2] - 2)

        arr_pos=[up_position, down_position, up_position, down_position]

        self.move_to(up_position)
        print(f"Moving up to position: {up_position}")
        self.move_to(down_position)
        print(f"Moving down to position: {down_position}")
        self.move_to(up_position)
        print(f"Moving up to position: {up_position}")
        self.move_to(down_position)
        print(f"Moving down to position: {down_position}")
        #FALTA MANDAR A UNITY LAS COORDENADAS DE ESTOS MOVIMIENTOS COMO ARRAY arr_pos

        #Agregar la logica para dar alerta a guardia FALTA VER SI SOLO ASI TAL CUAL
        if self.is_suspicious(object_name):
            self.confirm_alert(target_position, object_name)

    def confirm_alert(self, target_position, object_name):
        print(f"Confirming alert at position: {target_position}")
        if self.model.guard:  # Asegúrate de que haya al menos un guardia
            guard = self.model.guard[0]  # Suponiendo un único guardia para simplificar
            modified_position = (target_position[0], target_position[1] - 2, target_position[2])
            guard.receive_alert(modified_position, object_name)
        self.reached_destination = False  # Resetear para la siguiente misión

    def is_suspicious(self, object_name):
        # Lógica para determinar si el objeto es sospechoso utilizando la ontología
        obj_instance = onto.search_one(iri=f"*{object_name}")
        return isinstance(obj_instance, onto.SuspiciousObject) if obj_instance else False

    def move_to(self, position): #ESTO TECNICAMENTE NO LO NECESITAMOS PORQUE SE MUEVE EN UNITY, SEGUN NUESTRAS COORDENADAS
        if self.position != position:
            print(f"Moving drone from {self.position} to {position}")
            self.position = position
            #print(f"New drone position: {self.position}")
        else:
            print(f"Drone is already at position: {position}")

    def a_star_search(self, grid, start, goal):
        def heuristic(a, b):
            return np.linalg.norm(np.array(a) - np.array(b))

        def get_neighbors(position):
            directions = [(0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0),
                          (0, 0, 1), (0, 0, -1), (1, 1, 0), (1, -1, 0),
                          (-1, 1, 0), (-1, -1, 0), (1, 0, 1), (1, 0, -1),
                          (-1, 0, 1), (-1, 0, -1), (0, 1, 1), (0, 1, -1),
                          (0, -1, 1), (0, -1, -1), (1, 1, 1), (1, 1, -1),
                          (1, -1, 1), (1, -1, -1), (-1, 1, 1), (-1, 1, -1),
                          (-1, -1, 1), (-1, -1, -1)]
            neighbors = []
            for direction in directions:
                neighbor = tuple(np.array(position) + np.array(direction))
                if all(0 <= n < grid.shape[i] for i, n in enumerate(neighbor)):
                    neighbor = tuple(int(n) for n in neighbor)
                    if grid[neighbor] != 0:  # Asegurarse de que el vecino no esté bloqueado
                        neighbors.append(neighbor)
            return neighbors

        open_list = []
        closed_list = set()
        start = tuple(start)
        goal = tuple(goal)
        heapq.heappush(open_list, (0 + heuristic(start, goal), 0, start, []))

        while open_list:
            f, g, current, path = heapq.heappop(open_list)

            if current in closed_list:
                continue

            closed_list.add(current)

            if current == goal:
                return path + [current]

            for neighbor in get_neighbors(current):
                if neighbor in closed_list:
                    continue

                new_g = g + 1
                new_path = path + [current]
                f = new_g + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f, new_g, neighbor, new_path))

        return []