import pygame
import os
import time
import math
import neat
import random

from tracks import *
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
pygame.font.init()

STAT_FONT = pygame.font.SysFont("comicsans", 50)

WIN_WIDTH = 1400
WIN_HEIGHT = 800
FIELD_WIDTH = 5000
FIELD_LENGTH = 5000

GEN=0
level=1
levels = [level_1,level_4,level_2,level_3]
level_scores = [1,6,8,10]

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

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Welkom to hole.io')

class Player:
    def __init__(self,players, real_player = False):
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
        while start:
            if self.eat_player(players)[0]:
                self.x = random.randint(100, FIELD_WIDTH-60)
                self.y = random.randint(1, FIELD_LENGTH-60)

            else:start = False

    def move(self):
        global x_compensation,y_compensation, scalar
        if self.real_player:
            x_compensation = self.x -(WIN_WIDTH/2)
            y_compensation = self.y -(WIN_HEIGHT/2)
            scalar = 15/(self.radius**0.5 )

        self.x+=  self.vel * math.cos(self.direction)
        self.y-=  self.vel * math.sin(self.direction)
        if self.x-math.sqrt(self.size/math.pi)<0 or self.x+math.sqrt(self.size/math.pi)>FIELD_WIDTH:
            self.direction= math.pi-self.direction
        if self.y-math.sqrt(self.size/math.pi)<0 or self.y+math.sqrt(self.size/math.pi)>FIELD_LENGTH:
            self.direction= -self.direction
        self.vel=5*(25/self.radius)**0.1

    def draw(self,win):
        # draw a blue circle onto the surface
        radius= math.sqrt(self.size/math.pi)
        pygame.draw.circle(win, self.color, ((self.x-x_compensation-700)*scalar+700, (self.y-y_compensation-400)*scalar+400), radius*scalar, 0)

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
        pygame.draw.circle(win, self.color, ((self.x-x_compensation-700)*scalar+700, (self.y-y_compensation-400)*scalar+400), 5*scalar, 0)


def cordinate(x):
    pass


def draw_window(win, players,dots,score):
    win.fill(BLACK)
    for dot in dots:
        dot.draw(win)
    for player in players:
        player.draw(win)

    # draw the text's background rectangle onto the surface
    pygame.draw.polygon(win, GREEN, (((0-x_compensation-700)*scalar+700, (0-y_compensation-400)*scalar+400), ((FIELD_WIDTH-x_compensation-700)*scalar+700, (0-y_compensation-400)*scalar+400), ((FIELD_WIDTH-x_compensation-700)*scalar+700, (FIELD_LENGTH-y_compensation-400)*scalar+400), ((0-x_compensation-700)*scalar+700, (FIELD_LENGTH-y_compensation-400)*scalar+400)),round(6*scalar))
    # score
    score_label = STAT_FONT.render("Score: " + str(round(score)),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    pygame.display.update()