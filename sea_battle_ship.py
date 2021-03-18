class SeaBattleShip:
    _cells_xy = []
    _cells_alive = []
    _vertical = None
    
    def __init__(self, x1, y1, x2, y2):
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            self._cells_xy = [(x1, y) for y in range(y1, y2+1)]
            self._cells_alive = [True] * (y2-y1+1)
            self._vertical = True
        elif y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            self._cells_xy = [(x, y1) for x in range(x1, x2+1)]
            self._cells_alive = [True] * (x2-x1+1)
            self._vertical = False
        else:
            raise ValueError("A ship can be whether vertical or horizontal!")
            
    @property 
    def len(self):
        return len(self._cells_xy)
    
    @property
    def cells(self):
        return list(zip(self._cells_xy, self._cells_alive))

    @property
    def close_area_rect(self):
        cell_min = self._cells_xy[0]
        cell_max = self._cells_xy[-1]
        # returns (x1,y1,x2,y2) of the ship "own" area
        return (cell_min[0]-1, cell_min[1]-1, cell_max[0]+1, cell_max[1]+1)

    def is_compatible(self, another_ship):
        x_min, y_min, x_max, y_max = another_ship.close_area_rect
        for cell in self._cells_xy:
            if x_min <= cell[0] <= x_max and y_min <= cell[1] <= y_max:
                return False
        return True

if __name__ == "__main__":
    print("\n"*3, "-----------")
    s1 = SeaBattleShip(1,2,4,2)
    print(s1.cells)
    print(s1.len)
    print(s1.close_area_rect)

    s2 = SeaBattleShip(6,3,5,3)
    print(s2.cells)
    print(s2.is_compatible(s1))
