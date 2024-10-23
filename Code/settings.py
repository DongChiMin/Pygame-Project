from pygame.math import Vector2
#screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

# overlay positions
OVERLAY_POSITIONS = {
	'tool' : (SCREEN_WIDTH/2 - 75, SCREEN_HEIGHT - 40),
	'seed': (SCREEN_WIDTH/2 + 75, SCREEN_HEIGHT - 40),
	'square_tool' : (SCREEN_WIDTH/2 - 75, SCREEN_HEIGHT - 20),
	'square_seed' : (SCREEN_WIDTH/2 + 75, SCREEN_HEIGHT -20),
	'backpack' : (SCREEN_WIDTH - 40, SCREEN_HEIGHT -20),
	'setting_UI' : (15, 15),
	'weather' : (SCREEN_WIDTH - 10, 10),
	'weather icon': (SCREEN_WIDTH -33, 30)
}
PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'fruit': 9,
	'rain drops': 10
}

APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

SALE_PRICES = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}
