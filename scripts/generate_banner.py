"""Original animated profile artwork. Run with Python, Pillow and Fontconfig."""
from pathlib import Path
from functools import lru_cache
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
BG = '#080e1b'
CYAN = '#58e6db'
WHITE = '#eff5ff'
MUTED = '#9aaec9'

@lru_cache(None)
def font(size, bold=False, mono=False):
    family = 'monospace' if mono else 'Liberation Sans'
    if bold:
        family += ':style=Bold'
    path = subprocess.check_output(['fc-match', '-f', '%{file}', family], text=True)
    return ImageFont.truetype(path, size)

def text(d, xy, value, size, color=WHITE, bold=False, mono=False):
    d.text(xy, value, font=font(size, bold, mono), fill=color)

def base(w,h):
    im = Image.new('RGB',(w,h),BG)
    d=ImageDraw.Draw(im)
    for y in range(h):
        t=y/h
        d.line((0,y,w,y), fill=(8+int(t*4),14+int(t*8),27+int(t*14)))
    return im

def save(frames, name, duration=100):
    frames[min(29, len(frames)-1)].save(ASSETS / f'{name}.png')
    frames[0].save(ASSETS / f'{name}.gif', save_all=True, append_images=frames[1:], duration=duration, loop=0, optimize=True)
    print(name, (ASSETS / f'{name}.gif').stat().st_size, 'bytes')

def hero(i):
    im=base(1200,500)
    d=ImageDraw.Draw(im)
    # Travelling contour lines form a flowing technical landscape.
    for row in range(12):
        points=[]
        for x in range(0,1201,8):
            y=355+row*17+25*math.sin(x/160+i*math.tau/90+row*.20)
            points.append((x,y))
        d.line(points, fill=(20,45+row*3,61+row*3),width=1)
    for j in range(24):
        x=(j*151+i*2)%1200
        y=(j*71)%470
        r=2 if j%3 else 3
        d.ellipse((x,y,x+r,y+r),fill='#26445a')
    d.rounded_rectangle((30,28,1170,472),radius=24,outline='#284157',width=2)
    d.rounded_rectangle((60,56,368,90),radius=17,fill='#123339')
    d.ellipse((75,68,84,77),fill=CYAN)
    text(d,(96,63),'PRIVERJR  /  SOFTWARE ENGINEER',14,CYAN,True)
    text(d,(58,119),'Privatus',75,WHITE,True)
    text(d,(58,195),'Cosmas.',75,WHITE,True)
    roles=['Building useful digital products.','Web. Mobile. AI. Connected.','From idea to working software.']
    role=roles[i//30]
    n=min(len(role),int((i%30)*2.2)+1)
    text(d,(63,292),role[:n],25,CYAN)
    if i%10<6:
        offset=d.textlength(role[:n],font=font(25))
        d.rectangle((65+offset,295,67+offset,320),fill=CYAN)
    text(d,(63,350),'Full-Stack & Mobile Developer',22,MUTED)
    text(d,(63,385),'CEO, INCPRITECH  /  Mbeya, Tanzania',18,MUTED)
    text(d,(63,438),'depriver.tech',14,CYAN,mono=True)
    # Live terminal illustration with a moving signal graph.
    d.rounded_rectangle((700,106,1128,404),radius=16,fill='#101b2b',outline='#365167',width=2)
    for j,c in enumerate(('#fb7185','#fbbf24',CYAN)):
        d.ellipse((721+j*21,125,730+j*21,134),fill=c)
    text(d,(807,119),'priverjr / workspace',13,MUTED,mono=True)
    d.line((701,150,1127,150),fill='#2b4059')
    lines=[('$ whoami',CYAN),('Privatus Cosmas',WHITE),('> design thoughtful interfaces',MUTED),('> connect apps and APIs',MUTED),('> build tools that help people',MUTED)]
    for j,(line,c) in enumerate(lines):
        text(d,(723,171+j*29),line,15,c,mono=True)
    for j in range(35):
        h=10+int(24*(1+math.sin(j*.45-i*math.tau/30))/2)
        d.rounded_rectangle((724+j*11,367-h,730+j*11,367),radius=2,fill=CYAN if j<23 else '#8d85d9')
    text(d,(723,380),'CREATE  /  CONNECT  /  IMPROVE',11,MUTED,mono=True)
    return im

def divider(i):
    im=base(1200,36); d=ImageDraw.Draw(im)
    d.line((0,18,1200,18),fill='#26384e',width=2)
    for j in range(3):
        x=(i*20+j*400)%1200
        for tail in range(50):
            a=1-tail/50
            d.line(((x-tail*2)%1200,18,(x-tail*2)%1200+2,18),fill=(int(24+64*a),int(40+190*a),int(55+164*a)),width=3)
    return im

def card(i,title,subtitle,number,tags,color):
    im=base(580,230);d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,578,228),radius=18,outline='#2e455f',width=2)
    text(d,(27,22),number+' / SELECTED WORK',12,color,True,True)
    text(d,(26,61),title,37,WHITE,True)
    text(d,(28,115),subtitle,19,MUTED)
    text(d,(28,184),tags,13,color,True,True)
    # Animated routing trace, kept away from the project text.
    d.line((28,159,550,159),fill='#25384c',width=2)
    x=28+(i/39)*522
    d.line((28,159,x,159),fill=color,width=2)
    d.ellipse((x-4,155,x+4,163),fill=WHITE)
    return im

if __name__=='__main__':
    ASSETS.mkdir(exist_ok=True)
    save([hero(i) for i in range(90)],'profile-banner')
    save([divider(i) for i in range(60)],'flow-divider')
    for slug,title,subtitle,num,tags,color in [
        ('incdai','incdai','AI interfaces, SDKs and conversational tools','01','AI / PYTHON / JAVASCRIPT',CYAN),
        ('percelio','Percelio','Mobile experiences for courier workflows','02','FLUTTER / DART / LOGISTICS','#a99cf5'),
        ('depriver','depriver.tech','Stories, ideas and a personal web experience','03','ASTRO / GSAP / CONTENT',CYAN),
        ('privatus','Privatus','An interactive developer portfolio','04','REACT / THREE.JS / MOTION','#a99cf5')]:
        save([card(i,title,subtitle,num,tags,color) for i in range(40)],'project-'+slug)
