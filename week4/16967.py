# https://www.acmicpc.net/problem/16967


# 	배열 A를 복사해서 B 배열의 왼쪽 위에 그대로 붙임
# 	같은 A 배열을 (X, Y) 만큼 아래 오른쪽으로 이동해서, B에 다시 덧붙임
# 	겹치는 칸은 두 A 값이 더해져서 B 배열에 저장됨

# 겹치지 않은 부분 → 그냥 B의 값을 A로 복사

# 겹치는 부분:
# B[i][j] = A[i][j] + A[i-X][j-Y]
#  ->  A[i][j] = B[i][j] - A[i-X][j-Y]

# 입력
H, W, X, Y = map(int, input().split())
B = [list(map(int, input().split())) for _ in range(H + X)]

# 복원할 A 배열 초기화
A = [[0] * W for _ in range(H)]

# A 복원
for i in range(H):
    for j in range(W):
        # 겹치는 위치면 이전 A 값 빼주기
        if i >= X and j >= Y:
            A[i][j] = B[i][j] - A[i - X][j - Y]
        else:
            # 겹치지 않으면 그냥 복사
            A[i][j] = B[i][j]

# 결과 출력
for row in A:
    print(*row)