# https://www.acmicpc.net/problem/1800
# 이분 탐색 + 다익스트라 (0–1 BFS 스타일)

# limit 를 구해내는 것이 목표
#   - limit 이상 값은 K 개 이하가 되어야 한다.
#   - limit 이하의 값은 무시
#   - 이렇게 연결까지 되면 완료
import sys
import heapq
input = sys.stdin.readline

def can_install(limit):
    #dist[i] : i 까지 사용한 공짜찬스의 최솟값
    dist = [float('inf')] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    # pq 안에는 사용한 공짜 찬스 수, 현재 노드 번호
    while pq:
        used, u = heapq.heappop(pq)
        if used > dist[u]:
            continue
        # u 에 연결된 것들
        for v, w in adj[u]:
            cost = used + (1 if w > limit else 0)
            if cost < dist[v]:
                dist[v] = cost
                heapq.heappush(pq, (cost, v))
    # k 번보다 적게 썻을 경우에만 유효
    return dist[n] <= k

n, p, k = map(int, input().split())
adj = [[] for _ in range(n + 1)]
max_w = 0

# 그래프 입력 및 최대 비용 기록 양방향으로 모두 저장
for _ in range(p):
    u, v, w = map(int, input().split())
    adj[u].append((v, w))
    adj[v].append((u, w))
    if w > max_w:
        max_w = w

# 가능성있는 것을 좌우로 설정해서 이분 탐색 준비
left, right = 0, max_w
answer = -1

# 이분 탐색: mid가 가능한지 check
while left <= right:
    mid = (left + right) // 2
    if can_install(mid):
        answer = mid       # 가능하면 더 작은 값도 체크
        right = mid - 1
    else:
        left = mid + 1     # 불가능하면 상한 높임

print(answer)