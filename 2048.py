import pygame
from pygame.locals import *
from sys import exit
from random import *
pygame.init()
pygame.font.init()

n = 4
screen = pygame.display.set_mode((400,400),0,32)
pygame.display.set_caption('THE 2048!')
screen.fill((255,255,255))

num = [[0 for i in range(4)]for j in range(n)]
tiles = [[0 for i in range(n)]for j in range(n)]
cnt = 0
colour = {}
colour[0] = (204,192,179)
colour[2] = (238,228,218)
colour[4] = (237,224,200)
colour[8] = (242,177,121)
colour[16] = (245,149,99)
colour[32] = (246,124,95)
colour[64] = (246,94,59)
colour[128] = (237,207,114)
colour[256] = (237,204,97)
colour[512] = (237,200,80)
colour[1024] = (237,197,63)
colour[2048] = (237,194,46)
# colour[0] = (204,192,179)
# colour[2] = (230,67,254)
# colour[4] = (242,30,99)
# colour[8] = (156,239,76)
# colour[16] = (103,58,183)
# colour[32] = (33,150,243)
# colour[64] = (0,150,136)
# colour[128] = (139,195,74)
# colour[256] = (60,175,80)
# colour[512] = (255,152,0)
# colour[1024] = (255,87,34)
# colour[2048] = (121,85,72)

class tile():
	def __init__(self,val,size,x,y):
		self.x = x
		self.y = y
		self.val = val
		self.size = size
		self.col = colour[self.val]
		self.dim = (self.size,self.size)
		self.image = pygame.Surface(self.dim)

	def update(self):
		self.image.fill(self.col)
		self.font = pygame.font.SysFont("Times New Roman",30)
		if self.val:
			self.text = self.font.render(str(self.val),True,(0,0,0))
		else:
			self.text = self.font.render(str(self.val),True,(204,192,179))
		self.image.blit(self.text,(self.size//2 - self.text.get_width()//2,self.size//2 - self.text.get_height()//2))
		screen.blit(self.image,(72+self.size*self.x,72+self.size*self.y))

for i in range(n):
	for j in range(n):
		tiles[i][j] = tile(0,64,j,i)

class player():
	def possible(self):
		for i in range(1,n):
			for j in range(n):
				if num[i][j] and not num[i-1][j]:
					return True
		return False

	def get_random_tile(self):
		global cnt
		rx = randint(0,n-1)
		ry = randint(0,n-1)
		bias = randint(1,10)
		while num[ry][rx]:
			rx = randint(0,n-1)
			ry = randint(0,n-1)
		if bias <= 9:
			num[ry][rx] = 2
			tiles[ry][rx] = tile(2,64,rx,ry)
			cnt += 1
		else:
			num[ry][rx] = 4
			tiles[ry][rx] = tile(4,64,rx,ry)
			cnt += 1

	def moveUp(self):
		if not self.possible():
			return False
		i = n-1
		for j in range(n):
			if num[i-1][j] == 0:
				for k in range(-1,0):
					num[i+k][j] = num[i+k+1][j]
					tiles[i+k][j] = tile(tiles[i+k+1][j].val,tiles[i+k+1][j].size,j,i+k)
				num[i][j] = 0
				tiles[i][j] = tile(0,64,j,i)
			if num[i-2][j] == 0:
				for k in range(-2,0):
					num[i+k][j] = num[i+k+1][j]
					tiles[i+k][j] = tile(tiles[i+k+1][j].val,tiles[i+k+1][j].size,j,i+k)
				num[i][j] = 0
				tiles[i][j] = tile(0,64,j,i)
			if num[i-3][j] == 0:
				for k in range(-3,0):
					num[i+k][j] = num[i+k+1][j]
					tiles[i+k][j] = tile(tiles[i+k+1][j].val,tiles[i+k+1][j].size,j,i+k)
				num[i][j] = 0
				tiles[i][j] = tile(0,64,j,i)
		return True

	def rotateRight(self):
		global num, tiles
		num_tuples = (zip(*num[::-1]))
		num = [list(ele) for ele in num_tuples]
		for i in range(n):
			for j in range(n):
				tiles[i][j] = tile(num[i][j],64,j,i)

	def rotateLeft(self):
		for i in range(3):
			self.rotateRight()

	def flip(self):
		for i in range(2):
			self.rotateRight()

	def merge(self):
		i = n-1
		status = False
		for j in range(n):
			if num[i][j] and num[i-3][j] == num[i-2][j] and num[i-2][j] == num[i-1][j] and num[i-1][j] == num[i][j]:
				num[i-3][j] *= 2
				num[i-2][j] *= 2
				num[i-1][j] = 0
				num[i][j] = 0
				status = True
				continue

			if num[i-3][j] == num[i-2][j] and num[i-2][j] != num[i-1][j] and num[i-1][j] == num[i][j]:
				num[i-3][j] *= 2
				num[i-2][j] = num[i-1][j]*2
				num[i-1][j] = 0
				num[i][j] = 0
				status = True
				continue

			if num[i-3][j] and num[i-3][j] == num[i-2][j]:
				num[i-3][j] *= 2
				num[i-2][j] = num[i-1][j]
				num[i-1][j] = num[i][j]
				num[i][j] = 0
				status = True

			elif num[i-2][j] and num[i-2][j] == num[i-1][j]:
				num[i-2][j] *= 2
				num[i-1][j] = num[i][j]
				num[i][j] = 0
				status = True

			elif num[i-1][j] and num[i-1][j] == num[i][j]:
				num[i-1][j] *= 2
				num[i][j] = 0
				status = True

		for i in range(n):
			for j in range(n):
				tiles[i][j] = tile(num[i][j],64,j,i)
		
		return status

	def gameover(self):
		for i in range(n):
			for j in range(n-1):
				if i != n-1:
					if num[i][j] == 0:
						return False
					else:
						if (num[i][j] == num[i][j+1]) or (num[i][j] == num[i+1][j]):
							return False
				else:
					if num[i][j] == 0:
						return False
					else:
						if num[i][j] == num[i][j+1]:
							return False

		for i in range(n):
			if not num[i][n-1]:
				return False

		for i in range(n-1):
			if num[i][n-1] == num[i+1][n-1]:
				return False

		return True

	def victory(self):
		for i in range(n):
			for j in range(n):
				if num[i][j] == 2048:
					return True
		return False

p = player()

for i in range(2):
	p.get_random_tile()

while True:
	dir = "NONE"

	if p.victory():
		flag = 1
		break

	if p.gameover():
		flag = 0
		break

	screen.fill((255,255,255))
	pygame.draw.rect(screen,(0,0,0),(70,70,259,259),2)

	for event in pygame.event.get():
		if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			exit()

		if event.type == KEYDOWN:
			if event.key == K_UP:
				dir = "UP"
				pygame.mixer.music.load('clearly.mp3')
				pygame.mixer.music.play()
			if event.key == K_DOWN:
				dir = "DOWN"
				pygame.mixer.music.load('clearly.mp3')
				pygame.mixer.music.play()
			if event.key == K_LEFT:
				dir = "LEFT"
				pygame.mixer.music.load('clearly.mp3')
				pygame.mixer.music.play()
			if event.key == K_RIGHT:
				dir = "RIGHT"
				pygame.mixer.music.load('clearly.mp3')
				pygame.mixer.music.play()
		else:
			dir = "NONE"

	if dir == "UP":
		status1 = p.moveUp()
		status2 = p.merge()
		if status1 or status2:
			p.get_random_tile()

	if dir == "DOWN":
		p.flip()
		status1 = p.moveUp()
		status2 = p.merge()
		p.flip()
		if status1 or status2:
			p.get_random_tile()

	if dir == "LEFT":
		p.rotateRight()
		status1 = p.moveUp()
		status2 = p.merge()
		p.rotateLeft()
		if status1 or status2:
			p.get_random_tile()

	if dir == "RIGHT":
		p.rotateLeft()
		status1 = p.moveUp()
		status2 = p.merge()
		p.rotateRight()
		if status1 or status2:
			p.get_random_tile()

	for i in range(n):
		for j in range(n):
				tiles[i][j].update()

	for i in range(1,n):
		pygame.draw.line(screen,(0,0,0),(72+64*i,72),(72+64*i,72+257))
	for i in range(1,n):
		pygame.draw.line(screen,(0,0,0),(72,72+64*i),(72+257,72+64*i))

	pygame.display.update()

font = pygame.font.SysFont("Times New Roman",50)
if flag:
	end_text = font.render("You Won!",True,(255,0,0))
else:
	end_text = font.render("Game Over!",True,(255,0,0))

while True:
	for event in pygame.event.get():
		if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			exit()

	screen.blit(end_text,(200 - end_text.get_width()//2,340))
	pygame.display.update()
