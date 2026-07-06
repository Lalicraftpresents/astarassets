Web VPython 3.2


#Github에서 텍스쳐를 미리 불러옵니다
texture_void = "https://raw.githubusercontent.com/Lalicraftpresents/astarassets/main/void.png"
texture_wall = "https://raw.githubusercontent.com/Lalicraftpresents/astarassets/main/wall.png"
texture_start = "https://raw.githubusercontent.com/Lalicraftpresents/astarassets/main/start.png"
texture_end = "https://raw.githubusercontent.com/Lalicraftpresents/astarassets/main/end.png"
texture_searched = "https://raw.githubusercontent.com/Lalicraftpresents/astarassets/main/searched.png"
texture_actual = "https://raw.githubusercontent.com/Lalicraftpresents/astarassets/main/actual.png"



widthx = 50        
widthz = 50



#-------------------------------------------------맵 그리기-------------------------------------------------
#버튼
def draw_void():
    global draw_current_type
    draw_current_type = "void"
    print("현재 선택: 길")
def draw_wall():
    global draw_current_type
    draw_current_type = "wall"
    print("현재 선택: 장애물")
def draw_start():
    global draw_current_type
    draw_current_type = "start"
    print("현재 선택: 시작 지점")
    print("현재 시작 지점:", startpos_x, startpos_z)
def draw_end():
    global draw_current_type
    draw_current_type = "end"
    print("현재 선택: 도착 지점")
    print("현재 도착 지점:", endpos_x, endpos_z)
def draw_execute():
    global startpos_x
    global endpos_x
    if startpos_x is None or endpos_x is None:
        print("시작 지점과 도착 지점이 있어야 합니다")
    else:
        global draw_start_algorithm
        draw_start_algorithm = True


#마우스
def draw_mousedown():
    global draw_hold
    draw_hold = True
def draw_mouseup():
    global draw_hold
    draw_hold = False


#그리기
def draw_paint(target, type):
    if target is None:
        return
    global startpos_x
    global startpos_z
    global endpos_x
    global endpos_z
    target.walkable = True
    if startpos_x is not None:
        if target.pos == vec(startpos_x, 0, startpos_z):
            startpos_x = None
            startpos_z = None
    if endpos_x is not None:
        if target.pos == vec(endpos_x, 0, endpos_z):
            endpos_x = None
            endpos_z = None
        
    if type == "void":
        target.texture = texture_void
    if type == "wall":
        target.texture = texture_wall
        target.walkable = False

    startpos_virtual_x = startpos_x
    startpos_virtual_z = startpos_z
    
    
    if type == "start":
        if startpos_x is not None:
            grid[startpos_x][startpos_z].texture = texture_void
        target.texture = texture_start
        startpos_x = int(target.pos.x)
        startpos_z = int(target.pos.z)
        if startpos_x != startpos_virtual_x or startpos_z != startpos_virtual_z:
            print("시작 지점: ", startpos_x, startpos_z)             
    endpos_virtual_x = endpos_x
    endpos_virtual_z = endpos_z
    if type == "end":
        if endpos_x is not None:
            grid[endpos_x][endpos_z].texture = texture_void
        target.texture = texture_end
        endpos_x = int(target.pos.x)
        endpos_z = int(target.pos.z)
        if endpos_x != endpos_virtual_x or endpos_z != endpos_virtual_z:
            print("도착 지점: ", endpos_x, endpos_z)
        
graphics = canvas(width = 960, height = 540, background = color.white)


#그리드를 세팅합니다
grid = []
for i in range(widthx):
    grid.append([])
    for j in range(widthz):
        grid[i].append(box(canvas = graphics, pos = vec(i,0,j), texture=texture_void, emissive=True))

for i in range(widthx):
    for j in range(widthz):
        grid[i][j].walkable = True
        


#미로 그리기 처리
draw_start_algorithm = False
draw_current_type = "wall"

print("알고리즘이 통과할 미로를 그려주세요.")
print(" 시작지점과 도착지점이 반드시 있어야 한답니다!")

startpos_x = None
startpos_z = None

endpos_x = None
endpos_z = None

button_void = button(text = "길", bind = draw_void)
button_wall = button(text = "벽", bind = draw_wall)
button_start = button (text = "출발지점", bind = draw_start)
button_end = button(text = "도착지점", bind = draw_end)
button_execute = button(text = "그만 그릴래", bind = draw_execute)


draw_hold = False

graphics.bind('mousedown', draw_mousedown)
graphics.bind('mouseup', draw_mouseup)


while draw_start_algorithm is False:
    rate(60)
    if draw_hold is True:
        draw_paint(graphics.mouse.pick, draw_current_type)
        
graphics.unbind('mousedown', draw_mousedown)
graphics.unbind('mouseup', draw_mouseup)

button_void.visible = False
button_start.visible = False
button_wall.visible = False
button_end.visible = False
button_execute.visible = False

del button_void
del button_wall
del button_start
del button_end
del button_execute

#-------------------------------------------------알고리즘 처리-------------------------------------------------

howmuch = 0
current = [0,0]
def heuristic(currentx, currentz, targetx, targetz):
    return abs(targetx - currentx) + abs(targetz - currentz)

def add_cue(x,z,distance):
    global howmuch
    add_cue_dir(x+1,z,distance+1)
    add_cue_dir(x-1,z,distance+1)
    add_cue_dir(x,z+1,distance+1)
    add_cue_dir(x,z-1,distance+1)
    howmuch += 1
    grid[x][z].texture = texture_searched
    
def add_cue_dir(x,z,distance):
    if not (0 <= x < widthx and 0 <= z < widthz):
        return
    global endpos_x
    global endpos_z
    global cue
    if grid[x][z] is not None and grid[x][z].walkable is True:
        if grid[x][z].distance > distance:
            grid[x][z].distance = distance
            cue.append([x,z, heuristic(x,z,endpos_x,endpos_z) + distance])
    
    

cue = []


print("에이 스타 알고리즘을 시작합니다")

#거리 초기화: 시작 지점을 제외한 노드의 거리를 INF로 만듭니다.
for i in range(widthx):
    for j in range(widthz):
        grid[i][j].distance = 999999999
grid[startpos_x][startpos_z].distance = 0



cue.append([startpos_x,startpos_z, 0])

success = False


while True:
    rate(60)
    if cue != []:
        
        min_index = 0
    
        for i in range(1, len(cue)):
            if cue[i][2] < cue[min_index][2]:
                min_index = i
    
        current = cue[min_index]
        del cue[min_index]
    
        current_x = current[0]
        current_z = current[1]
        x = current[0]
        z = current[1]
    
        if current[0] == endpos_x and current[1] == endpos_z:
            success = True
            break
    
        distance = grid[x][z].distance
    
        add_cue(x, z, distance)
    else:
        break
    
if success:
    current = [endpos_x,endpos_z]
    while True:
        rate(30)
        cx = current[0]
        cz = current[1]
        grid[cx][cz].texture = texture_actual

        if cx == startpos_x and cz == startpos_z:
            break

        best = None
        best_dist = grid[cx][cz].distance

        for dx, dz in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx = cx + dx
            nz = cz + dz
            if 0 <= nx < widthx and 0 <= nz < widthz:
                if grid[nx][nz].distance < best_dist:
                    best_dist = grid[nx][nz].distance
                    best = [nx, nz]

        if best is None:
            # 이론상 일어나면 안 되지만, 안전장치
            break

        current = best
    print("최단거리 찾기 완료! 거리:",grid[endpos_x][endpos_z].distance, "탐색 노드:", howmuch)
        
else:
    label(pos=vec(0,-3,0),color=color.red, text=("길이 있어야 찾든 말든 하지!!!!!!!!!!"))
