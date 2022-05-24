import pygame
import random

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

normal_tick =  5
fast_tick = 2
tick = normal_tick

game_speed = 20
current_tick = 0

start = 0

collision = False
# pieces
pieces = ["OR", "HR", "BR", "TW", "CZ", "SB", "RZ"]
current_piece = ""
is_first_piece = True
rand = 0

pushing_down = False
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

			return
		if map[y][x + move_x_axis] == "P":

			return

	for i in range(len(moving_block_list)):
		moving_block_list[i] = [moving_block_list[i][0] + move_x_axis, moving_block_list[i][1]]


def generate_piece(piece_list, current_piece):

	current_p = ""
	rand = random.randint(0, 6)
	current_block_list = []


	while piece_list[rand] == current_piece:
		rand = random.randint(0, 6)

	if piece_list[rand] == "OR":
		current_block_list.append([4, 0])
		current_block_list.append([3, 0])

		current_block_list.append([5, 0])


		current_block_list.append([3, 1])
	elif piece_list[rand] == "BR":
		current_block_list.append([4, 0])
		current_block_list.append([5, 0])


		current_block_list.append([3, 0])
		current_block_list.append([5, 1])
	elif piece_list[rand] == "RZ":
		current_block_list.append([4, 1])
		current_block_list.append([4, 0])
		current_block_list.append([5, 0])
		current_block_list.append([3, 1])
	elif piece_list[rand] == "CZ":
		current_block_list.append([4, 1])
		current_block_list.append([4, 0])
		current_block_list.append([3, 0])

		current_block_list.append([5, 1])
	elif piece_list[rand] == "HR":
		current_block_list.append([4, 0])
		current_block_list.append([4, 1])
		current_block_list.append([4, 2])
		current_block_list.append([4, 3])
	elif piece_list[rand] == "SB":
		current_block_list.append([4, 0])
		current_block_list.append([5, 0])
		current_block_list.append([4, 1])
		current_block_list.append([5, 1])
	elif piece_list[rand] == "TW":
		current_block_list.append([4, 1])
		current_block_list.append([4, 0])

		current_block_list.append([3, 1])
		current_block_list.append([5, 1])
	return current_block_list, piece_list[rand]

def get_corners(center):
	topleft_corner = [center[0] - 1, center[1] - 1]
	topright_corner = [center[0] + 1, center[1] - 1]
	bottomright_corner = [center[0] + 1, center[1] + 1]
	bottomleft_corner = [center[0] - 1, center[1] + 1]

	return topleft_corner, topright_corner, bottomright_corner, bottomleft_corner

def rotate_piece(current_piece, current_block_list):
	normal_rotation = False
	hero_rotation = False
	smash_rotation = False
	if current_piece == "OR":
		normal_rotation = True
	elif current_piece == "BR":
		normal_rotation = True
	elif current_piece == "RZ":
		pass
	elif current_piece == "CZ":
		normal_rotation = True
	elif current_piece == "HR":
		return
	elif current_piece == "SB":
		return
	elif current_piece == "TW":
		normal_rotation = True

	# rotate normal pieces
	topleft_corner, topright_corner, bottomright_corner, bottomleft_corner = get_corners(current_block_list[0])

	x = 0
	while x != 2:

			# move all corners
			if current_block_list[i] == topleft_corner: # move right on x axis
				current_block_list[i] = [current_block_list[i][0] + 1, current_block_list[i][1] ]  #changed code here
			elif current_block_list[i] == topright_corner:
				current_block_list[i] = [current_block_list[i][0], current_block_list[i][1] + 1] # move down on y axis
			elif current_block_list[i] == bottomright_corner:
				current_block_list[i] = [current_block_list[i][0] - 1, current_block_list[i][1]] # move left axis
			elif current_block_list[i] == bottomleft_corner :
				current_block_list[i] = [current_block_list[i][0], current_block_list[i][1] - 1]# move up on y axis

			# move others
			elif current_block_list[i] == [current_block_list[0][0] - 1, current_block_list[0][1]] : # left of center, move it up
				current_block_list[i] = [current_block_list[i][0], current_block_list[i][1] - 1]
			elif current_block_list[i] == [current_block_list[0][0], current_block_list[0][1] -1] : # above center, move right
				current_block_list[i] = [current_block_list[i][0] + 1, current_block_list[i][1]]
			elif current_block_list[i] == [current_block_list[0][0] + 1, current_block_list[0][1]] : # right of center, move down
				current_block_list[i] = [current_block_list[i][0], current_block_list[i][1] + 1]
			elif current_block_list[i] == [current_block_list[0][0] , current_block_list[0][1] + 1] : # below center, move left
				current_block_list[i] = [current_block_list[i][0] - 1, current_block_list[i][1]]
		#current_block_list = new_block_list
		x += 1

	#current_block_list = new_block_list
	print("rotation complete, current block list length:", len(current_block_list))
def update_map(map, current_block_list):
	# clear map
	for y in range(len(map)):
		for x in range(len(map[y])):
			if map[y][x] == "#":
				map[y][x] = "0"


	# set map
	if currently_has_block:
		print("current block list length", len(current_block_list))
		for i in range(len(current_block_list)):
			#current_block_list[i] = [current_block_list[i][0], current_block_list[i][1]]

			map[current_block_list[i][1]] [current_block_list[i][0]] = "#"





def debug():

	with open('readme.txt', 'w') as f:
		for row in map:
			for block in row:
				f.write(" " + block + " ")
			f.write("\n")
		f.write("Move X Axis:" + str(move_x_axis))

hit_rotate_key = False
# -------- Main Program Loop -----------
map = create_map_grid(map_x_length, map_y_length)
while not done:
	#---- Start runs the first frame
	#print(move_x_axis)
	# set initial blocks
	if currently_has_block == False: # generate new block

		current_block_list, current_piece = generate_piece(pieces, current_piece)

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
			if event.key == pygame.K_DOWN:
				pushing_down = True
				tick = fast_tick
			if event.key == pygame.K_UP:
				rotate_piece(current_piece, current_block_list)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				tick = normal_tick
				pushing_down = False


	# check if a move was attempted --------------------
	if move_x_axis != 0:
		# if move attempted, detect collisions to specified side
		move(current_block_list, map,move_x_axis)

	# --- Game logic should go here

	# move blocks DOWN
	if current_tick >= tick:


		#print("tick reached")
		current_tick = 0

		# COLLISION DETECTION----------------------------------

		for block_coord in current_block_list: # check all collisions (placed block/hit bottom of screen)


			if block_coord[1] == len(map) - 1: # is working
				collision = True

				break
			elif map[block_coord[1] + 1][block_coord[0]] == "P": # check if any blocks in the tetris block is going to touch a placed block
				collision = True

				break


		# CHANGE BLOCK COORDS BASED ON COLLISION--------------------
		if collision:
			# CONVERT PLAYERS CURRENT BLOCK TO "PLACED"
			for i in range(len(current_block_list)):


				map[current_block_list[i][1]][current_block_list[i][0]] = "P"

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