import pygame
import random
from os import path

width,height=400,600
player_w,player_h=50,50
enemy_w,enemy_h=30,30
missiles_w,missiles_h=5,10
explosions_small_rect=(40,40)
explosions_big_rect=(80,80)
meteors_appear_last_time=0
shoot_num=0
hit_num=0
game_page=1

pygame.init()
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("My game")
clock=pygame.time.Clock()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.transform.flip(ship,False,True)
		self.image=pygame.transform.scale(self.image,(42,36))
		self.image.set_colorkey((0,0,0))
		self.radius=21
		self.rect=self.image.get_rect()
		self.rect.centerx=width/2
		self.rect.bottom=height
		self.hp=100
		self.score=0
		self.lives=3
		self.invincible=False
		self.move_allow=True

	def update(self):
		if self.move_allow==True:
			keystate=pygame.key.get_pressed()
			if keystate[pygame.K_LEFT]:
				self.rect.x-=5
			elif keystate[pygame.K_RIGHT]:
				self.rect.x+=5
			elif keystate[pygame.K_UP]:
				self.rect.y-=5
			elif keystate[pygame.K_DOWN]:
				self.rect.y+=5

			if self.rect.x<0:
				self.rect.x=0
			elif self.rect.x>(width-player_w):
				self.rect.x=(width-player_w)
			elif self.rect.y<0:
				self.rect.y=0
			elif self.rect.y>(height-player_h):
				self.rect.y=(height-player_h)

class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=meteors_img
		self.meteor_size=random.randint(20,50)
		self.image=pygame.transform.scale(self.image,(self.meteor_size,self.meteor_size))
		self.image.set_colorkey((0,0,0))
		self.rect=self.image.get_rect()
		self.radius=self.meteor_size
		self.rect.x=random.randint(0,width-self.meteor_size)
		self.rect.bottom=0
		self.vx=random.randint(-2,2)
		self.vy=random.randint(1,3)
		self.last_time=pygame.time.get_ticks()
		self.rotate_speed=random.randint(-5,5)
		self.image_origin=self.image.copy()
		self.rotate_angle=0

	def update(self):
		now=pygame.time.get_ticks()
		self.rect.y+=self.vy
		self.rect.x+=self.vx
		if self.rect.x<=0:
			self.vx=-self.vx
		elif self.rect.x>=(width-self.meteor_size):
			self.vx=-self.vx

		if now-self.last_time>30:
			self.rotate_angle=(self.rotate_angle+self.rotate_speed)%360
			old_center=self.rect.center
			self.image=pygame.transform.rotate(self.image_origin,self.rotate_angle)
			self.rect=self.image.get_rect()
			self.rect.center=old_center
			self.last_time=now	

		if self.rect.y==height:
			self.kill()

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=enemy_img
		self.image=pygame.transform.scale(self.image,(28,24))
		self.image.set_colorkey((0,0,0))
		self.radius=24
		self.rect=self.image.get_rect()
		self.pos=random.randint(0,width-21)
		self.rect.x=self.pos
		self.rect.bottom=0 
		self.shoot_time=0

	def update(self):
		self.rect.y+=2
		now=pygame.time.get_ticks()
		if now-self.shoot_time>=2000:
			bullet=Bullet(self.rect.centerx,self.rect.bottom)
			bullets.add(bullet)
			self.shoot_time=now
		if self.rect.top>=height:
			self.kill()

class Missile(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=missiles_list[0]
		self.image=pygame.transform.scale(self.image,(7,20))
		self.image.set_colorkey((0,0,0))
		self.rect=self.image.get_rect()
		self.rect.centerx=x
		self.rect.top=y
		self.frame=0
		self.last_time=pygame.time.get_ticks()

	def update(self):
		now=pygame.time.get_ticks()
		self.rect.y-=10
		if now-self.last_time>30:
			if self.frame==len(missiles_list):
				self.frame=0
			self.image=pygame.transform.scale(missiles_list[self.frame],(7,20))
			self.image.set_colorkey((0,0,0))
			self.frame+=1
			self.last_time=now
		if self.rect.bottom==0:
			self.kill()

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((8,15))
		self.image.fill((0,0,255))
		self.image.set_colorkey((0,0,0))
		self.rect=self.image.get_rect()
		self.rect.centerx=x
		self.rect.top=y

	def update(self):
		self.rect.y+=4
		if self.rect.top>=height:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self,center,explosions_rect):
		pygame.sprite.Sprite.__init__(self)
		self.image=explosion_list[0]
		self.image=pygame.transform.scale(self.image,explosions_rect)
		self.image.set_colorkey((0,0,0))
		self.rect=self.image.get_rect()
		self.rect.center=center
		self.frame=0
		self.last_time=pygame.time.get_ticks()

	def update(self):
		now=pygame.time.get_ticks()
		if now-self.last_time>30:
			if self.frame<len(explosion_list):
				self.image=pygame.transform.scale(explosion_list[self.frame],(40,40))
				self.image.set_colorkey((0,0,0))
				self.frame+=1
				self.last_time=now
			else:
				self.kill()

def draw_text(size,content,rect):
	font_name=pygame.font.match_font('arial')
	font=pygame.font.Font(font_name,size)
	text_surface=font.render(content,True,(255,255,255))
	text_rect=text_surface.get_rect()
	text_rect.center=rect
	screen.blit(text_surface,text_rect)

def homepage():
	screen.blit(background,background_rect)
	draw_text(20,'Space Shooter!',(width/2,height/2-100))
	draw_text(15,'Press any keyboard to start',(width/2,height/2-40))
	draw_text(15,'Press Esc to exit',(width/2,height/2+20))

def game_ui():
	if player.hp<=20:
		color=(255,0,0)
	else:
		color=(0,255,0)
	pygame.draw.rect(screen,color,(12,12,player.hp,6))
	pygame.draw.rect(screen,(255,255,255),(10,10,100,10),2)
	draw_text(10,'score:{}'.format(player.score),(width/3+10,10))
	if shoot_num>0:
		draw_text(10,'shooting:{}%'.format(int(hit_num/shoot_num*100)),(width/2,10))
	live_img=pygame.transform.scale(ship,(21,18))
	live_rect=live_img.get_rect()
	live_rect.right=width-10
	for _ in range(player.lives):
		live_img.set_colorkey((0,0,0))
		screen.blit(live_img,live_rect)
		live_rect.right-=10+live_rect.width

def game_over_page():
	screen.blit(background,background_rect)
	draw_text(20,'Game over!',(width/2,height/2-100))
	draw_text(15,'Press Enter to again',(width/2,height/2-40))
	draw_text(15,'Press Esc to exit',(width/2,height/2+20))
	try:
		draw_text(15,'score:{},shooter:{}'.format(player.score,int(hit_num/shoot_num*100)),(width/2,height/2-60))
	except:
		draw_text(15,'score:{}'.format(player.score),(width/2,height/2-60))	

img_dir=path.join(path.dirname(__file__),'img')
background_dir=path.join(img_dir,'background.png')
background=pygame.image.load(background_dir).convert()
background_rect=background.get_rect()
ship_dir=path.join(img_dir,'spaceShips_002.png')
ship=pygame.image.load(ship_dir).convert()
meteors_dir=path.join(img_dir,'spaceMeteors_004.png')
meteors_img=pygame.image.load(meteors_dir).convert()
enmey_dir=path.join(img_dir,'enemy.png')
enemy_img=pygame.image.load(enmey_dir).convert()
sound_dir=path.join(path.dirname(__file__),'sound')
shoot_voice=pygame.mixer.Sound(path.join(sound_dir,'shoot.wav'))
explosion_voice=pygame.mixer.Sound(path.join(sound_dir,'explosion.wav'))

explosion_list=[]
for i in range(9):
	explosion_dir=path.join(img_dir,'regularExplosion0{}.png'.format(i))
	explosion_img=pygame.image.load(explosion_dir).convert()
	explosion_list.append(explosion_img)
missiles_list=[]
for i in range(6):
	missiles_dir=path.join(img_dir,'spaceMissiles_{}.png'.format(i))
	missiles_img=pygame.image.load(missiles_dir).convert()
	missiles_list.append(missiles_img)

player=Player()
meteors=pygame.sprite.Group()
for _ in range(5):
	meteor=Meteor()
	meteors.add(meteor)
missiles=pygame.sprite.Group()
enemys=pygame.sprite.Group()
explosions=pygame.sprite.Group()
bullets=pygame.sprite.Group()

game_over=False
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.mixer.init()
while not game_over:
	clock.tick(60)
	event_list=pygame.event.get()
	if game_page==1:
		homepage()
		for event in event_list:
			if event.type==pygame.QUIT:
				game_over=True
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_ESCAPE:
					game_over=True
				else:
					game_page=2
	if game_page==2:
		now=pygame.time.get_ticks()
		enemy_change=random.random()
		if player.hp<=0:
			player.hp=100
			player.lives-=1
			player.rect.centerx=width/2
			player.rect.top=height+100
			player.invincible=True
			player.move_allow=False
			player_invincible_last_time=now
			explosion=Explosion(hit.rect.center,explosions_big_rect)
			explosions.add(explosion)
			explosion_voice.play()
			if player.lives==0:
				game_page=3
		if enemy_change>=0.985:
			enemy=Enemy()
			enemys.add(enemy)
		if now-meteors_appear_last_time>800:
			meteor=Meteor()
			meteors.add(meteor)
			meteors_appear_last_time=now
		if player.invincible==True:
			if now-player_invincible_last_time>=2000 and player.move_allow==False:
				player.rect.centerx=width/2
				player.rect.bottom=height
				player.move_allow=True
			if now-player_invincible_last_time>=5000:
				player.invincible=False
		for event in event_list:
			if event.type==pygame.QUIT:
				game_over=True
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_SPACE:
					if player.move_allow==True:
						missile=Missile(player.rect.centerx,player.rect.top)
						missiles.add(missile)
						shoot_num+=1
						shoot_voice.play()
				if event.key==pygame.K_ESCAPE:
					game_over=True

		player.update()
		meteors.update()
		missiles.update()
		enemys.update()
		bullets.update()
		explosions.update()

		player_hit=pygame.sprite.spritecollide(player,meteors,True,pygame.sprite.collide_circle)
		for hit in player_hit:
			if player.invincible==False:
				player.hp-=hit.radius/1.5
				explosion=Explosion(hit.rect.center,explosions_small_rect)
				explosions.add(explosion)
				explosion_voice.play()
		meteor_hit=pygame.sprite.groupcollide(meteors,missiles,True,True)
		for hit in meteor_hit:
			hit_num+=1
			player.score+=int((60-hit.radius)/5)
			explosion=Explosion(hit.rect.center,explosions_small_rect)
			explosions.add(explosion)
			explosion_voice.play()
		enemy_hit=pygame.sprite.spritecollide(player,enemys,True,pygame.sprite.collide_circle)
		for hit in enemy_hit:
			if player.invincible==False:
				player.hp-=hit.radius*1.5
				explosion=Explosion(hit.rect.center,explosions_small_rect)
				explosions.add(explosion)
				explosion_voice.play()
		enemy_be_hit=pygame.sprite.groupcollide(missiles,enemys,True,True)
		for hit in enemy_be_hit:
			hit_num+=1
			player.score+=10
			explosion=Explosion(hit.rect.center,explosions_small_rect)
			explosions.add(explosion)
			explosion_voice.play()	
		bullet_be_hit=pygame.sprite.groupcollide(missiles,bullets,True,True)
		for hit in bullet_be_hit:
			hit_num+=1
		bullet_hit=pygame.sprite.spritecollide(player,bullets,True,pygame.sprite.collide_circle)
		for hit in bullet_hit:
			if player.invincible==False:
				player.hp-=15
				explosion=Explosion(hit.rect.center,explosions_small_rect)
				explosions.add(explosion)
				explosion_voice.play()
		
		screen.blit(background,background_rect)
		screen.blit(player.image,player.rect)
		meteors.draw(screen)
		enemys.draw(screen)
		bullets.draw(screen)
		missiles.draw(screen)
		explosions.draw(screen)
		game_ui()
	if game_page==3:
		game_over_page()
		for event in event_list:
			if event.type==pygame.QUIT:
				game_over=True
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_ESCAPE:
					game_over=True
				elif event.key==pygame.K_RETURN:
					game_page=2
					player.kill()
					player=Player()
					shoot_num=0
					hit_num=0
					for meteor in meteors:
						meteor.kill()
					for bullet in bullets:
						bullet.kill()
					for enemy in enemys:
						enemy.kill()
					for _ in range(5):
						meteor=Meteor()
						meteors.add(meteor)

	pygame.display.flip()