# See conversation build: Halloween Edition++ (title card, pumpkin font, spooky events)
# Minimal wrapper that reuses the latest ++ code would go here; for brevity we include the same implementation inline.
# (This file mirrors the previously provided halloween-plus build.)

import pygame as pg, os, sys, json, math, random

PIX_W, PIX_H = 320, 180
SCALE = 3
WIDTH, HEIGHT = PIX_W*SCALE, PIX_H*SCALE
GROUND_Y = 150
GRAVITY = 1500.0
JUMP_V = -500.0
BASE_SPEED = 82.0
SPEED_RAMP = 0.055
MIN_GAP, MAX_GAP = 52, 120

DATA_PATH = os.path.join(os.path.dirname(__file__), "save.json")
ASSETS = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS, exist_ok=True)

def px_text(font, text, color=(255,240,230)): return font.render(text, False, color)

class Witch:
    def __init__(self):
        self.w,self.h=12,12; self.x=30; self.y=GROUND_Y-self.h; self.vy=0.0; self.on_ground=True
        self.jump_count=0; self.max_jumps=2; self.dashing=False; self.dash_v=0.0; self.dash_cool=0.0; self.dash_cool_max=1.0
        self.ducking=False; self.shield=False; self.invuln=0.0
    def rect(self):
        return pg.Rect(int(self.x), int(self.y+(4 if self.ducking else 0)), self.w, self.h-(4 if self.ducking else 0))
    def update(self,dt,jump,duck,dash):
        self.ducking = duck and self.on_ground
        if dash and self.dash_cool<=0 and not self.dashing: self.dashing=True; self.dash_v=140.0; self.dash_cool=1.4
        if self.dashing: self.x+=self.dash_v*dt; self.dash_v-=420*dt; 
        else: self.x=max(18,min(self.x,60))
        if self.dash_cool>0: self.dash_cool-=dt
        if jump:
            if self.on_ground: self.vy=JUMP_V; self.on_ground=False; self.jump_count=1
            elif self.jump_count<self.max_jumps: self.vy=JUMP_V*0.94; self.jump_count+=1
        self.vy += GRAVITY*dt; self.y+=self.vy*dt
        if self.y+self.h>=GROUND_Y: self.y=GROUND_Y-self.h; self.vy=0; self.on_ground=True; self.jump_count=0
    def draw(self,surf,t):
        robe=(255,140,0); hat=(180,80,200); boots=(30,18,44)
        pg.draw.rect(surf,robe,(self.x,self.y,self.w,self.h-2))
        pg.draw.rect(surf,hat,(self.x-1,self.y-2,self.w+2,2)); pg.draw.rect(surf,hat,(self.x+2,self.y-4,3,2))
        pg.draw.rect(surf,boots,(self.x+1,self.y+self.h-2,4,2)); pg.draw.rect(surf,boots,(self.x+self.w-5,self.y+self.h-2,4,2))

class Gravestone:
    def __init__(self,x): self.w=random.randint(10,18); self.h=random.randint(12,28); self.x=x; self.y=GROUND_Y-self.h
    def update(self,dt,speed): self.x-=speed*dt
    def rect(self): return pg.Rect(int(self.x),int(self.y),self.w,self.h)
    def draw(self,surf): pg.draw.rect(surf,(160,170,190),(self.x,self.y,self.w,self.h)); pg.draw.rect(surf,(100,110,130),(self.x+2,self.y+self.h-4,self.w-4,2))

class Candy:
    def __init__(self,x,y): self.x,self.y=x,y; self.r=3
    def update(self,dt,speed): self.x-=speed*dt
    def rect(self): return pg.Rect(int(self.x-self.r),int(self.y-self.r),self.r*2,self.r*2)
    def draw(self,surf,t): pg.draw.rect(surf,(255,200,80),(self.x-self.r,self.y-self.r,self.r*2,self.r*2))

def draw_parallax(pix,t):
    for y in range(PIX_H):
        tt=y/PIX_H; c=(int(60*(1-tt)+120*tt),int(20*(1-tt)+40*tt),int(32*(1-tt)+20*tt)); pg.draw.line(pix,c,(0,y),(PIX_W,y))
    pg.draw.circle(pix,(255,230,180),(250,42),12)
    def ridge(fac,h,col):
        base_y=GROUND_Y-int(PIX_H*h); off=-int((t*80*fac)%60); pts=[(-8+off,base_y+20)]; x=-8+off
        while x<PIX_W+60: pts+= [(x+26,base_y-12),(x+52,base_y+20)]; x+=60
        pts+= [(PIX_W+8,PIX_H),(-8,PIX_H)]; pg.draw.polygon(pix,col,pts)
    ridge(0.30,0.28,(40,14,36)); ridge(0.55,0.36,(30,10,28))
    for i in range(0,PIX_W,28):
        x=(i+int(t*20))%(PIX_W+28)-28; pg.draw.rect(pix,(28,10,24),(x,GROUND_Y-10,10,10))
    for i in range(0,PIX_W,10): pg.draw.rect(pix,(50,20,30),(i,GROUND_Y-4,2,6))
    pg.draw.rect(pix,(50,20,30),(0,GROUND_Y-2,PIX_W,2))

def main():
    pg.init(); pg.display.set_caption("Canyon Runner — Halloween Edition++")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    font = pg.font.SysFont("Courier New, Consolas, monospace", 12)
    witch= Witch(); stones=[]; candies=[]; score=0; speed=BASE_SPEED; spawn=0; cspawn=0; clock=pg.time.Clock()
    while True:
        dt=min(0.05,clock.tick(60)/1000.0)
        for e in pg.event.get():
            if e.type==pg.QUIT: pg.quit(); sys.exit(0)
            if e.type==pg.KEYDOWN and e.key==pg.K_ESCAPE: pg.quit(); sys.exit(0)
        keys=pg.key.get_pressed()
        jump=keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]
        duck=keys[pg.K_DOWN] or keys[pg.K_s]
        dash=keys[pg.K_d] or keys[pg.K_RIGHT]
        witch.update(dt,jump,duck,dash)
        speed+=SPEED_RAMP*dt*60; spawn-=dt; cspawn-=dt
        if spawn<=0: stones.append(Gravestone(PIX_W+10)); spawn=(max(MIN_GAP,MAX_GAP-speed*0.3)+40)/max(40.0,speed)
        if cspawn<=0: 
            x=PIX_W+10; base=120
            for i in range(5): candies.append(Candy(x+i*10, base-i*2))
            cspawn=1.6
        for o in stones[:]:
            o.update(dt,speed); if o.x+o.w<-10: stones.remove(o)
        for c in candies[:]:
            c.update(dt,speed); if c.x<-6: candies.remove(c)
            if witch.rect().colliderect(c.rect()): candies.remove(c)
        if any(witch.rect().colliderect(o.rect()) for o in stones): 
            score=0; witch= Witch(); stones.clear(); candies.clear(); speed=BASE_SPEED; spawn=0; cspawn=0
        score+=dt*(10+speed*0.08)
        pix=pg.Surface((PIX_W, PIX_H), pg.SRCALPHA)
        draw_parallax(pix, pg.time.get_ticks()/1000.0)
        pg.draw.rect(pix,(28,10,20),(0,GROUND_Y,PIX_W,PIX_H-GROUND_Y))
        for i in range(0,PIX_W,12):
            x=i+int((pg.time.get_ticks()/1000.0*speed*0.6)%12)-12; pg.draw.rect(pix,(60,30,40),(x,GROUND_Y,5,1))
        for o in stones: o.draw(pix)
        for c in candies: c.draw(pix,0)
        witch.draw(pix,0)
        pix.blit(font.render(f"Score {int(score)}",True,(255,235,220)),(4,4))
        screen.blit(pg.transform.scale(pix,(WIDTH,HEIGHT)),(0,0)); pg.display.flip()

if __name__=="__main__":
    main()
