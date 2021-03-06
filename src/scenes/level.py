import math
import random
import time

from wasabi2d import music
from wasabi2d.clock import clock

from src.constants import NB_TILES_HORIZONTAL, NB_TILES_VERTICAL, TILE_SIZE, LOOPS_LIMIT, TIME_PER_MSG
from src.entities.color_relic import ColorRelic
from src.entities.snowman import Snowman
from src.utilities.env_structure import EnvStructure
from src.utilities.utility_functions import get_base_name


def generate_neighbour(positions):
    neighbours = set()
    for pos in positions:
        for diff in ((0, 1), (0, -1), (-1, 0), (1, 0)):
            new_pos = (pos[0] + diff[0], pos[1] + diff[1])
            if new_pos not in positions and all([(minimum <= pos < maximum) for minimum, pos, maximum in
                                                 zip((0, 0), new_pos, (NB_TILES_HORIZONTAL, NB_TILES_VERTICAL))]):
                neighbours.add(new_pos)
    return random.choice(tuple(neighbours))


NB_ATTEMPTS = 8


def generate_valid_rect(min_width, min_height, max_width, max_height, avoid, min_dist=5, cooldown=NB_ATTEMPTS):
    width = random.randint(min_width, max_width)
    height = random.randint(min_height, max_height)
    init_pos = (
        random.randint(0, NB_TILES_HORIZONTAL - (width + 1)), random.randint(0, NB_TILES_VERTICAL - (height + 1)))
    final_pos = (init_pos[0] + width - 1, init_pos[1] + height - 1)

    for rect in avoid:
        if rect[0][0] <= final_pos[0] + min_dist and rect[1][0] + min_dist >= init_pos[0] and rect[0][1] <= final_pos[
            1] + min_dist and rect[1][1] + min_dist >= \
                init_pos[1]:
            if min_dist != 0:
                if cooldown == 0:
                    min_dist -= 1
                    cooldown = NB_ATTEMPTS
                else:
                    cooldown -= 1
            return generate_valid_rect(min_width, min_height, max_width, max_height, avoid, min_dist, cooldown)
    return init_pos, final_pos


def generate_random_rect_area(layers_content, min_width=3, min_height=3, max_width=5, max_height=5, avoid=None,
                              min_dist=5):
    if avoid is None:
        avoid = []
    init_pos, final_pos = generate_valid_rect(min_width, min_height, max_width, max_height, avoid, min_dist)

    for layer_content in layers_content:
        layer_content.layer.fill_rect(layer_content.get_content('main_content'), init_pos[0], init_pos[1],
                                      final_pos[0] + 1,
                                      final_pos[1] + 1)
        if layer_content.oriented_content:
            layer_content.layer[init_pos[0], init_pos[1]] = random.choice(layer_content.get_content('top_left'))
            layer_content.layer[final_pos[0], init_pos[1]] = random.choice(layer_content.get_content('top_right'))
            layer_content.layer[init_pos[0], final_pos[1]] = random.choice(layer_content.get_content('bottom_left'))
            layer_content.layer[final_pos[0], final_pos[1]] = random.choice(layer_content.get_content('bottom_right'))
            if final_pos[1] - init_pos[1] > 1:
                layer_content.layer.line(layer_content.get_content('left'), start=(init_pos[0], init_pos[1] + 1),
                                         stop=(init_pos[0], final_pos[1] - 1))
                layer_content.layer.line(layer_content.get_content('right'), start=(final_pos[0], init_pos[1] + 1),
                                         stop=(final_pos[0], final_pos[1] - 1))
            if final_pos[0] - init_pos[0] > 1:
                layer_content.layer.line(layer_content.get_content('top'), start=(init_pos[0] + 1, init_pos[1]),
                                         stop=(final_pos[0] - 1, init_pos[1]))
                layer_content.layer.line(layer_content.get_content('bottom'), start=(init_pos[0] + 1, final_pos[1]),
                                         stop=(final_pos[0] - 1, final_pos[1]))

    return init_pos, final_pos


def generate_random_area(layers_content, size=5):
    positions = [(random.randint(0, NB_TILES_HORIZONTAL - 1), random.randint(0, NB_TILES_VERTICAL - 1))]
    for _ in range(size - 1):
        positions.append(generate_neighbour(positions))

    for layer_content in layers_content:
        for pos in positions:
            content = 'main_content'
            if layer_content.oriented_content:
                if (pos[0] + 1, pos[1]) in positions and (pos[0] - 1, pos[1]) not in positions and (
                        pos[0], pos[1] + 1) in positions and (pos[0], pos[1] - 1) not in positions:
                    content = 'top_left'
                elif (pos[0] + 1, pos[1]) not in positions and (pos[0] - 1, pos[1]) in positions and (
                        pos[0], pos[1] + 1) in positions and (pos[0], pos[1] - 1) not in positions:
                    content = 'top_right'
                elif (pos[0] + 1, pos[1]) in positions and (pos[0] - 1, pos[1]) not in positions and (
                        pos[0], pos[1] + 1) not in positions and (pos[0], pos[1] - 1) in positions:
                    content = 'bottom_left'
                elif (pos[0] + 1, pos[1]) not in positions and (pos[0] - 1, pos[1]) in positions and (
                        pos[0], pos[1] + 1) not in positions and (pos[0], pos[1] - 1) in positions:
                    content = 'bottom_right'
            layer_content.layer[pos[0], pos[1]] = random.choice(layer_content.get_content(content))


def generate_random_tree(layer_content, avoid=None):
    if avoid is None:
        avoid = []
    init_pos, final_pos = generate_valid_rect(min_width=1, min_height=2, max_width=1, max_height=2,
                              avoid=avoid, min_dist=2)
    layer_content.layer[init_pos] = random.choice(layer_content.get_content('top'))
    layer_content.layer[final_pos] = random.choice(layer_content.get_content('bottom'))
    return init_pos,final_pos


class Level:
    def __init__(self, scene, active):
        self.scene = scene
        self.is_active = active
        self.snow_tiles = None
        self.env_tiles = None
        self.obstacles_tiles = None
        self.snowman = None
        self.color_relics = []
        self.message = None
        self.message_box = None
        self.timer = 0
        self.victory_time = 0
        self.victory_steps = 0

    def load(self):
        self.is_active = True

        music.play('level_soundtrack')

        self.scene.layers.clear()
        self.snow_tiles = None
        self.env_tiles = None
        self.obstacles_tiles = None
        self.snowman = None
        self.color_relics = []
        self.message = None
        self.message_box = None
        self.timer = time.time()

        self.generate_map()

        snowman_sprite = self.scene.layers[3].add_sprite('snowman_down_0',
                                                         pos=self.generate_available_pos(
                                                             [self.snow_tiles, self.env_tiles, self.obstacles_tiles], Snowman.BLOCKED_BY))
        self.snowman = Snowman(snowman_sprite, [self.snow_tiles, self.env_tiles, self.obstacles_tiles])

        self.generate_color_relic('red')
        self.generate_color_relic('green')
        self.generate_color_relic('blue')

        snow_storm = self.scene.layers[90].add_particle_group(texture='snowball', max_age=8, gravity=(-200, 100))
        snow_storm.add_emitter(pos=(self.scene.width, 0), pos_spread=300, angle=0.78, rate=250, size=1, size_spread=2,
                               vel=2, vel_spread=50)
        snow_storm.add_emitter(pos=(self.scene.width // 2,  self.scene.height // 2), pos_spread=300, angle=0.78, rate=250, size=1, size_spread=2,
                               vel=2, vel_spread=50)

    def generate_map(self):
        self.scene.background = '#fffafa'

        self.snow_tiles = self.scene.layers[1].add_tile_map()
        self.env_tiles = self.scene.layers[2].add_tile_map()
        self.obstacles_tiles = self.scene.layers[3].add_tile_map()

        layers_content_lakes = [
            EnvStructure(self.snow_tiles, ['boreal_lake_center'], oriented_content=True,
                         bottom_left_content='boreal_lake_bottom_left',
                         top_left_content='boreal_lake_top_left',
                         bottom_right_content='boreal_lake_bottom_right',
                         top_right_content='boreal_lake_top_right',
                         bottom_content='boreal_lake_bottom',
                         top_content='boreal_lake_top',
                         left_content='boreal_lake_left',
                         right_content='boreal_lake_right')
        ]

        lakes = []
        for _ in range(random.randint(3, 5)):
            lakes.append(
                generate_random_rect_area(layers_content_lakes, min_width=3, min_height=3, max_width=9, max_height=9,
                                          avoid=lakes, min_dist=5)
            )

        layers_content_grass = [
            EnvStructure(self.env_tiles, ['snow_grass'])
        ]

        grass_areas = []
        for _ in range(random.randint(12, 16)):
            grass_areas.append(
                generate_random_rect_area(layers_content_grass, min_width=2, min_height=2, max_width=5, max_height=5,
                                          avoid=grass_areas + lakes, min_dist=3))

        layer_content_trees_1 = EnvStructure(self.obstacles_tiles, [], oriented_content=True,
                         top_content='spruce_tree_top',
                         bottom_content='spruce_tree_bottom')
        layer_content_trees_2 = EnvStructure(self.obstacles_tiles, [], oriented_content=True,
                         top_content='spruce_tree_2_top',
                         bottom_content='spruce_tree_2_bottom')

        trees = []
        for _ in range(random.randint(20, 60)):
            trees.append(generate_random_tree(random.choice([layer_content_trees_1, layer_content_trees_2]), avoid=grass_areas + lakes + trees))

    def generate_color_relic(self, color):
        color_filter = self.scene.layers[95].add_sprite(color, pos=(self.scene.width // 2, self.scene.height // 2),
                                                        color=(1, 1, 1, 0), scale=2)
        entities_to_avoid = [
            {'entities': [self.snowman.sprite.pos],
             'min_dist': 400},
            {'entities': [cr.sprite.pos for cr in self.color_relics],
             'min_dist': 200}
        ]
        relic_pos = self.generate_pos_far_from([self.snow_tiles, self.env_tiles], ColorRelic.BLOCKED_BY,
                                               entities_to_avoid)
        color_relic_sprite = self.scene.layers[2].add_sprite(color + '_relic', pos=relic_pos, color=(1, 1, 1, 0))
        self.color_relics.append(ColorRelic(color, color_relic_sprite, [self.snow_tiles, self.env_tiles], color_filter))

    @staticmethod
    def is_pos_available(tilemaps, pos, blocking_elements):
        available = True
        for tilemap in tilemaps:
            x, y = int(pos[0] // TILE_SIZE), int(pos[1] // TILE_SIZE)
            try:
                element = tilemap[x, y]
                if get_base_name(element) in blocking_elements:
                    available = False
            except KeyError:
                pass
        return available

    def generate_pos_far_from(self, tilemaps, blocking_elements, entities_to_avoid):
        pos = (0, 0)
        far_enough_from_all = False
        loops = 0
        while not far_enough_from_all or not Level.is_pos_available(tilemaps, pos, blocking_elements):
            far_enough_from_all = True
            pos = (random.randint(TILE_SIZE // 2, self.scene.width - TILE_SIZE),
                   random.randint(TILE_SIZE // 2, self.scene.height - TILE_SIZE))
            for rule in entities_to_avoid:
                for pos_2 in rule['entities']:
                    dist = math.sqrt((pos[0] - pos_2[0]) ** 2 + (pos[1] - pos_2[1]) ** 2)
                    if not dist >= rule['min_dist']:
                        far_enough_from_all = False
            loops += 1
            if loops >= LOOPS_LIMIT:
                for rule in entities_to_avoid:
                    rule['min_dist'] *= 0.9
                return self.generate_pos_far_from(tilemaps, blocking_elements, entities_to_avoid)

        return pos

    def generate_available_pos(self, tilemaps, blocking_elements):
        pos = [self.scene.width / 2, self.scene.height / 2]

        while True:
            if Level.is_pos_available(tilemaps, pos, blocking_elements):
                return pos
            else:
                pos[0] += TILE_SIZE

    def remove_text_label(self):
        if self.message is not None and self.message_box is not None:
            self.message.delete()
            self.message_box.delete()
            self.message = None
            self.message_box = None

    def all_relics_found(self):
        return all([True if cr.visible else False for cr in self.color_relics])

    def relic_found(self, color_relic):
        if self.message:
            self.remove_text_label()

        self.message = self.scene.layers[10].add_label("You found the " + color_relic.name + " color relic !",
                                                       font='alagard_by_pix3m-d6awiwp.ttf', fontsize=30,
                                                       pos=(self.scene.width // 2, self.scene.height // 2),
                                                       align='center',
                                                       color='black')
        self.message_box = self.scene.layers[9].add_rect(width=len(self.message.text) * (self.message.fontsize // 2),
                                                         height=self.message.fontsize + 20,
                                                         fill=True)
        self.message_box.pos = (self.scene.width // 2, self.scene.height // 2 - 10)
        self.message_box.color = color_relic.name
        clock.schedule_unique(self.remove_text_label, TIME_PER_MSG)
        if self.all_relics_found():
            self.victory_time = int(time.time() - self.timer)
            self.victory_steps = int(self.snowman.nb_steps)
            clock.schedule(self.victory, TIME_PER_MSG + 0.05)

    def update(self):
        for color_relic in self.color_relics:
            if not color_relic.visible:
                if color_relic.update(self.snowman.sprite.pos):
                    self.relic_found(color_relic)

    def victory(self):
        self.message = self.scene.layers[10].add_label("You found all the relics, congratulations, it's a victory !",
                                                       font='alagard_by_pix3m-d6awiwp.ttf', fontsize=40,
                                                       pos=(self.scene.width // 2, self.scene.height // 2),
                                                       align='center',
                                                       color='white')
        self.message_box = self.scene.layers[9].add_rect(width=len(self.message.text) * (self.message.fontsize // 2),
                                                         height=self.message.fontsize + 20,
                                                         fill=True)
        self.message_box.pos = (self.scene.width // 2, self.scene.height // 2 - 10)
        self.message_box.color = 'black'

        stats_txt = "You made it in " + str(self.victory_steps) + " steps and " + str(self.victory_time) + " seconds"
        stats_fontsize = 20
        self.scene.layers[10].add_label(stats_txt,
                                        font='alagard_by_pix3m-d6awiwp.ttf', fontsize=stats_fontsize,
                                        pos=(self.scene.width // 2, self.scene.height // 2 + self.message.fontsize + 20),
                                        align='center',
                                        color='white')
        box = self.scene.layers[9].add_rect(width=len(stats_txt) * (stats_fontsize // 2),
                                            height=stats_fontsize + 20,
                                            fill=True)
        box.pos = (self.scene.width // 2, self.scene.height // 2 + self.message.fontsize + 15)
        box.color = 'black'

    def deactivate(self):
        self.is_active = False
