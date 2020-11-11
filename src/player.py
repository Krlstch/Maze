class Player:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def get_pos_int(self):
        return int(self.x), int(self.y)

    def get_rect(self):
        return (int(self.x - self.width / 2),
                int(self.y - self.height / 2),
                self.width,
                self.height)
