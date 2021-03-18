from sea_battle_ship import SeaBattleShip

FIELD_SIZE = 6
# [0] - hidden, [1] - empty, [2] - ship, [3] - shot empty, [4] - shot ship
CELL_SYMBOLS = ['-', '.', '#', 'x', '@']
SHIPS_NUMBER = {1: 4, 2: 2, 3: 1}
TEST_SHIP_SET = [SeaBattleShip(1,2, 3,2),
                 SeaBattleShip(6,1, 6,2),
                 SeaBattleShip(2,4, 3,4),
                 SeaBattleShip(5,4, 5,4),
                 SeaBattleShip(2,6, 2,6),
                 SeaBattleShip(4,6, 4,6),
                 SeaBattleShip(6,6, 6,6),
                 ]


class SeaBattleField:
    player_id = None
    _shots = {}
    _ships = []

    def __init__(self, player_id, manually):
        self.player_id = player_id
        if manually:
            # fill the field manually
            pass
        else:
            # fill the field automatically
            # temporary solution:
            self._ships = TEST_SHIP_SET.copy() # TODO write a random ship generator!

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

    def is_ship_cell(self, cell):
        #print("ship",cell)
        for ship in self._ships:
            if cell in ship.cells:
                return True
        return False

    def is_shot_cell(self, cell):
        #print("shot",cell)
        if cell in self._shots.keys():
            return True
        return False

    def show_text_whole(self, hidden = False):
        print(f" {' '*2}  ", end="")
        for x in range(1, FIELD_SIZE+1):
            print(f" {x}  ", end="")
        print()
        # lines enumeration
        for y in range(1, FIELD_SIZE+1):
            print(f"{y:3} |", end="")
            # columns enumeration
            for x in range(1, FIELD_SIZE+1):
                cell_code = 1 + self.is_shot_cell((x,y))*2 + self.is_ship_cell((x,y))*1
                if hidden and cell_code <= 2:
                    cell_code = 0
                print(f" {CELL_SYMBOLS[cell_code]} |", end="")
            print()


if __name__ == "__main__":
    f1 = SeaBattleField("Test", manually=False)
    f1.show_text_whole(hidden=False)

    f1._shots[(1,1)] = 5
    f1._shots[(2,4)] = 7
    f1.show_text_whole(hidden=True)

    print(True*1, True*2, False*1)
    print(f1.is_ship_cell((1,2)))

