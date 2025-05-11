from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame

class Piece:
    
    PADDING =15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king=False
        # white side will be up and the direction we moving will be positive, (up to down)
        # red side will be down and the direction we moving will be negative, (down to up)
        if self.color == RED:
            self.direction=-1
        else:
            self.direction =1
        self.x=0
        self.y=0
        self.calc_pos()

    def calc_pos(self):#becuase we will have dot in the center of box
        self.x=( SQUARE_SIZE * self.col ) + SQUARE_SIZE//2
        self.y=( SQUARE_SIZE * self.row ) + SQUARE_SIZE//2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius+self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        #for image x,y positions are the top-left but for circle draw is center point
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y-CROWN.get_height()//2))

    def move(self, row, col):
        self.row=row
        self.col=col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)