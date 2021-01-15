from wasabi2d import Scene, event, keys

from src.constants import GAME_TITLE, SCREEN_WIDTH
from src.scenes.level import Level


class MainMenu:
    def __init__(self, scene, active):
        self.scene = scene
        self.is_active = active

    def draw(self):
        self.scene.layers.clear()
        self.scene.layers[0].add_label(GAME_TITLE, font='alagard_by_pix3m-d6awiwp.ttf', fontsize=50,
                                       pos=(SCREEN_WIDTH // 2, 200), align='center'),
        self.scene.layers[0].add_label("Press return key to start playing", font='alagard_by_pix3m-d6awiwp.ttf',
                                       fontsize=22, pos=(SCREEN_WIDTH // 2, 400), align='center')

    def deactivate(self):
        self.is_active = False
