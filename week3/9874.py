# https://www.acmicpc.net/problem/9874

import sys
sys.setrecursionlimit(10000)

N = int(input())
wormholes = [tuple(map(int, input().split())) for _ in range(N)]

# next_on_right[i] = i에서 +x 방향으로 바로 오른쪽에 있는 웜홀 번호 (같은 y선상)
next_on_right = [None] * N

for i in range(N):
    x_i, y_i = wormholes[i]
    for j in range(N):
        x_j, y_j = wormholes[j]
        if y_i == y_j and x_j > x_i:
            if next_on_right[i] is None or x_j < wormholes[next_on_right[i]][0]:
                next_on_right[i] = j

# pairs[i] = i번 웜홀과 연결된 웜홀 번호
pairs = [-1] * N

def has_cycle():
    for start in range(N):
        pos = start
        for _ in range(N):  # N번 넘게 돌면 무한 루프
            partner = pairs[pos]
            if partner == -1:
                break
            pos = next_on_right[partner]
            if pos is None:
                break
        else:
            # N번 반복했는데도 빠져나오지 못하면 사이클
            return True
    return False

def count_pairs():
    # 아직 짝이 안지어진 첫 번째 웜홀 찾기
    for i in range(N):
        if pairs[i] == -1:
            break
    else:
        # 모두 짝 지어진 경우, 사이클 여부 체크
        return 1 if has_cycle() else 0

    total = 0
    for j in range(i + 1, N):
        if pairs[j] == -1:
            pairs[i] = j
            pairs[j] = i
            total += count_pairs()
            pairs[i] = pairs[j] = -1
    return total

print(count_pairs())