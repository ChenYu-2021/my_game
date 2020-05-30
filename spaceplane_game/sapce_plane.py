from __future__ import division
import pygame
from pygame.locals import *
import random
import codecs
from os import path  #用于获取文件的属性


##  1.先进入游戏画面把左右上下移动效果做出来
##  2.将玩家的飞机画出并进行上线移动


##  对游戏进行修改


#获取图像文件以及声音文件
img_dir = path.join(path.dirname(__file__),'image')
sound_dir = path.join(path.dirname(__file__),'sounds')

#############################
#参数初始化
WIDTH = 1000
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 10

#颜色定义
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255.255,0)
#############################

#############################
#游戏初始化并创建窗口
pygame.init()
pygame.mixer.init()  #for sound

#创建一个游戏窗口
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Space Shooter')  #窗口命名
clock = pygame.time.Clock() # for Syncing the FPS
#############################
font_name = pygame.font.match_font('arial')  #get the match font nane 获得游戏字体的类型

def mian_menu():
    global screen  # 全局屏幕对象
    #加载游戏界面音乐
    menu_song = pygame.mixer.music.load(path.join(sound_dir,"start_game.ogg"))   #加载菜单音乐
    pygame.mixer.music.play(-1)  #循环播放

    #加载主菜单图片
    title = pygame.image.load(path.join(img_dir,"main.png")).convert_alpha()
    title = pygame.transform.scale(title,(WIDTH,HEIGHT),screen)  #因为创建的窗口和图片的大小不一致， 要将图片的大小调到根窗口一样的分辨率
    screen.blit(title,(0,0))
    pygame.display.update()
    #事件处理以及游戏开始界面显示设置
    while True:
        event = pygame.event.poll()  #从队列中获得事件，返回的是EventType
        if event.type == pygame.KEYDOWN:  #当有按键按下时
                if event.key == pygame.K_RETURN:  #后退键按下
                    break
                if event.key == pygame.K_KP_ENTER:  #按下enter按键，则退出menu，进入准备开始界面
                    continue
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        elif event.type == pygame.QUIT:  #当按下Esc键时直接退出
                pygame.quit()
                quit()

        #若没有按出退出键，则显示进入游戏的text
        else:
            draw_text(screen,"Press [Enter] To Begin",30,WIDTH/2,HEIGHT/2)
            draw_text(screen,"or [Q] To Quit",30,WIDTH/2,HEIGHT/2 + 40)
            pygame.display.update()



    #进入准备开始游戏界面并播放对应的音频
    getready_music = pygame.mixer.Sound(path.join(sound_dir,"getready.ogg"))
    getready_music.play()
    #将屏幕变黑
    screen.fill(BLACK)
    draw_text(screen,"GET READY!",30,WIDTH/2,HEIGHT/2)
    pygame.display.update()


#选择字体来显示游戏界面
def draw_text(surface,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)    # draw text on a new Surface
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface,text_rect)
#显示汉字
def draw_chinese(surface,text,size,x,y):
    xtfont = pygame.font.SysFont('SimHei',size)
    text_surface = xtfont.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface,text_rect)

# 写入txt
def write_score_txt(text,way,path):
    f = codecs.open(path,way,'utf8')
    f.write(str(text))
    f.close()

# 读出txt
def read_score_txt(path):
    with open(path,'r',encoding='utf8')  as f:
        lines = f.readlines()
        return lines



#显示血条
def draw_shield_bar(surface,x,y,pct):
    pct = max(pct,0)
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)   #Rect()四个参数为left, top, width, height
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surface,GREEN,fill_rect)   #画出血条，颜色为绿色
    pygame.draw.rect(surface,WHITE,outline_rect,2)  #画出没有血时的血条

#显示boss的血条
def draw_boss_shield_bar(surface,x,y,pct):
    pct = max(pct,0)
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)   #Rect()四个参数为left, top, width, height
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surface,RED,fill_rect)   #画出血条，颜色为绿色
    pygame.draw.rect(surface,WHITE,outline_rect,2)  #画出没有血时的血条

#显示生命lives
def draw_lives(surface,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surface.blit(img,img_rect)


def newmob():
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)
def newenemy():
    enemy = Enemy()
    #enemy_bullet = Enemy_bullet(enemy.rect.centerx,enemy.rect.top)
    all_sprites.add(enemy)
    enemies.add(enemy)

    #all_sprites.add(enemy_bullet)
    #enemies_bullet.add(enemy)

#############################

#############################
#类的定义
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()  #以毫秒为单位获取时间
        self.frame_rate = 75  #帧率

    def update(self):
        now = pygame.time.get_ticks()  #获取时间，毫秒为单位
        if now - self.last_update >= self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill() #remove the Sprite from all Groups

            else:   #在爆炸的时候图片的中心不变
                old_center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = old_center

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery  = 0
        self.speedx = 0
        self.speedy = 0
        self.boss_shield = 100
        self.boss_last_shoot = pygame.time.get_ticks()
        self.boss_shoot_delay = 500
        self.move_delay = 300
        self.move_time = pygame.time.get_ticks()
    def update(self):
        self.speedx = 0
        self.speedy = 0
        now = pygame.time.get_ticks()
        if now - self.move_time > self.move_delay:
            self.move_time = now
            self.speedx = random.randrange(-25,25)
            self.speedy = random.randrange(-15,15)
            self.rect.x += self.speedx
            self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT / 2:
            self.rect.bottom = HEIGHT / 2

        self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.boss_last_shoot > self.boss_shoot_delay:
            self.boss_last_shoot = now
            boss_bullet = Boss_bullet(self.rect.centerx,self.rect.bottom)
            boss_bullets.add(boss_bullet)
            all_sprites.add(boss_bullet)

#Define the Player
class Player(pygame.sprite.Sprite):
    def __init__(self):   #初始化玩家飞机的各个参数
        pygame.sprite.Sprite.__init__(self)
        ## scale the player img down
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.hero = False
        self.rockt_timer = pygame.time.get_ticks()
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()
        self.paused = False
        self.flag = 0
        self.transport = 0
    def update(self):
        ## time out for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power -= 1
            self.power_timer = pygame.time.get_ticks()
        if self.hero == True:
            self. image = pygame.transform.scale(hero_image,(60,48))
        ## unhide
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.speedx = 0
        self.speedy = 0
        ## makes the player static in the screen by default.
        # then we have to check whether there is an event hanlding being done for the arrow keys being
        ## pressed

        ## will give back a list of the keys which happen to be pressed down at that moment
        keystate = pygame.key.get_pressed()  # get the state of all keyboard buttons
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx -= 5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx += 5
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speedy -= 5
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speedy += 5
        if keystate[K_p] and self.flag == 0:
            self.flag = 1
            self.game_paused()
        # Fire weapons by holding spacebar
        bottons = pygame.mouse.get_pressed()
        if bottons[0]: #0：鼠标左键；1：中间被按下；2：鼠标右键被按下
            self.shoot()


        ## check for the borders at the left and right
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        self.rect.x += self.speedx
        self.rect.y += self.speedy
    # game paused
    def game_paused(self):
        self.paused = True
        while self.paused:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        quit()
                    if event.key == K_p and self.flag ==1:
                        self.paused = False
            draw_text(screen,str('Paused'),30,WIDTH / 2,HEIGHT / 2)
            pygame.display.update()

    #shoot weapoons
    def shoot(self):
        #to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_music.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_music.play()
            if self.power == 3:
                bullet1 = BulletLeft(self.rect.left, self.rect.centery)
                bullet2 = BulletRight(self.rect.right, self.rect.centery)
                bullet3 = Missile(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_music.play()
                # missile_music.play()
            if self.power >= 4:
                bullet1 = Missile1(self.rect.centerx, self.rect.top)
                bullet2 = BulletLeft(self.rect.left, self.rect.centery)
                bullet3 = BulletRight(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_music.play()
                # missile_music.play()
    #transfrom player
    def transfrom(self):
        if self.hero:
            self.image = hero_image

    def playerup(self):
        self.hero = True

    def powerup(self):
        self.power += 1
        self.power_timer = pygame.time.get_ticks()  #重新计时

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2,HEIGHT + 200)


# boss的子弹
class Boss_bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_bullet_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()

#子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img  #导入子弹图
        self.image.set_colorkey(BLACK)  #将图片的黑色部分设置为透明色
        self.rect = self.image.get_rect()  #得到图片的大小
        ## place the bullet according to the current position of the player
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        if player.hero == True:
            self.image = hero_bullet_image1
    def update(self):
        #在player前面产生子弹
        self.rect.y += self.speedy
        #若子弹飞出屏幕外就从sprite类中删除它
        if self.rect.bottom < 0:
            self.kill()

class BulletLeft(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = hero_bullet_imageleft  #导入子弹图
        self.image.set_colorkey(BLACK)  #将图片的黑色部分设置为透明色
        self.rect = self.image.get_rect()  #得到图片的大小
        ## place the bullet according to the current position of the player
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = -10
    def update(self):
        #在player前面产生子弹
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #若子弹飞出屏幕外就从sprite类中删除它
        if self.rect.bottom < 0:
            self.kill()

class BulletRight(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = hero_bullet_imageright  #导入子弹图
        self.image.set_colorkey(BLACK)  #将图片的黑色部分设置为透明色
        self.rect = self.image.get_rect()  #得到图片的大小
        ## place the bullet according to the current position of the player
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx =  10
    def update(self):
        #在player前面产生子弹
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #若子弹飞出屏幕外就从sprite类中删除它
        if self.rect.bottom < 0:
            self.kill()
#导弹类
class Missile(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir,'missile.png'))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #导弹出现的位置
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
class Missile1(pygame.sprite.Sprite):   #power=4时发射的子弹
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir,'hero_bullet4.png'))
        if player.hero == True:
            self.image = hero_bullet_image2
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #导弹出现的位置
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
#Define the enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_enemy_orig = random.choice(enemy_images)
        self.image_enemy_orig.set_colorkey(BLACK)
        self.image = self.image_enemy_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speedy = random.randrange(4,8)
        self.speedx = random.randrange(-2,2)
        self.enemy_shoot = pygame.time.get_ticks()
        self.enemy_shoot_delay = 700
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-50)
            self.speedy = random.randrange(1,8)
        enemy_now = pygame.time.get_ticks()
        if enemy_now - self.enemy_shoot > self.enemy_shoot_delay:
            self.enemy_shoot = enemy_now
            enemy_bullet = Enemy_bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(enemy_bullet)
            enemies_bullet.add(enemy_bullet)
#Define the enemy bullet
class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.randrange(0,4)
        self.image = enemy_bullet_images[self.type]
        self.image.set_colorkey(BLACK)  # 设置图片黑色部分透明
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = random.randrange(2,5)  #子弹的速度
    def update(self):
        self.rect.y += self.speedy
        if self.speedy >= HEIGHT:
            self.kill()
#defines the Mob
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)
        ##将流星的横坐标微调
        self.speedx = random.randrange(-3,3)
        ##对流星添加旋转效果
        self.rotation = 0
        self.rotation_speed = random.randrange(-8,8)
        self.last_update_time = pygame.time.get_ticks()  ## time when the rotation has to happen

    #rotation 旋转
    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update_time > 50: ##in millisenconds毫秒
            self.last_update_time = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360  #旋转角度
            new_image = pygame.transform.rotate(self.image_orig,self.rotation)  #旋转后的新图片
            ##在旋转中保持中心不变
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    #update 更新
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #若流星们离开屏幕后，重新回到屏幕的上方
        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-50)
            self.speedy = random.randrange(1,8)
#define the sprite of playerups  暂时只有一个，所以type是直接赋值
class Playerup(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'transfrom'
        self.image = player_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
#define the sprite of Powerups  产生子弹升级的图案
class Powerup(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ##place the bullet according to the position of player
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        ##kill the sprite after it moves over the top border
        if self.rect.top > HEIGHT:
            self.kill()




##########################################################
#导入音乐
shoot_music = pygame.mixer.Sound(path.join(sound_dir,'pew.wav'))
explosion_music = []
for sound in ['expl3.wav','expl6.wav']:
    explosion_music.append(pygame.mixer.Sound(path.join(sound_dir,sound)))
player_die_music = pygame.mixer.Sound(path.join(sound_dir,'rumble1.ogg'))
power_up_music = pygame.mixer.Sound(path.join(sound_dir,'pickup.ogg'))
player_up_music = pygame.mixer.Sound(path.join(sound_dir,'powerup.ogg'))
game_over_music = pygame.mixer.Sound(path.join(sound_dir,'game_over.ogg'))
game_won_music = pygame.mixer.Sound(path.join(sound_dir,'game_won.ogg'))
#导入所有图片
#背景图片
bg_images = []
bg_images_list = [
    'bg0.jpg',
    'bg1.jpg',
    'bg2.jpg',
    'bg3.jpg'
]
for bg_image in bg_images_list:
    bg_images.append(pygame.image.load(path.join(img_dir,bg_image)))

background = pygame.image.load(path.join(img_dir,'starfield.png'))
background = pygame.transform.scale(background,(WIDTH,HEIGHT))
background_rect = background.get_rect()
#游戏结束背景图
game_over_image = pygame.image.load(path.join(img_dir,'title.jpg'))
game_over_image = pygame.transform.scale(game_over_image,(WIDTH,HEIGHT))
game_over_image_rect = game_over_image.get_rect()

#玩家的图片
player_img = pygame.image.load(path.join(img_dir,'playerShip1_orange.png')).convert()
player_live_img = pygame.transform.scale(player_img,(25,20))
#将图片对象的黑色部分设置为透明
player_live_img.set_colorkey(BLACK)
hero_image = pygame.image.load(path.join(img_dir,'hero.png')).convert_alpha()

# Boss的图片
boss_image = pygame.image.load(path.join(img_dir,'boss.png'))

#子弹的图片
bullet_img = pygame.image.load(path.join(img_dir,'laserRed16.png')).convert_alpha()
bullet_img1 = pygame.image.load(path.join(img_dir,'hero_bullet4.png')).convert_alpha()
hero_bullet_image1 = pygame.image.load(path.join(img_dir,'bullet1.png')).convert_alpha()
hero_bullet_imageleft = pygame.image.load(path.join(img_dir,'bullet4l.png')).convert_alpha()
hero_bullet_imageright = pygame.image.load(path.join(img_dir,'bullet4r.png')).convert_alpha()
hero_bullet_image2 = pygame.image.load(path.join(img_dir,'bullet2.png')).convert_alpha()
#enemy_bullet_image = pygame.image.load(path.join(img_dir,'enemy_bullet_image.png')).convert_alpha()
boss_bullet_image = pygame.image.load(path.join(img_dir,'boss_bullet.png')).convert_alpha()

# enemies bullets
enemy_bullet_images = []
enemy_bullet_list = [
    'enemy_bullet0.png',
    'enemy_bullet1.png',
    'enemy_bullet2.png',
    'enemy_bullet3.png',
]

for enemy_bullet_image in enemy_bullet_list:
    enemy_bullet_images.append(pygame.image.load(path.join(img_dir,enemy_bullet_image)))

#敌机的所有图片
enemy_images = []
enemy_list = [
    'enemy0.png',
    'enemy1.png',
    'enemy2.png',
    'enemy3.png',
]
for enemy_image in enemy_list:
    enemy_images.append(pygame.image.load(path.join(img_dir,enemy_image)).convert_alpha())
#流星的图片
meteor_images = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png',
    'meteorBrown_med1.png',
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png',
]
for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,image)).convert())
#爆炸动画 meteor explosion
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['enemy'] = []
explosion_anim['player'] = []
explosion_anim['boss'] = []
for i in range(9):  #i从0到8
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    #resize the explosion重新设置分辨率
    img_lg = pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img,(30,30))
    explosion_anim['sm'].append(img_sm)

    #player expolsion
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
#敌机被击中后爆炸的效果
for j in range(4):
    filename = 'enemy_down{}.png'.format(j)
    img_enemy = pygame.image.load(path.join(img_dir,filename)).convert_alpha()
    img_enemy.set_colorkey(BLACK)
    explosion_anim['enemy'].append(img_enemy)

# boss被击落后的效果
for k in range(1,7):
    filename = 'boom0{}.png'.format(k)
    img_boss = pygame.image.load(path.join(img_dir,filename)).convert_alpha()
    img_boss.set_colorkey(BLACK)
    explosion_anim['boss'].append(img_boss)

#load powerup images
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir,'hero_blood.png')).convert_alpha()
#powerup_images['transfrom'] = pygame.image.load(path.join(img_dir,'supply1.png')).convert_alpha()
powerup_images['gun'] = pygame.image.load(path.join(img_dir,'metro_supply.png')).convert()
#load playerup images
player_images = {}
player_images['transfrom'] = pygame.image.load(path.join(img_dir,'supply1.png')).convert_alpha()
##########################################################

##########################################################
running = True
menu_display = True
game_over = False
boss_come_flag = True
boss_shield_bar_flag = False
bg_select = random.randrange(0,4)
while running:
    if menu_display:
        mian_menu()
        pygame.time.wait(3000)

        # stop menu_music
        pygame.mixer.music.stop()
        # play gameplay music
        pygame.mixer.music.load(path.join(sound_dir, 'my_music.mp3'))
        pygame.mixer.music.play(-1)

        menu_display = False
        score = 0
        # 创建所有的sprite类的类群
        all_sprites = pygame.sprite.Group()
        # group for player
        player = Player()
        boss = Boss()
        all_sprites.add(player)
        # group for Bullet
        bullets = pygame.sprite.Group()
        enemies_bullet = pygame.sprite.Group()
        boss_bullets = pygame.sprite.Group()
        # group for up
        powerups = pygame.sprite.Group()
        playerups = pygame.sprite.Group()
        # group for mob
        mobs = pygame.sprite.Group()
        for i in range(5):
            newmob()
        enemies = pygame.sprite.Group()
        for j in range(5):
            newenemy()

    # 每隔FPS毫秒检查一次是否可以退出游戏
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ## Press ESC to exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    # call the update method of every member sprite(调用每个成员的更新方法，即是调用Player类中update()方法)
    all_sprites.update()
    # Boss Coming
    if score > 1000 and boss_come_flag:
        #all_sprites.remove(mobs)
        boss_come_flag = False
        boss_shield_bar_flag = True
        boss.boss_shield = 100
        #draw_boss_shield_bar(screen,WIDTH / 2,5,boss.boss_shield)
        all_sprites.add(boss)

    ## check if a boss_bullet hit player
    hits = pygame.sprite.spritecollide(player,boss_bullets,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 10
        if player.shield <= 0:
            player_die_music.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hero = False
            player.image = pygame.transform.scale(player_img, (60, 48))
            player.image.set_colorkey(BLACK)
            player.paused = False
            player.flag = 0
            player.hide()
            player.lives -= 1
            player.shield = 100

    ## check if a bullet hit boss
    hits = pygame.sprite.spritecollide(boss,bullets,True,pygame.sprite.collide_circle)
    for hit in hits:
        boss.boss_shield -= 2
        if boss.boss_shield <= 0:
            boss_death = Explosion(boss.rect.center,'boss')
            all_sprites.add(boss_death)
            boss.kill()
            all_sprites.remove(enemies)
            all_sprites.remove(enemies_bullet)
            all_sprites.remove(boss)
            all_sprites.remove(bullets)
            #player.game_paused()


    ## check if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)  # detect collision between a group and another group
    for hit in hits:
        score += 50 - hit.radius  # 击中流星大小不同的加不同的分数
        random.choice(explosion_music).play()
        explosion1 = Explosion(hit.rect.center, 'lg')
        all_sprites.add(explosion1)  # 加入到all_sprites中，以便在循环中用draw函数画出all_sprites里面所有图片
        # 以一定的概率产生火力升级图案
        if random.random() > 0.5:
            powerup = Powerup(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)
        # 重新产生一个流星
        newmob()
    # check if a bullet hit a enemy
    hits = pygame.sprite.groupcollide(enemies,bullets,True,True)
    for hit in hits:
        score += random.randrange(50,100)
        random.choice(explosion_music).play()
        explosion3 = Explosion(hit.rect.center,'enemy')
        all_sprites.add(explosion3)
        if random.random() > 0.8:
            playerup = Playerup(hit.rect.center)
            all_sprites.add(playerup)
            playerups.add(playerup)
        newenemy()
    ## check if the player collides with the enemy
    hits = pygame.sprite.spritecollide(player, enemies, True,pygame.sprite.collide_circle)  ##          gives back a list, True makes the mob element disappear
    for hit in hits:
        player.shield -= random.randrange(5,10)
        explosion4 = Explosion(hit.rect.center, 'enemy')
        all_sprites.add(explosion4)
        newenemy()
        if player.shield <= 0:
            player_die_music.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hero = False
            player.image = pygame.transform.scale(player_img, (60, 48))
            player.image.set_colorkey(BLACK)
            player.paused = False
            player.flag = 0
            player.hide()
            player.lives -= 1
            player.shield = 100

    ## check if the player collides with the enemies_bullet
    hits = pygame.sprite.spritecollide(player,enemies_bullet,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 10
        if player.shield <= 0:
            player_die_music.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hero = False
            player.image = pygame.transform.scale(player_img, (60, 48))
            player.image.set_colorkey(BLACK)
            player.paused = False
            player.flag = 0
            player.hide()
            player.lives -= 1
            player.shield = 100
    ## check if the player collides with the mob ，错误已经发现，在后面显示还有几条命的时候重新初始化了飞机的类，所以导致飞机的位置被固定
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)  ##          gives back a list, True makes the mob element disappear
    for hit in hits:
        player.shield -= hit.radius * 2
        explosion2 = Explosion(hit.rect.center, 'sm')
        all_sprites.add(explosion2)
        newmob()
        if player.shield <= 0:
            player_die_music.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hero = False
            player.image = pygame.transform.scale(player_img,(60,48))
            player.image.set_colorkey(BLACK)
            player.paused = False
            player.flag = 0
           # player.power = 1
            # running = False     ## GAME OVER 3:D
            player.hide()
            player.lives -= 1
            player.shield = 100

    ## if the player hit a palyerup
    hits = pygame.sprite.spritecollide(player,playerups,True)
    for hit in hits:
        if hit.type == 'transfrom':
            player_up_music.play()
            player.transport += 1
            if player.transport == 2:
                player.transport = 0
                player.playerup()

    ## if the player hit a power up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            power_up_music.play()
    ## 法式嘲笑
    if player.lives == 0 and not death_explosion.alive():
        pygame.mixer.music.load(path.join(sound_dir, 'game_over.mp3'))
        pygame.mixer.music.play(1)
        game_over_music.play()
        game_over = True
        while game_over:
            screen.fill(BLACK)
            screen.blit(game_over_image,game_over_image_rect)
            draw_text(screen, str('RestartGame'), 48, WIDTH / 2, HEIGHT / 2 )
            draw_text(screen,str('You have been slayed!! '),48,WIDTH / 2,HEIGHT / 2 + 50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                #点击重新开始，将游戏结束标志反转
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if WIDTH / 2 - 60 <= event.pos[0] \
                        and event.pos[0] <= WIDTH / 2 + 60 \
                        and HEIGHT / 2 - 60 <= event.pos[1] \
                        and event.pos[1] <= HEIGHT / 2 + 60:
                        #关闭当前音乐，播放游戏音乐
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(path.join(sound_dir, 'my_music.mp3'))
                        pygame.mixer.music.play(-1)
                        running = True  #进入游戏
                        game_over = False  #游戏结束标志清零
                        player.hero = False
                        player.lives = 3  #重新定义多少条命
                        player.power = 1
            pygame.display.flip()

        #running = False
    # Draw play screen
    bg = bg_images[bg_select]
    bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))
    bg_rect = bg.get_rect()
    screen.fill(BLACK)
    screen.blit(bg,bg_rect)
    #screen.blit(background, background_rect)
    # Draw player
    all_sprites.draw(screen)
    # 绘制分数显示
    #draw_text(screen, str('Paused'), 30, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    # 绘制血条显示
    # player = Player()   #错误出现在这，因为重新定义了player，所以飞机的位置也被初始化了
    draw_shield_bar(screen, 5, 5, player.shield)
    if boss_shield_bar_flag:
        draw_text(screen,str('Boss:'),18,WIDTH -320,5)
        draw_boss_shield_bar(screen, WIDTH - 300 ,6, boss.boss_shield)
    # 画出玩家有几条命
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_live_img)

    if boss.boss_shield <= 0:
        pygame.mixer.music.stop()
        game_won_music.play()
        all_sprites.empty()
        screen.fill(BLACK)
        screen.blit(game_over_image, game_over_image_rect)
        draw_text(screen, str('You Win'), 50, WIDTH / 2, HEIGHT / 2)
        #draw_text(screen,str('Ranking'),50,WIDTH / 2,HEIGHT / 2 + 50)
        pygame.display.flip()  #Update the full display Surface to the screen

    pygame.display.flip()
##########################################################

