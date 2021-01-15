import math


class ColorRelic:
    BLOCKED_BY = ['boreal_lake', 'small_pine']

    def __init__(self, name, sprite, layers, color_filter):
        self.name = name
        self.sprite = sprite
        self.layers = layers
        self.visible = False
        self.color_filter = color_filter

    def update(self, snowman_pos):
        dist = math.sqrt((snowman_pos[0] - self.sprite.pos[0]) ** 2 + (snowman_pos[1] - self.sprite.pos[1]) ** 2)
        if dist < 10:
            self.visible = True
            self.sprite.color = (self.sprite.color[0], self.sprite.color[1], self.sprite.color[2], 1)
            self.color_filter.delete()
            return True
        ratio = dist / 40
        transparency = 1 / ratio if ratio >= 1.25 else 0.8
        print(transparency)
        self.color_filter.color = (self.color_filter.color[0], self.color_filter.color[1], self.color_filter.color[2],
                                   transparency)
        return False
