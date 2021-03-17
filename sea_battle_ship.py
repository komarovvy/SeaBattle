class SeaBattleShip:
    _ship = {}
    
    def __init__(self, x1, y1, x2, y2):
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            self._ship = {(x1,y):True for y in range(y1, y2+1)}
        elif y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            self._ship = {(x,y1):True for x in range(x1, x2+1)}
        else:
            raise ValueError("A ship can be wether vertical or horizontal!")
            
    @property 
    def get_len(self):
        return len(self._ship)
    
    @property
    def cells(self):
        return self._ship
    
    
if __name__ == "__main__":
    print("\n"*3, "-----------")
    s = SeaBattleShip(1,2,4,2)
    print(s.cells)
    print(s.get_len)
            