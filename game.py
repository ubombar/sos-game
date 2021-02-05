import numpy as np 

class GameBoard():
    SYMBOL = {' ': 0, 'S': 1, 'O': 2}
    NUMBER = {0: ' ', 1: 'S', 2: 'O'}
    S = 1
    O = 2
    E = 0
    DECORATORS = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, dim=8):
        self.table = np.zeros((dim, dim))
        self.dim = dim
        self.player1: Player = None
        self.player2: Player = None
        self.turnOnP1 = True
        self.finished = False

    def turn(self):
        if self.finished:
            return 
        
        name = self.player1.name if self.turnOnP1 else self.player2.name

        print(self)
        print(f"{name}'s turn")

        if self.turnOnP1:
            resign = self.player1.decide()
        else:
            resign = self.player2.decide()
        
        if resign or self.finished:
            print(f'{name} resigned...')
            self.finished = True
            self.annonuce()

        self.turnOnP1 = not self.turnOnP1

    def inside(self, i, j):
        return i >= 0 and j >= 0 and i < self.dim and j < self.dim
    
    def equal(self, i, j, n):
        if self.inside(i, j):
            return self.table[i, j] == n
        return False

    def checkScores(self, i, j, n):
        if n == GameBoard.O:
            increment = 0
            if self.equal(i-1, j-1, GameBoard.S) and self.equal(i+1, j+1, GameBoard.S): 
                increment += 1
            if self.equal(i, j-1, GameBoard.S) and self.equal(i, j+1, GameBoard.S): 
                increment += 1
            if self.equal(i-1, j, GameBoard.S) and self.equal(i+1, j, GameBoard.S): 
                increment += 1
            if self.equal(i+1, j-1, GameBoard.S) and self.equal(i-1, j+1, GameBoard.S): 
                increment += 1
        elif n == GameBoard.S:
            increment = 0
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0: continue
                    if not self.equal(i + di, j + dj, GameBoard.O): continue

                    if self.equal(i + 2*di, j + 2*dj, GameBoard.S):
                        increment += 1

        if self.turnOnP1:
            self.player1.score += increment
        else:
            self.player2.score += increment

    def play(self, i, j, n):
        if self.inside(i, j):
            if self.table[i, j] == GameBoard.E:
                self.table[i, j] = n
                self.checkScores(i, j, n)
                self.finished = not GameBoard.E in self.table
                return True
        return False

    def annonuce(self):
        print('-------------------- FIN --------------------')
        if self.player1.score > self.player2.score:
            print(f'And {self.player1.name} won!')
        elif self.player1.score < self.player2.score:
            print(f'And {self.player2.name} won!')
        else:
            print("And it's a tie :(")
        
        print()
    
    def __str__(self):
        buffer = '{:25} {:25}'.format(f'{self.player1.name} scored {self.player1.score}', f'{self.player2.name} scored {self.player2.score}')
        buffer += '\n   '
        for i in range(self.dim):
            buffer += f'  {GameBoard.DECORATORS[i]} '
        buffer += ('\n   ')

        for i in range(self.dim):
            for j in range(self.dim):
                buffer += '+---'
            buffer += ('+\n{:2} '.format(i + 1))
            for j in range(self.dim):
                buffer += (f'|')
                buffer += f' {GameBoard.NUMBER[self.table[i, j]]} '
            buffer += ('|\n   ')
        for j in range(self.dim):
            buffer += '+---'
        buffer += ('+\n   ')
        return buffer

class Player():
    def __init__(self, board: GameBoard, name: str):
        self.board = board
        self.name = name
        self.score = 0
    
    def decide(self):
        raise NotImplementedError()

class BotPlayer(Player):
    def decide(self):
        self.board.play(0, 0, GameBoard.S)

class RealPlayer(Player):
    def decide(self):
        while True:
            try:
                print("format {<num><letter>}<symbol> to play (or 're' to resign): ", end="")
                raw = input()
                if 're' in raw:
                    return True

                processed = raw.replace(' ', '')
                assert len(processed) == 3

                i = -1
                for n in range(board.dim + 1):
                    if str(n) in processed:
                        i = n
                        break

                j = -1
                for c in board.DECORATORS:
                    if c in processed.lower():
                        j = board.DECORATORS.index(c)
                        break
                
                assert processed.upper().endswith('S') or processed.upper().endswith('O')
                s = processed[-1].upper()
                valid = self.board.play(i - 1, j, GameBoard.SYMBOL[s])

                # print(i, j, s, valid)
                assert valid == True
                return
            except AssertionError:
                print("move is not valid please enter again!")
        return False

board = GameBoard(16)
board.player1 = RealPlayer(board, "Bombar")
board.player2 = RealPlayer(board, "Dr. Dushenschwartz")

while not board.finished:
    board.turn()