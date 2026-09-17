import pygame
import math


class Light:
    def __init__(self, max_energy, idle_consumption, moving_consumption):
        self.max_energy = max_energy
        self.energy = max_energy

        self.idle_consumption = idle_consumption
        self.moving_consumption = moving_consumption

        self.ray_count = 360


        # --- Dados para o efeito pulsação
        self.base_radius = 130
        self.pulse_amount = 6
        self.pulse_speed = 1.8
        self.time = 0.0
        self.current_radius = self.base_radius


    def update(self, dt, is_moving):
        self.time += dt

        pulse = math.sin(self.time * self.pulse_speed)

        self.current_radius = (
            self.base_radius + pulse * self.pulse_amount
        )

        if is_moving:
            consumption = self.moving_consumption
            #print(f"Moving: Consuming {consumption} energy per second.")
        else:
            consumption = self.idle_consumption
            #print(f"Idle: Consuming {consumption} energy per second.")

        self.energy -= consumption * dt
        self.energy = max(0, self.energy)

        point = pygame.Vector2(90, 0)

        """ print(
        self.get_light_data(
            pygame.Vector2(0, 0),
            point
        )
        ) """

    def calculate_visibility(self, position, maze):
        points = []

        angle_step = math.tau / self.ray_count

        for ray_index in range(self.ray_count):
            angle = ray_index * angle_step

            direction = pygame.Vector2(
                math.cos(angle),
                math.sin(angle)
            )

            rey_end = position + direction * self.current_radius

            visible_point = maze.raycast(
                position,
                rey_end
            )

            light_data = self.get_light_data(
                position,
                visible_point
            )
            
            points.append(light_data)
        
        return points
    
    def get_intensity(self, distante):
        if distante >= self.current_radius:
            return 0
        
        intensity = 1 - (distante / self.current_radius)

        return intensity

    def get_intensity_at(self, light_position, target_position):
        distance = light_position.distance_to(target_position)

        return self.get_intensity(distance)
    
    def apply_to_color(self, color, intensity):
        r, g, b = color

        return (
            int(r * intensity),
            int(g * intensity),
            int(b * intensity)
        )
    
    def get_light_data(self, light_position, target_position):
        intensity = self.get_intensity_at(
            light_position,
            target_position
        )

        return {
            'position': target_position,
            'intensity': intensity
        }