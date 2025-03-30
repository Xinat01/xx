import tkinter as tk
import numpy as np
from itertools import combinations

# メインのウィンドウを作成
root = tk.Tk()
root.title("パズルゲーム")
root.geometry("800x500")

# フレームの作成
main_frame = tk.Frame(root)
main_frame.pack()

# 左側（ゴール状態）フレーム
goal_frame = tk.Frame(main_frame)
goal_frame.grid(row=0, column=0, padx=20)

# 右側（現在の状態）フレーム
current_frame = tk.Frame(main_frame)
current_frame.grid(row=0, column=1, padx=20)

# 下側（解答表示）フレーム
answer_frame = tk.Frame(main_frame)
answer_frame.grid(row=1, columnspan=2)

# ボタンリスト
buttons = []
goal_labels = []

# ゴール状態（サンプル）
goal_4x4 = np.array([
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
])

goal_5x5 = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

goal_6x6 = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

# 現在の状態
current_4x4 = np.copy(goal_4x4)
current_5x5 = np.copy(goal_5x5)
current_6x6 = np.copy(goal_6x6)

# 解答のステップを保持するリスト
steps = []
max_moves = 0  # 初期化
current_size = 4  # 初期のサイズ（4x4）

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
    
    return []  # 解が見つからない場合

# セルの色を反転する関数（見本のクリックで現在の状態を変更）
def toggle_color_on_current(row, col, current_state):
    current_color = buttons[row][col]["bg"]
    new_color = "white" if current_color == "black" else "black"
    buttons[row][col].config(bg=new_color)
    current_state[row][col] = 1 - current_state[row][col]  # 色を反転させる（0<=>1）

# セルの色を反転する関数（見本のクリックで見本自体も色変更）
def toggle_color_on_goal(row, col, goal_state):
    current_color = goal_labels[row][col]["bg"]
    new_color = "white" if current_color == "black" else "black"
    goal_labels[row][col].config(bg=new_color)
    goal_state[row][col] = 1 - goal_state[row][col]  # 色を反転させる（0<=>1）

# グリッド作成（見本のパズル & 現在のパズル）
def create_grid(size, goal_state, current_state):
    global buttons, goal_labels, current_size
    # 既存のボタン・ラベルを削除
    for widget in goal_frame.winfo_children():
        widget.destroy()
    for widget in current_frame.winfo_children():
        widget.destroy()

    buttons = []
    goal_labels = []
    
    # 見本（goal_state）を作成
    for r in range(size):
        row_buttons = []
        for c in range(size):
            button = tk.Button(goal_frame, width=3, height=2,
                               bg="black" if goal_state[r, c] == 1 else "white", 
                               command=lambda r=r, c=c: toggle_color_on_goal(r, c, goal_state))  # 見本のボタンも反転
            button.grid(row=r, column=c, padx=2, pady=2)
            row_buttons.append(button)
        goal_labels.append(row_buttons)

    # 現在のパズル（current_state）を作成
    for r in range(size):
        row_buttons = []
        for c in range(size):
            button = tk.Button(current_frame, width=3, height=2,
                               bg="black" if current_state[r, c] == 1 else "white", 
                               command=lambda r=r, c=c: toggle_color_on_current(r, c, current_state))  # 現在の状態のボタン反転
            button.grid(row=r, column=c, padx=2, pady=2)
            row_buttons.append(button)
        buttons.append(row_buttons)

    current_size = size  # 現在のサイズを更新

# すべてのマス目を白に戻す関数
def reset_grid():
    global current_4x4, current_5x5, current_6x6
    # 見本（goal）をすべて白に強制的にリセット
    goal_4x4.fill(0)
    goal_5x5.fill(0)
    goal_6x6.fill(0)
    
    # 現在の状態をすべて白に強制的にリセット
    if current_size == 4:
        current_4x4.fill(0)
        create_grid(4, goal_4x4, current_4x4)
    elif current_size == 5:
        current_5x5.fill(0)
        create_grid(5, goal_5x5, current_5x5)
    elif current_size == 6:
        current_6x6.fill(0)
        create_grid(6, goal_6x6, current_6x6)

# 解答ステップを表示する関数
def show_steps():
    global steps  # グローバル変数として使用

    # 一旦ステップの表示をリセット
    for widget in answer_frame.winfo_children():
        widget.destroy()

    # 解答計算結果を取得
    if current_size == 4:
        solution = solve_puzzle(current_4x4, goal_4x4, max_moves)
    elif current_size == 5:
        solution = solve_puzzle(current_5x5, goal_5x5, max_moves)
    elif current_size == 6:
        solution = solve_puzzle(current_6x6, goal_6x6, max_moves)
    
    # 解が見つかった場合、計算結果を表示
    if solution:
        steps = [f"Move{idx+1}: {step}" for idx, step in enumerate(solution)]
    else:
        steps = ["解が見つかりませんでした"]

    # 計算結果を表示
    for i, step in enumerate(steps):
        step_label = tk.Label(answer_frame, text=step, fg="red", font=("Arial", 12, "bold"))
        step_label.grid(row=0, column=i, padx=5, pady=5)  # 0行目、各列に順番に表示

# グリッドのサイズと初期状態を選択
def set_grid_size(size):
    global steps  # 解答リセット
    steps = []  # ステップをリセット
    if size == 4:
        create_grid(4, goal_4x4, current_4x4)
    elif size == 5:
        create_grid(5, goal_5x5, current_5x5)
    elif size == 6:
        create_grid(6, goal_6x6, current_6x6)

# サイズ選択ボタン
size_frame = tk.Frame(root)
size_frame.pack()

button_4x4 = tk.Button(size_frame, text="4x4", command=lambda: set_grid_size(4))
button_4x4.pack(side=tk.LEFT, padx=5)

button_5x5 = tk.Button(size_frame, text="5x5", command=lambda: set_grid_size(5))
button_5x5.pack(side=tk.LEFT, padx=5)

button_6x6 = tk.Button(size_frame, text="6x6", command=lambda: set_grid_size(6))
button_6x6.pack(side=tk.LEFT, padx=5)

# 最大回数を設定する関数
def set_max_moves(moves):
    global max_moves
    max_moves = moves

# 行動回数を設定するフレーム（チェックボックス式）
moves_frame = tk.Frame(root)
moves_frame.pack()

move_buttons = []
for i in range(1, 6):
    move_button = tk.Button(moves_frame, text=str(i), command=lambda i=i: set_max_moves(i), bg="lightgray")
    move_button.pack(side=tk.LEFT, padx=5)
    move_buttons.append(move_button)

# 解答表示ボタン
answer_button = tk.Button(root, text="解答を表示", command=show_steps)
answer_button.pack()

# すべてのマス目を白に戻すボタン
reset_button = tk.Button(root, text="リセット", command=reset_grid)
reset_button.pack()

# 最初に4x4グリッドを表示
set_grid_size(4)

# アプリケーションを実行
root.mainloop()
