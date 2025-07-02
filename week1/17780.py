# https://www.acmicpc.net/problem/17780

import sys
from collections import deque
input = sys.stdin.readline

# 입력
N, K = map(int, input().split())

# 보드판
board = []
for _ in range(N):
    row = input().split()
    board.append([int(x) for x in row])
    
# 기물
pieces = [None] * K

# 각칸에 모인 수
cells = []
for i in range(N):
    row = []
    for j in range(N):
        row.append(deque())  # 각 칸에는 deque를 하나씩 넣음
    cells.append(row)


# 방향 설정 (→, ←, ↑, ↓)
dirs = [(0,1),(0,-1),(-1,0),(1,0)]

def reverse(d):
    return d ^ 1

# 초기 말 위치 및 방향 설정
for i in range(K):
    r, c, d = map(int, input().split())
    # 인덱스 때문에 하나씩 줄여서 저장
    r -= 1; c -= 1; d -= 1
    pieces[i] = [r, c, d]
    cells[r][c].append(i)

# 말 이동 : 가장 아래인 말만 이동 가능
def move(piece_idx):
    r, c, d = pieces[piece_idx]
    # 가장 아래인지 확인
    if cells[r][c][0] != piece_idx:
        return False

    # 움직일 것
    dr, dc = dirs[d]
    # 이동할 위치
    nr, nc = r + dr, c + dc

    # 파란색 또는 범위 밖이면 방향 반대로 하고 다시 계산
    if not (0 <= nr < N and 0 <= nc < N) or board[nr][nc] == 2:
        d = reverse(d)
        pieces[piece_idx][2] = d
        dr, dc = dirs[d]
        nr, nc = r + dr, c + dc
        if not (0 <= nr < N and 0 <= nc < N) or board[nr][nc] == 2:
            return False

    # 현재 칸에 있는 말들을 모두 가져오기
    moving = list(cells[r][c])

    # 현재 칸 비우기
    cells[r][c].clear()

    '''
    이게 훨신 빠름 -> 왜지
    idx = cells[r][c].index(piece_idx)
    moving = list(cells[r][c])[idx:]  # piece_idx 위의 말들만 이동
    cells[r][c] = deque(list(cells[r][c])[:idx])  # 아래에 남긴 말들 유지
    '''


    # 빨간색이면 이동 순서 뒤집기
    if board[nr][nc] == 1:
        moving.reverse()

    # 이동한 말을 새 칸에 쌓고 위치 업데이트
    for p in moving: 
        cells[nr][nc].append(p)
        pieces[p][0], pieces[p][1] = nr, nc

    # 4개 이상 쌓이면 종료 신호
    return len(cells[nr][nc]) >= 4

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
