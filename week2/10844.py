# https://www.acmicpc.net/problem/10844

import sys
input = sys.stdin.readline

digit = int(input())

# dp[i][j] : 길이가 i이고, 마지막 숫자가 j인 계단 수의 개수
dp = [[0] * 10 for _ in range(digit + 1)]

# 길이가 1일 때 1~9는 1개씩 가능
for i in range(1, 10):
    dp[1][i] = 1

for i in range(2, digit + 1):
    for j in range(10):
        if j > 0:
            dp[i][j] += dp[i - 1][j - 1]
        if j < 9:
            dp[i][j] += dp[i - 1][j + 1]
        dp[i][j] %= 1_000_000_000

print(sum(dp[digit]) % 1_000_000_000)

'''

digit = int(input())

def count(num,now_digit):
    total=0
    if now_digit == digit:
        return 1
    if (num +1) < 10:
        total += count(num+1,now_digit+1)
        
    if (num -1) > -1:
        total += count(num-1,now_digit+1)
    return total

answer = 0
for i in range(1,10):
    answer += count(i,1)

print(answer % 1000000000)

'''