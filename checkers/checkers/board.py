import pygame
from .constants import BLACK, ROWS, COLS, RED, SQUARE_SIZE, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board=[]
        self.red_left = self.white_left =15
        self.red_kings = self.white_kings =0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row %2, COLS, 2): #for col in range (starting cord, ending, stepsixe):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) #rect(win, color, (position where to draw (x), position where to draw (y), width of rectangle, height of rectangle))

    '''def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (col % 2)==((row+1)%2):
                    if row<3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row>4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)'''

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range (COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (col % 2) == ((row + 1) % 2):  # Checkers pattern
                    # Place WHITE pieces in the first 3 rows (top)
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    # Place RED pieces in the last 3 rows (bottom)
                    elif row > ROWS - 4:  # Equivalent to row > 6 (for ROWS=10)
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)


    def get_valid_moves(self,piece):
        moves={}
        left=piece.col-1
        right=piece.col+1 
        row=piece.row

        if piece.color==RED or piece.king:
            moves.update(self.traverse_left(row-1,max(row-3,-1),-1,piece.color,left))
            moves.update(self.traverse_right(row-1,max(row-3,-1),-1,piece.color,right))
        if piece.color==WHITE or piece.king:
            moves.update(self.traverse_left(row+1,min(row+3,ROWS),1,piece.color,left))
            
            moves.update(self.traverse_right(row+1,min(row+3,ROWS),1,piece.color,right))
        return moves



    def traverse_left(self,start,stop,step,color,left,skipped=[]):
        moves={}
        last=[]
        for r in range(start,stop,step):
            if left < 0 or left >= COLS or r < 0 or r >= ROWS:

                break
            current=self.board[r][left]
            if current==0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,left)]=last+skipped
                else:
                    moves[(r,left)]=last
                
                if last:
                    if step==-1:
                        row=max(r-3,-1)
                    else:
                        row=min(r+3,ROWS)

                    moves.update(self.traverse_left(r+step,row,step,color,left-1,skipped=last))
                    moves.update(self.traverse_left(r+step,row,step,color,left+1,skipped=last))
                break
            elif current.color==color:
                break
            else:
                last=[current]
            
            left-=1
        return moves
    
    def traverse_right(self,start,stop,step,color,right,skipped=[]):
        moves={}
        last=[]
        for r in range(start,stop,step):
            if right < 0 or right >= COLS or r < 0 or r >= ROWS:
                break
            current=self.board[r][right]
            if current==0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)]=last+skipped
                else:
                    moves[(r,right)]=last
                
                if last:
                    if step==-1:
                        row=max(r-3,-1)
                    else:
                        row=min(r+3,ROWS)

                    moves.update(self.traverse_left(r+step,row,step,color,right-1,skipped=last))
                    moves.update(self.traverse_left(r+step,row,step,color,right+1,skipped=last))
                break
            elif current.color==color:
                break
            else:   
                last=[current]
            
            right+=1

        
        return moves

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row,col)

        if row == ROWS-1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings+=1
            else:
                self.red_kings+=1
                
    def get_piece(self, row, column):
        return self.board[row][column]
    
    def remove(self,pieces):
        for piece in pieces:
            self.board[piece.row][piece.col]=0
            if piece!=0:
                if piece.color==RED:
                    self.red_left-=1
                else:self.white_left-=1

    def winner(self):
        if self.red_left<=0:
            return WHITE
        elif self.white_left<=0:
            return RED
        
        else:
            return None
        


    def evaluate(self):
        return self.white_left -self.red_left + (self.white_kings*0.5 -self.red_kings*0.5)
    
    def get_all_pieces(self,color):
        pieces=[]
        for row in self.board:
            for piece in row:
                if piece!=0 and piece.color==color:
                    pieces.append(piece)
        return pieces