# https://www.acmicpc.net/problem/14529

# 모든 가능한 직사각형들을 검사하면서
#   - 딱 두 가지 색만 포함하고
#   - 그 중 하나는 연결된 덩어리가 1개이고, 다른 하나는 2개 이상인지 확인
#   - 해당 조건을 만족하면 정답 +1
#   - 단, 이미 더 큰 PCL에 포함되어 있는 건 제외

# 1. 가능한 모든 직사각형 영역을 순회
# → N×N 보드니까 가능한 모든 사각형을 전부 다 보면서 확인합니다.
# → 단, 넓이 큰 것부터 확인해야 중복되는 작은 PCL을 나중에 빼기 쉬움

# 2. 사각형 안에 있는 색이 2개인지 확인

# 3. 색마다 덩어리 개수를 계산
# → BFS로 연결된 같은 색 칸을 하나의 덩어리

# 4. 이미 더 큰 직사각형으로 인정된 경우는 skip
# → 중복 제거

import sys
from collections import deque
input = sys.stdin.readline

N = int(input().strip())
board = [list(input().strip()) for _ in range(N)]
# 사각형인지 확인하는 벡터 
Mark = [[[[False]*N for _ in range(N)] for _ in range(N)] for _ in range(N)]
ans = 0

dy = [1,-1,0,0]
dx = [0,0,1,-1]

# 색이 3개 이상이면 바로 None 반환
# 색마다 연결된 블록(component)의 개수를 BFS
def count_components(y1, x1, y2, x2):
    # 방문 배열
    seen = [[False]*N for _ in range(N)]
    colors = {}
    for i in range(y1, y2+1):
        for j in range(x1, x2+1):
            colors[board[i][j]] = colors.get(board[i][j], 0) + 1
            if len(colors) > 2:
                return None
    # 덩어리 개수 저장
    comps = {}
    for c in colors.keys():
        comps[c] = 0

    for i in range(y1, y2+1):
        for j in range(x1, x2+1):
            if not seen[i][j]:
                c = board[i][j]
                comps[c] += 1
                # BFS 같은 색, 같은 칸이면 추가
                q = deque([(i,j)])
                seen[i][j] = True
                while q:
                    y, x = q.popleft()
                    for d in range(4):
                        ny, nx = y+dy[d], x+dx[d]
                        if y1 <= ny <= y2 and x1 <= nx <= x2 and not seen[ny][nx] and board[ny][nx] == c:
                            seen[ny][nx] = True
                            q.append((ny,nx))
    return comps

# 넓이 큰 순서대로 순회
for height in range(N, 0, -1):
    for width in range(N, 0, -1):
        for y1 in range(0, N-height+1):
            y2 = y1 + height - 1
            for x1 in range(0, N-width+1):
                x2 = x1 + width - 1

                # 포함된 사각형 이미 PCL이면 skip
                skip = False
                for yy1 in range(0, y1+1):
                    for yy2 in range(y2, N):
                        for xx1 in range(0, x1+1):
                            for xx2 in range(x2, N):
                                if Mark[yy1][xx1][yy2][xx2]:
                                    skip = True
                                    break
                            if skip: break
                        if skip: break
                    if skip: break
                if skip: continue

                comps = count_components(y1, x1, y2, x2)
                if comps is None or len(comps) != 2:
                    continue

                cnts = list(comps.values())

                # 덩어리가 1개인 색이 정확히 하나인지 확인
                if cnts.count(1) == 1:
                    
                    # 나머지 색 중 덩어리가 2개 이상인 게 하나라도 있는지 확인
                    for c in cnts:
                        if c != 1 and c >= 2:
                            # 조건 만족 → PCL
                            ans += 1
                            Mark[y1][x1][y2][x2] = True
                            break

print(ans)


