class SeaBattleShip:
    _cells_lc = []
    _vertical = None
    
    def __init__(self, line1, col1, line2, col2):
        if line1 == line2:
            if col1 > col2:
                col1, col2 = col2, col1
            self._cells_lc = [(line1, col) for col in range(col1, col2+1)]
            self._vertical = False
        elif col1 == col2:
            if line1 > line2:
                line1, line2 = line2, line1
            self._cells_lc = [(line, col1) for line in range(line1, line2+1)]
            self._vertical = True
        else:
            raise ValueError("A ship can be whether vertical or horizontal!")
            
    @property 
    def len(self):
        return len(self._cells_lc)
    
    @property
    def cells(self):
        return self._cells_lc

    @property
    def close_area_rect(self):
        cell_min = self._cells_lc[0]
        cell_max = self._cells_lc[-1]
        # returns (line1,col1,line2,col2) of the ship "own" area
        return (cell_min[0]-1, cell_min[1]-1, cell_max[0]+1, cell_max[1]+1)

    def is_compatible(self, another_ship):
        line_min, col_min, line_max, col_max = another_ship.close_area_rect
        for cell in self._cells_lc:
            if line_min <= cell[0] <= line_max and col_min <= cell[1] <= col_max:
                return False
        return True
    
    def swap_lc(self):
        for i in range(len(self._cells_lc)):
            self._cells_lc[i] = (self._cells_lc[i][1], self._cells_lc[i][0])
        
        

if __name__ == "__main__":
    print("\n"*3, "-----------")
    s1 = SeaBattleShip(1,2,4,2)
    print(s1.cells)
    print(s1.len)
    print(s1.close_area_rect)

    s2 = SeaBattleShip(6,3,5,3)
    print(s2.cells)
    print(s2.is_compatible(s1))
