# https://www.acmicpc.net/problem/14466

import sys
from collections import deque
input = sys.stdin.readline

# 입력: N x N 격자, K 마리 소, R 개의 길 정보
N, K, R = map(int, input().split())

# roads[x][y][d]: (x, y)에서 방향 d(0~3)로 갈 때 '길이 막혀있는가' 여부
# 방향: 0=상, 1=하, 2=좌, 3=우
roads = []
for i in range(N + 1):
    row = []
    for j in range(N + 1):
        cell = [False, False, False, False]  # 처음엔 길이 없음 (막혀있지 않음)
        row.append(cell)
    roads.append(row)

# 방향 이동 정의: 상, 하, 좌, 우
dirs = [(-1,0),(1,0),(0,-1),(0,1)]

# 길 정보 입력
for _ in range(R):
    r1, c1, r2, c2 = map(int, input().split())

    # (r1, c1)에서 (r2, c2)로 가는 방향 확인
    # enumerate()는 리스트의 인덱스와 값을 동시에 꺼내줍
    for d, (dr, dc) in enumerate(dirs):
        if r1+dr == r2 and c1+dc == c2:
            # (r1, c1)에서 방향 d로 길이 막힘
            roads[r1][c1][d] = True
            # (r2, c2)에서 반대 방향(d^1)으로도 막힘 - 비트연산으로 구현
            roads[r2][c2][d^1] = True
            break

# 소 위치 입력
cows = []
for _ in range(K):
    x, y = map(int, input().split())
    cows.append((x, y))

# 두 소 사이에 길을 건너지 않고 도달 가능한지 확인 (BFS 탐색)
def can_meet(sx, sy, tx, ty):
    visited = []
    for i in range(N + 1):
        row = []
        for j in range(N + 1):
            row.append(False)
        visited.append(row)
        
    dq = deque([(sx, sy)])  # 시작 위치 큐에 넣기
    visited[sx][sy] = True

    while dq:
        # 맨앞 꺼내기
        x, y = dq.popleft()
        # 목적지 도달 시 True 반환
        if (x, y) == (tx, ty):
            return True

        # 4방향으로 이동
        for d, (dr, dc) in enumerate(dirs):
            nx, ny = x+dr, y+dc

            # 범위 밖이면 skip
            if not (1 <= nx <= N and 1 <= ny <= N):
                continue

            # 이미 방문한 곳이면 skip
            if visited[nx][ny]:
                continue

            # 길이 있으면 그 방향으로 이동 못함
            if roads[x][y][d]:
                continue

            # 이동 가능하므로 방문 처리 및 큐에 추가
            visited[nx][ny] = True
            dq.append((nx, ny))

    # 도달하지 못하면 False
    return False

# 만날 수 없는 소 쌍의 수 세기
ans = 0
for i in range(K):
    x1, y1 = cows[i]
    for j in range(i+1, K):
        x2, y2 = cows[j]
        if not can_meet(x1, y1, x2, y2):  # 길 안 건너고 만날 수 없으면 카운트 증가
            ans += 1

# 결과 출력
print(ans)