import chess
import time
import random as rand

class Engine:

    #initializes game based off difficulty and player's color
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.color = color
        self.maxDepth = maxDepth

    #determine best move
    def getBestMove(self):
        return self.engine(None, 1)

    #checks the value of the entire board
    def checkValue(self):
        compt = 0
        for i in range(64):
            compt+=self.squareResPoints(chess.SQUARES[i])
        compt += self.checkForMate() + self.opening() + 0.001*rand.random()
        return compt

    #check if checkmate can occur
    def checkForMate(self):
        if (self.board.legal_moves.count()==0):
            if (self.board.turn == self.color):
                return -999
            else:
                return 999
        else:
            return 0

    #develop the chess engine during the opening moves of the game
    def opening(self):
        if (self.board.fullmove_number<10):
            if (self.board.turn == self.color):
                return 1/30 * self.board.legal_moves.count()
            else:
                return -1/30 * self.board.legal_moves.count()
        else:
            return 0

    #determines the value of a square on the board based on the Hans Berliner system
    def squareResPoints(self, square):
        pieceValue = 0
        if(self.board.piece_type_at(square) == chess.PAWN):
            pieceValue = 1
        elif (self.board.piece_type_at(square) == chess.ROOK):
            pieceValue = 5.1
        elif (self.board.piece_type_at(square) == chess.BISHOP):
            pieceValue = 3.33
        elif (self.board.piece_type_at(square) == chess.KNIGHT):
            pieceValue = 3.2
        elif (self.board.piece_type_at(square) == chess.QUEEN):
            pieceValue = 8.8

        if (self.board.color_at(square)!=self.color):
            return -pieceValue
        else:
            return pieceValue

    
    def engine(self, possibleMove, depth):
        
        #check if at the maxDepth or if no more moves exist
        if ( depth == self.maxDepth
        or self.board.legal_moves.count() == 0):
            return self.checkValue()
        
        else:
            #get list of legal moves of the current position
            moveList = list(self.board.legal_moves)
            
            #initialise newPossibleMove
            newPossibleMove = None
            #odd depth indicates its the engine's turn
            if(depth % 2 != 0):
                newPossibleMove = float("-inf")
            else:
                newPossibleMove = float("inf")
            
            #check the board after deeper moves
            for i in moveList:

                #play move
                self.board.push(i)

                #get value of move
                value = self.engine(newPossibleMove, depth + 1) 

                #minmax algorithm, maximizes on engine's turn, minimizes on player's turn
                if(value > newPossibleMove and depth % 2 != 0):
                    if (depth == 1):
                        move = i
                    newPossibleMove = value

                elif(value < newPossibleMove and depth % 2 == 0):
                    newPossibleMove = value

                #alpha-beta pruning based on whose turn it is
                if (possibleMove != None
                 and value < possibleMove
                 and depth % 2 == 0):
                    self.board.pop()
                    break
                
                elif (possibleMove != None 
                and value > possibleMove 
                and depth % 2 != 0):
                    self.board.pop()
                    break
                
                #undo the past turn
                self.board.pop()

            
            if (depth>1):
                #return value of a move in the tree
                return newPossibleMove
            else:
                #return the move if its the first move
                return move
            
class Main:

    def __init__(self, board = chess.Board):
        self.board = board

    #play human move
    def playHumanMove(self):
        try:
            print(self.board.legal_moves)
            print("""To undo your last move, type "undo".""")

            #get user's move
            play = input("Your move: ")

            #step back two turns on "undo"
            if (play == "undo"):
                self.board.pop()
                self.board.pop()
                self.playHumanMove()
                return

            self.board.push_san(play)
        except:
            self.playHumanMove()

    #play engine move and check time passes
    def playEngineMove(self, maxDepth, color):
        startTimer = time.time()
        engine = Engine(self.board, maxDepth, color)
        self.board.push(engine.getBestMove())
        endTimer = time.time()
        print(endTimer - startTimer)

    #start a game
    def startGame(self):
        #get human player's color
        color = None
        while(color != "b" and color != "w"):
            color = input("""Play as (type "b" or "w"): """)
        maxDepth = None
        while(isinstance(maxDepth, int) == False):
            difficulty = input("""Choose difficulty (type "easy," "medium," or "hard"): """)
            
            if difficulty == "easy":
                maxDepth = 2
            elif difficulty == "medium":
                maxDepth = 3
            elif difficulty == "hard":
                maxDepth = 4
            
        #run game based off player's color
        if color == "b":
            while (self.board.is_checkmate() == False):
                print("Calculating moves...")
                self.playEngineMove(maxDepth, chess.WHITE)
                print(self.board)
                self.playHumanMove()
                print(self.board)
            print(self.board)
            print(self.board.outcome())   
         
        elif color == "w":
            while (self.board.is_checkmate() == False):
                print(self.board)
                self.playHumanMove()
                print(self.board)
                print("Calculating moves...")
                self.playEngineMove(maxDepth, chess.BLACK)
            print(self.board)
            print(self.board.outcome())
        
        #reset the board
        self.board.reset
        #start another game
        self.startGame()

#create an instance and start a game
newBoard = chess.Board()
game = Main(newBoard)
game.startGame()
