xmax = 215 # 30
xmin = 155 # 20
ymin = -132 #-10
ymax = -72 #-5

def pos(v, t):
    return (v * t) - (((t * t) - t) / 2)

hits = []
total = 0
for v0x in range(1, xmax + 1):
    for v0y  in range(ymin, -ymin):
        t = 0
        x = pos(v0x, t)
        y = pos(v0y, t)

        vx = v0x
        while x <= xmax and y >= ymin:
            if x >= xmin and y <= ymax:
                total += 1
                hits.append((v0x, v0y))
                break
            

            
            t += 1
            
            new_y = pos(v0y, t)
            y = new_y

            vx -= 1
            if vx >= 0:
                x = pos(v0x, t)
            else:
                x = last_x
            last_x = x



print(hits)
print(len(hits))

v0x = 5
v0y = 0

vx = v0x
for t in range(8):
    if vx >= 0:
        x = pos(v0x, t)
    else:
        x = last_x
    y = pos(v0y, t)
    print((pos(v0x, t), pos(v0y, t)))
    vx -= 1
    last_x = x

