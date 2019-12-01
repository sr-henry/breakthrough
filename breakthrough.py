WHITE = True
BLACK = False

class Board(object):
    def __init__(self, lines = 8, columns = 8, white_positions = [], black_positions = []):
        self.lines = lines
        self.columns = columns
        self.white_positions =  white_positions
        self.black_positions = black_positions
        self.black_directions = [(-1, 0), (-1, -1), (-1, 1)]
        self.white_directions = [(1, 0), (1, 1), (1, -1)]
        self.init() if not white_positions and not black_positions else None


    def __str__(self):
        return self.__to_print__()


    def init(self):
        if not (self.white_positions and self.black_positions):
            for c in range(1, self.columns + 1):
                self.white_positions.append((1, c))
                self.white_positions.append((2, c))
                self.black_positions.append((self.lines, c))
                self.black_positions.append((self.lines - 1, c))


    def __to_print__(self):
        print_board = ""
        for l in range(self.lines, 0, -1):
            for c in range(1, self.columns + 1):
                print_board += "w " if (l, c) in self.white_positions else\
                    "b " if (l, c) in self.black_positions else\
                    ". "
            print_board += "\n"
        return print_board


    def serialise(self):
        serialised_board = ""
        i = 0
        for l in range(self.lines, 0, -1):
            for c in range(1, self.columns + 1):
                if (l, c) in self.white_positions:
                    serialised_board += "w"
                elif (l, c) in self.black_positions:
                    serialised_board += "b"
                else:
                    serialised_board += "."
        return serialised_board


    def is_black_move(self, move_type):
        if move_type not in self.white_directions:
            if move_type in self.black_directions:
                return True
            else:
                return None
        return False


    def is_valid(self, move):
        if not move:
            return False

        origin, destination = move

        move_type = destination[0] - origin[0], destination[1] - origin[1]

        black_move = self.is_black_move(move_type)
        
        is_inside = True if 0 < origin[0] <= self.lines and\
                    0 < origin[1] <= self.columns and\
                    0 < destination[0] <= self.lines and\
                    0 < destination[1] <= self.columns\
                    else False
        
        if not is_inside or black_move is None:
            return False

        if black_move:
            integrity = True if origin in self.black_positions and\
                        destination not in self.black_positions else False
        else:
            integrity = True if origin in self.white_positions and\
                destination not in self.white_positions else False

        if not integrity:
            return False

        if origin[1] == destination[1]:
            if destination in self.white_positions or destination in self.black_positions:
                return False
        
        return True

        
    def possible_moves(self, piece_type):
        possible_moves = []

        piece_positions = self.white_positions if piece_type else self.black_positions
        directions = self.white_directions if piece_type else self.black_directions

        for x, y in piece_positions:
            for i, j in directions:
                move = ((x, y), (x + i, y + j))
                if self.is_valid(move):
                    possible_moves.append(move)

        return possible_moves
    

    def perform_move(self, move):
        if not move:
            return False

        origin, destination = move

        move_type = destination[0] - origin[0], destination[1] - origin[1]
        black_move = self.is_black_move(move_type)

        if black_move and not black_move is None:
            self.black_positions.remove(origin)
            self.black_positions.append(destination)
            if destination in self.white_positions:
                self.white_positions.remove(destination)
            return True
        else:
            self.white_positions.remove(origin)
            self.white_positions.append(destination)
            if destination in self.black_positions:
                self.black_positions.remove(destination)
            return True
        return False


    def is_gameover(self):
        for wp in self.white_positions:
            if wp[0] == self.lines:
                return True
        for bp in self.black_positions:
            if bp[0] == 1:
                return True
        return False
    
    def coordinates(self):
        for l in range(self.lines, 0, -1):
            for c in range(1, self.columns + 1):
                print("(%d, %d)"%(l, c), end=" ")
            print()
    
    def reset(self):
        self.white_positions.clear()
        self.black_positions.clear()
        self.init()

