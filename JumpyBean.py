# Imported Modules
from typing import Any
import pygame
from sys import exit
from random import randint , choice
pygame.init()
pygame.mixer.init()

# Sprite Classes and Functions

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load('graphics/player/walk1.png').convert_alpha()
        walk2= pygame.image.load('graphics/player/walk2.png').convert_alpha()
        walk3 = pygame.image.load('graphics/player/walk3.png').convert_alpha()
        walk4 = pygame.image.load('graphics/player/walk4.png').convert_alpha()
        walk5 = pygame.image.load('graphics/player/walk5.png').convert_alpha()
        self.walk = [walk1,walk2,walk3,walk4,walk5]
        self.index = 0
        self.jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(midbottom  = (80,300))

        
        self.jump_sound = pygame.mixer.Sound('music/jump.mp3')
        self.jump_sound.set_volume(0.1)
    def animation(self):
        # Jump Animation
        if self.rect.bottom < 300:
         self.image = self.jump
         # Walking Animation
        else:
         self.index += 0.2
         if self.index >= len(self.walk): self.index = 0
         self.image = self.walk[int(self.index)]

         # Death Reset

         global game_active
        if game_active == False:
          self.rect = self.image.get_rect(midbottom  = (80,300))

    def  movements(self):
      #GRAVITY
     if self.rect.bottom>= 300: self.gravity  = 0
     keys = pygame.key.get_pressed()
     if keys[pygame.K_SPACE] and self.rect.bottom>= 300 or keys[pygame.K_w] and self.rect.bottom>= 300 or keys[pygame.K_UP] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
     
     if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.rect.left>=0: self.rect.left -= 3
     elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.rect.right<=800: self.rect.right += 3

    def anti_gravity(self):
     self.gravity += 1
     self.rect.y += self.gravity
     if self.rect.bottom >= 300: self.rect.bottom = 300
           
    def update(self):
            self.movements()
            self.animation()
            self.anti_gravity()
       

class Enemies(pygame.sprite.Sprite):
   def __init__(self, type):
      super().__init__()

      if type == 'fly':
         fly_fly_1 = pygame.image.load('graphics/Fly/fly1.png').convert_alpha()
         fly_fly_2 = pygame.image.load('graphics/Fly/fly2.png').convert_alpha()
         self.list = [fly_fly_1,fly_fly_2]
         y_pos = 200
      elif type == 'snail':
         snail_walk_1 = pygame.image.load('graphics/Snail/snail1.png').convert_alpha()
         snail_walk_2 = pygame.image.load('graphics/Snail/snail2.png').convert_alpha()
         self.list = [snail_walk_1,snail_walk_2]
         y_pos = 300

      self.index = 0  
      self.image = self.list[int(self.index)]
      self.rect  = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    
   def animation(self):
        if self.rect.bottom ==  200:
             self.index += 0.1
             if self.index >= len(self.list): self.index = 0
             self.image = self.list[int(self.index)]
        if self.rect.bottom == 300:
             self.index += 0.05
             if self.index >= len(self.list): self.index = 0
             self.image = self.list[int(self.index)]
   def update(self):
      self.animation()
      self.rect.x -= 5
      if self.rect.x <= -100 : self.kill()
      

def sprite_collisions():
   if pygame.sprite.spritecollide(player.sprite, enemies , True):
      enemies.empty()
      return False
   else: return True
def score():
    counter = int(pygame.time.get_ticks()/1000 - reset)
    score = font.render(('Score: ' f'{counter}'),False, 'coral')
    score_r = score.get_rect(center = (400, 65))
    screen.blit(score,score_r)
    return counter

def read_high_score():
   with open ('HighScore.txt' , 'r') as h_s:
    high_score = h_s.readline().strip()
    if high_score:
       return int(high_score)
    else: return 0 
def write_high_score(score):
   prev_score = read_high_score()
   if prev_score < score:
      with open ('HighScore.txt' , 'w') as h_s:
         h_s.write(str(score))


screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Jumpy Bean Shaped Slime : With A Helmet For No Reason')
font = pygame.font.Font('font\pixeltype.ttf', 45)


# Sky
sky1= pygame.image.load('graphics\Sky.png').convert()
sky2= pygame.image.load('graphics\Sky.png').convert()
sky_rect_1 = sky1.get_rect(topleft = (0,0))
sky_rect_2 = sky2.get_rect(topleft = (800,0))

# Ground
ground1 = pygame.image.load('graphics\ground.png').convert()
ground2 = pygame.image.load('graphics\ground.png').convert()
ground_rect_1 = ground1.get_rect(topleft = (0,300))
ground_rect_2 = ground2.get_rect(topleft = (800,300))


# Front Menu Images

p_f = pygame.image.load('graphics/player/p1_front.png')
pf_s = pygame.transform.scale2x(p_f)
pf_rect = pf_s.get_rect(center  = (390,200))

# Front Menu Text

menu1 = font.render('Welcome To',False, 'coral')
m1_r = menu1.get_rect(midtop = (388, 35))
menul1 = font.render('"Jumpy Bean Shaped Slime: With A Helmet For No Reason"',False, 'coral')
ml1_r = menu1.get_rect(midtop = (100, 70))
menu2 = font.render("Press Any Button To Begin",False, 'coral')
m2_r = menu2.get_rect(midtop = (400, 315))
menul2 = font.render("(No, Power button doesn't count.)",False, 'coral')
ml2_r = menu2.get_rect(midtop = (350, 350))

# Death Menu

d1 = font.render('Your Score Was!',False, 'coral')
d1_r = d1.get_rect(midtop = (400, 50))
d2 = font.render('Press Any Button To Play Again',False, 'coral')
d2_r = d2.get_rect(midtop = (410, 280))

# Sound
Death = pygame.mixer.Sound('music/death.mp3')
music = pygame.mixer.Sound('music/music.mp3')

music.set_volume(0.20)
Death.set_volume(0.35)


# Sprite Groups

enemies = pygame.sprite.Group()

player = pygame.sprite.GroupSingle()
player.add(Player())


# Variables And Timers

game_active = False
game_start = True
game_over = False
start_time = 0

clock = pygame.time.Clock()
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1300)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

         # Enemies Spawning (Logic)

        if game_active: 
            if event.type == obstacle_timer:
                enemies.add(Enemies(choice(['fly','snail','snail'])))

         # Game Restart (After Death)       
             
        else:
         if event.type == pygame.KEYDOWN:
              score_d = 0
              game_active = True
              game_over = False
              music.play(-1)
              reset = pygame.time.get_ticks() /1000
    
            

    if game_active:
    # (Back)Ground

     sky_rect_1.right -=1.5
     sky_rect_2.right -=1.5
     screen.blit(sky1,sky_rect_1)
     screen.blit(sky2,sky_rect_2)
     if sky_rect_1.right <= 0: sky_rect_1.right = 1600
     if sky_rect_2.right <= 0: sky_rect_2.right = 1600


     ground_rect_1.right -=2.5
     ground_rect_2.right -=2.5  
     screen.blit(ground1,ground_rect_1)
     screen.blit(ground2,ground_rect_2)
     if ground_rect_1.right <= 0: ground_rect_1.right = 1600
     if ground_rect_2.right <= 0: ground_rect_2.right = 1600

     # Death Stuff
     
     game_active = sprite_collisions()
     if game_active == False:
         game_over = True
     player.draw(screen)
     player.update()

     
     if game_over == True:
        music.stop()
        Death.play()
 

     # Enemies and Player    
         
     enemies.draw(screen)
     enemies.update()


     # Random
     
     score()
     death_score = score()

     

     

    else:
     
     # Reset and Death Screen display

     sky_rect_1.right = 800
     sky_rect_2.right = 1600
     ground_rect_1.right = 800
     ground_rect_2.right = 1600


     screen.blit(sky1,(0,0))
     screen.blit(ground1,(0,300))

     screen.blit(d1, d1_r)
     screen.blit(d2 , d2_r)
    if game_over == True:
         # Death Score Display

         end_score = font.render(f'{death_score}', False , 'Coral')
         end_scores = pygame.transform.rotozoom(end_score , 0 , 4)
         end_score_rect = end_scores.get_rect(center = (400,175))
         screen.blit(end_scores, end_score_rect)

         prev_score = read_high_score()
         if prev_score > death_score:
            not_broken = font.render(f'Your All Time High Is {prev_score}' , False , 'Coral')
            not_broken_rect = not_broken.get_rect(center = (400,250))
            screen.blit(not_broken , not_broken_rect)
         else:
            broken = font.render('BRAVO! You Have Broken The Record' , False , 'darkgoldenrod1')
            broken_rect = broken.get_rect(center = (410,250))
            screen.blit(broken , broken_rect)

         write_high_score(death_score)


    if game_start:
         # Starting Screen

         screen.fill('#D0F4F7')
         screen.blit(pf_s, pf_rect)
         screen.blit(menu1,m1_r)
         screen.blit(menul1,ml1_r)
         screen.blit(menu2,m2_r)
         screen.blit(menul2,ml2_r)
         
         # Game Start :)

         if event.type == pygame.KEYDOWN:
            reset = pygame.time.get_ticks()/1000
            game_active = True
            game_start = False

    # Display and Frame speed

    pygame.display.update()
    clock.tick(60)