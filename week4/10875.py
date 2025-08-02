# https://www.acmicpc.net/problem/10875

# 	1.	입력값으로 격자 크기 L과 방향 명령 개수 N을 받는다.
# 	2.	각 명령을 (시간, 방향) 형태로 리스트에 저장한다.
# 	3.	시작 위치 (0, 0), 시작 방향(오른쪽), 누적 시간 0으로 초기화한다.
# 	4.	지금까지 이동한 직선 경로들을 저장할 traces 리스트를 만든다.
# 	5.	각 명령을 순서대로 처리하면서:
#       5-1. 현재 방향으로 t초 동안 이동한 (nx, ny)를 계산한다.
#       5-2. traces에 저장된 모든 경로와 충돌 여부를 검사한다.
#       5-3. 경계 밖으로 나갔는지 확인한다.
#       5-4. 아무 문제 없으면: 현재 이동한 경로를 traces에 추가하고, 위치와 방향을 갱신한다.
# 	6.	모든 명령을 처리한 뒤에도 충돌이나 벽을 만나지 않았다면:
#       6-1. 현재 방향으로 무한 직진한다고 가정하고 충돌 여부를 다시 확인한다.
#       6-2. 충돌하면 해당 지점까지 시간 출력.
#       6-3. 아니면 경계선까지 거리 + 1초를 더해 출력한다.


dx = [-1, 0, 1, 0]  # 방향: 상, 우, 하, 좌
dy = [0, 1, 0, -1]

x, y, d = 0, 0, 1  # 시작 좌표와 초기 방향 (오른쪽)
l = int(input())  # 격자 한 변의 길이
n = int(input())  # 명령 수

opers = [list(input().split()) for _ in range(n)]

totalT = 0  # 총 시간
traces = []  # 이전까지 이동한 경로를 저장

# 직선 segment 간 충돌 여부 확인
def isCrushed(tx1, ty1, tx2, ty2, x1, y1, x2, y2):
    # 기존 trace (tx1,ty1) ~ (tx2,ty2)
    # 현재 이동 (x1,y1) ~ (x2,y2)
    # 상하/좌우/수직 겹침에 따라 충돌 여부 판단
    if tx1 > tx2 and ty1 == ty2:
        if y1 == y2 and y1 == ty1:
            if tx1 >= x1 >= tx2 or tx1 >= x2 >= tx2:
                return True
        elif x1 == x2:
            if (y1 > y2 and y1 >= ty1 >= y2) or (y1 < y2 and y2 >= ty1 >= y1):
                if tx1 >= x1 >= tx2:
                    return True
    elif tx1 < tx2 and ty1 == ty2:
        if y1 == y2 and y1 == ty1:
            if tx1 <= x1 <= tx2 or tx1 <= x2 <= tx2:
                return True
        elif x1 == x2:
            if (y1 > y2 and y1 >= ty1 >= y2) or (y1 < y2 and y2 >= ty1 >= y1):
                if tx2 >= x1 >= tx1:
                    return True
    elif tx1 == tx2 and ty1 > ty2:
        if x1 == x2 and x1 == tx1:
            if ty1 >= y1 >= ty2 or ty1 >= y2 >= ty2:
                return True
        elif y1 == y2:
            if (x1 > x2 and x1 >= tx1 >= x2) or (x1 < x2 and x2 >= tx1 >= x1):
                if ty1 >= y1 >= ty2:
                    return True
    elif tx1 == tx2 and ty1 < ty2:
        if x1 == x2 and x1 == tx1:
            if ty1 <= y1 <= ty2 or ty1 <= y2 <= ty2:
                return True
        elif y1 == y2:
            if (x1 > x2 and x1 >= tx1 >= x2) or (x1 < x2 and x2 >= tx1 >= x1):
                if ty2 >= y1 >= ty1:
                    return True
    return False

allClear = False
for i in range(n):
    t, dir = int(opers[i][0]), opers[i][1]
    nx = x + dx[d] * t
    ny = y + dy[d] * t

    # 충돌 확인
    checked = False
    dist = int(1e9)
    for x1, y1, x2, y2 in traces:
        if isCrushed(x1, y1, x2, y2, x + dx[d], y + dy[d], nx, ny):
            if d in [0, 2]:  # 수직 방향
                dist = min(dist, abs(x - x1))
            else:  # 수평 방향
                dist = min(dist, abs(y - y1))
            checked = True
    if checked:
        totalT += dist
        allClear = True
        break

    # 경계 밖으로 나가는 경우
    if nx < -l or ny < -l or nx > l or ny > l:
        if d == 0:
            dist = abs(-l - x)
        elif d == 1:
            dist = abs(l - y)
        elif d == 2:
            dist = abs(l - x)
        elif d == 3:
            dist = abs(-l - y)
        totalT += dist + 1
        allClear = True
        break

    # 경로 저장 후 위치 이동
    traces.append((x, y, nx, ny))
    x, y = nx, ny
    d = (d + 1) % 4 if dir == 'L' else (d - 1) % 4
    totalT += t

# 명령 끝까지 수행한 경우: 무한 진행 확인
if not allClear:
    nx, ny = x, y
    if d == 0:
        nx = -l
    elif d == 1:
        ny = l
    elif d == 2:
        nx = l
    elif d == 3:
        ny = -l

    checked = False
    dist = int(1e9)
    for x1, y1, x2, y2 in traces:
        if isCrushed(x1, y1, x2, y2, x + dx[d], y + dy[d], nx, ny):
            if d in [0, 2]:
                dist = min(dist, abs(x - x1))
            else:
                dist = min(dist, abs(y - y1))
            checked = True
    if checked:
        totalT += dist
    else:
        if d == 0:
            dist = abs(-l - x)
        elif d == 1:
            dist = abs(l - y)
        elif d == 2:
            dist = abs(l - x)
        elif d == 3:
            dist = abs(-l - y)
        totalT += dist + 1
    print(totalT)
else:
    print(totalT)