import arcade
import os
from hand import Hand

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Full Screen Example"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 40

MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        # Open a window in full screen mode. Remove fullscreen=True if
        # you don't want to start this way.
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=False)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # This will get the size of the window, and set the viewport to match.
        # So if the window is 1000x1000, then so will our viewport. If
        # you want something different, then use those coordinates instead.
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.example_image = arcade.load_texture(":resources:images/tiles/boxCrate_double.png")
        # self.example_image2 = arcade.load_texture(":resources:images/hands/one.png")
        self.hands = None
        self.my_turn = True
        self.cpu_hand_left = None
        self.cpu_hand_right = None
        self.hand_left = None
        self.hand_right = None

    def setup(self):
        self.hands = arcade.SpriteList()
        cpu_hand_left = Hand(is_opponent=True, is_left=True)
        cpu_hand_right = Hand(is_opponent=True)
        cpu_hand_left.position = 300, 510
        cpu_hand_right.position = 500, 510
        my_hand_left = Hand(is_opponent=False, is_left=True)
        my_hand_right = Hand(is_opponent=False)
        my_hand_left.position = 300, 90
        my_hand_right.position = 500, 90
        self.hands.append(cpu_hand_left)
        self.hands.append(cpu_hand_right)
        self.hands.append(my_hand_left)
        self.hands.append(my_hand_right)
        self.cpu_hand_left = cpu_hand_left
        self.cpu_hand_right = cpu_hand_right
        self.hand_left = my_hand_left
        self.hand_right = my_hand_right


    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.hands.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.hands.update()

    def on_mouse_press(self, x, y, button, modifiers):
        print("Mouse button is pressed")
        sprite_clicked = arcade.get_sprites_at_point((x, y), self.hands)
        if sprite_clicked:
            hand = sprite_clicked[0]
            highlighted_hand = self.get_highlighted_hand()
            print("Highlighted hand: ", highlighted_hand)
            if hand.is_self() and self.my_turn and hand.fingers() > 0 and highlighted_hand is None:
                hand.highlight()
            elif not hand.is_self() and not self.my_turn and hand.fingers() > 0 and highlighted_hand is None:
                hand.highlight()
            elif (hand.is_self() and self.my_turn and highlighted_hand is not None and highlighted_hand.is_self()) or (
                    not hand.is_self() and not self.my_turn and highlighted_hand is not None and not highlighted_hand.is_self()):
                if hand.fingers() == 0:
                    # divisions
                    if highlighted_hand.fingers() == 4:
                        # TODO: show choice thingy, for now, just do 2 / 2
                        hand.set_fingers(2)
                        highlighted_hand.set_fingers(2)
                        self.remove_highlight()
                        self.my_turn = not self.my_turn
                    elif highlighted_hand.fingers() == 2:
                        hand.set_fingers(1)
                        highlighted_hand.set_fingers(1)
                        self.remove_highlight()
                        self.my_turn = not self.my_turn
                    elif highlighted_hand.fingers() == 3:
                        hand.set_fingers(1)
                        highlighted_hand.set_fingers(2)
                        self.remove_highlight()
                        self.my_turn = not self.my_turn
                else:
                    # transfers
                    if (hand.fingers() == 3 and highlighted_hand.fingers() == 1) or (
                            hand.fingers() == 1 and highlighted_hand.fingers() == 3):
                        hand.set_fingers(2)
                        highlighted_hand.set_fingers(2)
                        self.remove_highlight()
                        self.my_turn = not self.my_turn
                    elif hand.fingers() == 2 and highlighted_hand.fingers() == 2:
                        hand.set_fingers(1)
                        highlighted_hand.set_fingers(3)
                        self.remove_highlight()
                        self.my_turn = not self.my_turn
                    elif (hand.fingers() == 1 and highlighted_hand.fingers() == 4) or (
                            hand.fingers() == 4 and highlighted_hand.fingers() == 1):
                        hand.set_fingers(2)
                        highlighted_hand.set_fingers(3)
                        self.remove_highlight()
                        self.my_turn = not self.my_turn
                    elif (hand.fingers() == 2 and highlighted_hand.fingers() == 3) or (
                            hand.fingers() == 3 and highlighted_hand.fingers() == 2):
                        hand.set_fingers(1)
                        highlighted_hand.set_fingers(4)
                        self.remove_highlight()
                        self.my_turn = not self.my_turn
                    elif (hand.fingers() == 2 and highlighted_hand.fingers() == 4) or (
                            hand.fingers() == 4 and highlighted_hand.fingers() == 2):
                        hand.set_fingers(3)
                        highlighted_hand.set_fingers(3)
                        self.remove_highlight()
                        self.my_turn = not self.my_turn
                    elif hand.fingers() == 3 and highlighted_hand.fingers() == 3:
                        hand.set_fingers(2)
                        highlighted_hand.set_fingers(4)
                        self.remove_highlight()
                        self.my_turn = not self.my_turn
            elif highlighted_hand is not None:
                fingers = self.get_highlighted_finger_count()
                hand.tap(fingers)
                self.remove_highlight()
                self.my_turn = not self.my_turn

        if not self.my_turn:
            if self.cpu_hand_left.fingers() == 0:
                self.cpu_hand_right.highlight()


        print("Clicked: ", hand)

    def get_highlighted_hand(self):
        for hand in self.hands:
            print("FOUND HIGHLIGHTED HAND")
            if hand.is_highlighted():
                return hand
        return None

    def get_highlighted_finger_count(self):
        for hand in self.hands:
            if hand.is_highlighted():
                return hand.fingers()
        return 0

    def remove_highlight(self):
        for hand in self.hands:
            hand.unhighlight()
        return 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)

        if key == arcade.key.S:
            # User hits s. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Instead of a one-to-one mapping, stretch/squash window to match the
            # constants. This does NOT respect aspect ratio. You'd need to
            # do a bit of math for that.
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
