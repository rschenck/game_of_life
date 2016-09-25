import math
import random
import pygame
from conway_shapes import click_handler, Conway_Shape
black = (0,  0,  0)
white = (255,255,255)
darkgrey = (40, 40, 40)
red = (220,20,60)
b_red = (255,0,0)
green = (0,200,0)
b_green = (0,255,0)

def render_textrect(string, font, rect, text_color, background_color, justification=0):
	"""Returns a surface containing the passed text string, reformatted
	to fit within the given rect, word-wrapping as necessary. The text
	will be anti-aliased.

	Takes the following arguments:

	string - the text you wish to render. \n begins a new line.
	font - a Font object
	rect - a rectstyle giving the size of the surface requested.
	text_color - a three-byte tuple of the rgb value of the
				 text color. ex (0, 0, 0) = BLACK
	background_color - a three-byte tuple of the rgb value of the surface.
	justification - 0 (default) left-justified
					1 horizontally centered
					2 right-justified

	Returns the following values:

	Success - a surface object with the text rendered onto it.
	Failure - raises a TextRectException if the text won't fit onto the surface.
	"""

	import pygame

	final_lines = []

	requested_lines = string.splitlines()

	# Create a series of lines that will fit on the provided
	# rectangle.

	for requested_line in requested_lines:
		if font.size(requested_line)[0] > rect.width:
			words = requested_line.split(' ')
			# if any of our words are too long to fit, return.
			for word in words:
				if font.size(word)[0] >= rect.width:
					raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
			# Start a new line
			accumulated_line = ""
			for word in words:
				test_line = accumulated_line + word + " "
				# Build the line while the words fit.
				if font.size(test_line)[0] < rect.width:
					accumulated_line = test_line
				else:
					final_lines.append(accumulated_line)
					accumulated_line = word + " "
			final_lines.append(accumulated_line)
		else:
			final_lines.append(requested_line)

	# Let's try to write the text out on the surface.

	surface = pygame.Surface(rect.size)
	surface.fill(background_color)

	accumulated_height = 0
	for line in final_lines:
		if accumulated_height + font.size(line)[1] >= rect.height:
			raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
		if line != "":
			tempsurface = font.render(line, 1, text_color)
			if justification == 0:
				surface.blit(tempsurface, (0, accumulated_height))
			elif justification == 1:
				surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
			elif justification == 2:
				surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
			else:
				raise TextRectException, "Invalid justification argument: " + str(justification)
		accumulated_height += font.size(line)[1]

	return surface

def round_up_nearest_ten(n):
	return int(math.ceil(n / 10.0)) * 10

# returns a random rgb() color tuple from a preset array
def random_color():
	colors = [(255,0,0),(255,0,255),(135,0,255),(0,0,255),(0,195,255),(0,255,0),(225,255,0),(255,155,0)]
	return colors[random.randint(0,7)]

def button_tone():
	button = pygame.mixer.Sound('sound/button2.wav')
	pygame.mixer.Sound.play(button)


def user_select(gridDict, x, y, w, h, click_option):
	x = round_up_nearest_ten(x) - 10
	y = round_up_nearest_ten(y) - 10

	# if mouse pos != within banner add square
	# Banner Dimensions: (0, 470, 500, 30)
	if w > x > w-w and h-30 > y > h-h:
		button_tone()
		if gridDict[x,y].stat == 1:
			gridDict[x,y].stat = 0
		else:
			# print "Creating %s at [%s,%s]" % (Conway_Shape(click_option).name, x, y)
			click_handler(gridDict, x, y, click_option)


def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

def start(display_surface, x, y, pos=(0,0), mstate=(0,0,0)):
	xanchor = int(x/2.)
	yanchor = int(y/2.)
	if xanchor-25+50 > pos[0] > xanchor-25 and y-25+20 > pos[1] > y-25:
		pygame.draw.rect(display_surface, b_green, (xanchor-25, y-25, 50, 20))
		if mstate[0]:
			run = True
			button_tone()
		else:
			run = False
	else:
		pygame.draw.rect(display_surface, green, (xanchor-25, y-25, 50, 20))
		run = False

	smallText = pygame.font.Font("freesansbold.ttf",12)
	textSurf, textRect = text_objects("START!", smallText)
	textRect.center = ( (xanchor-25+(50/2)), (y-25+(20/2)) )
	display_surface.blit(textSurf, textRect)

	return run


def stop(display_surface, x, y, pos=(0,0), mstate=(0,0,0)):
	xanchor = int(x/2.)
	yanchor = int(y/2.)
	if (xanchor-60+50) > pos[0] > (xanchor-60) and (y-25+20) > pos[1] > y-25:
		pygame.draw.rect(display_surface, b_red, (xanchor-60, y-25, 50, 20))
		if mstate[0]:
			run = False
			button_tone()
		else:
			run = True
	else:
		pygame.draw.rect(display_surface, red, (xanchor-60, y-25, 50, 20))
		run = True

	smallText = pygame.font.Font("freesansbold.ttf",12)
	textSurf, textRect = text_objects("STOP!", smallText)
	textRect.center = ( (xanchor-60+(50/2)), (y-25+(20/2)) )
	display_surface.blit(textSurf, textRect)

	return run

def reset(display_surface, x, y, run, pos=(0,0), mstate=(0,0,0)):
	xanchor = int(x/2.)
	yanchor = int(y/2.)
	if (xanchor+10+50) > pos[0] > (xanchor+10) and (y-25+20) > pos[1] > y-25:
		pygame.draw.rect(display_surface, b_red, (xanchor+10, y-25, 50, 20))
		if mstate[0]:
			res_menu = True
			run = False
			button_tone()
		else:
			res_menu = False
			pass
	else:
		pygame.draw.rect(display_surface, red, (xanchor+10, y-25, 50, 20))
		res_menu = False

	smallText = pygame.font.Font("freesansbold.ttf",12)
	textSurf, textRect = text_objects("RESET", smallText)
	textRect.center = ( (xanchor+10+(50/2)), (y-25+(20/2)) )
	display_surface.blit(textSurf, textRect)

	return run, res_menu

def info_button(display_surface, x, y, run, pos=(0,0), mstate=(0,0,0)):
	xanchor = int(x/2.)
	yanchor = int(y/2.)

	pygame.draw.circle(display_surface, black, ((x-x+20), (y-25+(20/2))), 10, 2)

	smallText = pygame.font.Font("freesansbold.ttf",15)
	textSurf, textRect = text_objects("i", smallText)
	textRect.center = ( (x-x+20), (y-25+(20/2)+2))
	display_surface.blit(textSurf, textRect)

	# print str((pos[0],pos[1]))
	if x-x+30 > pos[0] > x-x+10 and y-5 > pos[1] > y-22:
		if mstate[0]:
			show_i = True
			run = False
		else:
			show_i = False
	else:
		show_i = False

	return run, show_i

def info(display_surface, x, y, pos=(0,0), mstate=(0,0,0)):
	xanchor = int(x/2.)
	yanchor = int(y/2.)
	pygame.draw.rect(display_surface, white, (0, 0, x, y))

	smallText = pygame.font.Font("freesansbold.ttf",18)
	textSurf, textRect = text_objects("Back", smallText)
	textRect.center = ( x-x+24 , y-y+10 )
	display_surface.blit(textSurf, textRect)

	text_info = """John Conway's Cellular Automaton"""
	text_info2 = """\n\nRules:\n\nEach Cell with one or no neighbors dies.\nEach cell with 4 or more neighbors dies.\nEach cell with two or three neighbors survives.\nEach empty cell with three neighbors becomes populated.\n\nControls:\n\nClick to populate/depopulate a cell.\nClick start to begin model.\nClick stop to end model.\nClick reset to clear or choose preset simulations.\n\nCreated by:\n\nRyan Oliver Schenck & Steven Lee-Kramer\n\ngithub.com/rschenck/game_of_life.git"""

	# Headers
	smallText = pygame.font.Font(None,26)
	back_rect = pygame.Rect((x-x, y-y+60, x, y-50))
	rendered_text = render_textrect(text_info, smallText, back_rect, black, white, 1)
	display_surface.blit(rendered_text, back_rect)

	# Other Text
	smallText = pygame.font.Font(None,22)
	back_rect = pygame.Rect((x-x, y-y+80, x, y-50))
	rendered_text = render_textrect(text_info2, smallText, back_rect, black, white, 1)
	display_surface.blit(rendered_text, back_rect)


	# print str((pos[0],pos[1]))
	if x-x+40 > pos[0] > x-x and y-y+18 > pos[1] > y-y:
		if mstate[0]:
			show_i = False
		else:
			show_i = True
	else:
		show_i = True


	return show_i


def reset_options(display_surface, x, y, pos=(0,0), mstate=(0,0,0)):
	xanchor = int(x/2.)
	yanchor = int(y/2.)

	pygame.draw.rect(display_surface, white, (xanchor-(yanchor/2.), 0-(y/4.0)+200, yanchor, 260))

	smallText = pygame.font.Font("freesansbold.ttf",18)
	textSurf, textRect = text_objects("Blank", smallText)
	textRect.center = ( (xanchor), (0-(y/4.0)+210) )
	display_surface.blit(textSurf, textRect)

	textSurf, textRect = text_objects("Gun", smallText)
	textRect.center = ( (xanchor), (0-(y/4.0)+240) )
	display_surface.blit(textSurf, textRect)

	textSurf, textRect = text_objects("Ten", smallText)
	textRect.center = ( (xanchor), (0-(y/4.0)+270) )
	display_surface.blit(textSurf, textRect)

	textSurf, textRect = text_objects("Binary", smallText)
	textRect.center = ( (xanchor), (0-(y/4.0)+300) )
	display_surface.blit(textSurf, textRect)

	textSurf, textRect = text_objects("Face", smallText)
	textRect.center = ( (xanchor), (0-(y/4.0)+330) )
	display_surface.blit(textSurf, textRect)

	textSurf, textRect = text_objects("Maze", smallText)
	textRect.center = ( (xanchor), (0-(y/4.0)+360) )
	display_surface.blit(textSurf, textRect)

	textSurf, textRect = text_objects("Pulsar", smallText)
	textRect.center = ( (xanchor), (0-(y/4.0)+390) )
	display_surface.blit(textSurf, textRect)

	textSurf, textRect = text_objects("Gliders", smallText)
	textRect.center = ( (xanchor), (0-(y/4.0)+420) )
	display_surface.blit(textSurf, textRect)

	textSurf, textRect = text_objects("Random", smallText)
	textRect.center = ( (xanchor), (0-(y/4.0)+450) )
	display_surface.blit(textSurf, textRect)

	# print str((pos[0],pos[1]))
	
	s = 30
	# clear
	if xanchor+30 > pos[0] > xanchor-30 and s+5 > pos[1] > s-10:
		if mstate[0]:
			option = 'Blank'
		else:
			option = ''
	elif xanchor+30 > pos[0] > xanchor-30 and s+30+5 > pos[1] > s+30-10:
		# print str((pos[0],pos[1]))
		if mstate[0]:
			option = 'Gun'
		else:
			option = ''
	elif xanchor+30 > pos[0] > xanchor-30 and s+60+5 > pos[1] > s+30-10:
		# print str((pos[0],pos[1]))
		if mstate[0]:
			option = 'Ten'
		else:
			option = ''
	elif xanchor+30 > pos[0] > xanchor-30 and s+90+5 > pos[1] > s+90-10:
		# print str((pos[0],pos[1]))
		if mstate[0]:
			option = 'Binary'
		else:
			option = ''
	elif xanchor+30 > pos[0] > xanchor-30 and s+120+5 > pos[1] > s+120-10:
		# print str((pos[0],pos[1]))
		if mstate[0]:
			option = 'Face'
		else:
			option = ''
	elif xanchor+30 > pos[0] > xanchor-30 and s+150+5 > pos[1] > s+150-10:
		# print str((pos[0],pos[1]))
		if mstate[0]:
			option = 'Maze'
		else:
			option = ''
	elif xanchor+30 > pos[0] > xanchor-30 and s+180+5 > pos[1] > s+180-10:
		# print str((pos[0],pos[1]))
		if mstate[0]:
			option = 'Pulsar'
		else:
			option = ''
	elif xanchor+30 > pos[0] > xanchor-30 and s+210+5 > pos[1] > s+210-10:
		# print str((pos[0],pos[1]))
		if mstate[0]:
			option = 'Gliders'
		else:
			option = ''
	elif xanchor+30 > pos[0] > xanchor-30 and s+240+5 > pos[1] > s+240-10:
		# print str((pos[0],pos[1]))
		if mstate[0]:
			option = 'Random'
		else:
			option = ''
	else:
		option = ''

	return option

def click_creator(display_surface, x, y, click_option, pos=(0,0), mstate=(0,0,0), ):
	xanchor = int(x/2.)
	
	# print str((pos[0],pos[1]))
	if (x) > pos[0] > (x-50) and (y-25+20) > pos[1] > y-25:
		pygame.draw.rect(display_surface, (200,200,200), (x-55, y-25, 50, 20))
		if mstate[0]:
			click_option = (click_option + 1) % (Conway_Shape(1).max() + 1) or 1
		else:
			pass
	else:
		pygame.draw.rect(display_surface, (150,150,150), (x-55, y-25, 50, 20))


	smallText = pygame.font.Font("freesansbold.ttf",12)
	textSurf, textRect = text_objects(Conway_Shape(click_option).name, smallText)
	textRect.center = ( x-30, (y-25+(20/2)) )
	display_surface.blit(textSurf, textRect)

	return click_option





