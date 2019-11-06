import os
import sys
from msvcrt import getch
from random import seed, randint, uniform
from time import time
from pathvalidate import sanitize_filename

def randosu(path, content):
    # Dictionary List for notes
    notes = []
    
    # Dictionary List for other notes (Sliders, Spinners)
    othernotes = []
    
    objindex = content.index('[HitObjects]\n')
    
    # Parse notes from the next row of [HitObjects] to EOF
    for c in content[objindex+1:]:
        # Syntax: x, y, extra
        content_split = c.split(',')
    
        # Normal note is either 1 or 5(new combo)
        if int(content_split[3]) % 2 != 1:
            othernotes.append(c)
        
        else:
            note_extra1 = content_split[:4]
            note_type = content_split[4]
            note_extra2 = content_split[5:]
            notes.append({
                'extra1': note_extra1,
                'type': note_type,
                'extra2': note_extra2
            })
    
    # Random Seed input
    print('read success')
    randseed = input('seed(optional): ')
    if randseed != '':
        seed(randseed)
    
    while True:
        try:
            print("Kimagure=20%, Detarame=50%, Abekobe(Mirror)=100%")
            switch = input('chance of switching colors(%, default 50): ')
            if switch == '':
                switch = 50
            switch = float(switch)
        except:
            print('number plz')
            continue
        if switch > 100:
            switch = 100
        if switch <= 0:
            print("what's the point?")
        else:
            break
    
    # Change difficulty & output file name
    for c in content:
        if c.startswith('Version:'):
            # Exclude '\n'
            diffname = c.split(':', 1)[1][:-1]
            index = content.index(c)
    
            if randseed == '':
                content[index] = f'Version:Randomized({switch}%)_{diffname}_{int(time())}\n'
                filename = f'{os.path.dirname(path)}\\rand({switch})_{sanitize_filename(diffname)}_{int(time())}.osu'
    
            # Example:
            # Diffname: Randomized(50.0%)_Insane_1572968652
            # Filename: ~~~.osu => rand50.0_~~~_1572968652.osu
    
            else:
                content[index] = f'Version:Randomized({switch}%)_{diffname} (Seed:{randseed})\n'
                filename = f'{os.path.dirname(path)}\\rand({switch})_{randseed}_{sanitize_filename(diffname)}'
    
            # Example:
            # Diffname: Randomized(100.0%)_Expert (Seed:joe mama)
            # Filename: ~~~.osu => rand100.0_joe mama_~~~.osu
    
    # Randomize position of the notes
    for n in notes:
        if uniform(0, 100) < switch:
            # 1: Normal, 2: Whistle, 4: Finish, 8: Clap
            hitsound = format(int(n["type"]) + 16, 'b')
            Kat = int(hitsound[1]) or int(hitsound[3])
            Big = int(hitsound[2])
    
            n["type"] = {
                #d -> k
                0: 2,
                #k -> d
                10: 0,
                #D -> K
                1: 6,
                #K -> D
                11: 4
            }.get(Kat * 10 + Big)
    
    with open(filename,'w',encoding='utf-8') as osu:
        for c in content[:objindex+1]:
            osu.write(c)
    
        for n in notes:
            osu.write(f'{",".join(n["extra1"])},{n["type"]},{",".join(n["extra2"])}')
    
        for n in othernotes:
            osu.write(n)
    
    print('done')
    getch()