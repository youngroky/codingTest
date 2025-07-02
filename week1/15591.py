# https://www.acmicpc.net/problem/15591
# 크루스칼 + DSU + 오프라인 쿼리

import sys
input = sys.stdin.readline

# 정점 수 n, 쿼리 수 q
n, q = map(int, input().split())

# 간선 정보
edges = []
for _ in range(n - 1):
    u, v, w = map(int, input().split())
    edges.append((u, v, w))

# 질문 정보 + 인덱스(나중에 정답 저장하려고)
questions = []
for i in range(q):
    k, v = map(int, input().split())
    questions.append((k, v, i))

# 간선과 쿼리를 유사도 기준으로 내림차순 정렬
edges.sort(key=lambda x: -x[2])      # 유사도 큰 순서
questions.sort(key=lambda x: -x[0])    # 쿼리 기준 유사도 큰 순서

# Union-Find용 자료 구조
parent = list(range(n + 1))  # 자기 자신이 루트
size = [1] * (n + 1) # 각 집합 크기

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

# union 연산 (크기 기준으로 병합)
def union(a, b):
    a = find(a)
    b = find(b)
    if a == b:
        return
    
    # 작은 집합을 큰 쪽에 합치기 -> 성능 향상 : 깊이가 줄어듬
    if size[a] < size[b]:
        a, b = b, a
    parent[b] = a
    size[a] += size[b]

# 결과 저장용 배열
ans = [0] * q
# 지금까지 처리한 간선 저장
idx = 0 

# 쿼리 하나씩 처리
for k, p, qi in questions:
    # 유사도 ≥ k인 간선들만 처리한다.
    while idx < len(edges) and edges[idx][2] >= k:
        u, v, w = edges[idx]
        union(u, v)
        idx += 1
    # 쿼리 결과 저장: p와 연결된 노드 수 - 1
    ans[qi] = size[find(p)] - 1

# 결과 출력
for a in ans:
    print(a)