import pygame, time, random, math
#variables
# boring display variables
window_width = 1500
window_height = 800
window = pygame.display.set_mode((window_width, window_height), 0, 32)

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
# more boring display variables
FPS = 35
fpsClock = pygame.time.Clock()
window.fill(WHITE)
pygame.display.update()
last_time = time.time()

can_shoot = True

# player things - variables
gravity = 1
jumping = True
falling = False
last_value = 0
collide = False
y_velocity = 0
x_velocity = 0
jump_force = 16
blue_ball_status = None
orange_ball_status = None
blue_portal = pygame.Rect(500, 500, 10, 10)
orange_portal = pygame.Rect(0, 0, 35, 35)

player_x = 100
player_y = 100
player_size_x = 20
player_size_y = 20

#more variables
test_level = [
    'x---------------------------------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x--------------xxxx---------------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x-------------------------xxx-----------------------------------------x',
    'x--------------------------------------xxxxxxx------------------------x',
    'x-----------------------------xxxx------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x------------------------xxx------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'x----------------xxxx-------------------------------------------------x',
    'x---------------------------------------------------------------------x',
    'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',

]

walls = []

x=0
y=0
for row in test_level:
    for col in row:
        if col == 'x':
            walls.append(pygame.Rect(x, y, 30, 39))
        x += window_width/len(row)
    y += (window_height/len(test_level))
    x = 0




#walls = [pygame.Rect(100, 50, 500, 50), pygame.Rect(0, 180, 50, 500), pygame.Rect(450, 180, 50, 500), pygame.Rect(0, 280, 500, 50), pygame.Rect(0, 180, 100, 50)]



class Player():
    def __init__(self, rect):
        self.player = rect


    def draw_player(self):
        window.fill(WHITE)
        pygame.draw.rect(window, BLUE, (self.player))
        pygame.display.update()


    def movement(self, walls):
        global falling, jumping, jump_force, gravity, last_value, y_velocity, x_velocity
        collide = False


        for i in range(abs(round(y_velocity))):

            last_value = self.player.y
            if y_velocity != 0:
                self.player.move_ip(0, y_velocity/abs(y_velocity))
                for wall in walls:
                    if self.player.colliderect(wall):
                        if y_velocity > 0:
                            jumping = False
                        y_velocity = 0
                        self.player.y = last_value

        for i in range(abs(round(x_velocity))):


            if x_velocity != 0:

                last_value = self.player.x
                self.player.move_ip(x_velocity/abs(x_velocity), 0)
                for wall in walls:
                    if self.player.colliderect(wall):
                        self.player.x = last_value

        if pressed_keys[pygame.K_w] and jumping == False:
            jumping = True
            y_velocity -= jump_force


class Shoot():
    def __init__(self, x, y, mouse_x, mouse_y, color):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(self.mouse_y-self.y, self.mouse_x-self.x)
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.color = color
    def draw(self, draw):
        global blue_ball_status, orange_ball_status,blue_portal,orange_portal, collide, player
        self.hitbox = pygame.Rect(self.x, self.y, 15, 15)
        a = abs(self.vel_y)
        b = abs(self.vel_x)
        collide = False

        while a > 0 or b > 0:

            if self.vel_y > 0 and a > 0:
                self.y += 0.1
                a -= 0.1
            if self.vel_y < 0 and a > 0:
                self.y -= 0.1
                a -= 0.1

            if self.vel_x > 0 and b > 0:
                self.x += 0.1
                b -= 0.1
            if self.vel_x < 0 and b > 0:
                self.x -= 0.1
                b -= 0.1
        pygame.draw.rect(window, self.color, self.hitbox)
        for wall in walls:
            if self.hitbox.colliderect(wall):

                if self.color == (0, 0, 255):
                    blue_ball_status = "open"
                    blue_portal.x = self.x
                    blue_portal.y = self.y
                    print(self.x, self.y)
                    print(blue_portal.x, blue_portal.y)
                    break


                if self.color == (255, 165, 0):
                    orange_ball_status = "open"
                    orange_portal.x = self.x
                    orange_portal.y = self.y
                    break









player = Player((pygame.Rect(player_x, player_y, player_size_x, player_size_y)))



        #print(x, y)
pygame.display.update()
while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_d]:
        x_velocity += 2
    if pressed_keys[pygame.K_a]:
        x_velocity -= 2

    x_velocity *= 0.8

    y_velocity += gravity

    #delta time thing(boring)
    delta_time = time.time() - last_time
    delta_time *= 60
    last_time = time.time()

    #pygame is bad, so I created an option to close the game. no thanks please
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()



    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            blue_ball = Shoot(player.player.x, player.player.y, mouse_x, mouse_y, BLUE)
            blue_ball_status = "fly"

        if event.button == 3:
            orange_ball = Shoot(player.player.x, player.player.y, mouse_x, mouse_y, ORANGE)
            orange_ball_status = "fly"

    # more boring display things
    window.fill(WHITE)

    player.movement(walls)
    player.draw_player()

    if blue_ball_status == "fly":
        blue_ball.draw(window)
    if orange_ball_status == "fly":
        orange_ball.draw(window)

    if orange_ball_status == "open":

        pygame.draw.rect(window, ORANGE, orange_portal)
    if blue_ball_status == "open":
        pygame.draw.rect(window, BLUE, blue_portal)


    for wall in walls:
        pygame.draw.rect(window, BLACK, wall)

        if wall.colliderect(player.player):
            pygame.draw.rect(window, RED, wall)



    pygame.display.update()
    fpsClock.tick(FPS)




