from wasabi2d import run, Scene, event, keys

from settings import SNOWMAN_SPEED
from src.scenes.level import Level
from src.scenes.main_menu import MainMenu
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE

if __name__ == "__main__":
    scene = Scene(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, rootdir='.')
    main_menu = MainMenu(scene, True)
    level = Level(scene, False)
    main_menu.draw()

    @event
    def on_key_up(key):
        if key == keys.RETURN:
            if main_menu.is_active:
                main_menu.deactivate()
                level.is_active = True
                level.build()
        if key == keys.R and level.is_active:
            level.build()
        if key == keys.ESCAPE:
            exit()


    @event
    def update(dt, keyboard):
        speed = SNOWMAN_SPEED
        speed_up = False
        if keyboard.lshift or keyboard.rshift:
            speed_up = True
            speed *= 2
        v = speed * dt

        if level.is_active:
            if keyboard.right or keyboard.d:
                level.snowman.move('right', (v, 0), speed_up)
            elif keyboard.left or keyboard.q:
                level.snowman.move('left', (-v, 0), speed_up)
            elif keyboard.up or keyboard.z:
                level.snowman.move('up', (0, -v), speed_up)
            elif keyboard.down or keyboard.s:
                level.snowman.move('down', (0, v), speed_up)
            level.update()

    @event
    def on_mouse_up(pos, button):
        print("Mouse button ", button, " clicked at ", pos)

    run()
