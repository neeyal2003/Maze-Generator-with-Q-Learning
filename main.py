import pygame, sys, random, time,math
import numpy as np
from pygame.locals import *

pygame.init()
font = pygame.font.SysFont("Verdana",12) #creates fonts that I will then use in the GUI
font2 = pygame.font.SysFont("Verdana",30)
font3 = pygame.font.SysFont("Verdana",17)
font4 = pygame.font.SysFont("Verdana",22)
font5 = pygame.font.SysFont(("Verdana"),47)
font6 = pygame.font.SysFont("Verdana",20)
font7 = pygame.font.SysFont("Verdana",30)
font7.set_bold(True) #sets font7 to be bold
font4.set_underline(True) #sets font4 to be underlined
clock = pygame.time.Clock()

class Maze:
    def __init__(self,x_size,y_size,start_choice,end_choice,pcolour,scolour):
        self.offset = 0  #how much away from pygame GUI the maze is
        self.length = 14  #how big the lines are for the maze
        self.pcolour = pcolour  #background colour
        self.scolour = scolour  #colour of the lines
        self.completed_episodes = 100  #a value that would have been used for the q_learning aspect
        self.visited = []  #used in creating the maze
        self.path = []  #used in creating the maze
        self.maze = []  #used for storing the maze as an array
        self.x_size = x_size  #defines the x_size of the maze
        self.y_size = y_size  #defines the y_size of the maze
        self.solution = []
        self.episodes = 30000
        self.epsilon = 0.1
        self.solution_toggle = False
        self.simulate_toggle = False
        self.return_toggle = False
        self.window = pygame.display.set_mode((600,800))  #creates the GUI for the maze using a formula to calculate the amount of pixels on the x and y sides
        self.create_template()  #creates the template for the maze
        self.create_endpoint(end_choice)  #creates the endpoint for the maze and defines the end location
        self.create_sprite(start_choice)  #creates the start point of the maze and the (x,y) coords of it
        self.start_sprite_x = self.sprite.x  #sets a value for the x coord to come back to
        self.start_sprite_y = self.sprite.y  #sets a value for the y coord to come back to
        self.create_maze()  #creates the maze by changing values of the maze template

    def create_endpoint(self,choice): #1 is top left, 2 top right, 3 bottom left, 4 bottom right
        if choice == 1:
            self.endpoint_x,self.endpoint_y = 0,0
        elif choice == 2:
            self.endpoint_x, self.endpoint_y = self.x_size-1, 0
        elif choice == 3:
            self.endpoint_x, self.endpoint_y = 0, self.y_size-1
        elif choice == 4:
            self.endpoint_x, self.endpoint_y = self.x_size-1, self.y_size - 1

    def create_sprite(self,choice):  # 1 is top left, 2 top right, 3 bottom left, 4 bottom right
        if choice == 1:
            self.sprite = Sprite(0,0)
            self.x,self.y =0,0
        elif choice == 2:
            self.sprite = Sprite(self.x_size-1,0)
            self.x,self.y = self.x_size-1,0
        elif choice == 3:
            self.sprite = Sprite(0, self.y_size-1)
            self.x,self.y = 0,self.y_size-1
        elif choice == 4:
            self.sprite = Sprite(self.x_size-1, self.y_size-1)
            self.x,self.y = self.x_size-1,self.y_size-1

    def create_template(self):  #creates an array for the size of the maze and fills every value in as 1 which means that it is a wall
        x = 0
        temp = []  #creates the y column
        while x != self.x_size * self.y_size + 1:  #while the x is not equal to the area of the maze
            if x == 0 or x % self.x_size != 0:
                temp2 = [1,1,1,1]  #format top,bottom,left,right  #creates the x column
                temp.append(temp2)  #adds x column to y array
            elif x % self.x_size == 0:
                self.maze.append(temp)  #appends the y column to the maze
                temp = []  #y column becomes empty again
                temp2 = [1,1,1,1]
                temp.append(temp2)  #adds x column to y array
            x += 1

    def display_arr(self):  #used for testing before pygame was implemented
        for i in self.maze:  #prints each y row of the maze
            print(i)

    def display_maze(self,choice):
        visited_colour = (220,20,60)
        solution_colour = (0,0,0)
        self.window.fill(self.pcolour)  #fills the background of the window with the background colour
        for i in range(0,len(self.maze)):  #for i range of the y column
            for j in range (0,len(self.maze[i])):  #for j in range of the x column
                if self.maze[i][j][0] == 1:  #adds a line if the first value (first value defines top of the cell) is equal to 1
                    pygame.draw.line(self.window,self.scolour,(self.offset+j*self.length,self.offset+i*self.length),(self.offset+j*self.length+self.length,self.offset+i*self.length),1)
                if self.maze[i][j][1] == 1:  #adds a line if the second value (second value defines bottom of the cell) is equal to 1
                    pygame.draw.line(self.window, self.scolour,(self.offset+j*self.length,self.offset+i*self.length+self.length),(self.offset+j*self.length+self.length,self.offset+i*self.length+self.length),1)
                if self.maze[i][j][2] == 1:  #adds a line if the third value (third value defines left of the cell) is equal to 1
                    pygame.draw.line(self.window, self.scolour,(self.offset+j*self.length,self.offset+i*self.length),(self.offset+j*self.length,self.offset+i*self.length+self.length),1)
                if self.maze[i][j][3] == 1:  #adds a line if the fourth value (fourth value defines right of the cell) is equal to 1
                    pygame.draw.line(self.window, self.scolour,(self.offset+j*self.length+self.length,self.offset+i*self.length),(self.offset+j*self.length+self.length,self.offset+i*self.length+self.length),1)

        if choice == 0:  #will display only the maze and won't run any more code
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                clock = pygame.time.Clock()
                clock.tick(60)
                pygame.display.update()
        if choice != 0:
            if choice == 1:  #when choice is 1, it will print the maze and show how it is being made
                for i in self.visited:
                    pygame.draw.circle(self.window, visited_colour, (self.offset + i[1] * self.length + round(self.length / 2),self.offset + i[0] * self.length + round(self.length / 2)), 3.5)
            elif choice == 2:  #when choice is 2, it will print the maze and the current path the sprite has been on
                for i in self.sprite_path:
                    pygame.draw.circle(self.window, solution_colour, (self.offset + i[1] * self.length + round(self.length / 2),self.offset + i[0] * self.length + round(self.length / 2)), 3.5)
            elif choice == 3:
                for i in self.solution:
                    pygame.draw.circle(self.window, solution_colour, (self.offset + i[1] * self.length + round(self.length / 2),self.offset + i[0] * self.length + round(self.length / 2)), 3.5)
            x = 0
            while x== 0:  #will print the maze with the new values given to it
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                clock = pygame.time.Clock()
                clock.tick(60)
                pygame.display.update()
                time.sleep(10)
                x = input("Enter number: ")  #allows the maze window to show but can allow code to resume once time is up

    def create_maze_surface(self):
        offset = 3.5
        HSP = math.sqrt(0.299*(self.pcolour[0]**2) + 0.587 *(self.pcolour[1]**2)+0.114*(self.pcolour[2]**2)) #finds out how light/dark a colour is
        if HSP>127.5:
            location_colour = (0,0,0) #if the colour is light sets the colour values to black
            solution_colour = (0,0,0)
        else:
            location_colour = (255,255,255) #if the colour is dark sets the colour values to white
            solution_colour = (255,255,255)
        self.maze_surface = pygame.surface.Surface((self.x_size * self.length + 1, self.y_size * self.length + 1)) #creates a surface for the maze
        self.maze_surface.fill((self.pcolour)) #fills the background of the maze with the primary colour
        #highlights the start and endpoints as a different colour
        pygame.draw.rect(self.maze_surface,location_colour,[self.endpoint_x*self.length+offset,self.endpoint_y*self.length+offset,
                                                            self.length-offset*2,self.length-offset*2],0)
        pygame.draw.rect(self.maze_surface, location_colour,[self.start_sprite_x * self.length+offset, self.start_sprite_y * self.length+offset,
                                                             self.length-offset*2, self.length-offset*2], 0)
        for i in range(0, len(self.maze)):  # for i range of the y column
            for j in range(0, len(self.maze[i])):  # for j in range of the x column
                if self.maze[i][j][0] == 1:  # adds a line if the first value (first value defines top of the cell) is equal to 1
                    pygame.draw.line(self.maze_surface, self.scolour, (self.offset + j * self.length, self.offset + i * self.length),
                                     (self.offset + j * self.length + self.length, self.offset + i * self.length), 1)
                if self.maze[i][j][1] == 1:  # adds a line if the second value (second value defines bottom of the cell) is equal to 1
                    pygame.draw.line(self.maze_surface, self.scolour,(self.offset + j * self.length, self.offset + i * self.length + self.length),
                                     (self.offset + j * self.length + self.length,self.offset + i * self.length + self.length), 1)
                if self.maze[i][j][2] == 1:  # adds a line if the third value (third value defines left of the cell) is equal to 1
                    pygame.draw.line(self.maze_surface, self.scolour,(self.offset + j * self.length, self.offset + i * self.length),
                                     (self.offset + j * self.length, self.offset + i * self.length + self.length), 1)
                if self.maze[i][j][3] == 1:  # adds a line if the fourth value (fourth value defines right of the cell) is equal to 1
                    pygame.draw.line(self.maze_surface, self.scolour,(self.offset + j * self.length + self.length, self.offset + i * self.length),
                                     ( self.offset + j * self.length + self.length,self.offset + i * self.length + self.length), 1)
        if self.solution_toggle == True: #if solution toggle true
            for i in range(1,len(self.solution)): #draws the solution
                pygame.draw.line(self.maze_surface, solution_colour, (self.offset + self.solution[i-1][1] * self.length + round(self.length / 2),
                                                                      self.offset + self.solution[i-1][0] * self.length + round(self.length / 2)),
                                 (self.offset + self.solution[i][1] * self.length + round(self.length / 2),
                                  self.offset + self.solution[i][0] * self.length + round(self.length / 2)), 2)
        elif self.simulate_toggle == True: #if simulate toggle true
            simulate_button = Column_Text("Simulate/ Solution ", 400, 658, self.window, font6, True, (144, 238, 144)) #updates simulate button to be green
            self.return_button = Column_Text("Return to/ Main Menu ", 77, 658, self.window, font6, True, (200,200,200)) #updates return button to be greyed out
            solution_button = Column_Text("Show/ Solution ", 530, 658, self.window, font6, True, (200, 200, 200)) #updates solution button to be greyed out
            for i in range(1,len(self.solution)):
                pygame.event.get() #simulates solution step-by-step
                pygame.draw.line(self.maze_surface, solution_colour, (self.offset + self.solution[i-1][1] * self.length + round(self.length / 2),
                                                                      self.offset + self.solution[i-1][0] * self.length + round(self.length / 2)),
                                 (self.offset + self.solution[i][1] * self.length + round(self.length / 2),
                                  self.offset + self.solution[i][0] * self.length + round(self.length / 2)), 2)
                self.maze_surfaceRect = self.maze_surface.get_rect(center=(300, 300))
                self.window.blit(self.maze_surface, self.maze_surfaceRect) #adds the simulated solution step to the window
                pygame.display.update() #updates display
                time.sleep(0.05)
            simulate_button = Column_Text("Simulate/ Solution ", 400, 658, self.window, font6, True, (255, 255, 255)) #sets the simulate button to be available and not green
            solution_button = Column_Text("Show/ Solution ", 530, 658, self.window, font6, True, (144, 238, 144)) #set the solution button to be green and active
            self.return_button = Column_Text("Return to/ Main Menu ", 77, 658, self.window, font6, True,(255, 255, 255)) #sets the return button to be available and not greyed out
            self.simulate_toggle = False
            self.solution_toggle = True
        self.maze_surfaceRect = self.maze_surface.get_rect(center=(300, 300))
        self.window.blit(self.maze_surface, self.maze_surfaceRect) #adds the maze surface to the window

    def maze_gui(self):
        pygame.display.set_caption("Maze") #sets the caption of the Maze Interface
        self.window.fill((255,255,255))
        pygame.draw.line(self.window, (0, 0, 0), (0, 0), (800, 0), 1)
        self.return_button = Column_Text("Return to/ Main Menu ", 77, 658, self.window, font6, True, (200,200,200)) #creates the return button
        self.create_maze_surface() #creates the maze interface
        pygame.draw.rect(self.window,(0,0,0),[15,15,570,570],2)
        solution_button = Column_Text("Show/ Solution ", 530, 658, self.window, font6, True, (200, 200, 200)) #creates the solution button
        simulate_button = Column_Text("Simulate/ Solution ",400,658,self.window,font6, True, (200,200,200)) #creates the simulate button
        redraw_solution_button = False
        redraw_simulate_button = False
        solution_found = False
        desperation = 1
        while True: #repeats until a force close or return to menu
            for event in pygame.event.get():
                if solution_found == False: #checks to see if solution was found
                    for i in range(0,50*desperation+1):
                        if i%50 == 0:
                            pygame.event.get() #to make sure the display is always updated
                        if len(self.solution) == 0: #will solve the maze until the solution is found
                            self.solve_maze()
                if len(self.solution) == 0: #makes it so the solution will be found faster
                    desperation += 1
                if event.type == QUIT: #checks for a force close
                    pygame.quit()
                    quit()
                if event.type == MOUSEBUTTONDOWN: #checks for a mouse click
                    pos = pygame.mouse.get_pos() #gets the current mouse position
                    if self.return_button.rect.x+self.return_button.width>pos[0]>self.return_button.rect.x and \
                            self.return_button.rect.y+self.return_button.height>pos[1]>self.return_button.rect.y: #checks if the return button was clicked
                        self.window.fill((255,255,255)) #resets the window
                        return #goes back to main menu
                    elif solution_button.rect.x+solution_button.width>pos[0]>solution_button.rect.x and \
                            solution_button.rect.y+solution_button.height>pos[1]>solution_button.rect.y and solution_found == True: #checks if solution button was pressed
                        self.solution_toggle = not self.solution_toggle #changes the solution toggle
                        redraw_solution_button = True
                    elif simulate_button.rect.x+simulate_button.width>pos[0]>simulate_button.rect.x and \
                            simulate_button.rect.y+simulate_button.height>pos[1]>simulate_button.rect.y and solution_found == True: #checks if the simulate button was pressed
                        self.simulate_toggle = True #changes the simulate toggle
                        self.solution_toggle = False #changes the simulate toggle
                        redraw_simulate_button = True
                        redraw_solution_button = True
                if solution_found == False and len(self.solution) > 0: #updates buttons to make them available
                    self.return_button = Column_Text("Return to/ Main Menu ", 77, 658, self.window, font6, True,(255,255,255)) #makes the return button available
                    solution_button = Column_Text("Show/ Solution ", 530, 658, self.window, font6, True,(255, 255, 255)) #makes the solution button available
                    simulate_button = Column_Text("Simulate/ Solution ", 400, 658, self.window, font6, True,(255,255,255)) #makes the simulate button available
                    solution_found = True
                if redraw_solution_button == True: #will update the solution button
                    redraw_solution_button = False
                    if self.solution_toggle == True:
                        solution_button = Column_Text("Show/ Solution ", 530, 658, self.window, font6, True,(144,238,144)) #makes the button green and active
                        self.create_maze_surface() #redraws the maze surface
                    elif self.solution_toggle == False:
                        solution_button = Column_Text("Show/ Solution ", 530, 658, self.window, font6, True,(255, 255, 255)) #makes the button normal and inactive
                        self.create_maze_surface()
                if redraw_simulate_button == True: #will update the simulation button
                    if self.simulate_toggle == True:
                        self.create_maze_surface() #redraws the maze surface


                clock = pygame.time.Clock()
                clock.tick(60)
                pygame.display.update()

    def remove_wall(self,first,last):  #uses coords as tuples and removes walls between the 2 points
        if first[1] == last[1] and first[0]+1 == last[0]:  #compares y and x components
            self.maze[first[0]][first[1]][1],self.maze[last[0]][last[1]][0] = 0,0  #removes bottom(first) and top(last) walls

        elif first[1] == last[1] and first[0]-1 == last[0]:  #compares y and x components
            self.maze[first[0]][first[1]][0],self.maze[last[0]][last[1]][1] = 0,0  #removes top(first) and bottom(last) walls

        elif first[0] == last[0] and first[1]+1 == last[1]: #compares x and y components
            self.maze[first[0]][first[1]][3], self.maze[last[0]][last[1]][2] = 0,0  #removes right(first) and left(last) walls

        elif first[0] == last[0] and first[1]-1 == last[1]: #compares x and y components
            self.maze[first[0]][first[1]][2], self.maze[last[0]][last[1]][3] = 0,0  #removes left(first) and right(last) walls

    def adjacent_cells(self):  #finds the adjacent cells to the maze generator's current cell
        temp = []
        temp.append((self.y+1,self.x))  #calculates any adjacent cells to the current one
        temp.append((self.y-1,self.x))
        temp.append((self.y,self.x+1))
        temp.append((self.y,self.x-1))
        temp2 = []
        for i in temp:  #if any adjacent cells produced in the area
            if (i[0] >= 0 and i[0]<self.y_size) and (i[1] >= 0 and i[1]<self.x_size):
                temp2.append(i)  #adds it to a new array that is then returned
        return temp2

    def remove_visited(self,arr):  #removes the visited cells from the adjacent cells bit (most likely will take input from adjacent_cells function)
        temp = []
        for i in arr:
            if i in self.visited:  #if any adjacent cells produced are in self.visited, nothing happens
                x = 0
            else:  #if any adjacent cells produced are not in self.visited,  then they are added to a new array that is outputted
                temp.append(i)
        return temp

    # 1. Choose the initial cell, mark it as visited and push it to the stack
    # 2. If any of the neighbouring cells aren't visited go to them
    # 3. Remove walls
    # 4. Mark the new one as visited
    # 5. Add the new cell to path cells
    # 6. Mark new one as current cell
    # 7. If all adjacent cells are visited then go back to previous path cell and remove the last value in path
    # 8. Repeat until len(visited) is same as the amount of cells(x_size*y_size)
    def create_maze(self):
        self.visited.append((self.y,self.x))  #adds the current to visited
        self.path.append((self.y,self.x))  #adds the current to path
        while len(self.visited) != self.x_size*self.y_size:  #while the length is not the same size as the area of the maze
            data = self.remove_visited(self.adjacent_cells())  #calculates adjacent cells and removes any of the visited cells
            if len(data) == 0:  #if there was no possible cells
                self.y,self.x = self.path[len(self.path)-1][0],self.path[len(self.path)-1][1]  #goes back to the last position it went to
                self.path.remove(self.path[len(self.path)-1])  #removes the last position it went to from array
            elif len(data) != 0:  #if there is possible cells that aren't visited
                choice = random.randint(0,len(data)-1)  #chooses a random position from the possible cells
                self.remove_wall((self.y,self.x),data[choice])  #removes wall between the current cell and the random cell that was chosen
                self.y,self.x = data[choice][0],data[choice][1]  #updates the value for the new cell it is in
                self.path.append(data[choice])  #adds the new cell to path and to visited
                self.visited.append(data[choice])
            #self.display_maze(1)  #used to see where the maze's current cell is and how it is removing walls
        self.create_possible_moves()
        self.possible_attached_cells()

    def create_possible_moves(self):  #creates an array of possible moves the sprite can make for each cell
        self.possible_moves = []
        self.q_table = []
        for i in range(0,len(self.maze)):  #for i in y column
            temp = []  #creates y column of possible_moves
            q_temp = []  #creates y column of q_table
            for j in range(0,len(self.maze[i])):  #for j in x column
                temp2 = []  #creates x column of possible_moves
                q_temp2 = []  #creates x column of q_table
                if self.maze[i][j][0] == 0:  #if the top of the cell is 0, add a 1 to move table and a random q value to the q_table
                    temp2.append(1)  #1 means move up
                    q_temp2.append(np.random.uniform(-7,0))
                if self.maze[i][j][1] == 0:  #if the bottom of the cell is 0, add a 2 to move table and a random q value to the q_table
                    temp2.append(2)  #2 means move down
                    q_temp2.append(np.random.uniform(-7,0))
                if self.maze[i][j][2] == 0:  #if the left of the cell is 0, add a 3 to move table and a random q value to the q_table
                    temp2.append(3)  #3 means move left
                    q_temp2.append(np.random.uniform(-7,0))
                if self.maze[i][j][3] == 0:  #if the right of the cell is 0, add a 4 to move table and a random q value to the q_table
                    temp2.append(4)  #4 means move right
                    q_temp2.append(np.random.uniform(-7,0))
                temp.append(temp2)  #adds x column to y column of the possible_moves
                q_temp.append(q_temp2)  #adds x column to y column of the q_table
            self.possible_moves.append(temp)  #adds y column to possible_moves
            self.q_table.append(q_temp)  #adds y column to q_table

    def sprite_move(self,choice):  # 1 moves up, 2 moves down, 3 moves left, 4 moves right
        if choice == 1:
            if self.sprite.y != 0:  #moves up
                self.sprite.y -= 1
        elif choice == 2:
            if self.sprite.y != self.y_size-1:  #moves down
                self.sprite.y += 1
        elif choice == 3:
            if self.sprite.x != 0:  #moves left
                self.sprite.x -= 1
        elif choice == 4:
            if self.sprite.x != self.x_size-1:  #moves right
                self.sprite.x += 1

    def possible_attached_cells(self): #function does the same as possible moves array but adds the tuple coords to a list
        self.possible_attached = [] #creates the possible attached array
        for i in range(0,len(self.maze)): #iterates through the y column
            temp = []
            for j in range(0,len(self.maze[i])): #iterates through the x column
                temp2 = []
                if self.maze[i][j][0] == 0: #if the top of the cell is 0, then tuple of the coord above is added to the array
                    temp2.append((i-1,j))
                if self.maze[i][j][1] == 0: #if the bottom of the cell is 0, then tuple of the coord below is added to array
                    temp2.append((i+1,j))
                if self.maze[i][j][2] == 0: #if the left of the cell is 0, then tuple of the coord to left is added to array
                    temp2.append((i,j-1))
                if self.maze[i][j][3] == 0: #if the right of the cell is 0, then tuple of the coord to right is added to array
                    temp2.append((i,j+1))
                temp.append(temp2) #adds x column to y column
            self.possible_attached.append(temp) #adds y column to the array

    def abstract_solution(self):
        temp = []
        for i in self.solution: #repeats for every value in the solution array
            if i in temp: #will remove any positions that were visited multiple times
                x = 0
            else:
                temp.append(i)
        self.solution = temp #sets it as the solution
        unattached = False
        while unattached == False: #repeats until unattached is True
            unattached = True
            temp = []
            temp.append(self.solution[0]) #adds the first position from the solution array to the new one
            for i in range(1,len(self.solution)): #repeats for every other position
                connections = 0
                data = self.possible_attached[self.solution[i][0]][self.solution[i][1]] #finds how many cells the current position in the iteration can be linked to
                for j in data:
                    if j in self.solution: #checks to see if any of the linked to cells are in the solution
                        connections += 1 #if any linked cells are in the solution it will add 1 to connections
                if connections == 1 and i != len(self.solution)-1: #if it finds a cell that is only attached to one other cell
                    unattached = False #make the loop restart after this iteration has finished
                elif connections >= 2: #adds the cell to the new array
                    temp.append(self.solution[i])
                if i == len(self.solution) -1: #adds the end point of the maze to the array
                    temp.append(self.solution[i])
            self.solution = temp #updates the solution

    def solve_maze(self):  # IMPLEMENT INTELLIGENCE
        eps_decay = 0.9999
        learning_rate = 0.1
        discount = 0.99
        self.sprite_path = []
        self.sprite.x = self.start_sprite_x  # sets the sprite back to the start
        self.sprite.y = self.start_sprite_y
        self.sprite_path.append((self.sprite.y, self.sprite.x))  # add the sprites start location to its path
        x = 0
        while x <= self.x_size * self.y_size:  # how many moves it can make per episode
            data = self.possible_moves[self.sprite.y][self.sprite.x]  # possible moves calculates possible moves for current location in a maze and returns an array
            if np.random.uniform() > self.epsilon:
                choice = np.argmax(self.q_table[self.sprite.y][self.sprite.x])
            else:
                choice = random.randint(0, len(data) - 1)
            curr_x, curr_y = self.sprite.x, self.sprite.y  # sets some variables to come back to
            curr_q = self.q_table[curr_y][curr_x][choice]  # gets the current q for its location and the move choice
            self.sprite_move(data[choice])  # actually moves the sprite
            max_future_q = np.max(self.q_table[self.sprite.y][self.sprite.x])  # finds the best possible q value for later on
            self.sprite_path.append((self.sprite.y, self.sprite.x))  # adds to the path
            if self.sprite.x == self.endpoint_x and self.sprite.y == self.endpoint_y:  # used to see if the AI reaches the end
                #print("We made it to the end!!!")
                new_q = 100  # rewards the bot for making it to the end
                self.q_table[curr_y][curr_x][choice] = new_q
                x = (self.x_size * self.y_size) ** 2  # ends the while loop
                self.solution = self.sprite_path
                self.abstract_solution()
            else:  # provides learning for the AI
                reward = -1
                new_q = (1 - learning_rate) * curr_q + learning_rate * (reward + discount * max_future_q)
                self.q_table[curr_y][curr_x][choice] = new_q  # updates the q value for the move that was taken
            x += 1
        self.epsilon = self.epsilon * eps_decay  # makes randomness less likely per episode



class Sprite:
    def __init__(self,x,y):
        self.x = x  #sets the position of the sprite
        self.y = y

    def display_coord(self):  #used for testing
        pos = (self.x,self.y)
        print(pos)

class Slider:
    def __init__(self, name, currVal, maxVal, minVal, xpos, ypos,colour,win):
        self.win = win
        self.currVal = currVal #sets the default val/ current val
        self.maxVal = maxVal #sets the max val
        self.minVal = minVal #sets the min val
        self.xpos = xpos
        self.ypos = ypos
        self.surf = pygame.surface.Surface((135, 50)) #creates the slider surface

        self.hit = False

        self.txtSurface = font3.render(name, 1, (0, 0, 0)) #adds a label to the slider
        self.txtwidth = self.txtSurface.get_width()
        self.txtheight = self.txtSurface.get_height()
        self.txtSurfaceRect = self.txtSurface.get_rect(center=(50, 15))
        self.surf.fill(colour) #fills the slider with the colour chosen
        pygame.draw.rect(self.surf,(255,255,255),[50-round(self.txtwidth/2)-1,15-round(self.txtheight/2)+2,self.txtwidth+3,self.txtheight]) #makes label background white
        pygame.draw.rect(self.surf, (0,0,0), [0, 0, 135, 50], 3) #adds a box to the slider surface
        pygame.draw.rect(self.surf, (255, 255, 255), [10, 30, 80, 5], 0) #creates the actual slider itself
        pygame.draw.rect(self.surf, (0,0,0), [10, 30, 80, 5], 1) #adds a border to the actual slider
        pygame.draw.rect(self.surf, (255, 255, 255), [100, 15, 25, 25], 0) #adds a square to the slider where the currval will be shown
        pygame.draw.rect(self.surf, (0,0,0), [100, 15, 25, 25], 1) #adds a border to the currval square
        self.surf.blit(self.txtSurface, self.txtSurfaceRect) #adds the label to the slider surface

        self.buttonSurf = pygame.surface.Surface((20, 20)) #creates the button which slider will use
        self.buttonSurf.fill((1, 1, 1))
        self.buttonSurf.set_colorkey((1, 1, 1))
        pygame.draw.circle(self.buttonSurf, (0, 0, 0), (10, 10), 6, 0) #adds a circle to the button surface
        pygame.draw.circle(self.buttonSurf, (0,0,0), (10, 10), 4, 0) #

    def draw(self):
        surf = self.surf.copy()
        pos = (10 + int((self.currVal - self.minVal) / (self.maxVal - self.minVal) * 80), 33 ) #finds the current pos of the button of slider
        self.buttonRect = self.buttonSurf.get_rect(center=pos)
        surf.blit(self.buttonSurf, self.buttonRect) #adds the button to the slider surface

        self.buttonRect.move_ip(self.xpos, self.ypos)
        self.win.blit(surf, (self.xpos, self.ypos)) #adds the slider to the window

        pygame.draw.rect(self.surf, (255, 255, 255), [100, 15, 25, 25], 0) #redraws the currval square onto slider
        pygame.draw.rect(self.surf, (0, 0, 0), [100, 15, 25, 25], 1)
        self.txtValue = font.render(str(round(self.currVal)),1,(0, 0, 0)) #renders the currval
        self.txtValueRect = self.txtValue.get_rect(center=(112,27))
        self.surf.blit(self.txtValue, self.txtValueRect) #adds the currval to the slider in it's position

    def moveSlider(self):
        self.currVal = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxVal - self.minVal) + self.minVal #finds the current value the slider is on
        if self.currVal < self.minVal: #sets the current val of the slider to be minVal when moved far left
            self.currVal = self.minVal
        if self.currVal > self.maxVal: #sets the current val of the slider to be maxVal when moved far right
            self.currVal = self.maxVal

class Colour_Picker:
    def __init__(self,choice,r,g,b):
        self.choice = choice
        self.colours = (r,g,b) #sets the colour as a tuple
        self.win = pygame.display.set_mode((600,800))
        self.win.fill((255, 255, 255))
        self.red = Slider("Red", r, 255, 0, 90, 585,(255, 50, 50),self.win) #creates a slider for the value of "r"
        self.green = Slider("Green", g, 255, 0, 232.5, 585,(0, 255, 50),self.win) #creates a slider for the value of "g"
        self.blue = Slider("Blue", b, 255, 0, 375, 585,(50, 50, 235),self.win) #creates a slider for the value of "b"

    def redraw(self):
        self.win.fill((255, 255, 255))
        pygame.draw.line(self.win, (0, 0, 0), (0, 0), (800, 0), 1)
        self.header = font2.render("Choose your " + self.choice, 1, (0, 0, 0)) #adds a Header
        self.headerRect = self.header.get_rect(center=(300, 65))
        self.win.blit(self.header, self.headerRect) #adds the header to the window
        self.done_button = Button(" Done ",525,700,self.win,font2) #creates the done button
        self.sliders = [self.red, self.green, self.blue] #creates an array that can be used to check for slider inputs
        pygame.display.set_caption(self.choice) #updates the display caption

    def draw(self):
        self.redraw() #makes sure the GUI is shown
        while True: #repeats till force close or user presses done button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #checks for a force close
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: #checks for mouse clicks
                    pos = pygame.mouse.get_pos() #gets the mouse position
                    if self.done_button.rect.x +self.done_button.rect.width > pos[0] > self.done_button.rect.x and \
                            self.done_button.rect.y +self.done_button.rect.height > pos[1] > self.done_button.rect.y: #checks if the done button was clicked
                        self.colours = (round(self.red.currVal),round(self.green.currVal),round(self.blue.currVal))
                        self.win.fill((255,255,255)) #resets the window
                        return True #goes back to main menu
                    else:
                        for s in self.sliders:
                            if s.buttonRect.collidepoint(pos): #checks if any sliders have been clicked
                                s.hit = True
                elif event.type == pygame.MOUSEBUTTONUP: #stops the click on sliders
                    for s in self.sliders:
                        s.hit = False
            # Move slides
            for s in self.sliders: #checks for any clicks on sliders
                if s.hit:
                    s.moveSlider() #moves the slider that was clicked
            #Update Screen
            for s in self.sliders: #checks all sliders
                s.draw() #updates the sliders
                pygame.draw.circle(self.win, (self.red.currVal,self.green.currVal,self.blue.currVal), (300,330),200, 0) #updates the chosen colour
                pygame.draw.circle(self.win, (0, 0, 0), (300,330),200, 3)
            pygame.display.flip() #updates the display

class Column_Text:
    def __init__(self,string,xpos,ypos,win,font,boxed,colour):
        self.string = string
        self.xpos = xpos #xpos is the centre of x-axis where txt/box will be placed
        self.ypos = ypos #ypos is the top of where the txt/box will be placed
        self.win = win
        self.font = font
        self.boxed = boxed #value to make this into a button
        self.colour = colour #background colour
        self.create_interface()

    def create_interface(self):
        self.height = 0 #sets height and width to be 0
        self.width = 0
        list = [] #creates a list
        single = ""
        for i in self.string:
            if i != "/":
                single = single + i #for every character that isn't a / it will add it to the single variable
            else:
                list.append(single) #if the character was a / then the word will be placed in a list
                txt = self.font.render(single,1,(0,0,0)) #renders the word that is stored in single
                self.height += txt.get_height() #adds the height of the rendered work to height
                if self.width < txt.get_width():
                    self.width = txt.get_width() #finds the max width of the text needed
                single = ""
        list.append(single)
        txt = self.font.render(single, 1, (0, 0, 0)) #renders the last word
        self.height += txt.get_height() #adds the height of the last word
        if self.width < txt.get_width():
            self.width = txt.get_width() #updates the max width of the txt
        self.surface = pygame.surface.Surface((self.width,self.height)) #creates a surface with dimensions width and height
        self.surface.fill((self.colour)) #fills the surface with a background
        if self.boxed == True: #will create a box around the surface
            pygame.draw.rect(self.surface,(0,0,0),[0,0,self.width,self.height],1)
        old_txt = self.font.render(list[0],1,(0,0,0)) #renders the first word in the list
        very_old_txt = self.font.render(list[0], 1, (0, 0, 0)) #renders the first word in the list
        old_txtSurface = old_txt.get_rect(center=((self.width)/2,very_old_txt.get_height()/2)) #finds the dimensions and key pos of the first word
        self.surface.blit(old_txt,old_txtSurface) #adds the first word to the surface
        for i in range(1,len(list)): #repeats for every other word in the list
            new_txt = self.font.render(list[i],1,(0,0,0)) #renders the word from the list
            new_txtSurface = new_txt.get_rect(center=((self.width)/2,(very_old_txt.get_height()/2)+ old_txt.get_height()*i))#finds the dimensions and key pos of the current word
            self.surface.blit(new_txt,new_txtSurface) #adds the word to the surface
            old_txt = new_txt #updates old word to be the new word
            old_txtSurface = new_txtSurface #updates old word surface to the new word surface
        self.win.blit(self.surface,((self.xpos-((self.width)/2)),self.ypos)) #adds the surface to the main window
        self.rect = self.surface.get_rect(center=(self.xpos,self.ypos+((self.height)/2)))  #use this to get the values needed for mouse clicks when using a button form

class Button:
    def __init__(self,string,xpos,ypos,win,font):
        self.string = string #string is the text that will be displayed on the button
        self.xpos = xpos #takes the x value for the centre of the button
        self.ypos = ypos #takes the y value for the top of the button
        self.win = win
        self.font = font
        self.create_button()

    def create_button(self):
        txt = self.font.render(self.string,1,(0,0,0)) #renders the font in
        self.height = txt.get_height()
        self.width = txt.get_width()
        self.surface = pygame.surface.Surface((self.width,self.height)) #creates a button surface that is the same height and width as the text
        self.surface.fill((255,255,255)) #fills the surface in with white
        txt_surface = txt.get_rect(center=((self.width/2,self.height/2))) #creates a surface that centres the text in the middle
        pygame.draw.rect(self.surface, (0, 0, 0), [0, 0, self.width, self.height], 1) #creates the box around the button
        self.surface.blit(txt,txt_surface) #adds the txt to the txt_surface then appends it to the button surface
        self.win.blit(self.surface,((self.xpos-((self.width)/2)),self.ypos)) #places the button surface on the window
        self.rect = self.surface.get_rect(center=(self.xpos,self.ypos+((self.height)/2))) #finds the dimensions and key points of the button

class Help:
    def __init__(self,win):
        self.clock = pygame.time.Clock()
        self.win = win
        self.win.fill((255,255,255)) #fills the window in as white
        pygame.draw.line(self.win, (0, 0, 0), (0, 0), (800, 0), 1)
        pygame.display.set_caption("Help") #sets the display's caption
        self.done_button = Button(" Done ", 525, 700, self.win, font2) #creates the done button
        self.header = font5.render("Instructions", 1, (0, 0, 0)) #creates the header
        self.headerRect = self.header.get_rect(center=(300, 35)) #creates a surface for the header
        self.win.blit(self.header, self.headerRect) #adds the text to the surface then adds that to the window
        self.string = "- Use the Slider to change the Height///- Use the Slider to change the Width///- Primary colour button will change the Background of the Maze///- Secondary colour button will change the Colour of the Lines///- Choose the Start point///- Choose the End point///- Press Generate to generate///- Wait for Buttons to not be greyed out"
        #Text that will be in the format for Column_Text class
        self.text = Column_Text(self.string, 300, 146, self.win, font3, False, (255, 255, 255)) #turns the string into text that is centred
        while True: #repeats until forced to quit or button is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #searches for a force quit
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN: #checks for mouse clicks
                    pos = pygame.mouse.get_pos() #gets the mouse position
                    if self.done_button.rect.x + self.done_button.rect.width > pos[0] > self.done_button.rect.x \
                            and self.done_button.rect.y + self.done_button.rect.height > pos[1] > self.done_button.rect.y: #checks if the mouse clicked a button
                        return #goes back to the main menu
            pygame.display.update()
            self.clock.tick(60)

class Menu:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.redraw_val = True
        self.win = pygame.display.set_mode((600,800))
        self.primary_colour = Colour_Picker("Primary Colour",255,255,255) #creates the colour_picker menu for the primary colour #also sets white as default
        self.secondary_colour = Colour_Picker("Secondary Colour",0,0,0) #creates the colour picker menu for the secondary colour #also sets black as default
        self.win.fill((255, 255, 255))
        self.startpoint = 1 #set startpoint to top left
        self.endpoint = 4 #set endpoint to bottom right
        self.height = Slider("Height",20,40,2,115,195,(255,255,255),self.win) #creates a height slider #sets default to 20
        self.width = Slider("Width", 20, 40, 2, 355, 195, (255,255,255), self.win) #creates a width slider #sets default to 20
        self.draw_txt() #draws all the txt based stuff
        self.sliders = [self.height,self.width] #creates a array to check for slider changes
        self.display() #displays the menu

    def draw_txt(self):
        self.startpointtxt = font4.render("Startpoint:", 1, (0, 0, 0)) #renders the start point text
        self.startpointtxtsurface = self.startpointtxt.get_rect(center=(100, 453))
        self.endpointtxt = font4.render("Endpoint:", 1, (0, 0, 0)) #renders the end point text
        self.endpointtxtsurface = self.endpointtxt.get_rect(center=(100, 556))
        self.win.blit(self.startpointtxt, self.startpointtxtsurface) #adds the start point txt to the window
        self.win.blit(self.endpointtxt, self.endpointtxtsurface) #adds the end point txt to the window

    def redraw(self):
        pygame.draw.line(self.win,(0,0,0),(0,0),(800,0),1)
        self.Header = Column_Text("Maze/Generator", 300, 5, self.win, font5, False,(255,255,255)) #creates the title for the main menu
        self.primary = Button(" Primary Colour ", 128, 326, self.win, font6) #creates the button to change primary colour
        self.secondary = Button(" Secondary Colour ", 401, 326, self.win, font6) #creates the button to change secondary colour
        self.help = Button(" ? ",33,10,self.win,font7) #creates a help button
        self.quit = Button(" Quit ",200,675,self.win,font7) #creates a quit button
        self.generate = Button(" Generate ",400,675,self.win,font7) #creates the generate button
        self.start_TL = Column_Text("Top/ Left ",self.startpointtxtsurface.x+self.startpointtxtsurface.width+50,435,self.win,font3,
                                    True,(255,255,255)) #creates buttons for start points
        self.start_TR = Column_Text("Top/ Right ", self.startpointtxtsurface.x+self.startpointtxtsurface.width+self.start_TL.width+50*2,
                                    435, self.win, font3, True,(255,255,255))
        self.start_BL = Column_Text(" Bottom /Left", self.startpointtxtsurface.x+self.startpointtxtsurface.width+self.start_TL.width+
                                    self.start_TR.width+50*3, 435, self.win, font3, True,(255,255,255))
        self.start_BR = Column_Text(" Bottom /Right", self.startpointtxtsurface.x+self.startpointtxtsurface.width+self.start_TL.width+
                                    self.start_TR.width+self.start_BL.width+50*4, 435, self.win, font3, True,(255,255,255))
        self.end_TL = Column_Text("Top/ Left ",self.start_TL.rect.x +self.start_TL.width/2,535,self.win,font3, True,(255,255,255)) #creates buttons for end points
        self.end_TR = Column_Text("Top/ Right ", self.start_TR.rect.x+self.start_TR.width/2, 535, self.win, font3, True,(255,255,255))
        self.end_BL = Column_Text(" Bottom /Left", self.start_BL.rect.x+self.start_BL.width/2, 535, self.win, font3, True,(255,255,255))
        self.end_BR = Column_Text(" Bottom /Right", self.start_BR.rect.x+self.start_BR.width/2, 535, self.win, font3, True,(255,255,255))
        self.chosen_colour = (220,20,60) #sets a colour to shown when a button is currently chosen
        if self.startpoint == 1: #changes the border colour of the start point selected
            pygame.draw.rect(self.win,self.chosen_colour,[self.start_TL.rect.x,self.start_TL.rect.y,self.start_TL.width,self.start_TL.height],1)
        if self.startpoint == 2:
            pygame.draw.rect(self.win,self.chosen_colour,[self.start_TR.rect.x,self.start_TR.rect.y,self.start_TR.width,self.start_TR.height],1)
        if self.startpoint == 3:
            pygame.draw.rect(self.win,self.chosen_colour,[self.start_BL.rect.x-1,self.start_BL.rect.y,self.start_BL.width,self.start_BL.height],1)
        if self.startpoint == 4:
            pygame.draw.rect(self.win,self.chosen_colour,[self.start_BR.rect.x-1,self.start_BR.rect.y,self.start_BR.width,self.start_BR.height],1)
        if self.endpoint == 1: #changes the border colour of the end point selected
            pygame.draw.rect(self.win,self.chosen_colour,[self.end_TL.rect.x,self.end_TL.rect.y,self.end_TL.width,self.end_TL.height],1)
        if self.endpoint == 2:
            pygame.draw.rect(self.win,self.chosen_colour,[self.end_TR.rect.x,self.end_TR.rect.y,self.end_TR.width,self.end_TR.height],1)
        if self.endpoint == 3:
            pygame.draw.rect(self.win,self.chosen_colour,[self.end_BL.rect.x,self.end_BL.rect.y,self.end_BL.width,self.end_BL.height],1)
        if self.endpoint == 4:
            pygame.draw.rect(self.win,self.chosen_colour,[self.end_BR.rect.x,self.end_BR.rect.y,self.end_BR.width,self.end_BR.height],1)
        pygame.draw.rect(self.win, self.primary_colour.colours, [223, 321, 36, 36], 0) #shows the current colour alongside the primary colour button
        pygame.draw.rect(self.win, (0, 0, 0), [223, 321, 36, 36], 2)
        pygame.draw.rect(self.win, self.secondary_colour.colours, [510, 321, 36, 36], 0) #shows the current colour alongside the secondary colour button
        pygame.draw.rect(self.win, (0, 0, 0), [510, 321, 36, 36], 2)
        pygame.display.set_caption("Main Menu") #sets the caption to Main Menu

    def display(self):
        while True:
            if self.redraw_val == True:
                self.redraw() #draws the buttons onto the gui
                self.redraw_val = not self.redraw_val
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #checks for a force close
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN: #checks for a mouse click
                    pos = pygame.mouse.get_pos() #gets the current mouse position
                    if self.quit.rect.x + self.quit.width > pos[0] > self.quit.rect.x and \
                            self.quit.rect.y + self.quit.height > pos[1] > self.quit.rect.y: #checks if quit button was pressed
                        pygame.quit()
                        quit()
                    elif self.generate.rect.x + self.generate.width > pos[0] > self.generate.rect.x and \
                            self.generate.rect.y + self.generate.height > pos[1] > self.generate.rect.y: #checks if generate button was pressed
                        #creates the Maze using user choices
                        self.maze = Maze(round(self.width.currVal),round(self.height.currVal),self.startpoint,self.endpoint,
                                         self.primary_colour.colours,self.secondary_colour.colours)
                        self.maze.maze_gui() #displays the Maze
                        self.win = pygame.display.set_mode((600, 800))
                        self.win.fill((255, 255, 255))
                        self.draw_txt() #redraws all the txt when the user finishes with the Maze interface
                        self.redraw_val = True #sets a value to redraw buttons
                    elif self.primary.rect.x + self.primary.width > pos[0] > self.primary.rect.x and \
                            self.primary.rect.y + self.primary.height> pos[1] > self.primary.rect.y: #checks if primary colour button was clicked
                        self.primary_colour.draw() #displays primary colour picker GUI
                        self.draw_txt()
                        self.redraw_val = True
                    elif self.secondary.rect.x + self.secondary.width > pos[0] > self.secondary.rect.x and \
                            self.secondary.rect.y + self.secondary.height> pos[1] > self.secondary.rect.y: #checks if secondary colour button was clicked
                        self.secondary_colour.draw() #displays secondary colour picker GUI
                        self.draw_txt()
                        self.redraw_val = True
                    #this will check if any of the start points have been clicked and will make sure they can't be the same as the endpoint
                    elif self.start_TL.rect.x + self.start_TL.width > pos[0] > self.start_TL.rect.x and \
                            self.start_TL.rect.y + self.start_TL.height > pos[1] > self.start_TL.rect.y and self.endpoint!=1:
                        self.startpoint = 1 #updates the startpoint
                        self.redraw_val = True
                    elif self.start_TR.rect.x + self.start_TR.width > pos[0] > self.start_TR.rect.x and \
                            self.start_TR.rect.y + self.start_TR.height > pos[1] > self.start_TR.rect.y and self.endpoint!=2:
                        self.startpoint = 2
                        self.redraw_val = True
                    elif self.start_BL.rect.x + self.start_BL.width > pos[0] > self.start_BL.rect.x and \
                            self.start_BL.rect.y + self.start_BL.height > pos[1] > self.start_BL.rect.y and self.endpoint!=3:
                        self.startpoint = 3
                        self.redraw_val = True
                    elif self.start_BR.rect.x + self.start_BR.width > pos[0] > self.start_BR.rect.x and \
                            self.start_BR.rect.y + self.start_BR.height > pos[1] > self.start_BR.rect.y and self.endpoint!=4:
                        self.startpoint = 4
                        self.redraw_val = True
                    # this will check if any of the end points have been clicked and will make sure they can't be the same as the startpoint
                    elif self.end_TL.rect.x + self.end_TL.width > pos[0] > self.end_TL.rect.x and \
                            self.end_TL.rect.y + self.end_TL.height > pos[1] > self.end_TL.rect.y and self.startpoint!=1:
                        self.endpoint = 1 #updates the endpoint
                        self.redraw_val = True
                    elif self.end_TR.rect.x + self.end_TR.width > pos[0] > self.end_TR.rect.x and \
                            self.end_TR.rect.y + self.end_TR.height > pos[1] > self.end_TR.rect.y and self.startpoint!=2:
                        self.endpoint = 2
                        self.redraw_val = True
                    elif self.end_BL.rect.x + self.end_BL.width > pos[0] > self.end_BL.rect.x and \
                            self.end_BL.rect.y + self.end_BL.height > pos[1] > self.end_BL.rect.y and self.startpoint!=3:
                        self.endpoint = 3
                        self.redraw_val = True
                    elif self.end_BR.rect.x + self.end_BR.width > pos[0] > self.end_BR.rect.x and \
                            self.end_BR.rect.y + self.end_BR.height > pos[1] > self.end_BR.rect.y and self.startpoint!=4:
                        self.endpoint = 4
                        self.redraw_val = True
                    elif self.help.rect.x + self.help.rect.width> pos[0] > self.help.rect.x and \
                            self.help.rect.y + self.help.rect.height > pos[1] > self.help.rect.y: #checks if help button was clicked
                        Help(self.win) #displays the help menu
                        self.win = pygame.display.set_mode((600, 800))
                        self.win.fill((255, 255, 255))
                        self.draw_txt()
                        self.redraw_val = True
                    for s in self.sliders: #checks for any slider changes
                        if s.buttonRect.collidepoint(pos): #if a slider is clicked
                            s.hit = True
                elif event.type == pygame.MOUSEBUTTONUP: #checks if a slider is not clicked anymore
                    for s in self.sliders:
                        s.hit = False

                for s in self.sliders: #checks if any sliders were clicked then moves them accordingly
                    if s.hit:
                        s.moveSlider()

                # Update Screen
                for s in self.sliders: #updates each slider
                    s.draw()
                pygame.display.flip() #flips the display
            pygame.display.update() #updates display
            self.clock.tick(60)

menu = Menu()


