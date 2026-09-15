class Light:
    def __init__(self, max_energy, idle_consumption, moving_consumption):
        self.max_energy = max_energy
        self.energy = max_energy

        self.idle_consumption = idle_consumption
        self.moving_consumption = moving_consumption

        self.radius = 60

    def update(self, dt, is_moving):
        if is_moving:
            consumption = self.moving_consumption
            #print(f"Moving: Consuming {consumption} energy per second.")
        else:
            consumption = self.idle_consumption
            #print(f"Idle: Consuming {consumption} energy per second.")

        self.energy -= consumption * dt
        self.energy = max(0, self.energy)