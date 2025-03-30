import numpy as np
from itertools import combinations

# 3x3を裏返す関数
def flip_3x3(grid, x, y):
    rows, cols = grid.shape
    for i in range(max(0, x-1), min(x+2, rows)):
        for j in range(max(0, y-1), min(y+2, cols)):
            grid[i, j] = 1 - grid[i, j]  # 0 <=> 1

# パズルを解く関数
def solve_puzzle(current, goal, max_moves):
    rows, cols = current.shape
    positions = [(i, j) for i in range(rows) for j in range(cols)]
    
    # max_moves回で解くためのすべての選択肢を試す
    for moves in combinations(positions, max_moves):
        test_grid = current.copy()  # 現在のグリッドをコピー
        
        # 選択した位置を3x3裏返す
        for x, y in moves:
            flip_3x3(test_grid, x, y)
        
        # ゴールと一致するか確認
        if np.array_equal(test_grid, goal):
            # 結果を1-basedで表示
            return [(x+1, y+1) for x, y in moves]  # 1から始まるインデックスに変換
    
    return None  # 解が見つからない場合

# ゴールと現在の状態（4x4の場合の例）
goal_4x4 = np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])

current_4x4 = np.array([
    [1, 0, 1, 1],
    [0, 0, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 1]
])

# ゴールと現在の状態（5x5の場合の例）
goal_5x5 = np.array([
    [0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0],
    [0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0],
    [1, 1, 0, 1, 0]
])

current_5x5 = np.array([
    [1, 0, 1, 1, 0],
    [0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 1, 1],
    [1, 1, 1, 0, 0]
])

# ゴールと現在の状態（6x6の場合の例）
goal_6x6 = np.array([
    [0, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1],
    [0, 1, 0, 1, 0, 0],
    [1, 0, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 0]
])

current_6x6 = np.array([
    [0, 1, 1, 0, 1, 1],
    [1, 0, 0, 1, 0, 0],
    [1, 0, 0, 1, 1, 1],
    [0, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 1],
    [0, 0, 0, 1, 0, 1]
])

# 4x4のパズルを3回の動きで解く
solution_4x4 = solve_puzzle(current_4x4, goal_4x4, 3)
print("Solution for 4x4:", solution_4x4)

# 5x5のパズルを4回の動きで解く
solution_5x5 = solve_puzzle(current_5x5, goal_5x5, 4)
print("Solution for 5x5:", solution_5x5)

# 6x6のパズルを5回の動きで解く
solution_6x6 = solve_puzzle(current_6x6, goal_6x6, 5)
print("Solution for 6x6:", solution_6x6)
