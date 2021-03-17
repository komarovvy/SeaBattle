FIELD_SIZE = 6
SHIPS_NUMBER = {1:4, 2:3, 3:2, 4:1}
TEST_SHIP_SET = [
              ]


class SeaBattleField:
    player_id = None
    _field = [[0 for j in range(FIELD_SIZE)] for i in range(FIELD_SIZE)]
    _ships_position = []

    def __init__(self, player_id, manually):
        self._player_id = player_id
        if manually:
            # fill the field manually
            pass
        else:
            # fill the field automatically
            pass

    @property
    def is_not_empty(self):
        return True

    @property
    def is_empty(self):
        return not self.is_not_empty

    def get_turn(self, manually):
        if manually:
            # get the turn manually
            pass
        else:
            # get the turn automatically
            pass

    def show_text_whole(self):
        for l_num, lines in enumerate(self._field):
            print(f"{l_num:3} |", end="")
            for cell in lines:
                print(f" {cell} |", end="")
            print()