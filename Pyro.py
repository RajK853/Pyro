import random, pygame, sys, os
from pygame.locals import *

pygame.init()
# set up window, mouse and sound
WINW = 700
WINH = 500
windowSurface = pygame.display.set_mode((WINW, WINH))
pygame.display.set_caption("Flamboyant Flame")
pygame.mixer.music.load("Data/background_music.mp3")
gameOver = pygame.mixer.Sound("Data/game_over.ogg")

# set up color
WHITE = (255, 255, 255)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
TEAL = (0, 128, 128)

# set up player rectangle
playerRect = pygame.Rect(windowSurface.get_rect().centerx, WINH-93, 50, 75)

# set up cloud's constants
cloudImg = pygame.image.load("Data/clouds.png")
MAXCLOUDS = 15           # Maximum clouds in the screen
CLOUDMINSIZE = 20
CLOUDMAXSIZE = 100
CLOUDMINSPEED = 8
CLOUDMAXSPEED = 40
cloudSpeeds = [i/8 for i in range(CLOUDMINSPEED, CLOUDMAXSPEED, 5)]            # Stores all possible speed for clouds
# set up rain or snow's constants
RAINRATE = 3
RAINMINSIZE = 15
RAINMAXSIZE = 30
RAINMINSPEED = 2
RAINMAXSPEED = 8
rainSpeeds = [i/2 for i in range(RAINMINSPEED, RAINMAXSPEED)]   # Create all possible speed for rains

def EXIT():     # Exit code
	topScoreFile("save")
	pygame.quit()
	sys.exit()

def writeText(text, color, size, x, y, returnTextInfo):           # writes text on the surface
	font = pygame.font.SysFont("Comic Sans MS", size, True)
	textObj = font.render(text, True, color)
	textRect = textObj.get_rect()
	textRect.topleft = (x, y)
	if returnTextInfo:              # if rectangle data requested, return textObj and textRect
		return textObj, textRect
	windowSurface.blit(textObj, textRect)
	pygame.display.update()

def pause(text):        # Pause the game with a message until an event happens
	pygame.mouse.set_visible(True)
	while True:
		textObj, textRect = writeText(text, TEAL, 30, 0, WINH/2-20, True)
		textRect.centerx = windowSurface.get_rect().centerx             # places the text at the center of the screen
		pygame.draw.rect(windowSurface, (bgcolor, bgcolor, bgcolor), (textRect.left-10, textRect.top-25, textRect.width+20, textRect.height+50))
		windowSurface.blit(textObj, textRect)
		for event in pygame.event.get():
			if event.type == QUIT:
				EXIT()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					EXIT()
				# else make mouse invisible again and exit
				pygame.mouse.set_visible(False)
				return
			if event.type == MOUSEBUTTONUP:
				pygame.mouse.set_visible(False)
				return
		pygame.display.update()

def makeBackground():           # draw background on the screen
	bgImg = pygame.transform.scale(pygame.image.load("Data/background.png"), (WINW, WINH))
	windowSurface.blit(bgImg, windowSurface.get_rect())

def makeNewClouds():    # Makes new cloud and add it in the list "clouds"
	while len(clouds) != MAXCLOUDS:
		cloudW = random.randint(CLOUDMINSIZE, CLOUDMAXSIZE)
		cloudH = int(2*cloudW/3)
		newCloud = {"rect" : pygame.Rect(WINW, random.randint(-10, 50), cloudW, cloudH), "speed" : random.choice(cloudSpeeds), "image" : pygame.transform.scale(cloudImg, (cloudW, cloudH))}
		clouds.append(newCloud)

def moveClouds():       # Moves each cloud stored in the list "clouds" in left direction
	for c in clouds[:]:
		c["rect"].move_ip(-1*c["speed"], 0) # Move cloud with its speed
		windowSurface.blit(c["image"], c["rect"])   # Draw the cloud on the surface
		# remove a cloud when it passes throught the left side of the window
		if c["rect"].right < 0:
			clouds.remove(c)

def displayScore():          # Displays the score and top score on the screen
	score1Text, score1Rect = writeText("Score:", TEAL, 24, 10, 10, True)
	score2Text, score2Rect = writeText(str(score), BLUE, 24, score1Rect.right+5, 10, True)
	topScore1Text, topScore1Rect = writeText("Top Score:", TEAL, 24, 10, score1Rect.bottom+3, True)
	topScore2Text, topScore2Rect = writeText(str(topScore), BLUE, 24, topScore1Rect.right+5, score1Rect.bottom+3, True)
	windowSurface.blit(score1Text, score1Rect)
	windowSurface.blit(score2Text, score2Rect)
	windowSurface.blit(topScore1Text, topScore1Rect)
	windowSurface.blit(topScore2Text, topScore2Rect)

def playerGotHit(playerRect):       # Check if player collided with any rain 
	for r in rains:
		if playerRect.colliderect(r["rect"]):
			return True
	return False

def makeRain(score, RAINRATE):      # Makes new rains and adds them to the the rains list. 
	rate = RAINRATE
	for i in range(rate):
		rainW = random.randint(RAINMINSIZE, RAINMAXSIZE)
		if score < 1000:
			rainH = int(3*(rainW/2))
			rainImg = pygame.transform.scale(pygame.image.load("Data/rain1.png"), (rainW, rainH))
		if 1000 <= score < 2500:
			RAINRATE = 4
			rainH = int(3*(rainW/2))
			rainImg = pygame.transform.scale(pygame.image.load("Data/rain2.png"), (rainW, rainH))
		if 2500 <= score < 3500:
			RAINRATE = 5
			rainH = rainW
			rainImg = pygame.transform.scale(pygame.image.load("Data/star.png"), (rainW, rainH))
		if 3500 <= score < 4500:
			RAINRATE = 6
			rainH = 2*rainW
			rainImg = pygame.transform.scale(pygame.image.load("Data/thunder.png"), (rainW, rainH))
		if score >= 4500:
			if score%50 == 0:           # Increase rainrate for every 50 increase in score
				RAINRATE += 1
			x = random.randint(0, 3)
			if x == 0:
				rainH = int(3*(rainW/2))
				rainImg = pygame.transform.scale(pygame.image.load("Data/rain1.png"), (rainW, rainH))
			elif x == 1:
				rainH = int(3*(rainW/2))
				rainImg = pygame.transform.scale(pygame.image.load("Data/rain2.png"), (rainW, rainH))
			elif x == 2:
				rainH = rainW
				rainImg = pygame.transform.scale(pygame.image.load("Data/star.png"), (rainW, rainH))
			else:
				rainH = 2*rainW
				rainImg = pygame.transform.scale(pygame.image.load("Data/thunder.png"), (rainW, rainH))
		newRain = {"rect" : pygame.Rect(random.randint(0, WINW-rainW), 0, rainW, rainH), "speed" : random.choice(rainSpeeds), "image" : rainImg}
		rains.append(newRain)

def topScoreFile(mode):           # save topScore in a file and load it later
	if mode == "load":          # Load score
		if not os.path.isfile("Data/topScore.txt"):             # if topScore file not present, return zero (0)
			return 0
		else:
			with open("Data/topScore.txt") as file:  #else read the score from the file
				data = file.read().lower()
			score = ""
			for i in data:
				# If someone messes with the topScore file
				if (ord(i)-ord("a")) > 9:
					gameOver.play()
					windowSurface.fill(WHITE)
					writeText("Nice try messing with the top score file.", TEAL, 24, 150, 135, False)
					writeText("But you are busted!! Top score is resetted to 0.", TEAL, 24, 100, 165, False)
					with open("Data/topScore.txt", "w") as file:
						file.write("a")
					pause("Press a key loser!")
					return 0
				score += str(ord(i)-ord("a"))
			return int(score)
	if mode == "save":          # Save score
		eScore = ""         # encrypt score before storing
		for i in str(topScore): eScore += str(chr(ord("a")+int(i)))
		with open("Data/topScore.txt", "w") as file:
			file.write(eScore)

# Start of the program
while True:
	pygame.mouse.set_visible(True)
	# Display information about the game
	clouds = []     # Stores dictionary of all the clouds
	rains = []          # Stores dictionary of all the rains
	bgcolor = 255       # holds numerical value for background color which will decrease with time to make an effect of night
	topScore = topScoreFile("load")                 # load top score from the file
	# randomly choose player image of different colours
	playerImg = random.choice([pygame.transform.scale(pygame.image.load("Data/player1.png"), (50, 75)), pygame.transform.scale(pygame.image.load("Data/player2.png"), (50, 75)), pygame.transform.scale(pygame.image.load("Data/player3.png"), (50, 75)), pygame.transform.scale(pygame.image.load("Data/player2.png"), (50, 75))])
	score = 0       # set initial score to zero
	day = True      # will be used to change day to night and vice versa
	windowSurface.fill(WHITE)
	makeBackground()
	writeText("Flamboyant Flame", RED, 30, (WINW/2)-130, 145, False)
	pygame.time.wait(800)
	writeText("Avoid falling objects and score more.", BLACK, 18, 180, 200, False)
	pygame.time.wait(800)
	writeText("Move you mouse to move the character.", BLACK, 18, 170, 230, False)
	pygame.time.wait(800)
	writeText("Press 'p' to pause game and 'Esc' to exit.", BLACK, 18, 158, 260, False)
	pygame.time.wait(3000)
	pause("Press any key to start the game.")
	pygame.mouse.set_visible(False)
	pygame.mixer.music.play(-1, 6.0)
	while True:
		score += 1
		# game starts from here
		windowSurface.fill((bgcolor, bgcolor, bgcolor))
		windowSurface.blit(playerImg, pygame.Rect(playerRect.left, playerRect.top-25, playerRect.width, playerRect.height-25))
		if score % 50 == 0:             # add rains in the screen for every 50 increment in the score
			# Add rains to rains dictionary
			makeRain(score, RAINRATE)
			if day:
				if bgcolor > 0:
					bgcolor -= 4        # change the bgcolor so that background color change from white(day) to black(night) slowly
					if bgcolor < 0:
						bgcolor = 0
						day = False
			else:
				if bgcolor < 255:
					bgcolor += 4        # change the bgcolor so that background color change from black(night) to white(day) slowly
					if bgcolor > 255:
						bgcolor = 255
						day = True
		# move the rains downward
		for r in rains[:]:
			r["rect"].move_ip(0, r["speed"])
			windowSurface.blit(r["image"], r["rect"])
			# remove any rain that touches the green ground
			if r["rect"].bottom > WINH-35:
				rains.remove(r)
		makeBackground()
		displayScore()
		makeNewClouds()
		moveClouds()
		# event handling
		for event in pygame.event.get():
			if event.type == QUIT:
				EXIT()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					EXIT()
				if event.key == ord("p"):
					pause("Paused")
			if event.type == MOUSEMOTION:
				# move the playerRect to cursor's x-coordinate.
				playerRect.centerx = event.pos[0]
		# move mouse cursor to the playerRect
		pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)
		if playerGotHit(playerRect):
			if score > topScore:
				topScore = score
			break
		# Update windowSurface
		pygame.display.update()
	pygame.mixer.music.stop()
	gameOver.play()
	if score == topScore:
		writeText("New Top Score: %s" % str(score), RED, 30, (WINW/2)-130, WINH/2+5, False)
	else:
		writeText("Your Score: %s" % str(score), BLACK, 30, (WINW/2)-110, WINH/2+5, False)
	writeText("Game Over!", BLACK, 30, (WINW/2)-70, (WINH/2)-24, False)
	pygame.display.update()
	pygame.time.wait(3000)
	pause("Press any key to play again.")
	topScoreFile("save")
