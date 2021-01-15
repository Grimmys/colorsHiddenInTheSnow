class EnvStructure:
    def __init__(self, layer, content, oriented_content=False, bottom_left_content=None, top_left_content=None, bottom_right_content=None, top_right_content=None, bottom_content=None, top_content=None, left_content=None, right_content=None):
        self.layer = layer
        self.oriented_content = oriented_content
        self.main_content = content
        self.oriented_content = {
            "bottom_left": [bottom_left_content],
            "top_left": [top_left_content],
            "bottom_right": [bottom_right_content],
            "top_right": [top_right_content],
            "bottom": [bottom_content],
            "top": [top_content],
            "left": [left_content],
            "right": [right_content]
        }
        self.correct_content()

    def correct_content(self):
        if not self.main_content:
            self.main_content = [None]

        for key in self.oriented_content.keys():
            if self.oriented_content[key] == [None]:
                self.oriented_content[key] = self.main_content

    def get_content(self, key):
        if key == 'main_content':
            return self.main_content
        else:
            return self.oriented_content[key]
