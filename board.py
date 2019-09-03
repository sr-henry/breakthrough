import random

class Board:
    def __init__(self, lines, columns):
        self.lines = lines
        self.columns = columns
        self.white_positions = []
        self.black_positions = []

        for c in range(1, self.columns + 1):
            self.white_positions.append((1, c))
            #self.white_positions.append((2, c))
            self.black_positions.append((self.lines, c))
            #self.black_positions.append((self.lines - 1, c))


    def generate_random_position(self):
        self.white_positions.clear()
        self.black_positions.clear()

        middle_rows = int(self.lines/2)
        middle_columns = int(self.columns/2)
        half_area = middle_rows * middle_columns
        n_pieces = random.randint(2, half_area)

        wp = 0
        while wp <= n_pieces:
            row = random.randint(1, middle_rows)
            column = random.randint(1, self.columns)
            position = (row, column)
            if position not in self.white_positions:
                self.white_positions.append(position)
                wp += 1

        bp = 0
        while bp <= n_pieces:
            row = random.randint(middle_rows, self.lines)
            column = random.randint(1, self.columns)
            position = (row, column)
            if position not in self.black_positions:
                self.black_positions.append(position)
                bp += 1


    def display(self):
        for r in range(self.lines, 0, -1):
            print(r, end = " ")
            for c in range(1, self.columns + 1):
                if (r, c) in self.white_positions:
                    print("w", end = " ")
                elif (r, c) in self.black_positions:
                    print("b", end = " ")
                else:
                    print(".", end = " ")
            print()
        print("  ", end = "")
        for x in range(1, self.columns + 1):
            print(x, end = " ")
        print("\n\n")


    def white_valid_move(self, move):
        if not move :
            return False
        
        origem, destino = move

        if not 0 < origem[0]  <= self.lines :
            return False
        if not 0 < destino[0] <= self.lines :
            return False
        if not 0 < origem[1]  <= self.columns :
            return False
        if not 0 < destino[1] <= self.columns :
            return False
        
        if not origem in self.white_positions :
            return False
        
        if destino in self.white_positions :
            return False
        
        if not (destino[0] - origem[0] == 1 and 
            abs(destino[1] - origem[1]) <= 1) :
            return False
            
        if (origem[1] == destino[1]) :
            if destino in self.black_positions :
                return False
        return True


    def black_valid_move(self, move):
        if not move :
            return False
        
        origem, destino = move
        
        if not self.lines >= origem[0]  > 0:
            return False
        if not self.lines >= destino[0] > 0:
            return False
        if not 0 < origem[1]  <= self.columns :
            return False
        if not 0 < destino[1] <= self.columns :
            return False
        
        if not origem in self.black_positions :
            return False
        
        if destino in self.black_positions :
            return False
        
        if not (destino[0] - origem[0] == -1 and abs(destino[1] - origem[1]) <= 1) :
            return False
            
        if (origem[1] == destino[1]) :
            if destino in self.white_positions :
                return False
        return True


    def white_possible_moves(self):
        possible_moves = []

        for origin in self.white_positions:
            destiny = origin[0]+1, origin[1]-1
            if self.white_valid_move((origin, destiny)):
                possible_moves.append((origin, destiny))
                
            destiny = origin[0]+1, origin[1]
            if self.white_valid_move((origin, destiny)):
                possible_moves.append((origin, destiny))
                
            destiny = origin[0]+1, origin[1]+1
            if self.white_valid_move((origin, destiny)):
                possible_moves.append((origin, destiny))

        return possible_moves


    def black_possible_moves(self):
        possible_moves = []

        for origin in self.black_positions:
            destiny = origin[0]-1, origin[1]-1
            if self.black_valid_move((origin, destiny)):
                possible_moves.append((origin, destiny))
                
            destiny = origin[0]-1, origin[1]
            if self.black_valid_move((origin, destiny)):
                possible_moves.append((origin, destiny))
                
            destiny = origin[0]-1, origin[1]+1
            if self.black_valid_move((origin, destiny)):
                possible_moves.append((origin, destiny))

        return possible_moves

    
    def perform_white_move(self, move):
        if not self.white_valid_move(move):
            return False
        
        origem, destino = move    
        
        self.white_positions.remove(origem)    
        self.white_positions.append(destino)
        
        if destino in self.black_positions :
            self.black_positions.remove(destino)
        return True


    def perform_black_move(self, move):
        if not self.black_valid_move(move):
            return False
        
        origem, destino = move    
        
        self.black_positions.remove(origem)    
        self.black_positions.append(destino)
        
        if destino in self.white_positions :
            self.white_positions.remove(destino)
        return True

    
    def evaluation(self):
        ## Value of Pieces
        value_pieces = 0
        for v in range(1, self.lines + 1):
            pieces_w = list(filter(lambda pos: pos[0] == v, self.white_positions))
            pieces_b = list(filter(lambda pos: pos[0] == (9 - v), self.black_positions))
            value_pieces += v*(len(pieces_w) - len(pieces_b))

        ## Mobility (the number of legal moves)
        white_legal_moves = self.white_possible_moves()
        black_legal_moves = self.black_possible_moves()
        mobility = len(white_legal_moves) - len(black_legal_moves)

        ## Blocked Pieces
        white_origins = set(map(lambda move: move[0], white_legal_moves))
        black_origins = set(map(lambda move: move[0], black_legal_moves))
        white_positions_blocked = len(self.white_positions) - len(white_origins)
        black_positions_blocked = len(self.black_positions) - len(black_origins) 
        blocks = white_positions_blocked - black_positions_blocked    

        ## Connectivity

        ## Evaluation
        score = value_pieces + .2*mobility - .5*blocks

        return score


    def game_is_over(self):
        for wp in self.white_positions:
            if wp[0] == self.lines:
                return True

        for bp in self.black_positions:
            if bp[0] == 1:
                return True

        return False
    

    def turn(self):
        new_white = []
        new_black = []
        
        for coord in self.black_positions :
            new_white.append((self.lines-coord[0]+1, self.columns-coord[1]+1))
        for coord in self.white_positions :
            new_black.append(( self.lines-coord[0]+1, self.columns-coord[1]+1))
        
        self.white_positions = new_white
        self.black_positions = new_black
