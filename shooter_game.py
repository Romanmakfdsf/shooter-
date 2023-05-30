from random import randint
from time import sleep
from pygame import * 
#подключение музыки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (100,0,0))
font2 = font.SysFont('Arial', 36)
#название музыки
img_back = "galaxy.jpg"
img_hero = "rocket.png" 
img_bullet = "bullet.png" 
img_enemy = "ufo.png" 
 
goal = 10 # сколько монстров надо убить для победы
score = 0 # монстров подбито
lost = 0 # монстров пропущено
max_lost = 3 # наибольшее число пропущенных монстров 
 
# создание класса GameSprite
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
# создание корабля - класс наследник GameSprite
class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
# метод стрельбы
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
 
 
# класс монстров - наследник GameSprite
class Enemy(GameSprite):
   def update(self):
       self.rect.y += self.speed
       global lost

       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
 
 
# класс пуля - наследник GameSprite
class Bullet(GameSprite):
   def update(self):
       self.rect.y += self.speed
       if self.rect.y < 0:
           self.kill()
 
 

win_width = 700 # ширина окна
win_height = 500 # высота окна
display.set_caption("Shooter") # название окна
window = display.set_mode((win_width, win_height)) # создание окна
background = transform.scale(image.load(img_back), (win_width, win_height)) # установка картинки заднего фона
 

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10) # создание игрока-ракеты
 
 
monsters = sprite.Group() # создание группы монстров
for i in range(1, 6): # размещение монстров по ширине окна
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
 
 
bullets = sprite.Group() # создание группы пуль 
 
 

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
 
 
    if not finish: # если игра не закончена
        window.blit(background,(0,0)) # поставить фон в окно
        
 
 

        ship.update()
        monsters.update()
        bullets.update()
 
 
      
        ship.reset()
        monsters.draw(window) # рисование монстров в окне
        bullets.draw(window) # рисование пукль на окне

        collides = sprite.groupcollide(bullets, monsters, True, True) # если пуля и монстр столкнулись,
        #то они исчезают и группа монстргов обновляется
        for monster in collides:
            score += 1 # счетчик убитых прибавляет 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster) # добавление монстра в группу морнстров
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost: # если корабль и монстр
            #столкнулись или счетчик пропущенных больше допустимого, то игра закончилась
             # счетчик пропущенных прибавляет 1 
            monsters.update()
            window.blit(lose, (200, 200)) # установка надписи проигрыша на окне
            run = False # игра закончена 
            
        
        if score >= goal: # если число убимтых больше чем цель, то игра заканчивается
            window.blit(win,(200,200)) # установка победной надписи на окне
            run = False # игра закончена 

        text = font2.render("Счет: " + str(score), 1, (255, 255, 255)) # создание счетчика убитых монстров 
        window.blit(text, (10, 20)) # размещение счетчика на окне
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255)) # счетчик пропущенных монстров 
        window.blit(text_lose, (10, 50)) # размещение счетчика пропущенных на окне
        
        
        
 
 
        display.update()
    time.delay(50)