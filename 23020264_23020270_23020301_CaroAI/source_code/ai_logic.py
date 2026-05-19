size = 9
win_length = 4
blank = ""
depth = 4
exact = 0
lowerbound = 1
upperbound = 2
T_TABLE = {}
state_visit = 0
# Các biến toàn cục 
ai_marker = "o"
human_marker = "x"
empty_char = "."

def set_marker(ai, human):
    global ai_marker, human_marker
    ai_marker = ai
    human_marker = human
def reset_states():
    global state_visit
    state_visit = 0
def get_states():
    return state_visit
def init_board():
    return [[blank for _ in range(size)] for _ in range(size)]
def check_winner_local(b, r, c):
    player = b[r][c]
    if player == blank: return None 
    axes = [(0, 1),(1, 0),(1, 1),(1, -1)]
    for dr, dc in axes:
        count = 1  
        # Tiến
        for i in range(1, win_length):
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < size and 0 <= nc < size and b[nr][nc] == player:  count += 1
            else:  break    
        # Lùi
        for i in range(1, win_length):
            nr, nc = r - dr * i, c - dc * i
            if 0 <= nr < size and 0 <= nc < size and b[nr][nc] == player: count += 1
            else: break
        if count >= win_length: return player
    return None

def get_local_lines(b, r, c):
    lines = []
    row_line = [b[r][i] if b[r][i] != blank else "." for i in range(max(0, c - 4), min(size, c + 5))]
    lines.append("".join(row_line))
    
    col_line = [b[i][c] if b[i][c] != blank else "." for i in range(max(0, r - 4), min(size, r + 5))]
    lines.append("".join(col_line))
    
    diag1 = []
    for i in range(-4, 5):
        nr, nc = r + i, c + i
        if 0 <= nr < size and 0 <= nc < size:
            diag1.append(b[nr][nc] if b[nr][nc] != blank else ".")
    lines.append("".join(diag1))
    
    diag2 = []
    for i in range(-4, 5):
        nr, nc = r + i, c - i
        if 0 <= nr < size and 0 <= nc < size:
            diag2.append(b[nr][nc] if b[nr][nc] != blank else ".")
    lines.append("".join(diag2))

    return lines

def check_winner_logic(b):
    for r in range(size):
        for c in range(size):
            if b[r][c] ==blank: continue
            player =b[r][c]
            
            directions = [(0, 1),(1, 0),(1, 1),(1, -1)]
            for dr, dc in directions:
                win = True
                for i in range(1, win_length):
                    nr, nc = r + dr * i, c + dc * i
                    if nr <0 or nr >=size or nc <0 or nc >=size or b[nr][nc] !=player:
                        win =False
                        break
                if win: return player
    return None

# Hàm sinh nước đi
def get_ordered_moves(b):
    # Kiểm tra xem có phải bàn cờ trống không
    empty_board =True
    for r in range(size):
        for c in range(size):
            if b[r][c] !=blank:
                empty_board =False
                break
        if not empty_board: break     
    if empty_board:
        return [(size//2, size//2)] # Đánh ngay vào giữa bàn cờ 
     
    moves = set()
    for r in range(size):
        for c in range(size):
            if b[r][c] != blank:
                for dr in [-2,-1,0, 1, 2]:
                    for dc in [-2,-1, 0, 1, 2]:
                        nr, nc =r + dr,c + dc
                        if 0 <= nr < size and 0 <= nc < size and b[nr][nc] == blank:
                            moves.add((nr, nc))
                            
    if not moves: return [] # Bàn cờ đầy, không còn nước đi hợp lệ

    def move_score(move):
        r, c = move
        score = 0
        # Tính điểm tấn công
        b[r][c] = ai_marker
        lines_ai = get_local_lines(b, r, c)
        for line in lines_ai:
            score +=abs(evaluate_string(line, ai_marker, human_marker))
        # Tính điểm phòng thủ
        b[r][c] = human_marker
        lines_hu = get_local_lines(b, r, c)
        for line in lines_hu:
            score +=abs(evaluate_string(line, ai_marker,human_marker))      
        b[r][c] =blank
        return score
    ordered_moves = sorted(list(moves),key=move_score,reverse=True)
    return ordered_moves[:12] # Chỉ lấy 12 nước đi tốt nhất

def evaluate_string(line_str, ai, hu):
    score = 0
    # Máy tấn công
    if ai * 4 in line_str: score += 100000 
    if f"{empty_char}{ai*3}{empty_char}" in line_str: score += 10000 
    if f"{hu}{ai*3}{empty_char}" in line_str: score += 1000
    if f"{empty_char}{ai*3}{hu}" in line_str: score += 1000
    if f"{empty_char}{ai*2}{empty_char}" in line_str: score += 100
    # Máy phòng thủ
    if hu * 4 in line_str: score -= 100000 
    if f"{empty_char}{hu*3}{empty_char}" in line_str: score -= 15000 
    if f"{ai}{hu*3}{empty_char}" in line_str: score -= 1500
    if f"{empty_char}{hu*3}{ai}" in line_str: score -= 1500
    if f"{empty_char}{hu*2}{empty_char}" in line_str: score -= 150
    return score
 
def evaluate_board(b):
    score = 0
    def to_str(cells):
        return "".join([c if c != blank else empty_char for c in cells])
    for i in range(size):
        row_str = to_str(b[i])
        col_str = to_str([b[r][i] for r in range(size)])
        score += evaluate_string(row_str, ai_marker, human_marker)
        score += evaluate_string(col_str, ai_marker, human_marker)
    for p in range(size * 2 - 1):
        diag1 = [b[r][p-r] for r in range(max(0, p-size + 1), min(size, p + 1))]
        if len(diag1) >= win_length:
            score += evaluate_string(to_str(diag1), ai_marker, human_marker)
            
        diag2 = [b[r][size-1-(p-r)] for r in range(max(0, p-size+1), min(size, p+1))]
        if len(diag2) >= win_length:
            score += evaluate_string(to_str(diag2), ai_marker, human_marker)
    return score
# pruning phân tách Minimax và Alpha-Beta
def minimax(b, depth, alpha, beta, maximize, last_r=None, last_c=None, pruning=True):
    global state_visit, ai_marker,human_marker, T_TABLE
    state_visit +=1 
    board_hash = tuple(tuple(row) for row in b)
    
    # Đọc thông tin từ table dựa trên chế độ cắt nhánh
    if board_hash in T_TABLE:
        entry = T_TABLE[board_hash]
        if entry['depth'] >=depth:
            if pruning:
                if entry['flag'] ==exact: return entry['value']
                elif entry['flag'] ==lowerbound: alpha =max(alpha, entry['value'])
                elif entry['flag'] == upperbound: beta =min(beta, entry['value'])
                if alpha >= beta: return entry['value']
            else:
                if entry['flag'] == exact: return entry['value']
    original_alpha = alpha
 
    if last_r is not None and last_c is not None:
        winner = check_winner_local(b, last_r, last_c)
        if winner == ai_marker: return 100000 + depth
        if winner == human_marker: return -100000 - depth
    
    moves = get_ordered_moves(b)
    if depth == 0 or not moves: return evaluate_board(b) 
    best_value = -float('inf') if maximize else float('inf')
    
    if maximize:
        for r, c in moves:
            b[r][c] = ai_marker
            # đệ quy chuyển sang lượt của đối thủ
            eval_score = minimax(b, depth - 1, alpha, beta, False, r, c, pruning)
            b[r][c] = blank
            best_value = max(best_value, eval_score)
            if pruning:
                alpha = max(alpha, best_value)
                if beta <= alpha: break 
    else:
        for r, c in moves:
            b[r][c] = human_marker
            # đệ quy chuyển sang lượt của AI
            eval_score = minimax(b, depth - 1, alpha, beta, True, r, c, pruning)
            b[r][c] = blank
            best_value = min(best_value, eval_score)
            if pruning:
                beta = min(beta, best_value)
                if beta <= alpha: break 
    if pruning:
        flag = exact
        if best_value <= original_alpha:
            flag = upperbound
        elif best_value >= beta:
            flag = lowerbound
    else:
        flag = exact 
 
    T_TABLE[board_hash] = {
        'value': best_value,
        'depth': depth,
        'flag': flag
    }
    
    return best_value