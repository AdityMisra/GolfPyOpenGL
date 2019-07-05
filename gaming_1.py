import pygame
import pygame.freetype
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random	
import time
display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
ground_vertices = (
	(-110,-1,220),
	(110,-1,220),
	(110,-1,-220),
	(-110,-1,-220),
	)

ground_vertices2 = (
	(170,-1,-220),
	(111,-1,-220),
	(111,-1,+220),
	(170,-1,+220),
	)
ground_vertices3 = (
	(110,-1,-220),
	(111,-1,-220),
	(111,-1,+20),
	(110,-1,+20),
	)

ground_vertices4 = (
	(110,-1,22),
	(111,-1,22),
	(111,-1,220),
	(110,-1,220),
	)

xf,yf,zf = random.randint(-110,110),-1,random.randint(-220,220)
radius = 1
epsilon = 1e-2
dist_to_ball = 10
MV_FACT = -0.555

def Ground():  
	glBegin(GL_QUADS)

	x = 0
	for vertex in ground_vertices:
		x+=1
		glColor3fv((0,1,0))
		glVertex3fv(vertex)
	glEnd()

def Ground2():
	glBegin(GL_QUADS)
	x=0
	for vertex in ground_vertices2:
		x+=1
		glColor3fv((1,0,0))
		glVertex3fv(vertex)
	glEnd()

def Ground3():
	glBegin(GL_QUADS)
	x=0
	for vertex in ground_vertices3:
		x+=1
		glColor3fv((1,1,0))
		glVertex3fv(vertex)
	glEnd()

def Ground4():
	glBegin(GL_QUADS)
	x=0
	for vertex in ground_vertices4:
		x+=1
		glColor3fv((1,0,1))
		glVertex3fv(vertex)
	glEnd()

def ball(camera_x,camera_y,camera_z):
	glPushMatrix();
	glColor3f(0.5,0.4,0.6);
	# print(camera_x,camera_z)
	glTranslatef(camera_x,camera_y,camera_z-dist_to_ball)
	gluSphere(gluNewQuadric(),radius,100,100);
	glPopMatrix();

def flag():
	x,y,z = xf,yf,zf
	top = y + 8
	
	glColor3fv((0.71,0.396,0.114))
	glLineWidth((3))
	glBegin(GL_LINES)
	glVertex3fv((x,y,z))
	glVertex3fv((x,top,z))
	glEnd()

	glColor3fv((1,0,0))
	glBegin(GL_TRIANGLES)
	glVertex3fv((x,top,z))
	glVertex3fv((x,top-2,z))
	glVertex3fv((x+2,top-1,z))
	glEnd()

	'''print('Flag',x,y,z)'''
def isCollision(x,y,z):
	'''Will send in location of center of ball'''
	llz = zf - 5
	ulz = zf + 5
	if (z < ulz and z > llz) and (x*-0.555*-0.555 > (int(MV_FACT*(xf)))-10 and x*-0.555*-0.555 < (int(MV_FACT*(xf)))+10):
		return True
	else:
		return False


def main():
	start = time.time()
	seconds = 3460	
	pygame.init()
	display = (800,600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

	gluPerspective(45, (display[0]/display[1]), 0.1, 200.0)
	x_move = 0
	z_move = 0

	score = 0
	max_distance = 3

	object_passed = True

	i = 0

	VELO = 0.5

	# x,y,z = 0,-1,50
	# x,y,z = random.randint(-110,110),-1,random.randint(-220,220)

	while score < 5:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_LEFT:
					x_move = VELO
					
				if event.key == pygame.K_RIGHT:
					x_move = -VELO

				if event.key == pygame.K_UP:
					z_move = VELO

				if event.key == pygame.K_DOWN:
					z_move = -VELO

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					x_move = 0
					
				if event.key == pygame.K_RIGHT:
					x_move = 0

				if event.key == pygame.K_UP:
					z_move = 0

				if event.key == pygame.K_DOWN:
					z_move = 0

		
		x = glGetDoublev(GL_MODELVIEW_MATRIX)

		glTranslatef(x_move,0,z_move)

		camera_x = x[3][0]
		camera_y = x[3][1]
		camera_z = x[3][2]
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		Ground()  
		Ground2()
		Ground3()
		Ground4()

		object_passed = isCollision(camera_x,camera_y,camera_z-dist_to_ball)
		seconds=seconds-1
		if object_passed:
			global xf,yf,zf
			xf,yf,zf = random.randint(-110,110),-1,random.randint(-220,220)
			score += 1		#increment score
			seconds+=865.051903114
			print(score)
			object_passed = False
		if seconds<0 and score<5:
			print("Score"+str(score))
			print("Game Over!")
			break
		if score == 5:
			print("You Win!")
			break
		# '''print('Your location:',camera_x,camera_y,camera_z-dist_to_ball,'\t',end='')'''

		flag()
		
		ball(MV_FACT*camera_x,camera_y,camera_z)
			          
		pygame.display.flip()

random.seed()		
start = time.time()
main()