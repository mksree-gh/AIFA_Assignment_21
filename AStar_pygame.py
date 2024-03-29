#AIFA Assignment
#A* Algorithm for Path Planning

#Team Members = [(Keerthi Sree Marrapu 20MF10015),(Sudeshna Bose,21MM61R04), (Pendem Ganesh, 20ME10061)

import math
import pygame	#Using pygame environment to visualise A star Algorithm
import time		#To delay the program for better understanding of the working of the code
from queue import PriorityQueue	#Efficient way to find the minimum element

#Global Variables
SPAN = 800
ROWS = 60
SCREEN = pygame.display.set_mode((SPAN, SPAN))
pygame.display.set_caption("A* Algorithm for Path Planing")

#Specifying Color codes
BEGIN_C = (227, 180, 72)
END_C = (42, 161, 15)

FREET_C = (255, 255, 255)
GRID_C = (238, 237, 231)
OBSTACLE_C = (0, 0, 0)

CLOSEDT_C = (210, 43, 43)
OPENT_C = (144, 238, 144)

FINALP_C = (0, 48, 96)

class Tile:
	def __init__(self, row, col, span, total_rows):
		#Defining variables corresponding to each tile
		self.row = row
		self.col = col
		self.x = row * span
		self.y = col * span
		self.color = FREET_C
		self.span = span
		self.total_rows = total_rows

	#Define the colors
	def mark_begin(self):
		self.color = BEGIN_C

	def mark_end(self):
		self.color = END_C

	def mark_obstacle(self):
		self.color = OBSTACLE_C

	#Find position of the vehicle
	def get_pos(self):
		return self.row, self.col

	#Tiles indicating their staus - whether they are in open list / closed list
	def mark_open(self):
		self.color = OPENT_C

	def mark_closed(self):
		self.color = CLOSEDT_C

	#Final path color
	def create_path(self):
		self.color = FINALP_C

	#Checking if the given tile is an obstacle. If obstacle, function returns TRUE
	def check_obstacle(self):
		return self.color == OBSTACLE_C

	#Reset grid
	def reset(self):
		self.color = FREET_C

	#Drawing the grid
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.span, self.span))

	#adj_tiles will only have those tiles which can be taken, i.e., it removes tiles which are obstacles
	def update_adj_tiles(self, grid):
		self.adj_tiles = []

		#Moving Forwards
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].check_obstacle():
			self.adj_tiles.append(grid[self.row][self.col + 1])
		#Moving Backwards
		if self.col > 0 and not grid[self.row][self.col - 1].check_obstacle():
			self.adj_tiles.append(grid[self.row][self.col - 1])
		#Moving Upwards
		if self.row > 0 and not grid[self.row - 1][self.col].check_obstacle():
			self.adj_tiles.append(grid[self.row - 1][self.col])
		#Moving Downwards
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].check_obstacle(): # DOWN
			self.adj_tiles.append(grid[self.row + 1][self.col])

#Gives the heuristic estimate of a node
def dist(t1, t2):
	x1,y1 = t1
	x2,y2 = t2
	#Manhattan Distance is being returned (since we are considering our vehicle cannot traverse diagonally)
	return abs(x1-x2)+abs(y1-y2)

def algorithm(draw, grid, begin, end):
	count = 0
	open_list = PriorityQueue()
	open_list.put((0, count, begin)) #First parameter here is the f(x)=0

	#To keep track of which tile we came from,
	from_tile = {}

	#We initialise all unexplored tiles with g and h values to be infinity, assuming that it takes infinity to reach there

	gValue = {tile: float("inf") for row in grid for tile in row}
	gValue[begin] = 0  #At starting node, g(x) is zero

	fValue = {tile: float("inf") for row in grid for tile in row}
	#f(x) = h(x)+g(x)
	#h(x)=heuristic function=distance between beginning tile and end tile
	fValue[begin] = dist(begin.get_pos(), end.get_pos()) + gValue[begin]

	#To keep track of what items are there in open_list, making a set
	open_list_set = {begin}

	while not open_list.empty():

		#To quit the loop,
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		present_tile = open_list.get()[2] #To get the tile parameter from open_list
		open_list_set.remove(present_tile) #To remove duplicates

		if present_tile == end:
			rebuild_path(from_tile, end, draw)
			end.mark_end()
			#time.sleep(0.8)
			return True

		for adj_tile in present_tile.adj_tiles:
			#Adding 1 because we are assuming the distance between a tile and its adjacent tile is 1
			tent_gValue = gValue[present_tile] + 1

			#Finding the minimum g value and keeping track of that path
			if tent_gValue < gValue[adj_tile]:
				from_tile[adj_tile] = present_tile
				gValue[adj_tile] = tent_gValue

				#f(n)=g(n)+h(n)
				fValue[adj_tile] = tent_gValue + dist(adj_tile.get_pos(), end.get_pos())

				#If the adj_tile has lesser f value, and is not in the open_list, then we increase count and we add it to the list
				if adj_tile not in open_list_set:
					count += 1
					open_list.put((fValue[adj_tile], count, adj_tile))
					open_list_set.add(adj_tile)
					adj_tile.mark_open()
					#time.sleep(0.8)

		draw()

		if present_tile != begin:
			present_tile.mark_closed()

	return False

def rebuild_path(from_tile, present_tile, draw):
	while present_tile in from_tile:
		present_tile = from_tile[present_tile]
		present_tile.create_path()
		#time.sleep(0.5)
		draw()

#Building the required grid map
def build_grid(rows, span):
	grid = []
	width = span // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			tile = Tile(i, j, width, rows)
			grid[i].append(tile)

	return grid

def draw_grid(screen, rows, span):
	width = span // rows
	for i in range(rows):
		pygame.draw.line(screen, GRID_C, (0, i*width), (span, i*width))

		for j in range(rows):
			pygame.draw.line(screen, GRID_C, (j*width, 0), (j*width, span))

def draw(screen, grid, rows, span):
	screen.fill(FREET_C)

	for row in grid:
		for tile in row:
			tile.draw(screen)

	draw_grid(screen, rows, span)
	pygame.display.update()

#returns position of the tiles
def get_clicked_pos(loc, rows, span):
	width = span // rows
	j, i = loc

	row = j // width
	col = i // width

	return row, col

def main(screen, span):

	grid = build_grid(ROWS, span)

	begin = None
	end = None

	run = True
	while run:

		#draws the grid
		draw(screen, grid, ROWS, span)

		#Ends running when we click the 'x' button
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			#Using left mouse button to define the begining, ending tiles and obstacles
			if pygame.mouse.get_pressed()[0]: # Left mouse button
				loc = pygame.mouse.get_pos()
				row, col = get_clicked_pos(loc, ROWS, span)
				tile = grid[row][col]

				#Colors the tiles to mark the beginning and the ending tiles
				if not begin and tile != end:
					begin = tile
					begin.mark_begin()
				elif not end and tile != begin:
					end = tile
					end.mark_end()

				#Colors the obstacles
				elif tile != end and tile != begin:
					tile.mark_obstacle()

			#Using right click to reset the definitions
			elif pygame.mouse.get_pressed()[2]: # Right mouse button
				loc = pygame.mouse.get_pos()
				row, col = get_clicked_pos(loc, ROWS, span)
				tile = grid[row][col]
				tile.reset()
				if tile == begin:
					begin = None
				elif tile == end:
					end = None

			if event.type == pygame.KEYDOWN:

				#Click enter to start the algorithm
				if event.key == pygame.K_RETURN and begin and end:
					for row in grid:
						for tile in row:
							tile.update_adj_tiles(grid)

					algorithm(lambda: draw(screen, grid, ROWS, span), grid, begin, end)

				#To reset screen
				if event.key == pygame.K_r:
					begin = None
					end = None
					grid = build_grid(ROWS, span)

	pygame.quit()

main(SCREEN, SPAN)
