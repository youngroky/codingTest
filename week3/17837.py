# https://www.acmicpc.net/problem/17837

import sys
from collections import deque
input = sys.stdin.readline

# 입력 - 크기(N), 말 수(K)
N, K = map(int, input().split())

# 보드판 - 0은 흰색, 1은 빨간색, 2는 파란색
board = []
for _ in range(N):
    row = input().split()
    board.append([int(x) for x in row])
    
# 방향 설정 (→, ←, ↑, ↓)
dirs = [(0,1),(0,-1),(-1,0),(1,0)]

# 기물들의 현재 위치 + 방향 정보를 저장할 것
pieces = [None] * K

# 기물들의 위치를 저장할 배열
position = []
for i in range(N):
    row = []
    for j in range(N):
        # 각 칸에 deque 를 이용해서 이동할 때, 위 아래로 추가가 쉽도록 함.
        # - 맨 앞이 제일 아래 에 있는 것, 맨 뒤가 제일 위에 있는 것 
        row.append(deque())
    position.append(row)


# 기물 - 행, 열, 방향(순서대로 →, ←, ↑, ↓)
for i in range(K):
    r, c, d = map(int, input().split())
    # 인덱스 때문에 하나씩 줄여서 저장
    r -= 1; c -= 1; d -= 1
    pieces[i] = {
        "pos": (r, c),        # 위치 (행, 열)
        "dir": dirs[d]        # 방향
    }
    position[r][c].append(i)

# 말 인덱스를 받아 해당 말 위에 있는 모든 말들 deque 로 추출
def get_pieces(piece_index):
    x, y = pieces[piece_index]["pos"]
    idx = position[x][y].index(piece_index)
    moving = deque()
    while len(position[x][y]) > idx:
        moving.append(position[x][y].pop())
    return moving

# 말 이동 처리
def move(piece_index):
    x, y = pieces[piece_index]["pos"]
    dx, dy = pieces[piece_index]["dir"]
    mx, my = x + dx, y + dy

    # 맵 벗어나거나 파란색 칸인 경우
    if not (0 <= mx < N and 0 <= my < N) or board[mx][my] == 2:
        dx, dy = -dx, -dy  # 방향 반전
        pieces[piece_index]["dir"] = (dx, dy)
        mx, my = x + dx, y + dy
        # 반전 후에도 벗어나거나 파란색이면 이동 안 함
        if not (0 <= mx < N and 0 <= my < N) or board[mx][my] == 2:
            return False

    # 이동할 말들 추출
    moving = get_pieces(piece_index)

    # 빨간색이면 순서 뒤집기
    if board[mx][my] == 1:
        moving = deque(reversed(moving))

    # 말 이동
    position[mx][my].extend(moving)
    for m in moving:
        pieces[m]["pos"] = (mx, my)

    # 종료 조건: 말이 4개 이상 쌓이면 게임 끝
    if len(position[mx][my]) >= 4:
        return True
    return False

# 게임 진행
turn = 0
result = -1

while turn < 1000:
    turn += 1
    for i in range(K):
        if move(i):
            result = turn
            break
    if result != -1:
        break

print(result)