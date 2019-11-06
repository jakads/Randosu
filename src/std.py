import os
import sys
from msvcrt import getch
from random import seed, randint, uniform
from time import time
from math import sin, cos, pi
from pathvalidate import sanitize_filename

def randosu(path, content):
    # Dictionary List for notes
    notes = []
    
    # Change Stack Leniency to 0
    for c in content:
        if c.startswith('StackLeniency:'):
            content[content.index(c)] = 'StackLeniency:0\n'
            break
    
    objindex = content.index('[HitObjects]\n')
    
    # Parse notes from the next row of [HitObjects] to EOF
    for c in content[objindex+1:]:
        # Syntax: x, y, extra
        content_split = c.split(',')
        note_x = int(content_split[0])
        note_y = int(content_split[1])
        note_ms = int(content_split[2])
        note_extra = content_split[3:]
        notes.append({
            'x': note_x,
            'y': note_y,
            'ms': note_ms,
            'extra': note_extra,
            'isSlider': len(content_split) > 7
        })
    
    # Random Seed input
    print('read success')
    randseed = input('seed(optional): ')
    if randseed != '':
        seed(randseed)
    
    print('True Random? (Y/N)')
    while True:
        answer = getch().decode()
        if answer in 'yYnN':
            break
    TrueRandom = True if answer in 'yY' else False
    
    if not TrueRandom:
        while True:
            try:
                min = input('min scale factor(default 0.5): ')
                if min == '':
                    min = 0.5
                min = float(min)
    
                max = input('max scale factor(default 1.5): ')
                if max == '':
                    max = 1.5
                max = float(max)
                break
            except:
                print('number plz')
    
        # I bet someone would try this so
        if min > max:
            tmp = min
            min = max
            max = tmp
    
    while True:
        try:
            red = input('chance of red anchors(%, default 25): ')
            if red == '':
                red = 25
            red = float(red)
            break
        except:
            print('number plz')
    
    if red > 100:
        red = 100
    if red < 0:
        red = 0
    
    # Change difficulty & output file name
    for c in content:
        if c.startswith('Version:'):
            # Exclude '\n'
            diffname = c.split(':', 1)[1][:-1]
            index = content.index(c)
    
            rand = f"truerand({red})" if TrueRandom else f"rand({min}~{max},{red})"
            Rand = f"TrueRandomized(Red:{red}%)" if TrueRandom else f"Randomized({min}~{max}x, Red:{red}%)"
    
            if randseed == '':
                content[index] = f'Version:{Rand}_{diffname}_{int(time())}\n'
                filename = f'{os.path.dirname(path)}\\{rand}_{sanitize_filename(diffname)}_{int(time())}.osu'
    
            # Example:
            # Diffname: Randomized(0.5~2.0, Red:75.0%)_Insane_1572968652
            # Filename: ~~~.osu => rand(0.5~2.0,75)_~~~_1572968652.osu
    
            else:
                content[index] = f'Version:{Rand}_{diffname} (Seed:{randseed})\n'
                filename = f'{os.path.dirname(path)}\\{rand}_{randseed}_{sanitize_filename(diffname)}'
    
            # Example:
            # Diffname: TrueRandomized(Red:0%)_Expert (Seed:joe mama)
            # Filename: ~~~.osu => truerand(0)_joe mama_~~~.osu
    
    i=0
    randnotes = []
    rad=0
    
    # Randomize position of the notes
    for n in notes:
        # Distance should be lower than set
        while True:
            if (i == 0) or TrueRandom:
                randx = randint(0, 512)
                randy = randint(0, 384)
                break
    
            # Add 0~10 for chaos
            diffx = n['x'] - notes[i-1]['x'] + uniform(0, 10)
            diffy = n['y'] - notes[i-1]['y'] + uniform(0, 10)

            distance = (diffx ** 2 + diffy ** 2) ** 0.5
    
            rad += 2 * pi * uniform(-1, 1) ** 3
            factor = uniform(min, max)
    
            randx = randnotes[i-1]['x'] + int(distance * factor * cos(rad))
            randy = randnotes[i-1]['y'] + int(distance * factor * sin(rad))
    
            # If factor is too high, corner the object
            if int(distance * factor) > 640:
                if randx < 0:
                    randx = 0
                if randx > 512:
                    randx = 512
                if randy < 0:
                    randy = 0
                if randy > 384:
                    randy = 384
    
            if (0 <= randx <= 512) and (0 <= randy <= 384):
                break
            
        # if slider:
        if n['isSlider']:
            # Getting curve points
            point = n['extra'][2].split('|')
            curve = [point[0]]
    
            # Randomize curve points
            for k in range(len(point)-1):
                curvex = randint(0, 512)
                curvey = randint(0, 384)
                curve.append(f'{curvex}:{curvey}')
    
                # Red Anchors
                # Always end with normal curve point to prevent slider ending too early
                if uniform(0, 100) < red and k != len(point) - 2:
                    curve.append(f'{curvex}:{curvey}')
    
            n['extra'][2] = '|'.join(curve)
    
        randnotes.append({
                'x': randx,
                'y': randy,
                'ms': n['ms'],
                'extra': n['extra']
            })
        i+=1
    
        
    with open(filename,'w',encoding='utf-8') as osu:
        for c in content[:objindex+1]:
            osu.write(c)
    
        for n in randnotes:
            osu.write(f'{n["x"]},{n["y"]},{n["ms"]},{",".join(n["extra"])}')
    
    print('done')
    getch()