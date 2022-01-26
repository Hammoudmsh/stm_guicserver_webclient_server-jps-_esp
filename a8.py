#last ok
import pygame
import math
from tkinter import *
from queue import PriorityQueue
import csv
from tkinter import messagebox
import time
pygame.font.init()

WIDTH,HEIGHT = 500,500
ROWS,COLS = 25,25
 
WIDTH=WIDTH-WIDTH%COLS

HEIGHT=HEIGHT-HEIGHT%ROWS
gapx=gapy=WIDTH//ROWS
WIDTH=COLS*gapy
HEIGHT=ROWS*gapx



WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finding Algorithm(Build map)")

font = pygame.font.SysFont('chalkduster', 15)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


Niegbours=[[1,1,0,-1,-1,-1,0,1],[0,-1,-1,-1,0,1,1,1]]
m8=[0,1,2,3,4,5,6,7]
m4=[0,3,5,7]
Direction_names=['Right','up_right','Up','up_left','Left','Down_left','Down','Down_right']
                


def isvalid(rr,cc):
	return rr>=0 and rr <ROWS and cc >=0 and cc<COLS
    
class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows
		vals=[0,0,0,0,0,0,0,0]
#self.right,self.d1,self.up,self.d2,self.left,self.d3,self.down,self.d4
	def get_val(self,x=8):
		if x==8:
			return   vals
		else:
			return vals[x]
    
	def set_val(self,val,x=8):
		if x==8:
			vals=val
		else:
			vals[x]=val
    
        
    
    
	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


	def update_neighbors(self, grid,m):
		self.neighbors = []
		for k in m:            
			rr=self.row+Niegbours[0][k]
			cc=self.col+Niegbours[1][k]
			print(rr,"*",cc)
			if isvalid(rr,cc) and not grid[cc][rr].is_barrier():
				self.neighbors.append(grid[cc][rr])
                
	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)



def reconstruct_path(start,end,came_from, current, draw):#start normal
	global clear
	robot_path=[]
	while current in came_from:
		current = came_from[current]
		if current!= start and current!= end:
			current.make_path()
		xx,yy=current.get_pos()
		robot_path.append([xx,yy])
		draw()
	robot_path=robot_path[::-1]
	#print(robot_path)
	dirs=[]
	for idx in range(len(robot_path)-1):
		x0,y0=robot_path[idx]
		x1,y1=robot_path[idx+1]
		dx=x1-x0
		dy=y1-y0
		if dx==0:   
			if dy==-1:
				dirs.append(2)
			elif dy==1:
				dirs.append(5)
		elif dx==1:
			if dy==0:
				dirs.append(0)
			elif dy==-1:
				dirs.append(1)
			elif dy==1:
				dirs.append(7)
		elif dx==-1:
			if dy==0:
				dirs.append(4)
			elif dy==-1:
				dirs.append(3)
			elif dy==1:
				dirs.append(6)
	return dirs,robot_path


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			xxx,yyy=reconstruct_path(start,end,came_from, end, draw)
			print('Dirs are:',xxx)
			for i in xxx:
				print(Direction_names[i])
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()
#	messagebox.showinfo("No Solution", "There was no solution" )
	return False
def get_grid(grid):
	map2save=[]
	startn=[]
	endn=[]
	tmp=[]
	listmap=[]
	map2save.append(startn)
	map2save.append(endn)
	for i in range(ROWS):
		for j in range(ROWS):
			spot=grid[i][j]
			if spot.is_barrier():
				map2save.append([i,j])
				tmp.append(1)
                
			elif spot.is_start():
				map2save[0]=[i,j]
				tmp.append(0)
			elif spot.is_end():
				map2save[1]=[i,j]
				tmp.append(0)
			else:
				tmp.append(0)
		#print(tmp)        
		listmap.append(tmp)
		tmp=[]
	print(listmap)
	return map2save

def save_grid(grid):
	grid2save=get_grid(grid)
	d=grid2save[2:len(grid2save)]
	f = open('E:\Mohammed\Micro Controller\STM\Thesis\Master_Project\Project_code\w\stm_guicserver_webclient_server(jps)_esp/numbers2.csv', 'w')
	with f:
		writer = csv.writer(f)
		for row in d:
			writer.writerow(row)
def save_gridtotxt(grid):
	f = open('E:\Mohammed\Micro Controller\STM\Thesis\Master_Project\Project_code\w\stm_guicserver_webclient_server(jps)_esp/map'+str(ROWS)+'.txt','w')
	with f:
		for i in range(ROWS):
			for j in range(COLS):
				if grid[i][j].is_barrier():
					f.write('0')
				else:
					f.write('1')
			f.write("\n")

def make_grid(rows, width):
	grid = []
	#gap = width // rows
	for i in range(COLS):
		grid.append([])
		for j in range(ROWS):
			spot = Spot(i, j, gapx, rows)
			grid[i].append(spot)
	return grid

def draw_grid(win, rows, width):
	#gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gapx), (WIDTH, i * gapx))
		for j in range(COLS):
			pygame.draw.line(win, GREY, (j * gapy, 0), (j * gapy, HEIGHT))#width

def draw(win, grid, rows, width):
	win.fill(WHITE)
#	img = font.render('hello', True, RED)
#	win.blit(img, (width-50, width-50))

	for row in grid:
		for spot in row:

			spot.draw(win)
	draw_grid(win, rows, width)


	pygame.display.update()

def draw_text(win,msg):
	X,Y=WIDTH,HEIGHT
	font=pygame.font.Font('freesansbold.ttf',35)
	text=font.render(msg,True,GREEN,WHITE)
	textRect=text.get_rect()
	textRect.center=(X//2,Y//2)
	win.blit(text,textRect)
	pygame.display.update()
	time.sleep(1)
def get_clicked_pos(pos, rows, width):
	#gap = width // rows
	y, x = pos

	row = y // gapx
	col = x // gapy


	return row, col

def main(win, width,ROWS,COLS):
	global clear
	grid = make_grid(ROWS, width)

	start = None
	end = None
	run = True
	t=False
	map2save=[]
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				print(row,"*",col)
				spot = grid[row][col]      
				if not start and spot != end:
					start = spot
					start.make_start()
				elif not end and spot != start:
					end = spot
					end.make_end()
				elif spot != end and spot != start :
					spot.make_barrier()
			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None
			elif event.type ==pygame.KEYDOWN:
				#if event.key == pygame.K_4 and start and end:
				#	for row in grid:
				#		for spot in row:
				#			spot.update_neighbors(grid,m4)
				#	map2save=get_grid(grid)
				#	algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
				if event.key == pygame.K_8 and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid,m8)
					map2save=get_grid(grid)
					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
				elif event.key == pygame.K_s:
					save_grid(grid)
					save_gridtotxt(grid)
					draw_text(win,"Map saved")
					
					#messagebox.showinfo('Saved','Ok')
					#print(grid)
				elif event.key == pygame.K_v and t==False:
					t=True                    
					start=None
					end=None
					grid = make_grid(ROWS, width)
				elif event.key == pygame.K_c:
					grid = make_grid(ROWS, width)
					print(map2save)
					ii,jj=map2save[0]
					spot=grid[ii][jj]
					spot.make_start()
					ii,jj=map2save[1]
					spot=grid[ii][jj]
					spot.make_end()
					for n in range(2,len(map2save)):
						ii,jj=map2save[n]
						spot=grid[ii][jj]
						spot.make_barrier()
				elif event.key == pygame.K_b:
					print(ROWS,COLS)
					for i in range(COLS):
						for j in range(ROWS):
							print(i,j)
							if i==0 or j==0 or  i==COLS-1 or j==ROWS-1:
								spot=grid[i][j]
								spot.make_barrier()
				elif event.key == pygame.K_h:
					draw_text(win,"s: Save map, b: Set borders, 8:A8 , 4:A4 , D:Dijkistra, J:JPS")
									
	pygame.quit()
main(WIN, WIDTH,ROWS,COLS)

