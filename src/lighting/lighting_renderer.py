import pygame


class LightingRenderer:
    # player_position,
    def __init__(self, screen, maze, camera):

        self.screen = screen
        # self.player_position = player_position,
        self.maze = maze
        self.camera = camera
        self.darkness = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.light_mask = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.light_gradient = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

    def render(self, light, light_position):
        self.darkness.fill((0, 0, 0, 255))

        self._render_visibility(
            light,
            light_position
        )
        self._render_gradient(
            light,
            light_position
        )

        self.light_gradient.blit(
            self.light_mask,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MIN
        )

        """ self.darkness.blit(
            self.light_gradient,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_SUB
        ) """

        self.screen.blit(self.light_gradient,(0, 0))

    def _render_visibility(self, light, light_position):
        visibility_points = light.calculate_visibility(
            light_position,
            self.maze
        )

        polygon_points = [
            self._to_screen_position(light_data['position'])
            for light_data in visibility_points
        ]

        self.light_mask.fill((0, 0, 0, 0))
        if len(polygon_points) >= 3:
            pygame.draw.polygon(
                self.light_mask,
                (255, 255, 255, 255),
                polygon_points
            )

        return self.light_mask

    def _render_gradient(self, light, light_position):
        self.light_gradient.fill((0, 0, 0, 0))

        screen_light_position = self._to_screen_position(light_position)
        radius = int(light.current_radius)

        for current_radius in range(radius, 0, -2):
            intensity = light.get_intensity(current_radius)
            alpha = int(255 * intensity)

            pygame.draw.circle(
                self.light_gradient,
                (0, 0, 0, alpha),
                screen_light_position,
                current_radius
            )

        return self.light_gradient

    def _to_screen_position(self, world_position):
        screen_position = world_position - self.camera.position
        return int(screen_position.x), int(screen_position.y)