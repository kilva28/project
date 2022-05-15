import pygame
pygame.init()
pygame.event.get()

back = (200,255,255)
win_size = 600
window = pygame.display.set_mode((win_size,win_size))
clock = pygame.time.Clock()

game_over = False

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x,y,width,height)
        self.fill_color = back
    def color(self,new_color):
        self.fill_color = new_color
    def fill(self):
        pygame.draw.rect(window,self.fill_color,self.rect)
    def colliderect(self,rect):
        return self.rect.colliderect(rect)
    def outline(self,frame_color,thickness):
        pygame.draw.rect(window, frame_color, self.rect, thickness)

class Picture(Area):
    def __init__(self,filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Label(Area):
    def set_text(self, text, fsize = 12, text_color = (0,0,0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x = 0, shift_y = 0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

platform_x = 240
platform_y = 500

speed_x = speed_y = 6

Move_left = Move_right = False
x1 = 0
x2 = win_size

monster_x = 5
monster_y = 5
total_enemies = 9
enemies = []

pygame.display.set_caption('Арканоид')

ball = Picture('ball.png',160,200,50,50)
platform = Picture('platform.png',platform_x, platform_y, 100, 30)

for j in range(3):
    y = monster_y + (55*j)
    x = monster_x + (34*j)
    for i in range(total_enemies):
        monster = Picture('enemy.png',x,y,50,50)
        enemies.append(monster)
        x += 68
    total_enemies -= 1

while not game_over:
    window.fill(back)
    ball.fill()
    platform.fill()

    for m in enemies:
        m.draw()
        if m.rect.colliderect(ball.rect):
            enemies.remove(m)
            m.fill()
            speed_y *= -1

    ball.draw()
    platform.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Move_left = True
            elif event.key == pygame.K_RIGHT:
                Move_right = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                Move_left = False
            elif event.key == pygame.K_RIGHT:
                Move_right = False

    if Move_left:
        platform.rect.x -= 6
    elif Move_right:
        platform.rect.x += 6

#шар
    ball.rect.x += speed_x
    ball.rect.y += speed_y

    if ball.colliderect(platform.rect):
        speed_y *= -1
#Барьер
    if platform.rect.x < x1:
        platform.rect.x = x1
    elif platform.rect.x > x2:
        platform.rect.x = x2

    if ball.rect.y < 0:
        speed_y *= -1
    elif ball.rect.x > win_size-50 or ball.rect.x < 0:
        speed_x *= -1

#победа/проигрыш
    elif ball.rect.y >= (platform_y+40):
        Lose = Label(150,150,50,50,back)
        Lose.set_text('YOU LOSE', 60,(255,0,0))
        Lose.draw(10,10)
        game_over = True

    elif len(enemies) == 0:
        Win = Label(150,150,50,50,back)
        Win.set_text('YOU WIN', 60,(0,255,0))
        Win.draw(10,10)
        game_over = True

    pygame.display.update()
    clock.tick(40)