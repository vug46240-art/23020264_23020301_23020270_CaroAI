# game_rules.py
import ai_logic

def is_board_full(board):
    #Kiểm tra trạng thái hòa
    for r in range(ai_logic.size):
        for c in range(ai_logic.size):
            if board[r][c] == ai_logic.blank:
                return False
    return True

def get_winning_path(b):
    for r in range(ai_logic.size):
        for c in range(ai_logic.size):
            if b[r][c] == ai_logic.blank: continue
            player = b[r][c]
            directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
            for dr, dc in directions:
                win = True
                path = [(r, c)]
                for i in range(1, ai_logic.win_length):
                    nr, nc = r + dr * i, c + dc * i
                    if nr < 0 or nr >= ai_logic.size or nc < 0 or nc >= ai_logic.size or b[nr][nc] != player:
                        win = False
                        break
                    path.append((nr, nc))
                if win: return path
    return []