MENU_STRUCTURE = {"select midi input device", {"display fullscreen", "show debug info", "back"}, "close menu"}


class MenuStructure:
    """class to contain an application menu and its current state"""

    def __init__(self):
        self.menu_position = list()
        self.menu_active = False
