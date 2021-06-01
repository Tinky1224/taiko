import pygame
from os import getcwd, path, listdir
from tja_to_time import tja_to_time



def main_game(song_name):
    def music_load(file_name:str):
        pygame.mixer.music.load(file_name)
    
    def time_to_x(time_list:list,scroll_list:str):
        init_pos = 266
        pos_list = []
        for i in range(len(time_list),0,-1):
            x = init_pos + (time_list[i-1]+3) * 8 * float(scroll_list[i-1]) * 100  #8:move length per sec
            pos_list.append(x)
        return pos_list

    def draw_note(note_list,pos_list,time_list, scroll_list):
        for i in range(len(time_list),0,-1):
            if note_list[i-1] == '1':
                image = small_don_img
            elif note_list[i-1] == '2':
                image = small_ka_img
            elif note_list[i-1] == '3':
                image = big_don_img
            elif note_list[i-1] == '4':
                image = big_ka_img
            elif note_list[i-1] == '5':
                continue
    #            image = small_da_img 
            elif note_list[i-1] == '6':
                continue
    #            image = big_da_img
            elif note_list[i-1] == '7':
                continue
            elif note_list[i-1] == '8':
                continue #skip
            elif note_list[i-1] == '9':
                continue
            x = pos_list[-i]
            t = time_list[i-1] +3
            scroll = float(scroll_list[i-1])
            note_score = 1200000 // len(note_list) +1
            note = Note(image,x,t,note_list[i-1],note_score,scroll)
            note_sprites.add(note)
        
    def draw_Acc(img):
        acc = Acc(img)
        acc_sprites.add(acc)
        acc = Acc(img)
        acc_sprites.add(acc)
        acc = Acc(img)
        acc_sprites.add(acc)

    def draw_Explosion(Acc):
        explosion = Note_Explosion(Acc)
        note_explosion_sprites.add(explosion)

    class Note(pygame.sprite.Sprite): 
        def __init__(self,image,x,t,img_type,note_score,scroll):
            super().__init__()
            self.score = note_score
            self.img_type = img_type
            self.image = image
            self.t = t
            self.x = x #click center = 266
            self.y = 310
            self.scroll = scroll
            self.rect = self.image.get_rect()
            self.rect.center = (self.x,self.y)
        def update(self,t,player):
            self.x -= 8 * self.scroll * t /10
            if self.x < 0 :
                self.kill()
                player.combo = 0
                player.bad += 1
            self.rect.center = (self.x,self.y)
        def hit_don(self,player,hit_time):
            if abs(hit_time - self.t) < 0.06:
                self.kill()
                draw_Explosion(0)
                draw_Acc(perfect_img)
                player.score += self.score
                player.combo += 1
                player.perfect += 1
            elif 0.06 < abs(hit_time - self.t) < 0.14:
                self.kill()
                draw_Explosion(1)
                draw_Acc(good_img)
                player.score += self.score//2
                player.combo += 1
                player.good += 1
            elif 0.14 < abs(hit_time - self.t) < 0.2:
                self.kill()
                draw_Acc(bad_img)
                player.combo = 0
                player.bad += 1
        def hit_ka(self,player,hit_time):
            if abs(hit_time - self.t) < 0.06:
                self.kill()
                draw_Explosion(0)
                draw_Acc(perfect_img)
                player.score += self.score
                player.combo += 1
                player.perfect += 1
            elif 0.06 < abs(hit_time - self.t) < 0.14:
                self.kill()
                draw_Explosion(1)
                draw_Acc(good_img)
                player.score += self.score//2
                player.combo += 1
                player.good += 1
            elif 0.14 < abs(hit_time - self.t) < 0.2:
                self.kill()
                draw_Acc(bad_img)
                player.combo = 0
                player.bad += 1
    
    class Acc(pygame.sprite.Sprite):
        def __init__(self,img):
            super().__init__()
            self.image = img
            self.x = 265
            self.y = 230
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
        def update(self):
            if self.y < 190:
                self.kill()
            self.y -= 8
            self.rect.center = (self.x, self.y)
    
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.combo = 0
            self.score = 0
            self.perfect = 0
            self.good = 0
            self.bad = 0
            self.max_combo = 0
        def update(self):
            if self.combo > self.max_combo :
                self.max_combo = self.combo

    class Note_Explosion(pygame.sprite.Sprite):
        def __init__(self,Acc):
            super().__init__()
            self.ogimage = note_explosion_img
            self.image = self.ogimage
            self.len = 222
            self.y = [0,222,444,666,888]
            self.x = Acc * 222
            self.pos = 0
            self.rect = self.image.get_rect()
            self.rect.center = (153,200)
        def update(self):
            if self.pos >= 5:
                self.kill()
            else :
                self.image = self.ogimage.subsurface(pygame.Rect(self.x,self.y[self.pos],self.len,self.len))
                self.rect = self.image.get_rect()
                self.rect.center = (264,311)
                self.pos += 1

    WIDTH = 1280
    HEIGHT = 800
    FPS = 60
    
    # define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (255,0,255)
    GRAY = (100,100,100)
    
    # initialize pygame and create window
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.7)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MUSIC!!")
    pygame.key.set_repeat(0)
    clock = pygame.time.Clock()
    
    # set up asset folders
    game_folder = getcwd()
    image_folder = path.join(game_folder,'img')
    music_folder = path.join(game_folder,'music')
    font_folder = path.join(game_folder,'font')
    audio_folder = path.join(game_folder,'audio')
    
    song_list = [i[:-4] for i in listdir(music_folder) if i.endswith('.ogg')]
    
    #my_font = pygame.font.SysFont("arial", 25)
    my_font = pygame.font.Font(path.join(font_folder,'TnT.ttf'), 25)
    small_don_img = pygame.image.load(path.join(image_folder,'small_don.jpg')).convert()
    small_don_img = pygame.transform.scale(small_don_img,(260,160))
    small_ka_img = pygame.image.load(path.join(image_folder,'small_ka.jpg')).convert()
    small_ka_img = pygame.transform.scale(small_ka_img,(260,160))
    big_don_img = pygame.image.load(path.join(image_folder,'big_don.jpg')).convert()
    big_don_img = pygame.transform.scale(big_don_img,(260,160))
    big_ka_img = pygame.image.load(path.join(image_folder,'big_ka.jpg')).convert()
    big_ka_img = pygame.transform.scale(big_ka_img,(260,160))
    small_da_img = pygame.image.load(path.join(image_folder,'small_da.jpg')).convert()
    small_da_img = pygame.transform.scale(small_da_img,(260,160))
    big_da_img = pygame.image.load(path.join(image_folder,'big_da.jpg')).convert()
    big_da_img = pygame.transform.scale(big_da_img,(260,160))
    background_img = pygame.image.load(path.join(image_folder,'background.jpg')).convert()
    background_img = pygame.transform.scale(background_img,(1280,800))
    perfect_img = pygame.image.load(path.join(image_folder,'perfect.jpg')).convert()
    perfect_img = pygame.transform.scale(perfect_img,(80,100))
    good_img = pygame.image.load(path.join(image_folder,'good.jpg')).convert()
    good_img = pygame.transform.scale(good_img,(80,100))
    bad_img = pygame.image.load(path.join(image_folder,'bad.jpg')).convert()
    bad_img = pygame.transform.scale(bad_img,(80,200))
    note_explosion_img = pygame.image.load(path.join(image_folder,'notes_explosion.jpg')).convert()
    colorkey = small_don_img.get_at((0,0))
    small_don_img.set_colorkey(colorkey, pygame.RLEACCEL)
    colorkey = small_ka_img.get_at((0,0))
    small_ka_img.set_colorkey(colorkey, pygame.RLEACCEL)
    colorkey = big_don_img.get_at((0,0))
    big_don_img.set_colorkey(colorkey, pygame.RLEACCEL)
    colorkey = big_ka_img.get_at((0,0))
    big_ka_img.set_colorkey(colorkey, pygame.RLEACCEL)
    colorkey = small_da_img.get_at((0,0))
    small_da_img.set_colorkey(colorkey, pygame.RLEACCEL)
    colorkey = big_da_img.get_at((0,0))
    big_da_img.set_colorkey(colorkey, pygame.RLEACCEL)
    colorkey = perfect_img.get_at((0,0))
    perfect_img.set_colorkey(colorkey, pygame.RLEACCEL)
    colorkey = good_img.get_at((0,0))
    good_img.set_colorkey(colorkey, pygame.RLEACCEL)
    colorkey = bad_img.get_at((0,0))
    bad_img.set_colorkey(colorkey, pygame.RLEACCEL)
    colorkey = note_explosion_img.get_at((0,0))
    note_explosion_img.set_colorkey(colorkey, pygame.RLEACCEL)

    don_sound = pygame.mixer.Sound(path.join(audio_folder,'se_don.ogg'))
    don_sound.set_volume(1.4)
    ka_sound = pygame.mixer.Sound(path.join(audio_folder,'se_ka.ogg'))
    ka_sound.set_volume(1.4)
    
    #define sprite
            
    note_sprites = pygame.sprite.Group()
    acc_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()
    note_explosion_sprites = pygame.sprite.Group()
    
    # Game loop
    running = True
    gaming = True
    t = 0 #music time
    t_t = 0 #real time
    player = Player()
    player_sprites.add(player)
    time_list, note_list, scroll_list = tja_to_time(path.join(music_folder,song_name+'.tja'))
    pos_list = time_to_x(time_list,scroll_list)
    draw_note(note_list, pos_list, time_list, scroll_list)
    music_end = 0
    pre_gt = 0
    screen.fill(WHITE)
    screen.blit(background_img,(0,0))
    while gaming:
        # keep loop gaming at the right speed
        dt = clock.tick(FPS)
        t_t += dt
        gt = pygame.mixer.music.get_pos()
        t = gt - pre_gt
        if t < -2000:
            t += 3000
        pre_gt = gt
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                gaming = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q :
                    gaming = False
                if event.key == pygame.K_j or event.key == pygame.K_f:
                    don_sound.play(maxtime=100)
                    if t_t > 2000:
                        for note in reversed(note_sprites.sprites()):
                            if note.img_type in ['1','3']:
                                if  gt/1000 - note.t < -2:
                                    gt += 3000
                                if abs(gt/1000 - note.t) < 0.2 :
                                    note.hit_don(player,gt/1000)
                                    break
                                elif note.t - gt/1000 < -0.2:
                                    continue
                                else:
                                    break
    #                small_don = Note(small_don_img,1225)
    #                note_sprites.add(small_don)
    #                j = time()
                if event.key == pygame.K_k or event.key == pygame.K_d:
                    ka_sound.play()
                    if t_t > 2000:
                        for note in reversed(note_sprites.sprites()):
                            if note.img_type in ['2','4']:
                                if  gt/1000 - note.t < -2:
                                    gt += 3000
                                if 0 < abs(gt/1000 - note.t) < 0.2 :
                                    note.hit_ka(player,gt/1000)
                                    break
                                elif note.t - gt/1000 < -0.2:
                                    continue
                                else :
                                    break 
    #                small_ka = Note(small_ka_img,1800)
    #                note_sprites.add(small_ka)
        if not pygame.mixer.music.get_busy():
            if music_end :
                gaming = False
    #        pass
    #        screen.fill(WHITE)
    #        screen.blit(background_img,(0,0))
            pygame.display.flip()
            music_load(path.join(audio_folder,'space.ogg'))
            pygame.mixer.music.play()
            pygame.mixer.music.queue(path.join(music_folder,song_name+'.ogg'))
    #        pygame.time.delay(5000)
            music_end = 1
        # Update
        combo_text = my_font.render(f'{player.combo} combo',True,(0,0,0))
        max_combo_text = my_font.render(f'max_combp : {player.max_combo}',True,(0,0,0))
        score_text = my_font.render(f'{player.score}',True,(0,0,0))
        perfect_text = my_font.render(f'良：　　{player.perfect}',True,(0,0,0))
        good_text = my_font.render(f'可：　　{player.good}',True,(0,0,0))
        bad_text = my_font.render(f'不可：　　{player.bad}',True,(0,0,0))
        note_explosion_sprites.update()
        note_sprites.update(t,player)
        acc_sprites.update()
        player_sprites.update()
        screen.fill(WHITE)
        screen.blit(background_img,(0,0))
        screen.blit(combo_text, (300,50))
        screen.blit(score_text, (300,100))
        screen.blit(max_combo_text, (300,150))
        screen.blit(perfect_text, (600,50))
        screen.blit(good_text, (600,100))
        screen.blit(bad_text, (600,150))
        # Draw / render
        note_explosion_sprites.draw(screen)
        acc_sprites.draw(screen)
        note_sprites.draw(screen)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    #print(k-j)
    pygame.quit()

main_game('やわらか戦車')
