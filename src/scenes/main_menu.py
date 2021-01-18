import random

from wasabi2d import music, clock

from src.constants import GAME_TITLE, SCREEN_WIDTH, TILE_SIZE


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
        self.relics = []

    def get_next_color(self):
        self.current_color += 1
        if self.current_color >= len(MainMenu.COLORS):
            self.current_color = 0
        return MainMenu.COLORS[self.current_color]

    def load(self):
        self.is_active = True

        music.play('menu_soundtrack')

        self.scene.layers.clear()
        self.scene.layers[0].add_label(GAME_TITLE, font='alagard_by_pix3m-d6awiwp.ttf', fontsize=50,
                                       pos=(SCREEN_WIDTH // 2, 100), align='center')
        self.animate_relics()
        self.display_goal()
        self.display_commands()

    def animate_relics(self):
        relative_pos = 0
        sep = 200
        base_x = SCREEN_WIDTH // 2 - (sep * (len(MainMenu.COLORS) - 1)) // 2
        for color in MainMenu.COLORS:
            self.relics.append(self.scene.layers[0].add_sprite(color + '_relic', pos=(base_x + relative_pos, 150)))
            relative_pos += sep
        clock.schedule_interval(self.rotate, 0.01)

    def rotate(self):
        for relic in self.relics:
            relic.angle += 0.01

    def display_goal(self):
        relative_pos = 0
        for line in MainMenu.GOAL_DESCRIPTION:
            self.scene.layers[0].add_label(line, font='alagard_by_pix3m-d6awiwp.ttf', fontsize=25,
                                           pos=(SCREEN_WIDTH // 2, 250 + relative_pos), align='center')
            relative_pos += 40

    def display_commands(self):
        commands_pos = 500
        self.scene.layers[0].add_line(
            vertices=[(400, commands_pos - 15), (SCREEN_WIDTH // 2 - (55 + 50), commands_pos - 15)])
        print(SCREEN_WIDTH // 2 - (80 + 50) - 300)
        self.scene.layers[0].add_label("COMMANDS", font='alagard_by_pix3m-d6awiwp.ttf', fontsize=40,
                                       pos=(SCREEN_WIDTH // 2 + 20, commands_pos), align='center')
        self.scene.layers[0].add_line(
            vertices=[(SCREEN_WIDTH // 2 + (75 + 50), commands_pos - 15), (SCREEN_WIDTH - 380, commands_pos - 15)])
        print((SCREEN_WIDTH - 300) - (SCREEN_WIDTH // 2 + (80 + 50)))

        dist = 40
        relative_pos = 0
        for action, cmd in MainMenu.COMMANDS.items():
            self.scene.layers[0].add_label(action + " : ", font='alagard_by_pix3m-d6awiwp.ttf', fontsize=25,
                                           pos=(SCREEN_WIDTH // 2, commands_pos + 50 + relative_pos), align='right',
                                           color=self.get_next_color())
            self.scene.layers[0].add_label(cmd, font='alagard_by_pix3m-d6awiwp.ttf', fontsize=25,
                                           pos=(SCREEN_WIDTH // 2 + 50, commands_pos + 50 + relative_pos), align='left',
                                           color=self.get_next_color())
            relative_pos += dist

    def deactivate(self):
        self.is_active = False
