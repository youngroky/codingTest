# https://www.acmicpc.net/problem/16639
# DP

import sys
input = sys.stdin.readline

n = int(input())
exp = input().strip()

nums = []  # 숫자만 저장할 리스트
ops = []   # 연산자만 저장할 리스트

for i in range(n):
    if i % 2 == 0:
        nums.append(int(exp[i]))  # 짝수 번째는 숫자
    else:
        ops.append(exp[i])        # 홀수 번째는 연산자

length = len(nums)  # 숫자의 개수

# DP 테이블 초기화
hi = []  # 최댓값 저장용
lo = []  # 최솟값 저장용

for i in range(length):
    hi_row = []
    lo_row = []
    for j in range(length):
        hi_row.append(-float('inf'))  # 아주 작은 값으로 초기화
        lo_row.append(float('inf'))   # 아주 큰 값으로 초기화
    hi.append(hi_row)
    lo.append(lo_row)


# hi[i][j]: 수식 nums[i] ~ nums[j] 사이에서 만들 수 있는 최댓값
# lo[i][j]: 수식 nums[i] ~ nums[j] 사이에서 만들 수 있는 최솟값
# 최소값을 구해야 하는 이유 : (최대값)-(최대값) -> (최대값) - (최소값), 이런경우가 존해한다. 즉 음수가 나올 수 있기 때문

for i in range(length):
    hi[i][i] = lo[i][i] = nums[i]

for gap in range(1, length): 
    for start in range(length - gap):
        end = start + gap
        # mid 는 나눌 연산자 지점을 의미
        for mid in range(start, end):
            a, b = hi[start][mid], lo[start][mid]
            c, d = hi[mid+1][end], lo[mid+1][end]
            op = ops[mid]
            if op == '+':
                candidates = [a + c, b + d]
            elif op == '-':
                candidates = [a - d, b - c]
            else:
                candidates = [a * c, a * d, b * c, b * d]
            # * -> 개별인자로 분리해서 넘김
            hi[start][end] = max(hi[start][end], *candidates)
            lo[start][end] = min(lo[start][end], *candidates)

print(hi[0][length - 1])