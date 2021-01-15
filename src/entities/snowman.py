from src.constants import NB_TILES_HORIZONTAL, NB_TILES_VERTICAL, TILE_SIZE
from src.utilities.utility_functions import get_base_name


class Snowman:
    FRAME_LIMIT = 4
    BLOCKED_BY = ['boreal_lake', 'small_pine']

    def __init__(self, sprite, layers, direction='down'):
        self.sprite = sprite
        self.direction = direction
        self.layers = layers
        self.current_frame = 0

    def move(self, direction, mvt):
        if direction != self.direction:
            self.current_frame = 0
            self.direction = direction

        if direction == 'right':
            img_direction = 'snowman_walk_right'
        elif direction == 'left':
            img_direction = 'snowman_walk_left'
        elif direction == 'down':
            img_direction = 'snowman_walk_down'
        else:
            img_direction = 'snowman_walk_up'
        self.sprite.image = img_direction + '_' + str(self.current_frame // 4)

        simulate_mvt = self.sprite.pos + mvt
        move_allowed = True
        for layer in self.layers:
            x, y = int((simulate_mvt[0] // TILE_SIZE)), int(((simulate_mvt[1] + self.sprite.height // 2) // TILE_SIZE))
            try:
                element = layer[x, y]
                if get_base_name(element) in Snowman.BLOCKED_BY:
                    move_allowed = False
            except KeyError:
                # No specific element at this position, so this is good
                pass

        if move_allowed:
            self.sprite.pos += mvt

        self.current_frame += 1
        if self.current_frame == Snowman.FRAME_LIMIT * 4:
            self.current_frame = 0
