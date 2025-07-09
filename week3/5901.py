# https://www.acmicpc.net/problem/5901

import sys
import heapq
from itertools import permutations
input = sys.stdin.readline

# 일단 입력을 받아야된다. N:노드,M:길,K:마켓
N, M, K = map(int, input().split())

# 마켓 위치 입력
market = []
for _ in range(K):
    market.append(int(input()))

is_market = [False] * (N + 1)
for m in market:
    is_market[m] = True

# 길 입력받아서 그래프 완성
graph = [[] for _ in range(N+1)]
for _ in range(M):
    a, b, c = map(int, input().split())
    graph[a].append((b, c))
    graph[b].append((a, c))

# 다익스트라 알고리즘 -> 우선순위 큐를 통해 구현
def dijkstra(start):
    dist = [10_000] * (N+1)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        cost, node = heapq.heappop(pq)
        # 그냥 가는거 보다 더 짧은게 있으면 패스
        if cost > dist[node]:
            continue
        for next_node, w in graph[node]:
            new_cost = cost + w
            # 더 작으면 넣기
            if dist[next_node] > new_cost:
                dist[next_node] = new_cost
                heapq.heappush(pq, (new_cost, next_node))
    return dist

# 각 마켓에서 모든 노드까지 계산
d_market = [dijkstra(m) for m in market]

# 마켓끼리 이동할 떄 최단 경로를 미리 구해놓음 -> 속도 증가를 위해서
# 이떄 마켓 순서 0,1,2
market_dist = [[0]*(K) for _ in range(K)]
for i in range(K):
    for j in range(K):
        market_dist[i][j] = d_market[i][market[j]]

# 마켓 순서대로 돌면서 찾기
min_total_dist = 100_000

for farm in range(1,N+1):
    # 마켓있으면 넘김
    if farm in market:
        continue

    # farm → market[i] 거리
    to_markets = [d_market[i][farm] for i in range(K)]

    # 마켓 방문 순열 생성
    for order in permutations(range(K)):
        total = 0
        # 집 → 첫 마켓
        total += to_markets[order[0]]
        # 마켓 간 이동
        for i in range(K - 1):
            total += market_dist[order[i]][order[i+1]]
        # 마지막 마켓 → 집
        total += to_markets[order[-1]]
        min_total_dist = min(min_total_dist, total)

print(min_total_dist)
