# https://www.acmicpc.net/problem/10021
# 최소 스패닝 트리 + 필터링

import sys
import heapq
input = sys.stdin.readline

# 입력: n 필드 수, c 최소 설치 비용
n, c = map(int, input().split())

pts = []
for _ in range(n):
    x, y = map(int, input().split())
    pts.append((x, y))

edges = []
for i in range(n):
    x1, y1 = pts[i]
    for j in range(i + 1, n):
        x2, y2 = pts[j]
        d = (x1 - x2)**2 + (y1 - y2)**2
        if d >= c:
            # 리스트에 모으지 않고 바로 힙에 넣음
            heapq.heappush(edges, (d, i, j))  

# 유니온파인드 구조 초기화
parent = list(range(n))

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # 경로 압축
    return parent[x]

def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False
    parent[rb] = ra
    return True

# 크루스칼 MST
cnt = 0     # 연결된 간선 수
cost = 0    # 누적 비용
while len(edges) > 0 and cnt < n - 1:
    d, u, v = heapq.heappop(edges)
    if union(u, v):
        cost += d
        cnt += 1

# 전체 연결 여부 확인
if cnt == n - 1:
    print(cost)
else:
    print(-1)
