import constants as co


class Particle:
    def __init__(self, part_x, part_y, part_vx, part_vy, texture):
        self.x = part_x
        self.y = part_y
        self.vx = part_vx
        self.vy = part_vy
        self.texture = texture
        self.life = co.PARTICLE_DURATION
        self.done = False
    
    def age(self):
        self.x += self.vx
        self.y += self.vy

        self.life -= 1
        if self.life <= 0:
            self.done = True
