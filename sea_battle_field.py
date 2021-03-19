import random as rnd
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
    _shots = None
    _ships = None

    def __init__(self, player_id, manually):
        self.player_id = player_id
        if manually:
            self._ships = []
            self._shots = {}
            # fill the field manually
            need_to_add = SHIPS_NUMBER.copy()
            print(f"You need to place {sum(need_to_add.values())} ships on a field: {self.show_ship_number(need_to_add)}")
            print("Enter a ship the first and the last cells in format 'line1,column1 line2,column2'")
            print(" e.g. '1,1 1,3' for horizontal 3-cell ship:")
            ship_counter = 0
            while need_to_add:
                resp = input(f" your ship #{ship_counter+1}: ")
                try:
                    self._ships.append(SeaBattleShip(*self.ship_str_to_coords(resp)))
                except ValueError:
                    print("A ship can be whether vertical (column1 = column2) or horizontal (line1 = line2)!")
                    print("Try again, please.")
                except TypeError:
                    print(f"Four integers in 1..{FIELD_SIZE} range separated by ' ' or ',' should be in input!")
                    print("Try again, please.")
                else:
                    new_ship = self._ships[-1]
                    if new_ship.len in need_to_add.keys():
                        for n, old_ship in enumerate(self._ships[:-1]):
                            if not new_ship.is_compatible(old_ship):
                                self._ships.pop()
                                print(f"This ship is conflicting with a ship #{n+1}: {old_ship.cells[0]}..{old_ship.cells[-1]}. Try again!")
                                break
                        else:
                            need_to_add[new_ship.len] -= 1
                            if need_to_add[new_ship.len] == 0:
                                need_to_add.pop(new_ship.len)
                            ship_counter += 1
                    else:
                        print("You do not need a ship of length ", new_ship.len)
                        self._ships.pop()
                self.show_text_whole(hidden=False)
                print(f"You need to place more {sum(need_to_add.values())} ships on a field: {self.show_ship_number(need_to_add)}")
        else:
            # fill the field automatically
            self._ships = []
            self._shots = {}
            # add multicell ships
            need_to_add = {ship_type: ship_num for ship_type, ship_num in SHIPS_NUMBER.items() if ship_type > 1}
            cur_cell = (rnd.randint(1,2), 1)
            for ship_type in need_to_add:
                while need_to_add[ship_type] > 0:
                    cur_cell = self.add_ship_after_cell(cur_cell, ship_type)
                    need_to_add[ship_type] -= 1
            # # flip ships diagonally
            if rnd.randint(0,1):
                for ship in self._ships:
                    ship.swap_lc()
            # add 1-cell ships
            if 1 in SHIPS_NUMBER.keys():
                for i in range(SHIPS_NUMBER[1]):
                    for cell in self.get_next_cell(init_cell=(rnd.randint(1, FIELD_SIZE), rnd.randint(1, FIELD_SIZE))):
                        test_ship = SeaBattleShip(*cell, *cell)
                        for ship in self._ships:
                            if not test_ship.is_compatible(ship):
                                break
                        else:
                            self._ships.append(test_ship)
                            break
                    else:
                        assert False, "1-cell ships can not be allocated"


    def add_ship_after_cell(self, start_cell, ship_len, tolerance=1):
        #print("Enter with a cell =", start_cell, ", ship length = ", ship_len)
        assert FIELD_SIZE >= ship_len, "Can not initialize a field: a ship is longer than a field!"
        if start_cell[0] + ship_len - 1 > FIELD_SIZE:
            assert start_cell[1] + 2 <= FIELD_SIZE, "Can not allocate multicell ships via 'parallel parking' algorithm."
            start_cell = (rnd.randint(1, 1+tolerance), start_cell[1]+2)
            if start_cell[0] + ship_len - 1 > FIELD_SIZE:
                start_cell = (1, start_cell[1])

        #print(f"Add ship {start_cell[0]},{start_cell[1]} - {start_cell[0] + ship_len - 1},{start_cell[1]}")
        self._ships.append(SeaBattleShip(start_cell[0], start_cell[1],
                                         start_cell[0] + ship_len - 1, start_cell[1]))
        return start_cell[0] + ship_len + 1, start_cell[1]

    @staticmethod
    def ship_str_to_coords(ship_str):
        try:
            result = tuple(map(int, ship_str.replace(",", " ").strip().split()))
            if len(result) == 2:
                # 1-cell ship
                result = result * 2
            elif len(result) != 4:
                raise ValueError("Exactly 4 integers (start line, column, end line, column) are expected!")
        except ValueError:
            raise TypeError("Incorrect string structure! It should consists of digits, spaces and commas.")
        else:
            if len(result) != 4:
                raise TypeError("Incorrect number of coordinates! Four numbers should be in input.")
        return result

    @staticmethod
    def show_ship_number(ship_len_num_dict):
        result = ""
        for ship_len, ship_num in ship_len_num_dict.items():
            result = result + f"{ship_num} of {ship_len}-cell, "
        return result[:-2]

    @property
    def is_not_empty(self):
        alive_ship_cells = 0
        for ship in self._ships:
            for cell in ship.cells:
                if cell not in self._shots:
                    return True
        return False

    @property
    def is_empty(self):
        return not self.is_not_empty

    @staticmethod
    def get_next_cell(init_cell=(1,1)):
        #TODO place this function out of method to aviod duplication!
        def correct_cell(cell):
            if cell[0] > FIELD_SIZE:
                cell = (1, cell[1]+1)
            if cell[1] > FIELD_SIZE:
                cell = (cell[0], 1)
            return cell

        iter_cell = init_cell
        yield iter_cell
        while True:
            iter_cell = (iter_cell[0] + 1, iter_cell[1])
            iter_cell = correct_cell(iter_cell)
            if iter_cell == init_cell:
                break
            yield iter_cell

    def get_turn(self, turn_num, manually):
        if manually:
            # get the turn manually
            while True:
                try:
                    shot_coords = tuple(map(int, input("Enter a cell to shot (line, column): ")
                                                 .replace(","," ").strip().split()))
                    if len(shot_coords) != 2:
                        raise ValueError("Exactly two integers (line and column numbers) are expected!")
                except ValueError:
                    print(f"Two integers in 1..{FIELD_SIZE} range separated by ' ' or ',' should be in input!")
                else:
                    if not (1 <= shot_coords[0] <= FIELD_SIZE and 1 <= shot_coords[1] <= FIELD_SIZE):
                        print(f"Coordinates of shot should be in 1..{FIELD_SIZE} range!")
                    elif shot_coords in self._shots.keys():
                        print(f"This cell was already attacked! Choose another cell, please.")
                    else:
                        self._shots[shot_coords] = turn_num
                        break
        else:
            # get the turn automatically
            start_cell = (rnd.randint(1, FIELD_SIZE), rnd.randint(1, FIELD_SIZE))
            for cell in self.get_next_cell(start_cell):
                if cell not in self._shots.keys():
                    self._shots[cell] = turn_num
                    break
            else:
                raise AssertionError("All the fields are shot, but some ships looks alive!")

    def is_ship_cell(self, cell):
        for ship in self._ships:
            if cell in ship.cells:
                return True
        return False

    def is_shot_cell(self, cell):
        if cell in self._shots.keys():
            return True
        return False

    def show_text_whole(self, hidden = False):
        print(f" {' '*2}  ", end="")
        for col in range(1, FIELD_SIZE+1):
            print(f" {col}  ", end="")
        print()
        # lines enumeration
        for line in range(1, FIELD_SIZE+1):
            print(f"{line:3} |", end="")
            # columns enumeration
            for col in range(1, FIELD_SIZE+1):
                cell_code = 1 + self.is_shot_cell((line, col))*2 + self.is_ship_cell((line, col))*1
                if hidden and cell_code <= 2:
                    cell_code = 0
                print(f" {CELL_SYMBOLS[cell_code]} |", end="")
            print()

    def line_by_line(self, hidden = False):
        line_str = f" {' '*2}  "
        for col in range(1, FIELD_SIZE+1):
            line_str += f" {col}  "
        yield line_str
        # lines enumeration
        for line in range(1, FIELD_SIZE+1):
            line_str = f"{line:3} |"
            # columns enumeration
            for col in range(1, FIELD_SIZE+1):
                cell_code = 1 + self.is_shot_cell((line, col))*2 + self.is_ship_cell((line, col))*1
                if hidden and cell_code <= 2:
                    cell_code = 0
                line_str += f" {CELL_SYMBOLS[cell_code]} |"
            yield line_str


if __name__ == "__main__":
    f1 = SeaBattleField("Test", manually=False)
    f1.show_text_whole(hidden=False)

    f1._shots[(1,1)] = 5
    f1._shots[(2,4)] = 7
    f1.show_text_whole(hidden=True)

    for cell in f1.get_next_cell((2,2)):
        print(cell)



