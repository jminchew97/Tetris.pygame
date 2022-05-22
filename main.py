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

# Map info
map_x_length = 10
map_y_length = 20

# player movement
current_block_list = []
currently_has_block = False
move_x_axis = 0
move_x_offset = 0
# visuals

moving_tick =  5
game_speed = 20
current_tick = 0

start = 0

collision = False

def create_map_grid(map_x, map_y):
	map = []
	for y in range(map_y_length):

		map.append([])
		for x in range(map_x_length):
			map[y].append("0")
	return map
def move(moving_block_list, map, move_x_axis):
	for i in range(len(moving_block_list)):
		x = current_block_list[i][0]
		y = current_block_list[i][1]
		if (move_x_axis <0 and x==0) or (move_x_axis >0 and x == 9): # the space the player is trying to move to is within range
			print(current_block_list)
			return
		if map[y][x + move_x_axis] == "P":
			print(x)
			return

	for i in range(len(moving_block_list)):
		moving_block_list[i] = [moving_block_list[i][0] + move_x_axis, moving_block_list[i][1]]
	print(current_block_list)
def update_map(map, current_block_list):
	# clear map
	for y in range(len(map)):
		for x in range(len(map[y])):
			if map[y][x] == "#":
				map[y][x] = "0"


	# set map
	if currently_has_block:

		for i in range(len(current_block_list)):
			current_block_list[i] = [current_block_list[i][0], current_block_list[i][1]]
			map[current_block_list[i][1]][current_block_list[i][0]] = "#"


def debug():

	with open('readme.txt', 'w') as f:
		for row in map:
			for block in row:
				f.write(" " + block + " ")
			f.write("\n")
		f.write("Move X Axis:" + str(move_x_axis))
# -------- Main Program Loop -----------
map = create_map_grid(map_x_length, map_y_length)
while not done:
	#---- Start runs the first frame
	#print(move_x_axis)
	# set initial blocks
	if currently_has_block == False: # generate new block
		current_block_list = []
		current_block_list.append([0, 2])
		current_block_list.append([0,0])
		current_block_list.append([0, 1])

		currently_has_block = True

	# --- Main event loop
	dt = clock.tick(FPS) / 1000

	# Reset input
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

		# COLLISION DETECTION----------------------------------

		for block_coord in current_block_list: # check all collisions (placed block/hit bottom of screen)


			if block_coord[1] == len(map) - 1: # is working
				collision = True
				print("bottom of screen collision", collision)
				print("Hit bottom of screen")
				break
			elif map[block_coord[1] + 1][block_coord[0]] == "P": # check if any blocks in the tetris block is going to touch a placed block
				collision = True
				print("Hit another block")
				break


		# CHANGE BLOCK COORDS BASED ON COLLISION--------------------
		if collision:
			# CONVERT PLAYERS CURRENT BLOCK TO "PLACED"
			for i in range(len(current_block_list)):


				map[current_block_list[i][1]][current_block_list[i][0]] = "P"
				print(map[current_block_list[i][1]][current_block_list[i][0]])
			collision = False
			currently_has_block = False
			current_block_list = []
		# MOVE PLAYER BLOCKS DOWN SINCE NO COLLISION IS DETECTED
		else:
			# add gravity by adding +1 to every Y coordinate in current_block_list
			for i in range(len(current_block_list)):
				current_block_list[i] = [current_block_list[i][0], current_block_list[i][1] + 1]
				map[current_block_list[i][1]][current_block_list[i][0]] = "#"
	# update map list
	update_map(map, current_block_list)




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

	# --- Limit to 60 frames per second
	clock.tick(FPS)

# Close the win