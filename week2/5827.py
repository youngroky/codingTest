# https://www.acmicpc.net/problem/5827
# 실패
import sys
from collections import deque

input = sys.stdin.readline

N, M = map(int, input().split())
world = [list(input().strip()) for _ in range(N)]

# 시작점, 도착점 좌표
for i in range(N):
    for j in range(M):
        if world[i][j] == 'C':
            cx, cy = j, i
        if world[i][j] == 'D':
            dx, dy = j, i

# 상수
CANT = -1

# 가중치 - 각 좌표당 중력반전 횟수 - 아래중력(0), 위중력(1) 일때 나눠서 계산
dist = []
for y in range(N):
    row = []
    for x in range(M):
        row.append([-1, -1])
    dist.append(row)

# 중력 낙하 함수 : g가 0 이면 정상, 1 이면 반대 중력 작용
def fall(x, y, g):
    direction = (1 if g==0 else -1)
    while True:
        ny = y + direction
        if not (0 <= ny < N): 
            return None
        if world[ny][x] == '#': 
            break
        if dist[ny][x][g] == CANT:
            dist[ny][x][g] = dist[y][x][g]
        y = ny
    return x, y

dq = deque()

# 1. D에서 시작, 중력 ↓로 낙하
dist[dy][dx][0] = 0
start = fall(dx, dy, 0)
if start is not None:
    x, y = start
    dq.appendleft((x, y, 0))

# 2. D에서 시작, 중력 ↑로 낙하
dist[dy][dx][1] = 1
start = fall(dx, dy, 1)
if start is not None:
    x, y = start
    dq.appendleft((x, y, 1))

# 반복하면서 계산
while dq:
    x, y, g = dq.popleft()
    cur_cost = dist[y][x][g]

    # 좌우 이동 (fall 후 위치에서 방문 체크)
    for dx_ in [-1, 1]:
        nx = x + dx_
        if 0 <= nx < M and world[y][nx] == '.':
            fall_result = fall(nx, y, g)
            if fall_result:
                fx, fy = fall_result
                if dist[fy][fx][g] == CANT:
                    dist[fy][fx][g] = cur_cost
                    dq.appendleft((fx, fy, g))  # 비용 0 → 앞에 넣기

    # 중력 반전
    ng = 1 - g
    fall_result = fall(x, y, ng)
    if fall_result:
        fx, fy = fall_result
        if dist[fy][fx][ng] == CANT:
            dist[fy][fx][ng] = cur_cost + 1
            dq.append((fx, fy, ng))  # 비용 1 → 뒤에 넣기

# 4. 정답: C 좌표의 중력 ↓, ↑ 중 최소값
if dist[cy][cx][0] == -1 and dist[cy][cx][1] == -1:
    ans = -1
elif dist[cy][cx][0] == -1:
    ans = dist[cy][cx][0]
elif dist[cy][cx][1] == -1:
    ans = dist[cy][cx][1]
else:
    ans = min(dist[cy][cx][0], dist[cy][cx][1])

print(ans)