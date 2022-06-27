import arcade


class Hand(arcade.Sprite):
    """ Hand sprite """

    def __init__(self, is_opponent, is_left=False, scale=1):
        """ Hand constructor """
        super().__init__()
        self._scale = scale
        self._textures = []
        self._highlight_textures = []
        self._highlighted = False
        for i in range(0, 6):
            self._textures.append(
                arcade.load_texture(f"/Users/vnordling/PycharmProjects/pythonProject/images/hands/{i}.png",
                                    flipped_horizontally=is_left if not is_opponent else not is_left))
        for i in range(0, 6):
            self._highlight_textures.append(
                arcade.load_texture(f"/Users/vnordling/PycharmProjects/pythonProject/images/hands/{i}_highlight.png",
                                    flipped_horizontally=is_left if not is_opponent else not is_left))
        self._is_opponent = is_opponent
        self._is_left = is_left
        self._fingers = 1
        self.texture = self._textures[1]

    def tap(self, fingers):
        self._fingers += fingers
        if self._fingers >= 5:
            self._fingers = 0
        self.texture = self._textures[self._fingers]

    def set_fingers(self, fingers):
        self._fingers = fingers
        self.texture = self._textures[self._fingers]

    def update(self):
        if self._is_opponent:
            self.angle = 180

    def is_opponent(self):
        return self._is_opponent

    def is_self(self):
        return not self.is_opponent()

    def highlight(self):
        self._highlighted = True
        self.texture = self._highlight_textures[self.fingers()]

    def unhighlight(self):
        self._highlighted = False
        self.texture = self._textures[self.fingers()]

    def is_highlighted(self):
        return self._highlighted

    def fingers(self):
        return self._fingers
