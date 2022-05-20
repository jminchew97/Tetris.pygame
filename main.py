"""
 Pygame base template for opening a window

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""

import pygame



# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

# Set the width and height of the screen [width, height]
size = (400, 800)
screen = pygame.display.set_mode(size)
FPS = 60

BLOCK_SIZE = 40
pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# move blocks


# Used to manage how fast the screen updates
clock = pygame.time.Clock()

map =          [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]]
# player movement
current_block_list = []
currently_has_block = True
move_x_axis = 0
move_x_offset = 0
# visuals

moving_tick =  5
game_speed = 20
current_tick = 0

start = 0



def move(moving_block_list, map, move_x_axis):
	x = 0
	for block_coordinates in moving_block_list:
		if move_x_axis < 0: # player trying to move left
			if block_coordinates[0] > 0 and map[block_coordinates[1]][block_coordinates[0] - 1] != "P": # if block to left not out of screen or == to P
				print("can move left")

			else:
				print("CANT move left")
				return 0
		if move_x_axis > 0:  # player trying to move right
			if block_coordinates[0] < len(map[0]) - 1 and map[block_coordinates[1]][
				block_coordinates[0] - 1] != "P":  # if block to left not out of screen or == to P
				print("can move left")
			else:
				print("CANT move right")
				return 0
	for block_coordinates in moving_block_list:
		if move_x_axis < 0:  # player trying to move left
			map[block_coordinates[1]][block_coordinates[0] - 1] = "#" # move block to left
			map[block_coordinates[1]][block_coordinates[0]] = "0"
		elif move_x_axis > 0:  # player trying to move right
			map[block_coordinates[1]][block_coordinates[0] + 1] = "#"  # move block to left
			map[block_coordinates[1]][block_coordinates[0]] = "0"
		moving_block_list.remove(block_coordinates) # remove item from list

map[0][3] = "#"
y = 0
for row in map:
	x = 0
	for block in row:

		if block == "#":
			current_block_list.append([x,y])
		x +=1
	y+=1
def debug():

	with open('readme.txt', 'w') as f:
		for row in map:
			for block in row:
				f.write(" " + block + " ")
			f.write("\n")
		f.write("Move X Axis:" + str(move_x_axis))
# -------- Main Program Loop -----------
while not done:
	#---- Start runs the first frame
	#print(move_x_axis)
	# set initial blocks
	if currently_has_block == False:
		map[0][3] = "#"
		currently_has_block = True

	# --- Main event loop
	dt = clock.tick(FPS) / 1000

	move_x_axis = 0
	# INPUT---------------------------
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				move_x_axis = 1
				#print("right")
			elif event.key == pygame.K_LEFT:
				move_x_axis = -1
				#print("left")
			if event.key == pygame.K_SPACE:
				debug()
	# check if a move was attempted --------------------
	if move_x_axis != 0:
		# if move attempted, detect collisions to specified side
		move(current_block_list, map,move_x_axis)

	# --- Game logic should go here
	# move blocks DOWN
	if current_tick >= moving_tick:


		#print("tick reached")
		current_tick = 0
		y = len(map) - 1 # 18
		#print(y)
		while y >= 0:
			x = len(map[0]) - 1
			while x >= 0:
				block_above = map[y - 1][x]
				current_position = map[y][x]
				if map[y - 1][x] == "#": # Block above current position is a falling block
					#print('x:',x)
					#print('move_offset',move_offset)
					current_block_list = []
					current_block_list.append([x, y])
					print(current_block_list)
					if map[y][x] == "P":
						map[y - 1][x] = "P"
						currently_has_block = False
						#print("Block landed on P")
					elif y == len(map)-1: # check if row below is out of range, then place block
						map[y - 1][x] = "0"
						map[y][x] = "P"
						currently_has_block = False

					else : # move block above to current position

						map[y][x] = "#"  # set current position to block
						map[y - 1][x] = "0" # set block above to empty



				if block == "0":
					pass
				x -= 1
			y -= 1




	# --- Screen-clearing code goes here

	# Here, we clear the screen to white. Don't put other drawing commands
	# above this, or they will be erased with this command.

	# If you want a background image, replace this clear with blit'ing the
	# background image.
	screen.fill(BLACK)

	# --- Drawing code should go here

	#  ---Draw blocks onto screen
	y2 =0
	for row in map:
		x2 = 0
		for block in row:
			if block == "#":

				pygame.draw.rect(screen, GREEN, pygame.Rect(x2 * BLOCK_SIZE, y2 * BLOCK_SIZE , BLOCK_SIZE, BLOCK_SIZE))

			if block == "P":
				pygame.draw.rect(screen, GREEN, pygame.Rect(x2 * BLOCK_SIZE, y2 * BLOCK_SIZE , BLOCK_SIZE, BLOCK_SIZE))

				pass

			if block == "0":
				pass
			x2 += 1
			#print(" ")
		y2 += 1 #  #

	current_tick += dt * game_speed

	# --- Go ahead and update the screen with what we've drawn.
	pygame.display.flip()
	if start == 0:
		start += 1
	# --- Limit to 60 frames per second
	clock.tick(FPS)

# Close the win