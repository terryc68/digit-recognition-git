import pygame as pyg
from util import v_add, colorMapping
import sys
import random
from model import Model
from neuron import Neuron
import sample
from util import isNeighbor
import copy

WIDTH = 850
HEIGHT = 450
TITLE = "Digit Recognition"
FPS = 60
CYAN = (10,186,181)
BACKGROUND = CYAN
WHITE = (255,255,255)
DIMMED_CYAN = (5,160,158)
BLACK = (0,0,0)
GRID_DIM = (20,20)
BTN_COLOR = WHITE
SCALE = 10
isPressed = False
grid = [[0 for c in xrange(GRID_DIM[0])] for r in xrange(GRID_DIM[1])]
output_grid = [[0 for c in xrange(GRID_DIM[0])] for r in xrange(GRID_DIM[1])]

#Panel
panel_grid_size = (GRID_DIM[0]*SCALE, GRID_DIM[1]*SCALE)
input_cord = (WIDTH/4 - panel_grid_size[0]/2, HEIGHT/2 - panel_grid_size[1]/2)
output_cord = (3*WIDTH/4 - panel_grid_size[0]/2, HEIGHT/2 - panel_grid_size[1]/2)

#BUTTON
BTN_DIM = (90,40)
BTN_CNT = 4
btn_cords = []

#MODEL
m = Model()
n_array_size = 10
n_array = []

#samples
sample_size1 = 40
sample_size2 = 40

pyg.init()
clock = pyg.time.Clock()
screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption(TITLE)

def mouseHover(dim,cord):
    mouse = pyg.mouse.get_pos()
    return True if cord[0] < mouse[0] < (cord[0]+dim[0]) and cord[1] < mouse[1] <(cord[1]+dim[1]) else False

def drawInputGrid():
    for r in xrange(GRID_DIM[0]):
        for c in xrange(GRID_DIM[1]):
            if grid[r][c]:
                cord = (input_cord[0] + SCALE*c, input_cord[1] + SCALE*r)
                pyg.draw.rect(screen,colorMapping(grid[r][c]),(cord[0], cord[1], SCALE, SCALE), 0)

def drawOutputGrid():
    for r in xrange(GRID_DIM[0]):
        for c in xrange(GRID_DIM[1]):
            if output_grid[r][c]:
                cord = (output_cord[0] + SCALE*c, output_cord[1] + SCALE*r)
                pyg.draw.rect(screen,colorMapping(output_grid[r][c]),(cord[0], cord[1], SCALE, SCALE), 0)


def drawInputPanel():
    pyg.draw.rect(screen,WHITE,(input_cord[0], input_cord[1],panel_grid_size[0],panel_grid_size[1]),0)

def drawOutputPanel():
    pyg.draw.rect(screen,WHITE,(output_cord[0], output_cord[1],panel_grid_size[0],panel_grid_size[1]),0)

def drawText(cords,isHover,i):
    text_color = CYAN if isHover else WHITE
    font = pyg.font.SysFont("arial",20)
    text_array = [
                  font.render("     Train",25,text_color),
                  font.render("     Noise",25,text_color),
                  font.render("   Classify",25,text_color),
                  font.render("     Clear",25,text_color),
                 ]
    text = text_array[i]
    screen.blit(text,(cords[i][0],cords[i][1] + 8))

def drawButtons():
    #GENERATE CORDINATE
    for x in xrange(BTN_CNT):
        btn_cords.append((WIDTH/2 - BTN_DIM[0]/2, (x+1) * HEIGHT/(BTN_CNT + 2) +10))

    for x in xrange(BTN_CNT):
        #DRAW BUTTON
        BTN_COLOR = DIMMED_CYAN if mouseHover(BTN_DIM,btn_cords[x]) else CYAN
        pyg.draw.rect(screen, BTN_COLOR, (btn_cords[x][0], btn_cords[x][1], BTN_DIM[0], BTN_DIM[1]),0)
        #DRAW TEXT
        drawText(btn_cords, mouseHover(BTN_DIM,btn_cords),x)

def draw():
    drawInputPanel()
    drawInputGrid()
    drawOutputPanel()
    drawOutputGrid()
    drawButtons()

def update():
    screen.fill(BACKGROUND)
    draw()
    pyg.display.update()
    clock.tick(FPS)

def displaySamples(samples):
    global grid
    for x in xrange(sample_size1):
        edited_s = copy.deepcopy(samples[x])
        del edited_s[19][20]
        grid = edited_s
        update()

def train():
    global grid

    for x in xrange(n_array_size):
        print "\n\nTraining: {}".format(x)
        samples = sample.generateSamples(x,sample_size1,sample_size2,GRID_DIM)
        displaySamples(samples)
        for _ in xrange(3):
            random.shuffle(samples)
        m.train(samples)
        n_array.append(Neuron(m.weights,m.threshold))
        m.renewVariables()

    grid = [[0 for c in xrange(GRID_DIM[0])] for r in xrange(GRID_DIM[1])]
    print "Finished"

def getNoise(r,c):
    global grid
    return round(random.uniform(0.1,0.3),3) if isNeighbor(grid,r,c) else round(random.uniform(0.01,0.03),3)

def noise():
    for r in xrange(GRID_DIM[0]):
        for c in xrange(GRID_DIM[1]):
            n = getNoise(r,c)
            grid[r][c] = min(1,grid[r][c] + n)

def classify():
    global output_grid
    for x in xrange(10):
        output = n_array[x].predict(grid)
        if output:
            output_grid = copy.deepcopy(sample.example[x])
            break
        print "{}: {}".format(x,output)
    print "\n"

def clear():
    grid = [[0 for c in xrange(GRID_DIM[1])] for r in xrange(GRID_DIM[0])]

def processMousAction(btn_index, mouse, event = None):
    global grid

    if mouseHover(panel_grid_size,input_cord) and btn_index == 0:
        index = (mouse[0]-input_cord[0]) / SCALE, (mouse[1]-input_cord[1]) / SCALE
        grid[index[1]][index[0]] = 1
    elif mouseHover(panel_grid_size,input_cord) and btn_index == 2:
        index = (mouse[0]-input_cord[0]) / SCALE, (mouse[1]-input_cord[1]) / SCALE
        grid[index[1]][index[0]] = 0
    elif btn_index == 0:
        if mouseHover(BTN_DIM,btn_cords[0]):
            train()
        elif mouseHover(BTN_DIM,btn_cords[1]):
            noise()
        elif mouseHover(BTN_DIM,btn_cords[2]):
            classify()
        elif mouseHover(BTN_DIM,btn_cords[3]):
            grid = [[0 for c in xrange(GRID_DIM[1])] for r in xrange(GRID_DIM[0])]
    elif btn_index == 3:
        keys = [pyg.K_0, pyg.K_1, pyg.K_2, pyg.K_3, pyg.K_4, pyg.K_5, pyg.K_6, pyg.K_7, pyg.K_8, pyg.K_9]
        for x in xrange(10):
            if event.key == keys[x]:
                grid =  copy.deepcopy(sample.example[x])
                update()

def run():
    while True:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            elif pyg.mouse.get_pressed()[0]:
                processMousAction(0, pyg.mouse.get_pos())
            elif pyg.mouse.get_pressed()[2]:
                processMousAction(2, pyg.mouse.get_pos())
            elif event.type == pyg.KEYDOWN:
                processMousAction(3, pyg.mouse.get_pos(),event)

        update()

run()
