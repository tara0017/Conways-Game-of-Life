import math, pygame

class block:
    def __init__(self, x, y, num_sides, r, color, screen, angle_offset = 0):

        self.x = x
        self.y = y
        self.num_sides = num_sides
        self.color = color
        self.neighbors = []
        self.angle_offset = angle_offset

        points = []
        for i in range(num_sides):
            p = (self.x + r * math.cos(angle_offset + 2 * i * math.pi / num_sides), self.y + r * math.sin(angle_offset + 2 * i * math.pi / num_sides))
            points.append(p)
        self.points = tuple(points)
        self.screen = screen
        
    def update_color(self):
        
        pygame.draw.polygon(self.screen, self.color, self.points)
