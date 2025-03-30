import numpy as np
from itertools import combinations

def flip_3x3(grid, x, y):
    """
    指定した座標 (x, y) を中心に 3x3 の領域を反転させる
    """
    for i in range(max(0, x-1), min(4, x+2)):
        for j in range(max(0, y-1), min(4, y+2)):
            grid[i][j] = 1 - grid[i][j]  # 0 ⇄ 1 を反転

# 目標のパターン（ゴール状態）
goal = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])

# 現在の状態（初期状態）
current = np.array([
    [1, 0, 1, 1],
    [0, 0, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 1]
])

# 4x4 の全ての座標をリスト化
positions = [(i, j) for i in range(4) for j in range(4)]

# 3回の選択で目標の状態にする
solution = None
for moves in combinations(positions, 3):
    test_grid = current.copy()
    
    for x, y in moves:
        flip_3x3(test_grid, x, y)
    
    if np.array_equal(test_grid, goal):
        solution = [(x+1, y+1) for x, y in moves]  # 1行目から数えるように調整
        break

print("Solution (3 moves):", solution)
