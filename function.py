import pygame
import os
import time
import math
import neat
import random
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#initialize and difine a font
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

#set width and length of the screen and the playing field
WIN_WIDTH = 1400
WIN_HEIGHT = 800
FIELD_WIDTH = 4000
FIELD_LENGTH = 4000

#global variables to get every point on the screen of relevant
scalar = 2
x_compensation =0
y_compensation =0

#colors
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (50,255,50) #background
BLACK = (0,0,0)
BLUE = (0,0,255)
ORANGE = (255,128,0)
YELLOW = (255,255,0)
colors = [BLUE,GREEN,RED,WHITE,ORANGE]

pygame.display.set_caption('Welkom to agar.io')

#a player is a circle on the screen both controled by the player as not controled
#this is needed for later implementation of the ai
class Player:
    def __init__(self,players, real_player = False):
        # a new player is placed somewhere on the sreen and checked that is doesnot die when initialized
        self.x = random.randint(100, FIELD_WIDTH-60)
        self.y = random.randint(1, FIELD_LENGTH-60)
        self.color = colors[random.randint(0, 4)]
        self.vel = 5
        self.direction = random.random()*math.pi*2
        self.radius = random.randint(10, 45)
        self.size = math.pi*self.radius**2
        self.real_player = real_player
        if real_player:
            self.color = YELLOW
            self.radius = 10
            self.size = math.pi*self.radius**2

        start = True
        i=0
        while start and i<10:
            i+= 1
            if self.eat_player(players)[0]:
                self.x = random.randint(100, FIELD_WIDTH-60)
                self.y = random.randint(1, FIELD_LENGTH-60)

            else:start = False

    def move(self):
        """
        this is the function that is called to move a player and should be called every frame for every players
        """
        global x_compensation,y_compensation, scalar
        if self.real_player:
            x_compensation = self.x -(WIN_WIDTH/2)
            y_compensation = self.y -(WIN_HEIGHT/2)
            scalar = 15/(self.radius**0.5 )

        self.x+=  self.vel * math.cos(self.direction)
        self.y-=  self.vel * math.sin(self.direction)
        if self.x<self.radius or self.x>FIELD_WIDTH-self.radius:
            self.direction= math.pi-self.direction
        if self.y<self.radius or self.y>FIELD_LENGTH-self.radius:
            self.direction= -self.direction
        self.vel=25/(self.radius)**0.5

    def draw(self,win):
        # draw a blue circle onto the surface
        radius= math.sqrt(self.size/math.pi)
        pygame.draw.circle(win, self.color, matrix(self.x,self.y) ,round(self.radius*scalar), 0)

    def eat_dots(self, dots):
        for x,dot in enumerate(dots):
            distance = math.sqrt((dot.x-self.x)**2+(dot.y-self.y)**2)
            if distance<= self.radius:
                self.size += 80
                dots.pop(x)
        self.radius = math.sqrt(self.size/math.pi)
        return dots

    def eat_player(self, players,y=2000):
        for x,player in enumerate(players):
            distance = math.sqrt((player.x-self.x)**2+(player.y-self.y)**2)
            if player.radius < self.radius*0.9:
                if distance <= self.radius*0.9+10 and not x==y:
                    self.size += player.size
                    self.radius = math.sqrt(self.size/math.pi)
                    return [True, player]
                else: pass
        return [False]

    def change_direction(self, goal_x,goal_y):
        distance= math.sqrt((goal_x-700)**2+(goal_y-400)**2)
        if (goal_y-400)<0:
            self.direction = math.acos((goal_x-700)/distance)
        if (goal_y-400)>0:
            self.direction = -math.acos((goal_x-700)/distance)

class Dot:
    def __init__(self):
        self.x = random.randint(1, FIELD_WIDTH)
        self.y = random.randint(1, FIELD_LENGTH)
        self.color = colors[random.randint(0, 4)]
    def draw(self,win):
        pygame.draw.circle(win, self.color, matrix(self.x,self.y), round(5*scalar), 0)

def matrix(x,y):
    x_onscreen = (x-x_compensation-(WIN_WIDTH/2))*scalar+(WIN_WIDTH/2)
    y_onscreen = (y-y_compensation-(WIN_HEIGHT/2))*scalar+(WIN_HEIGHT/2)
    return (round(x_onscreen),round(y_onscreen))

def draw_window(win, players,dots,score):
    win.fill(BLACK)
    for dot in dots:
        dot.draw(win)
    for player in players:
        player.draw(win)

    # draw the text's background rectangle onto the surface
    pygame.draw.polygon(win, GREEN, (matrix(0,0), matrix(FIELD_WIDTH,0),matrix(FIELD_WIDTH,FIELD_LENGTH),matrix(0,FIELD_LENGTH) ),round(6*scalar))
    # score
    score_label = STAT_FONT.render("Score: " + str(round(score)),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    pygame.display.update()
