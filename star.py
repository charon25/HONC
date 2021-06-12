import constants as co


class Star:
    def __init__(self, star_x, star_y, star_vx, star_vy, texture):
        self.x = star_x
        self.y = star_y
        self.vx = star_vx
        self.vy = star_vy
        self.texture = texture
        self.out = False
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > co.WIDTH or self.y < 0 or self.y > co.HEIGHT:
            self.out = True
