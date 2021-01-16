import random

from src.constants import GAME_TITLE, SCREEN_WIDTH


class MainMenu:
    COMMANDS = {
        'Start game': 'RETURN',
        'Movement': 'ZQSD / ARROWS',
        'Sprint': 'LSHIFT / RSHIFT',
        'Regenerate game': 'R',
        'Exit game': 'ESCAPE'
    }

    COLORS = ['red', 'blue', 'green']

    GOAL_DESCRIPTION = [
        "You have been sent by the king of the Snowmen to find the sacred color relics.",
        "They must be all found, and are probably hidden in the snow due to the storm.",
        "Their power is so high that your vision will begin to fade when you are close enough to one.",
        "Don't let the storm get the better of you.",
        "May the snow be with you."]

    def __init__(self, scene, active):
        self.scene = scene
        self.is_active = active
        self.current_color = -1

    def get_next_color(self):
        self.current_color += 1
        if self.current_color >= len(MainMenu.COLORS):
            self.current_color = 0
        return MainMenu.COLORS[self.current_color]

    def draw(self):
        self.scene.layers.clear()
        self.scene.layers[0].add_label(GAME_TITLE, font='alagard_by_pix3m-d6awiwp.ttf', fontsize=50,
                                       pos=(SCREEN_WIDTH // 2, 100), align='center'),
        self.display_goal()
        self.display_commands()

    def display_goal(self):
        relative_pos = 0
        for line in MainMenu.GOAL_DESCRIPTION:
            self.scene.layers[0].add_label(line, font='alagard_by_pix3m-d6awiwp.ttf', fontsize=25,
                                           pos=(SCREEN_WIDTH // 2, 250 + relative_pos), align='center')
            relative_pos += 40

    def display_commands(self):
        self.scene.layers[0].add_label("***** COMMANDS *****", font='alagard_by_pix3m-d6awiwp.ttf', fontsize=40,
                                       pos=(SCREEN_WIDTH // 2, 500), align='center')
        relative_pos = 0
        for action, cmd in MainMenu.COMMANDS.items():
            self.scene.layers[0].add_label(action + " : ", font='alagard_by_pix3m-d6awiwp.ttf', fontsize=25,
                                           pos=(SCREEN_WIDTH // 2, 550 + relative_pos), align='right',
                                           color=self.get_next_color())
            self.scene.layers[0].add_label(cmd, font='alagard_by_pix3m-d6awiwp.ttf', fontsize=25,
                                           pos=(SCREEN_WIDTH // 2 + 50, 550 + relative_pos), align='left',
                                           color=self.get_next_color())
            relative_pos += 40

    def deactivate(self):
        self.is_active = False
