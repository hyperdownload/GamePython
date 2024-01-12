class Block:
    def __init__(self, x, y, block_type, collidable,kill=None, texture=None, color=None):
        self.x = x
        self.y = y
        self.collidable = collidable
        self.block_type = block_type
        self.width = 50
        self.height = 50
        self.texture = texture
        self.color = color
        self.morido = kill
        if not self.morido:
            self.morido = False
        if not self.texture and not self.color:
            self.color = (255, 0, 255)#asdasdasdasdas
