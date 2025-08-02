# https://www.acmicpc.net/problem/16918


# 봄버맨은 크기가 R×C인 직사각형 격자판 위에서 살고 있다. 격자의 각 칸은 비어있거나 폭탄이 들어있다.
# 폭탄이 있는 칸은 3초가 지난 후에 폭발하고, 폭탄이 폭발한 이후에는 폭탄이 있던 칸이 파괴되어 빈 칸이 되며, 인접한 네 칸도 함께 파괴된다. 
# 즉, 폭탄이 있던 칸이 (i, j)인 경우에 (i+1, j), (i-1, j), (i, j+1), (i, j-1)도 함께 파괴된다. 
# 만약, 폭탄이 폭발했을 때, 인접한 칸에 폭탄이 있는 경우에는 인접한 폭탄은 폭발 없이 파괴된다. 따라서, 연쇄 반응은 없다.
# 봄버맨은 폭탄에 면역력을 가지고 있어서, 격자판의 모든 칸을 자유롭게 이동할 수 있다. 봄버맨은 다음과 같이 행동한다.

# 1. 가장 처음에 봄버맨은 일부 칸에 폭탄을 설치해 놓는다. 모든 폭탄이 설치된 시간은 같다.
# 2. 다음 1초 동안 봄버맨은 아무것도 하지 않는다.
# 3. 다음 1초 동안 폭탄이 설치되어 있지 않은 모든 칸에 폭탄을 설치한다. 즉, 모든 칸은 폭탄을 가지고 있게 된다. 폭탄은 모두 동시에 설치했다고 가정한다.
# 4. 1초가 지난 후에 3초 전에 설치된 폭탄이 모두 폭발한다.
# 5. 3과 4를 반복한다.
# 폭탄을 설치해놓은 초기 상태가 주어졌을 때, N초가 흐른 후의 격자판 상태를 구하려고 한다.

# 4초씩 반복된다.
# 3초 상태와 5초 상태가 이후 계속 번갈아 등장하기 때문



import sys
from collections import deque
input = sys.stdin.readline

R, C, N = map(int, input().split())
grid = [list(input().strip()) for _ in range(R)]

# 1초: 초기 상태 유지
if N == 1:
    for row in grid:
        print(''.join(row))
    sys.exit(0)

# 방향 벡터
dirs = [(1,0),(-1,0),(0,1),(0,-1)]

def boom(board):
    R, C = len(board), len(board[0])
    will = [[False]*C for _ in range(R)]
    q = deque()
    # 폭탄이 있는 칸들 기록
    for i in range(R):
        for j in range(C):
            if board[i][j] == 'O':
                will[i][j] = True
                q.append((i,j))

    # 새 격자판: 전부 폭탄으로 가득 채운 상태
    newb = [['O']*C for _ in range(R)]

    # 폭탄이 터짐: 자기 위치 + 상하좌우를 '.' 처리
    while q:
        i, j = q.popleft()
        newb[i][j] = '.'
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < R and 0 <= nj < C:
                newb[ni][nj] = '.'
    return newb

# 짝수 초: full bomb
full = [['O']*C for _ in range(R)]

# N이 짝수
if N % 2 == 0:
    for row in full:
        print(''.join(row))
    sys.exit(0)

# N > 1이고 홀수 → N % 4 == 3 or 1

# 첫 explosion 패턴
e1 = boom(grid)

# 두번째 explosion 패턴: full에서 폭발
e2 = boom(e1)

if N % 4 == 3:
    res = e1
else:  # N % 4 == 1
    res = e2

for row in res:
    print(''.join(row))