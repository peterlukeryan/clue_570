import pygame
import random
import math
from AStar import a_star 

class Person:
    RED = (255,0,0)
    BLUE = (0,0,255)
    GREEN = (0,255,0)
    PINK = (255,153,255)
    colors = [RED, BLUE, GREEN, PINK]
    color_string = ["RED", "BLUE", "GREEN", "PINK"]
    def __init__(self, name):
        self.name = name
        self.position = None
        self.color = Person.colors[name] 

    def __str__(self):
        return f"Player {self.name} is color {Person.color_string[self.name]}"

class Tile:
    WALL = 1
    OPEN = 2
    DOOR = 3
    YELLOW = (255, 153, 51)
    WHITE=(255,255,255)
    BLACK=(0,0,0)
    BROWN = (222, 184, 135)

    def __init__(self, x, y):
        self.player = None
        self.name = "tile"
        self.x = x
        self.y = y
        self.left = self.right = self.top = self.bot = self.OPEN
        self.visited = False
        self.color = Tile.YELLOW

        # setting the boundaries of the board
        if(x == 0):
            self.left = self.WALL
        if(x == 24):
            self.right = self.WALL
        if(y == 0):
            self.bot = self.WALL
        if(y == 24):
            self.top = self.WALL

class Board:

    def draw_board(self):
        cell_size = 25 
        pygame.init()
        screen = pygame.display.set_mode((25 * cell_size, 25 * cell_size))
        pygame.display.set_caption("Clue Board")


        font = pygame.font.Font(None, 36)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(Tile.BLACK)

            for i in range(25):
                for j in range(25):
                    tile = self.board[i][j]
                    color = Tile.YELLOW
                    outline = 1 
                    if(tile.name != "tile"):
                        #if(tile.y == 12):
                            #print(f"({tile.x},{tile.y})")
                        color = Tile.BROWN
                        outline = 2 
                    if(tile.visited):
                        color = tile.player.color

                    # color inside of rectangle
                    pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size), 13)
                    # color outline
                    pygame.draw.rect(screen, Tile.BLACK, (j * cell_size, i * cell_size, cell_size, cell_size), outline)
                    text = font.render(str(self.board[i][j]), True, Tile.BLACK)
                    text_rect = text.get_rect(center=((j + 0.5) * cell_size, (i + 0.5) * cell_size))
                    #screen.blit(text, text_rect)

            pygame.display.flip()

        pygame.quit()

    def test_board(self):
        max_visits = 216
        for x in self.starting_points:
            tile = x
        #tile = self.starting_points[0]
            tile.visited = True
            visited = self.iterate_board(tile)
            print(f"starting at ({tile.x},{tile.y})")
            print(f"visited -> {visited}")
            print(f"total counted -> {max_visits}")
            for x in self.board:
                for y in x:
                    y.visited = False
    
    def iterate_board(self, tile):
        tile.visited = True
        x = tile.x
        y = tile.y
        visited = 1
        if(tile.top == Tile.OPEN and self.board[x][y+1].visited == False):
            visited += self.iterate_board(self.board[x][y+1])
        if(tile.top == Tile.DOOR):
            visited += 1
            print(f"({x},{y}) found door to the top")
        if(tile.bot == Tile.OPEN and self.board[x][y-1].visited == False):
            visited += self.iterate_board(self.board[x][y-1])
        if(tile.bot == Tile.DOOR):
            print(f"({x},{y}) found door to the bot")
            visited += 1
        if(tile.left == Tile.OPEN and self.board[x-1][y].visited == False):
            visited += self.iterate_board(self.board[x-1][y])
        if(tile.left == Tile.DOOR):
            visited += 1
            print(f"({x},{y}) found door to the left")
        if(tile.right == Tile.OPEN and self.board[x+1][y].visited == False):
            visited += self.iterate_board(self.board[x+1][y])
        if(tile.right == Tile.DOOR):
            visited += 1
            print(f"({x},{y}) found door to the right")
        return visited 

    def roll_dice(self):
        die1 = random.randint(1,6); 
        die2 = random.randint(1,6); 
        return die1 + die2
            
    def get_path(self, room_name):
        start = (17,8)
        #self.board[17][8].visited = True
        #self.board[17][8].player = self.players[self.current_player] 
        shortest_path = []
        goal_doors = self.rooms[room_name]
        shortest = math.inf
        if(len(goal_doors) > 1):
            for door in goal_doors:
                goal = (door.x, door.y)
                path = a_star(start, goal, self.board) 
                if (len(path) < shortest):
                    shortest_path = path
                    shortest = len(path)
            #print(shortest_path)
            
        else:
            goal = (goal_doors[0].x, goal_doors[0].y)
            shortest_path = a_star(start, goal, self.board)
            #print(shortest_path)
        return shortest_path

    def take_turn(self, room_name):
        steps = self.roll_dice()
        path = self.get_path(room_name)

        # get the current player
        player = self.players[self.current_player]
        self.current_player += 1
        if(self.current_player == len(self.players)):
            self.current_player = 0

        # slice array to rolled steps 
        path = path[:steps]

        # get the tile where the player finished
        tile_coords = path[len(path) - 1]
        tile = self.board[tile_coords[0]][tile_coords[1]]

        # set the player to its current position on the board
        tile.player = player
        tile.visited = True
        # inside the room 
        return tile.name == room_name



    def find_doors(self):
        count = 0
        for x in range(25):
            for y in range(25):
                tile = self.board[x][y]
                if(tile.left == Tile.DOOR):
                    print(f"tile : ({x}, {y}) -> door left")
                    count += 1
                if(tile.right == Tile.DOOR):
                    print(f"tile : ({x}, {y}) -> door right ")
                    count += 1
                if(tile.top == Tile.DOOR):
                    print(f"tile : ({x}, {y}) -> door top")
                    count += 1
                if(tile.bot == Tile.DOOR):
                    print(f"tile : ({x}, {y}) -> door bot")
                    count += 1
        print(f"count -> {count}")
        print(f"count -> {len(self.starting_points)}")

        
    def __init__(self, num_players):
        self.players = [None for _ in range(num_players)]
        for i in range(num_players):
            self.players[i] = Person(i)
            print(self.players[i])
        self.current_player = 0
        self.starting_points = []
        self.board = [[None for _ in range(25)] for _ in range(25)]
        for x in range(25):
            for y in range(25):
                self.board[x][y] = Tile(x, y)

        self.rooms = {
            "Study"  : [self.board[6][20]],
            "Hall"   : [self.board[11][18], self.board[12][18], self.board[13][18], self.board[9][19]],
            "Lounge" : [self.board[18][19]],
            "Dining Room" : [self.board[18][15], self.board[17][12]],
            "Kitchen"     : [self.board[19][6]],
            "Ballroom"    : [self.board[6][5], self.board[15][6], self.board[9][6], self.board[8][5]],
            "Conservatory" : [self.board[4][4]],
            "Billiard Room" : [self.board[6][9], self.board[1][11]],
            "Library"       : [self.board[3][13], self.board[7][15]]

        }

        # create conservatory
        room_name = "conservatory"
        for x in range(5):
            for y in range(5):
                self.board[x][y].name = room_name 
        self.board[5][0].name = room_name
        self.board[5][0].right = Tile.WALL 
        self.board[5][1].name = room_name
        self.board[5][1].right = Tile.WALL 
        self.board[5][2].name = room_name
        self.board[5][2].right = Tile.WALL 
        self.board[5][3].name = room_name
        self.board[5][3].right = Tile.WALL 
        self.board[5][3].top = Tile.WALL 

        self.board[4][4].right = Tile.DOOR
        
        self.board[1][5].top = self.board[1][5].left = Tile.WALL
        self.board[2][5].top = Tile.WALL
        self.board[3][5].top = Tile.WALL
        self.board[4][5].top = self.board[4][5].right = Tile.WALL

        #create Billiard Room
        room_name = "Billiard Room"
        for x in range(7):
            for y in range(8,12):
                self.board[x][y].name = room_name
                if(y == 8):
                    self.board[x][y].bot = Tile.WALL
                if(y == 11):
                    self.board[x][y].top = Tile.WALL
                if(x == 6):
                    self.board[x][y].right = Tile.WALL
        self.board[6][9].right = Tile.DOOR
        self.board[1][11].top = Tile.DOOR

        #create Library
        room_name = "Library"
        for x in range(1,7):
            for y in range(13,18):
                self.board[x][y].name = room_name
        for x in range(1,7):
            self.board[x][13].bot = Tile.WALL
            self.board[x][17].top = Tile.WALL
        self.board[3][13].bot = Tile.DOOR 
        self.board[6][13].right = Tile.WALL
        self.board[1][17].left = Tile.WALL
        self.board[6][17].right = Tile.WALL

        self.board[7][14].right = self.board[7][14].bot = Tile.WALL
        self.board[7][15].right = Tile.DOOR
        self.board[7][16].right = self.board[7][16].top = Tile.WALL

        # create Study
        room_name = "Study"
        for x in range(6):
            for y in range(20,25):
                self.board[x][y].name = room_name
                if(y == 24):
                    self.board[x][y].top = Tile.WALL
                if(y == 20):
                    self.board[x][y].bot = Tile.WALL
        for y in range(20,24):
            self.board[6][y].right = Tile.WALL

        self.board[6][20].bot = Tile.DOOR
        self.board[6][23].top = Tile.WALL
        
        # create Hall
        # didnt't do the top part of the room that isn't squared
        room_name = "Hall"
        for x in range(9, 16):
            for y in range(18, 24):
                self.board[x][y].name = room_name
                if(y == 18):
                    self.board[x][y].bot = Tile.WALL
                if(x == 9):
                    self.board[x][y].left = Tile.WALL
                if(x == 15):
                    self.board[x][y].right = Tile.WALL
        self.board[9][19].left = Tile.DOOR
        self.board[11][18].bot = Tile.DOOR
        self.board[12][18].bot = Tile.DOOR
        self.board[13][18].bot = Tile.DOOR

        # create Lounge
        room_name = "Lounge"
        for x in range(19, 25):
            for y in range(19, 25):
                self.board[x][y].name = room_name
                if(x == 24):
                    self.board[x][y].right = Tile.WALL
                if(y == 19):
                    self.board[x][y].bot = Tile.WALL
                if(y == 24):
                    self.board[x][y].top = Tile.WALL
        for y in range(19,24):
            self.board[18][y].name = room_name
            self.board[18][y].left = Tile.WALL
        self.board[18][23].top = Tile.WALL
        self.board[18][19].left = Tile.DOOR

        # create Dining Room
        room_name = "Dining Room"
        for x in range(17, 25):
            for y in range(10,16):
                self.board[x][y].name = room_name
                if(x == 17):
                    self.board[x][y].left = Tile.WALL
                if(x == 24):
                    self.board[x][y].right = Tile.WALL
                if(y == 10 and (x == 17 or x == 18 or x == 19)):
                    self.board[x][y].bot = Tile.WALL
                if(y == 15):
                    self.board[x][y].top = Tile.WALL
        for x in range(20, 25):
            self.board[x][9].name = room_name
            self.board[x][9].bot = Tile.WALL

        self.board[20][9].left = Tile.WALL
        self.board[24][9].right = Tile.WALL
        self.board[17][12].left = Tile.DOOR
        self.board[18][15].top = Tile.DOOR

        # create kitchen
        room_name = "Kitchen"
        for x in range(19,25):
            for y in range(6):
                self.board[x][y].name = room_name
                if(y == 0):
                    self.board[x][y].bot = Tile.WALL
                if(x == 19):
                    self.board[x][y].left = Tile.WALL
                if(x == 24):
                    self.board[x][y].right= Tile.WALL
        for x in range(19,24):
            self.board[x][6].name = room_name
            self.board[x][6].top = Tile.WALL

        self.board[19][6].left = Tile.DOOR
        self.board[23][6].right = Tile.WALL
        self.board[24][5].top = Tile.WALL


       # create Ball Room
        room_name = "Ball Room"
        for x in range(8,17): 
            for y in range(2, 7):
                self.board[x][y].name = room_name
                if(x == 8):
                    self.board[x][y].left = Tile.WALL
                if(x == 16):
                    self.board[x][y].right = Tile.WALL
                if(y == 6):
                    self.board[x][y].top = Tile.WALL
                if(y == 2 and (x == 8 or x == 9 or x == 15 or x == 16)):
                    self.board[x][y].bot = Tile.WALL
        self.board[10][1].name = room_name
        self.board[10][1].left = Tile.WALL 
        self.board[14][1].name = room_name 
        self.board[14][1].right = Tile.WALL 
        self.board[8][5].left = Tile.DOOR
        self.board[9][6].top = Tile.DOOR
        self.board[15][6].top = Tile.DOOR
        self.board[16][5].right = Tile.DOOR



        # doing the rest of the board
        for x in range(1, 25):
            if(x >= 1 and x <= 6):
                self.board[x][7].top = Tile.WALL
            if(x >= 8 and x <= 16):
                self.board[x][7].bot = Tile.WALL
            # ballrom doors
            self.board[9][7].bot = Tile.DOOR
            self.board[15][7].bot = Tile.DOOR
            if(x >= 19 and x <= 24):
                self.board[x][7].bot = Tile.WALL
             #starting point?
        self.board[24][7].right = self.board[24][7].top = Tile.WALL
        self.starting_points.append(self.board[24][7])
        self.board[1][7].left = Tile.WALL

        for x in range(5):
            self.board[x][6].bot = Tile.WALL
        # starting point?
        self.board[0][6].left = self.board[0][6].top = Tile.WALL
        self.starting_points.append(self.board[0][6])

        self.board[5][5].left = Tile.WALL
        #conservatory door
        self.board[5][4].left = Tile.DOOR
        self.board[5][4].bot = Tile.WALL
        self.board[6][3].left = Tile.WALL
        self.board[6][2].left = self.board[6][2].bot  = Tile.WALL
        self.board[7][1].left = self.board[7][1].bot = Tile.WALL
        self.board[8][1].top = self.board[8][1].bot = Tile.WALL
        self.board[9][1].top = self.board[9][1].right = Tile.WALL
        # starting point?
        self.board[9][0].bot = self.board[9][0].right = self.board[9][0].left = Tile.WALL
        self.starting_points.append(self.board[9][0])

        #starting point? 
        self.board[15][0].left = self.board[15][0].bot = self.board[15][0].right = Tile.WALL
        self.starting_points.append(self.board[15][0])
        self.board[15][1].left = self.board[15][1].top = Tile.WALL
        self.board[16][1].bot = self.board[16][1].top = Tile.WALL
        self.board[17][1].bot = self.board[17][1].right = Tile.WALL

        for y in range(2, 7):
            self.board[17][y].left = Tile.WALL
        # ballroom door
        self.board[17][5].left = Tile.DOOR

        for y in range(2, 7):
            self.board[18][y].right = Tile.WALL
        # kitched door
        self.board[18][6].right = Tile.DOOR

        self.board[18][2].bot = Tile.WALL

        for x in range(7, 24):
            if(x >= 10 and x <= 14):
                self.board[x][8].top = Tile.WALL
                self.board[x][16].bot = Tile.WALL
            #if(x >= 17 and x <= 23):
            if(x >= 20 and x <= 23):
                self.board[x][8].top = Tile.WALL

        self.board[23][8].right = Tile.WALL

        self.board[17][9].top = Tile.WALL
        self.board[18][9].top = Tile.WALL
        self.board[19][9].top = self.board[19][9].right  = Tile.WALL

        for y in range(7, 24):
            if(y >= 14 and y <=16):
                self.board[8][y].left = Tile.WALL
            if(y >= 18 and y <= 23):
                self.board[8][y].right = Tile.WALL
        self.board[8][23].top = Tile.WALL
        # library door 
        self.board[8][15].left = Tile.DOOR
        #hall door
        self.board[8][19].right = Tile.DOOR

        for y in range(20, 25):
            self.board[7][y].left = Tile.WALL
         # starting point?
        self.board[7][24].top = self.board[7][24].right = Tile.WALL
        self.starting_points.append(self.board[7][24])


        for x in range(1, 7):
            self.board[x][19].top = Tile.WALL
        # study door
        self.board[6][19].top = Tile.DOOR
        self.board[1][19].left = Tile.WALL

        for x in range(7):
            self.board[x][18].bot = Tile.WALL
        # starting point
        self.board[0][18].left = self.board[0][18].top = Tile.WALL
        self.starting_points.append(self.board[0][18])
        self.board[7][17].left = self.board[7][17].bot = Tile.WALL
        self.board[7][13].top = self.board[7][13].left = Tile.WALL

        for x in range(1, 7):
            self.board[x][12].top = self.board[x][12].bot = Tile.WALL
        # billiard room door
        self.board[1][12].bot = Tile.DOOR
        self.board[1][12].left = Tile.WALL
        #library door
        self.board[3][12].top = Tile.DOOR

        for y in range(2, 12):
            if (y >= 2 and y <= 6):
                self.board[7][y].right = Tile.WALL

            if (y >= 8 and y <= 11):
                self.board[7][y].left = Tile.WALL
        # ballroom door
        self.board[7][5].right = Tile.DOOR
        #billiard room door
        self.board[7][9].left = Tile.DOOR

        for x in range(9, 16):
            self.board[x][17].top = Tile.WALL
        # hall doors
        self.board[11][17].top = self.board[12][17].top = self.board[13][17].top = Tile.DOOR

        for y in range(18, 24):
            self.board[16][y].left = Tile.WALL
        self.board[16][23].top = Tile.WALL

        for y in range(19, 25):
            self.board[17][y].right = Tile.WALL
        #starting point?
        self.board[17][24].top = self.board[17][24].left = Tile.WALL
        self.starting_points.append(self.board[17][24])
        #lounge door
        self.board[17][19].right = Tile.DOOR

        for x in range(18, 24):
            self.board[x][18].top = Tile.WALL
        self.board[23][18].right = Tile.WALL
        #starting point?
        self.board[24][17].right = self.board[24][17].top = self.board[24][17].bot = Tile.WALL
        self.starting_points.append(self.board[24][17])

        for x in range(17, 24):
            self.board[x][16].bot = Tile.WALL
        # dining room door
        self.board[18][16].bot = Tile.DOOR
        self.board[23][16].right = Tile.WALL

        for y in range(10, 16):
            self.board[16][y].right = Tile.WALL

        # dining room door
        self.board[16][12].right = Tile.DOOR

        for y in range(9, 16):
            self.board[9][y].right = Tile.WALL
            self.board[15][y].left = Tile.WALL








                

