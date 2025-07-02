# https://www.acmicpc.net/problem/18500

import sys
from collections import deque
input = sys.stdin.readline

# 동, 서, 북, 남 방향 (오른쪽, 왼쪽, 위, 아래)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# 미네랄 부수기
def break_mineral(map_info, height, L2R):
    row = len(map_info) - height  # 입력은 아래부터 높이, 배열은 위에서부터라 변환
    if L2R:
        cols = range(0, len(map_info[0]))  # 0번 열부터 오른쪽으로
    else:
        cols = range(len(map_info[0]) - 1, -1, -1)  # 마지막 열부터 왼쪽으로

    for col in cols:
        if map_info[row][col] == 'x':
            map_info[row][col] = '.'
            return (row, col)
    return None

# 땅에 붙어 있는 미네랄들을 표시한다
def ground_connected(map_info):
    R, C = len(map_info), len(map_info[0])
    visited = [[False]*C for _ in range(R)]
    queue = deque()

    for col in range(C):  # 바닥 행의 모든 열을 검사
        if map_info[R-1][col] == 'x':
            visited[R-1][col] = True
            queue.append((R-1, col))

    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                if map_info[nr][nc] == 'x' and not visited[nr][nc]:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
    return visited  # 땅에 붙어있는 미네랄은 True로 표시됨

# 떠 있는 미네랄 클러스터를 아래로 떨어뜨린다
def drop_cluster(map_info, visited):
    R, C = len(map_info), len(map_info[0])
    floating = []

    # 떠 있는 미네랄 찾기
    for r in range(R):
        for c in range(C):
            if map_info[r][c] == 'x' and not visited[r][c]:
                floating.append((r, c))
                map_info[r][c] = '.'

    if not floating:  # 떨어질 게 없으면 종료
        return

    # 얼마나 떨어질 수 있는지 계산
    fall_distance = R
    for r, c in floating:
        step = 0
        nr = r + 1
        while nr < R and map_info[nr][c] == '.':
            nr += 1
            step += 1
        if nr < R and visited[nr][c]:  # 땅에 붙은 거 위에 닿으면 멈춤
            step = step - 1
        fall_distance = min(fall_distance, step)

    for r, c in floating:  # 떨어진 위치에 미네랄 다시 놓기
        map_info[r + fall_distance][c] = 'x'


R, C = map(int, input().split())
# 동굴 상태
map_info = []
for _ in range(R):
    line = input().strip()
    row = list(line)
    map_info.append(row) 
    
N = int(input()) 
throws = list(map(int, input().split()))

L2R = True  # 처음 던질 땐 왼쪽부터

for height in throws:
    result = break_mineral(map_info, height, L2R)
    L2R = not L2R  # 방향 바꾸기

    if result:  # 미네랄을 부쉈다면
        connected = ground_connected(map_info)  # 땅에 붙은 미네랄 표시
        drop_cluster(map_info, connected)  # 떠 있는 미네랄 떨어뜨리기

for row in map_info:
    print(''.join(row))