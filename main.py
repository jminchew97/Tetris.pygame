import pygame
import random
import pickle
from operator import itemgetter

# Define some colors
BLACK = (0, 0, 0)
OR_color = (255,166,0)
HR_color = (68,255,255)
BR_color = (0,0,255)
TW_color = (171,0,255)
SB_color = (255,255,0)
RZ_color = (0, 255, 0)
CZ_color = (255, 0, 0)

pygame.init()
pygame.display.set_caption('Juli-ETRIS')
# Set the width and height of the screen [width, height]
# 400/800
size = (800, 800)
offset = 200
screen = pygame.display.set_mode(size)
FPS = 60

BLOCK_SIZE = 40


# Loop until the user clicks the close button.
done = False

# move blocks


# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Map info
map_x_length = 10
map_y_length = 20

# player movement
block1 = []


update_placed_blocks = False
current_block_list = []
next_block_list = []
next_piece_name = ""

currently_has_block = False
move_x_axis = 0
move_x_offset = 0
# visuals

normal_tick = 5
fast_tick = .5
tick = normal_tick

game_speed = 15
current_tick = 0

start = 0

collision = False
# pieces
pieces = ["OR", "HR", "BR", "TW", "CZ", "SB", "RZ"]
current_piece = ""
is_first_piece = True

rand = 0


hero_iteration = 0
pushing_down = False

holding_move = False
move_timer_max = 1
move_current_time = 0
move_speed = 45

score = 0
add_score = 0

end_game = False

total_lines = 0
current_line_counter = 0
score_list = []
HIGHSCORE = 0
level = 1

fast_move_initiated = False
holding_move_button_time = 0
move_button_timer_max = .1
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
	global end_game
	current_p = ""
	rand = random.randint(0, 6)
	#rand = 1
	current_block_list = []


	while piece_list[rand] == current_piece:
		rand = random.randint(0, 6)

	if piece_list[rand] == "OR":
		current_block_list.append([4, 0, "OR"])
		current_block_list.append([3, 0, "OR"])
		current_block_list.append([5, 0, "OR"])
		current_block_list.append([3, 1, "OR"])
	elif piece_list[rand] == "BR":
		current_block_list.append([4, 0, "BR"])
		current_block_list.append([5, 0, "BR"])
		current_block_list.append([3, 0, "BR"])
		current_block_list.append([5, 1, "BR"])
	elif piece_list[rand] == "RZ":
		current_block_list.append([4, 1, "RZ"])
		current_block_list.append([4, 0, "RZ"])
		current_block_list.append([5, 0, "RZ"])
		current_block_list.append([3, 1, "RZ"])
	elif piece_list[rand] == "CZ":
		current_block_list.append([4, 1, "CZ"])
		current_block_list.append([4, 0, "CZ"])
		current_block_list.append([3, 0, "CZ"])
		current_block_list.append([5, 1, "CZ"])
	elif piece_list[rand] == "HR":
		current_block_list.append([4, 1, "HR"])
		current_block_list.append([4, 0, "HR"])
		current_block_list.append([4, 2, "HR"])
		current_block_list.append([4, 3, "HR"])
	elif piece_list[rand] == "SB":
		current_block_list.append([4, 0, "SB"])
		current_block_list.append([5, 0, "SB"])
		current_block_list.append([4, 1, "SB"])
		current_block_list.append([5, 1, "SB"])
	elif piece_list[rand] == "TW":
		current_block_list.append([4, 1, "TW"])
		current_block_list.append([4, 0, "TW"])
		current_block_list.append([3, 1, "TW"])
		current_block_list.append([5, 1, "TW"])

	for i in range(len(current_block_list)):
		for x in range(len(block1)):
			if current_block_list[i][0] == block1[x][0] and current_block_list[i][1] == block1[x][1]:
				end_game = True
				pygame.mixer.Sound.play(death_sound)
				pygame.mixer.music.stop()
				print(end_game)

	return current_block_list, piece_list[rand]

def get_corners(center):
	topleft_corner = [center[0] - 1, center[1] - 1]
	topright_corner = [center[0] + 1, center[1] - 1]
	bottomright_corner = [center[0] + 1, center[1] + 1]
	bottomleft_corner = [center[0] - 1, center[1] + 1]

	return topleft_corner, topright_corner, bottomright_corner, bottomleft_corner

def rotate_piece(current_piece):
	normal_rotation = False
	hero_rotation = False
	smash_rotation = False
	global current_block_list
	global hero_iteration
	previous_hero_iteration = hero_iteration
	wall_bounce = False
	templist = current_block_list.copy()

	if current_piece == "OR":
		normal_rotation = True
	elif current_piece == "BR":
		normal_rotation = True
	elif current_piece == "RZ":
		normal_rotation = True
	elif current_piece == "CZ":
		normal_rotation = True
	elif current_piece == "HR":
		hero_rotation = True
	elif current_piece == "SB":
		return
	elif current_piece == "TW":
		normal_rotation = True

	# rotate normal pieces
	topleft_corner, topright_corner, bottomright_corner, bottomleft_corner = get_corners(current_block_list[0])
	if normal_rotation:
		x = 0
		while x != 2:
			for i in range(1, len(current_block_list)):
				# move all corners
				if templist[i] == topleft_corner: # move right on x axis
					#templist.append([current_block_list[i][0] + 1, current_block_list[i][1]])
					templist[i] = [templist[i][0] + 1, templist[i][1] ]  #changed code here
				elif templist[i] == topright_corner:
					#templist.append([current_block_list[i][0], current_block_list[i][1] + 1])
					templist[i] = [templist[i][0], templist[i][1] + 1] # move down on y axis
				elif templist[i] == bottomright_corner:
					#templist.append([current_block_list[i][0] - 1, current_block_list[i][1]])
					templist[i] = [templist[i][0] - 1, templist[i][1]] # move left axis
				elif templist[i] == bottomleft_corner :
					#templist.append([current_block_list[i][0], current_block_list[i][1] - 1])
					templist[i] = [templist[i][0], templist[i][1] - 1]# move up on y axis

				# move others
				elif templist[i] == [templist[0][0] - 1, templist[0][1]] : # left of center, move it up
					#templist.append([current_block_list[i][0], current_block_list[i][1] - 1])
					templist[i] = [templist[i][0], templist[i][1] - 1]
				elif templist[i] == [templist[0][0], templist[0][1] -1] : # above center, move right
					templist[i] = [templist[i][0] + 1, templist[i][1]]
					#templist.append([current_block_list[i][0] + 1, current_block_list[i][1]])
				elif templist[i] == [templist[0][0] + 1, current_block_list[0][1]] : # right of center, move down
					templist[i] = [templist[i][0], templist[i][1] + 1]
					#templist.append([current_block_list[i][0], current_block_list[i][1] + 1])
				elif templist[i] == [templist[0][0] , templist[0][1] + 1] : # below center, move left
					templist[i] = [templist[i][0] - 1, templist[i][1]]
					#templist.append([current_block_list[i][0] - 1, current_block_list[i][1]])
			x += 1
	if hero_rotation:
		templist = []

		if hero_iteration == 0:
			#current_block_list[0] = [current_block_list[0][0] + 1, current_block_list[0][1] ] # move right
			templist.append([current_block_list[0][0] + 1, current_block_list[0][1] ])
			templist.append([current_block_list[0][0] + 2, current_block_list[0][1]]) #
			templist.append([templist[0][0] -1, templist[0][1]])
			templist.append([templist[0][0] - 2, templist[0][1]])
			hero_iteration += 1

		elif hero_iteration == 1:
			#current_block_list[0] = [current_block_list[0][0], current_block_list[0][1] + 1] # move down
			templist.append([current_block_list[0][0], current_block_list[0][1] + 1])
			templist.append([current_block_list[0][0], current_block_list[0][1] + 2])
			templist.append([templist[0][0], templist[0][1] - 1])
			templist.append([templist[0][0], templist[0][1] - 2])
			hero_iteration += 1
		elif hero_iteration == 2:
			#current_block_list[0] = [current_block_list[0][0] - 1, current_block_list[0][1]] # move left
			templist.append([current_block_list[0][0] - 1, current_block_list[0][1]])
			templist.append([current_block_list[0][0] - 2, current_block_list[0][1]])
			templist.append([templist[0][0] + 1, templist[0][1]])
			templist.append([templist[0][0]  + 2, templist[0][1]])
			hero_iteration += 1
		elif hero_iteration == 3:
			#current_block_list[0] = [current_block_list[0][0], current_block_list[0][1] - 1]# move up
			templist.append([current_block_list[0][0], current_block_list[0][1] - 1])
			templist.append([current_block_list[0][0], current_block_list[0][1] -2])
			templist.append([templist[0][0], templist[0][1] +1])
			templist.append([templist[0][0], templist[0][1] +2])
			hero_iteration = 0

	# check if any rotated block overlaps with a placed block, if so, exit function cancel rotation
	for i in range(len(templist)):
		for b in range(len(block1)):
			if templist[i][0] == block1[b][0] and templist[i][1] == block1[b][1]:
				print("collision")
				return
	# check if any of the current coordinates of the rotated piece are out of bounds
	wall_check = templist.copy()
	wall_check.sort()


	x_diff = 0
	y_diff = 0
	# check both sides of x axis for wall kick
	if wall_check[0][0] < 0:

		x_diff = wall_check[0][0] * -1
		wall_bounce = True
	if wall_check[-1][0] > map_x_length - 1:
		x_diff = wall_check[-1][0] - (map_x_length - 1)
		x_diff = x_diff * -1
		wall_bounce = True

	# sorts based on y positions
	wall_check.sort( key=itemgetter(1))
	if wall_check[-1][1] > map_y_length - 1:
		y_diff = wall_check[-1][1] - (map_y_length - 1)
		y_diff = y_diff * -1

		wall_bounce = True
	if wall_bounce:

		# add all offsets
		for i in range(len(templist)):
			templist[i][0] += x_diff
			templist[i][1] += y_diff
	# set rotated piece

	current_block_list = templist

def check_for_tetris():

	clear_y_axis = []
	lines_cleared = 0
	global current_block_list
	global block1
	global update_placed_blocks
	has_cleared_lines = False
	for i in range(len(current_block_list)):
		counter = 0
		# get current block y coordinate
		y = current_block_list[i][1]
		# count every placed block "P" on each Y axis the current block affects
		for x in range(map_x_length):

			if map[y][x] == "P":
				counter += 1

			else:
				break
		# check if placed blocks equals map length
		if counter == map_x_length:
			lines_cleared += 1
			has_cleared_lines = True
			update_placed_blocks = True
			if not y in clear_y_axis:

				clear_y_axis.append(y)


	if has_cleared_lines:
		pygame.mixer.Sound.play(clear_lines_sound)
		global add_score
		global total_lines
		global current_line_counter
		global level
		global game_speed
		global level_text
		global total_lines_text
		total_lines += len(clear_y_axis)

		current_line_counter += len(clear_y_axis)
		total_lines_text = font.render('LINES:{0}'.format(total_lines), True, (255, 255, 255))
		if lines_cleared ==  1:
			add_score += 40
		elif lines_cleared == 2:
			add_score += 100
		elif lines_cleared == 3:
			add_score += 300
		elif lines_cleared == 4:
			add_score+= 1200
		 # all y axis that were cleared, stored as ints
		new_placed_list = []

		# check if current_line_counter is above 10, if so level up and reset counter
		if current_line_counter >= 10:
			remainder = current_line_counter - 10
			level +=1
			current_line_counter = remainder
			game_speed += 2
			print("level up")
			level_text = font.render('LEVEL:{0}'.format(level), True, (255,255,255))

			print(total_lines)
		print(current_line_counter)
		# get rid of any y axis duplicated in new list
		for i in range(len(block1)):
			if block1[i][1] in clear_y_axis:
				pass
			else:
				new_placed_list.append(block1[i]) # add blocks that are remaining after clearing to a new list
		block1 = new_placed_list # reset block list to the new list


		# sort cleared y list from lowest ( top of map to bottom)
		clear_y_axis.sort()
		# for every y axis in list
		for y in clear_y_axis:

		# move all blocks above current y cleared, down
			for i in range(len(block1)):
				if block1[i][1]  < y:
					block1[i][1] += 1


def update_map(map, current_block_list):
	global update_placed_blocks
	# clear map
	for y in range(len(map)):
		for x in range(len(map[y])):
			if map[y][x] != "0":
				map[y][x] = "0"


	# set map
	if currently_has_block:
		for i in range(len(current_block_list)):
			#current_block_list[i] = [current_block_list[i][0], current_block_list[i][1]]

			map[current_block_list[i][1]] [current_block_list[i][0]] = "#"

	#update placed blocks
	for i in range(len(block1)):
		map[block1[i][1]][block1[i][0]] = "P"

	update_placed_blocks = False

def get_block_color(name):
	if name == "OR":
		return OR_color
	elif name == "BR":
		return BR_color
	elif name == "RZ":
		return RZ_color
	elif name == "CZ":
		return CZ_color
	elif name == "HR":
		return HR_color
	elif name == "SB":
		return SB_color
	elif name == "TW":
		return TW_color

def debug():

	with open('readme.txt', 'w') as f:
		for row in map:
			for block in row:
				f.write(" " + block + " ")
			f.write("\n")
		f.write("Move X Axis:" + str(move_x_axis))

def endgame_screen():
	pass

def load_scores():
	global score_list
	global HIGHSCORE
	try:
		score_list = pickle.load(open("score_list.pickle", "rb"))
		HIGHSCORE = score_list[-1]
	except (OSError, IOError) as e:
		score_list.append(0)
		pickle.dump(score_list, open("score_list.pickle", "wb"))
		print("created file")
		print(score_list)

def save_score():
	if score not in score_list:
		score_list.append(score)
		print("new high score")
	score_list.sort()
	pickle.dump(score_list, open("score_list.pickle", "wb"))



hit_rotate_key = False

# FONTS
font = pygame.font.Font('slkscreb.ttf', 32)
smaller_font = pygame.font.Font('slkscreb.ttf', 22)
medium_font = pygame.font.Font('slkscreb.ttf', 26)
# FONT RENDERS
score_text = font.render('SCORE:', True, (255,255,255))
level_text = medium_font.render('LEVEL:{0}'.format(level), True, (255,255,255))
total_lines_text = medium_font.render('LINES:{0}'.format(total_lines), True, (255,255,255))
next_piece_text = smaller_font.render('NEXT PIECE'.format(total_lines), True, (255,255,255))
highscore_text = smaller_font.render('HIGHSCORE:', True, (255,255,255))
endgame_text = font.render('PRESS ANY KEY TO PLAY AGAIN', True, (255,255,255), (50,50,50))

scoreRect = score_text.get_rect()

# load sounds/music
place_sound = pygame.mixer.Sound("click.wav")
death_sound = pygame.mixer.Sound("explosion.wav")
clear_lines_sound = pygame.mixer.Sound("clear_lines.wav")
pygame.mixer.music.load('tetris_song.wav')
# -------- Main Program Loop -----------
pygame.mixer.music.set_volume(.2)
pygame.mixer.music.play(-1)
map = create_map_grid(map_x_length, map_y_length)
load_scores()
highscore_text_num = smaller_font.render(str(HIGHSCORE), True, (255, 255, 255))
holding_L = False
holding_R = False

current_block_list, current_piece = generate_piece(pieces, current_piece)
next_block_list, next_piece_name = generate_piece(pieces, current_piece)
currently_has_block = True
while not done:

	score_num_text = font.render(str(score), True, (255, 255, 255))
	score_num_rect = score_num_text.get_rect()

	#---- Start runs the first frame

	if end_game == True:

		while end_game:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					save_score()
					done = True
					end_game = False
				if event.type == pygame.KEYDOWN:
					save_score()
					load_scores()
					current_block_list = []
					block1 = []
					currently_has_block = True
					pygame.mixer.music.play(-1)
					current_block_list, current_piece = generate_piece(pieces, current_piece)
					next_block_list, next_piece_name = generate_piece(pieces, current_piece)
					score = 0
					game_speed = 15
					tick = normal_tick
					end_game = False
					pushing_down = False
					highscore_text_num = smaller_font.render(str(HIGHSCORE), True, (255, 255, 255))



	# set initial blocks
	if currently_has_block == False: # generate new block

		current_block_list, current_piece = next_block_list, next_piece_name
		next_block_list, next_piece_name = generate_piece(pieces, current_piece)


		currently_has_block = True


	# --- Main event loop
	dt = clock.tick(FPS) / 1000

	# Reset input

	# INPUT---------------------------
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			save_score()
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				moving_right = True
				holding_R = True
				move_x_axis = 1
				holding_move = True
				move(current_block_list, map, 1)
				fast_move_initiated = False
				holding_move_button_time = 0
			elif event.key == pygame.K_LEFT:
				moving_left = True
				move_x_axis = -1
				holding_L = True
				holding_move = True
				fast_move_initiated = False
				holding_move_button_time = 0
				move(current_block_list, map, -1)
			if event.key == pygame.K_SPACE:
				debug()
			if event.key == pygame.K_DOWN:
				pushing_down = True
				tick = fast_tick
			if event.key == pygame.K_UP:
				rotate_piece(current_piece)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				tick = normal_tick
				pushing_down = False
			if event.key == pygame.K_LEFT and holding_R:
				holding_L = False
				move_x_axis = 1
				holding_move_button_time = 0
				fast_move_initiated = False
			elif event.key == pygame.K_LEFT:
				holding_L = False
			if event.key == pygame.K_RIGHT and holding_L:
				holding_R = False
				move_x_axis = -1
				holding_move_button_time = 0
				fast_move_initiated = False
			elif event.key == pygame.K_RIGHT:
				holding_R = False

	if holding_L:
		#move_x_axis = -1
		holding_move = True
		holding_move_button_time += dt
	elif holding_R:
		#move_x_axis = 1
		holding_move = True
		holding_move_button_time += dt
	else:
		move_x_axis = 0
		move_current_time = False
		holding_move = False
		holding_move_button_time = 0
		fast_move_initiated = False
	if holding_move_button_time >= move_button_timer_max:
		holding_move_button_time = 0
		fast_move_initiated = True
	#print("L:{0} - R:{1} - MoveTimer:{2} - HoldingMove:{3}".format(holding_L, holding_R, move_current_time, holding_move))
	# check if a move was attempted --------------------
	if move_x_axis != 0 and holding_move and move_current_time >= move_timer_max and fast_move_initiated:
		# if move attempted, detect collisions to specified side
		move(current_block_list, map,move_x_axis)
		move_current_time = 0

	# --- Game logic should go here

	# move blocks DOWN
	if current_tick >= tick:
		if pushing_down:
			add_score += 2
		else:
			add_score +=1


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
			pygame.mixer.Sound.play(place_sound)
			# CONVERT PLAYERS CURRENT BLOCK TO "PLACED"
			for i in range(len(current_block_list)):


				map[current_block_list[i][1]][current_block_list[i][0]] = "P"
				block1.append([current_block_list[i][0] ,current_block_list[i][1], current_piece])
			collision = False
			currently_has_block = False

			check_for_tetris()

			current_block_list = []

		# MOVE PLAYER BLOCKS DOWN SINCE NO COLLISION IS DETECTED
		else:
			# add gravity by adding +1 to every Y coordinate in current_block_list
			for i in range(len(current_block_list)):
				current_block_list[i] = [current_block_list[i][0], current_block_list[i][1] + 1]
				map[current_block_list[i][1]][current_block_list[i][0]] = "#"
	# update map list
	update_map(map, current_block_list)
	score += add_score
	add_score = 0



	# --- Screen-clearing code goes here

	# Here, we clear the screen to white. Don't put other drawing commands
	# above this, or they will be erased with this command.

	# If you want a background image, replace this clear with blit'ing the
	# background image.
	screen.fill(BLACK)

	# --- Drawing code should go here

	#  ---Draw blocks onto screen
	# draw current piece
	for block in current_block_list:

		pygame.draw.rect(screen, get_block_color(current_piece),pygame.Rect(block[0] * BLOCK_SIZE + offset, block[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
	# draw placed blocks
	for placed_block in block1:
		pygame.draw.rect(screen, get_block_color(placed_block[2]), pygame.Rect(placed_block[0] * BLOCK_SIZE + offset, placed_block[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

	# draw next block
	for block in next_block_list:
		pygame.draw.rect(screen, get_block_color(next_piece_name),
		                 pygame.Rect(block[0] * BLOCK_SIZE + 525, block[1] * BLOCK_SIZE + 200, BLOCK_SIZE, BLOCK_SIZE))
	# draw all game lines
	for i in range(20):
		pygame.draw.line(screen, (0, 0, 0), [offset, i *BLOCK_SIZE], [600, i*BLOCK_SIZE], 2)
	for i in range(10):
		pygame.draw.line(screen, (0, 0, 0), [offset + i * BLOCK_SIZE, 0 ], [offset + i * BLOCK_SIZE, 800 ],2 )


	pygame.draw.line(screen, (201, 201, 201), [offset,0], [BLOCK_SIZE * 20, 0], 3)
	pygame.draw.line(screen, (201, 201, 201), [offset, 800], [600,800 ], 3)
	pygame.draw.line(screen, (201, 201, 201), [offset, 0], [offset, 800], 3)
	pygame.draw.line(screen, (201, 201, 201), [600 - 1, 0], [600 - 1, 800], 3)

	# handle TEXT
	if end_game:
		screen.blit(endgame_text, pygame.Rect(400 - (endgame_text.get_width() / 2) , 400, 60, 60))

	screen.blit(score_text, scoreRect)
	score_num_rect.y += 40
	screen.blit(score_num_text, score_num_rect)
	screen.blit(level_text, pygame.Rect(0, 100, 60, 60))
	screen.blit(next_piece_text, pygame.Rect(605, 150, 60, 60))
	screen.blit(total_lines_text, pygame.Rect(0, 160, 60, 60))
	screen.blit(highscore_text, pygame.Rect(0, 260, 60, 60))
	screen.blit(highscore_text_num, pygame.Rect(0, 280, 60, 60))



	current_tick += dt * game_speed

	if holding_R or holding_L and fast_move_initiated:
		move_current_time += dt * move_speed
	# --- Go ahead and update the screen with what we've drawn.
	pygame.display.flip()

	# --- Limit to 60 frames per second
	clock.tick(FPS)

# Close the win