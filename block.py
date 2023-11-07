class Block:
    def __init__(self, x, y, block_type, collidable, texture=None, color=None):
        self.x = x
        self.y = y
        self.collidable = collidable
        self.block_type = block_type
        self.width = 50
        self.height = 50
        self.texture = texture
        self.color = color

        if not self.texture and not self.color:
            self.color = (255, 0, 255)
