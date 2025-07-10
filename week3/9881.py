# https://www.acmicpc.net/problem/9881

# N개의 언덕, 높이는 0~100
# 언덕의 차이가 17보다 크면 안됨 17까지 가능
# 언덕 하나를 줄이면 나머지 하나에 추가해야됨 -> (줄인것)^2 * 2 = 비용

import sys
input = sys.stdin.readline

# N 개수
N = int(input())
# 언덕 높이
mountain = [ int(input()) for _ in range(N)]

min_cost = float('inf')

for low in range(0, 84):  # high = low + 17
    high = low + 17
    cost = 0
    for h in mountain:
        if h < low:
            cost += (low - h) ** 2
        elif h > high:
            cost += (h - high) ** 2
    min_cost = min(min_cost, cost)

print(min_cost)