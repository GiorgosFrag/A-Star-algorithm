import pygame
import math
from queue import PriorityQueue

Width = int(input("Give the dimension of the square panel:")) #Eisagwgh diastashs tetragwnou
Window = pygame.display.set_mode((Width,Width)) #Dimiourgia panel
pygame.display.set_caption("A* Algorithm") #Epikefalida efarmoghs

#Dimiourgia xrwmatwn
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 255, 0)
Yellow = (255, 255, 0)
White = (255, 255, 255)
Black = (0, 0, 0)
Purple = (128, 0, 128)
Orange = (255, 165 ,0)
Grey = (128, 128, 128)
Turquoise = (64, 224, 208)

#Dimiourgia ths klashs Node pou antiprosopeuei to kathe tetragwno mesa sto panel
class Node:
	def __init__(self, row, column, width, total_rows):
		self.row = row
		self.column = column
		self.x = row * width
		self.y = column * width
		self.color = White
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_position(self): #epistrefei thn thesh tou tetragwnou
		return self.row, self.column

	def is_it_closed(self): #elegxei an to geitonika tetragwna ta exoume hdh episkeuthei 
		return self.color == Red

	def is_it_open(self): #elegxei an ta geitonika tetragwna einai anoixta pros episkepsh 
		return self.color == Green

	def is_it_wall(self): #elegxei an ta geitonika tetragwna einai ampodio
		return self.color == Black

	def start(self): #elegxei an einai to tetragwno pou orisame gia arxei
		return self.color == Orange

	def end(self): #elegxei an to tetragwno einai to auto pou orisame gia teliko
		return self.color == Turquoise

	def reset(self): #ksanakanei aspro ena tetragwno pou exoume allaksei xrwma
		self.color = White

	def color_closed(self): #allazei se kokkino to xrwma tou tetragwnou an to exoume episkeuthei
		self.color = Red

	def color_open(self): #allazei se prasino to xrwma tou tetragwnou an einai geitoniko tetragwnou pou exoume hdh episkeuthei alla to idio den eto exoume episkeuthei
		self.color = Green

	def color_wall(self): #allazei to xrwma tou tetragwnou se mauro an to epileksoume gia empodio
		self.color = Black

	def color_start(self): #kanei portokali to arxiko tetragwno
		self.color = Orange

	def color_end(self): #kanei galazio to teliko tetragwno
		self.color = Turquoise

	def color_path(self): #kanei to teiko beltisto monopati mob
		self.color = Purple

	def draw(self, window): #dimiourgei to kathe tetragwno mesa sto panel mas 
		pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

	#elegxei panw, katw, deksia kai aristera an ta geitonika tetragwna einai empodia
	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_it_wall():#elegxw gia katw 
			self.neighbors.append(grid[self.row + 1][self.column])

		if self.row > 0 and not grid[self.row - 1][self.column].is_it_wall():#elegxw gia panw 
			self.neighbors.append(grid[self.row - 1][self.column])

		if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_it_wall():#elegxw gia deksia 
			self.neighbors.append(grid[self.row][self.column + 1])

		if self.column > 0 and not grid[self.row][self.column - 1].is_it_wall():#elegxw gia aristera 
			self.neighbors.append(grid[self.row][self.column - 1])

	def __lt__(self, other):
		return False

# Xrisimopoioume thn apostash Manhattan h opoia gia ena shmeio p1 (x1, y1) kai ena shmeio p2 (x2, y2), einai |x1 - x2| + |y1 - y2|
def h(p1,p2):
	x1 , y1 = p1
	x2 , y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def create_path(came_from, current_node, draw):
	while current_node in came_from:
		current_node = came_from[current_node]
		current_node.color_path()
		draw()


#Algorithmos A*
def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = h(start.get_position(), end.get_position())
	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current_node = open_set.get()[2]
		open_set_hash.remove(current_node)

		if current_node == end: #dimiourgia kai xrwmatismou tou monopatiou
			create_path(came_from, end, draw)
			return True

		for neighbor in current_node.neighbors:
			count_g_score = g_score[current_node] + 1
			if count_g_score < g_score[neighbor]:
				came_from[neighbor] = current_node
				g_score[neighbor] = count_g_score
				f_score[neighbor] = count_g_score + h(neighbor.get_position(), end.get_position())
				if neighbor not in open_set_hash:
					count = count + 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.color_open()

		draw()

		if current_node != start:
			current_node.color_closed()

	return False



#kataskeuazoume to Grid gia na mporoume na diazeiristoume ola auta ta tetragwna pou dimiourgisame
def create_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range (rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)
	return grid

#zwgrafizoume to grid "zwgrafizoume tis grizes grammes anamesa sta tetragwna gia na ta diaxwrisoume"
def draw_grid(window, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(window, Grey, (0, i*gap), (width, i*gap))
		for j in range(rows):
			pygame.draw.line(window, Grey, (j*gap, 0), (j*gap, width))

#h main sunartish pou zwgrafizei ta panta
def draw(window, grid, rows, width):
	window.fill(White)
	for row in grid:
		for node in row:
			node.draw(window)

	draw_grid(window, rows, width)
	pygame.display.update()

#pairnei tis suntetagmenes tou tetragwnou pou pathsame
def get_clicked_position(mouse_pos, rows, width):
	gap = width // rows
	y, x = mouse_pos
	row = y // gap
	column = x // gap
	return row, column

#h basikh epanalhpsh pou diatraxei kathe event pou symbenei sto pygame kai orismos tou ti tha kanei to kathe click sto pontiki kai ti tha kanei to Space
def main(window, width):
	Rows = 50
	grid = create_grid(Rows,width)
	start = None
	end = None
	run = True 
	started = False

	while run:
		draw(window, grid, Rows, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #an patisoume to x panw deksia tha klisei h efarmogh
				run = False

			if started:
				continue

			#pairnei thn thesh tou tetragwnou pou klikarame me to aristero click
			if pygame.mouse.get_pressed()[0]: #0 = aristero click
				mouse_pos = pygame.mouse.get_pos()
				row, column = get_clicked_position(mouse_pos, Rows, width)
				node = grid[row][column]

				#an einai to prwto tetragwno pou klikaroume tote to kanei portokali
				if not start and node != end:#elegxos oti h arxh kai to telos den einai ta idia
					start = node
					start.color_start()

				#an einai to deutero tetragwno tou klikaroume tote to kanei galazio
				elif not end and node != start:#elegxos oti to telos kai h arxh den einai ta idia
					end = node
					end.color_end()

				#an den einai kapoio apo ta parapanw tote kanei ta tetragwna maura 
				elif node != start and node !=end:
					node.color_wall()

			#pairnei thn thesh tou tetragwnou pou klikaroume me to deksi click kai epanaferei sto aspro xrwma to tetragwno 
			elif pygame.mouse.get_pressed()[2]: #2 = deksi click
				mouse_pos = pygame.mouse.get_pos()
				row, column = get_clicked_position(mouse_pos, Rows, width)
				node = grid[row][column]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)

					algorithm(lambda: draw(window, grid, Rows, width), grid, start, end)



	pygame.quit()

main(Window, Width)






