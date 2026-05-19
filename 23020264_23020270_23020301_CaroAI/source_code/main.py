# main.py
import time
from tkinter import *
import ai_logic 
import game_rules # Import file luật chơi vừa tách
# UI
BG_COLOR = "#0D0E15"        
FRAME_BG = "#1A1D2B"        
BTN_NORMAL = "#151821"      
BTN_HOVER = "#232736"       
TEXT_COLOR = "#FFFFFF"      
X_COLOR = "#FF003C"         
O_COLOR = "#00E5FF"         
TITLE_COLOR = "#39FF14"       
BTN_MENU_BG = "#2D1B4E"         
BTN_MENU_FG = "#FFD700"         
BTN_MENU_HOVER = "#4B2875"    
BTN_MENU_ACTIVE_BG = "#FFD700"  
BTN_MENU_ACTIVE_FG = "#000000" 
FONT_UI = ('Consolas', 12, 'bold')
fontboard = ('Consolas', 18, 'bold')

# Biến trạng thái
board = ai_logic.init_board()
current_player = "x"
human_marker = "x"
ai_marker = "o"
current_selected_mode = None  
ai_algorithm = "alphabeta" 
# Các biến ở chế độ kiểm thử
check_mode = False
check_marker = "x" 

def apply_hover_effect(btn):
    btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER) if btn['text'] == "" else None)
    btn.bind("<Leave>", lambda e: btn.config(bg=BTN_NORMAL) if btn['text'] == "" else None)

def apply_menu_hover_effect(btn, mode_name):
    def on_enter(e):
        if current_selected_mode != mode_name:
            btn.config(bg=BTN_MENU_HOVER)
    def on_leave(e):
        if current_selected_mode != mode_name:
            btn.config(bg=BTN_MENU_BG)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

def highlight_winner(path):
    for r, c in path:
        player = board[r][c]
        glow_bg = X_COLOR if player == 'x' else O_COLOR
        buttons[r][c].config(bg=glow_bg, fg="#000000")

def ai_turn():
    global current_player
    label.config(text=f"AI ({ai_marker.upper()}) Đang tính toán", fg=O_COLOR if ai_marker=='o' else X_COLOR)
    window.update()
    ai_logic.reset_states()
    start_time = time.time()
    moves = ai_logic.get_ordered_moves(board)
    use_pruning = True if ai_algorithm == "alphabeta" else False
    best_score = -float('inf')
    best_move = None
    for r, c in moves:
        board[r][c] = ai_marker
        score = ai_logic.minimax(board, ai_logic.depth - 1, -float('inf'), float('inf'), False, r, c, use_pruning) 
        board[r][c] = ai_logic.blank       
        if score > best_score:
            best_score = score
            best_move = (r, c)
            
    end_time = time.time()
    print(f"[{ai_algorithm.upper()}] Nước đi: {best_move} | Điểm số: {best_score} | Số trạng thái: {ai_logic.get_states()} | Thời gian: {end_time - start_time:.4f}s")
    
    if best_move:
        r, c = best_move
        board[r][c] = ai_marker
        color = X_COLOR if ai_marker == 'x' else O_COLOR
        buttons[r][c].config(text=ai_marker.upper(), fg=color, bg=BTN_NORMAL)
        
        if ai_logic.check_winner_logic(board) == ai_marker:
            label.config(text=f"AI ({ai_marker.upper()}) THẮNG!", fg=X_COLOR)
            current_player = None 
            highlight_winner(game_rules.get_winning_path(board)) 
        elif game_rules.is_board_full(board):
            label.config(text="HÒA!", fg=TEXT_COLOR)
            current_player = None
        else:
            current_player = human_marker
            label.config(text=f"Đến lượt bạn ({human_marker.upper()})", fg=O_COLOR if human_marker=='o' else X_COLOR)

def cell_clicked(r, c):
    global current_player, check_marker
    if check_mode:
        if board[r][c] == ai_logic.blank:
            if check_marker == "x":
                board[r][c] = "x"
                buttons[r][c].config(text="X", fg=X_COLOR)
                check_marker = "o" 
                label.config(text="Lượt của (O)", fg=TITLE_COLOR)
            else:
                board[r][c] = "o"
                buttons[r][c].config(text="O", fg=O_COLOR)
                check_marker = "x" 
                label.config(text="Lượt của (X)", fg=TITLE_COLOR)
        else:
            board[r][c] = ai_logic.blank
            buttons[r][c].config(text="", bg=BTN_NORMAL)
        return

    if current_player == human_marker and board[r][c] == ai_logic.blank:
        board[r][c] = human_marker
        color = X_COLOR if human_marker == 'x' else O_COLOR
        buttons[r][c].config(text=human_marker.upper(), fg=color)
        
        if ai_logic.check_winner_logic(board) == human_marker:
            label.config(text=f"BẠN ({human_marker.upper()}) THẮNG!", fg=O_COLOR)
            current_player = None
            highlight_winner(game_rules.get_winning_path(board)) 
        elif game_rules.is_board_full(board):
            label.config(text="HÒA!", fg=TEXT_COLOR)
            current_player = None
        else:
            current_player = ai_marker
            window.after(100, ai_turn)

def start_game(first_player):
    global board, current_player, human_marker, ai_marker, current_selected_mode, check_mode
    if check_mode: toggle_sandbox() 
    
    board = ai_logic.init_board()
    current_selected_mode = first_player  
    
    if first_player == "human":
        btn_human_first.config(bg=BTN_MENU_ACTIVE_BG, fg=BTN_MENU_ACTIVE_FG)
        btn_ai_first.config(bg=BTN_MENU_BG, fg=BTN_MENU_FG)
        human_marker, ai_marker, current_player = "x", "o", "x"
        label.config(text="Đến lượt bạn (X)", fg=X_COLOR)
    else:
        btn_ai_first.config(bg=BTN_MENU_ACTIVE_BG, fg=BTN_MENU_ACTIVE_FG)
        btn_human_first.config(bg=BTN_MENU_BG, fg=BTN_MENU_FG)
        human_marker, ai_marker, current_player = "o", "x", "x"
        label.config(text="AI (X) đi trước", fg=X_COLOR)
        
    ai_logic.set_marker(ai_marker, human_marker)
    for r in range(ai_logic.size):
        for c in range(ai_logic.size):
            buttons[r][c].config(text="", bg=BTN_NORMAL)    
            
    if first_player == "ai":
        window.after(100, ai_turn)

def toggle_algo(algo):
    global ai_algorithm
    ai_algorithm = algo
    if algo == "minimax":
        btn_minimax.config(bg=BTN_MENU_ACTIVE_BG, fg=BTN_MENU_ACTIVE_FG)
        btn_alphabeta.config(bg=BTN_MENU_BG, fg=BTN_MENU_FG)
    else:
        btn_alphabeta.config(bg=BTN_MENU_ACTIVE_BG, fg=BTN_MENU_ACTIVE_FG)
        btn_minimax.config(bg=BTN_MENU_BG, fg=BTN_MENU_FG)

def toggle_sandbox():
    global check_mode, current_player, check_marker
    check_mode = not check_mode
    if check_mode:
        check_marker = "x" 
        btn_sandbox.config(bg=X_COLOR, fg="#000000", text="Chế độ kiểm thử: ON")
        label.config(text="Đánh (X)", fg=TITLE_COLOR)
        current_player = None 
    else:
        btn_sandbox.config(bg=BTN_MENU_BG, fg=BTN_MENU_FG, text="Bật Chế độ kiểm thử")

def run_sandbox_analysis():
    if not check_mode:
        label.config(text="Hãy bật kiểm thử!", fg=X_COLOR)
        return
        
    count_x = sum(row.count("x") for row in board)
    count_o = sum(row.count("o") for row in board)
    
    if count_x > count_o:
        temp_ai = "o"   
    elif count_o > count_x:
        temp_ai = "x"   
    else:
        temp_ai = check_marker 
        
    temp_human = "x" if temp_ai == "o" else "o"
    ai_logic.set_marker(temp_ai, temp_human)
    
    label.config(text=f"AI đang phân tích nước đi kế tiếp cho quân {temp_ai.upper()}...", fg=TITLE_COLOR)
    window.update()
    
    ai_logic.reset_states()
    ai_logic.T_TABLE.clear() 
    start_time = time.time()
    moves = ai_logic.get_ordered_moves(board)
    
    if not moves or (moves == [(ai_logic.size//2, ai_logic.size//2)] and board[ai_logic.size//2][ai_logic.size//2] != ai_logic.blank):
        label.config(text="Bàn cờ đầy hoặc không có nước đi hợp lệ!", fg=X_COLOR)
        return
        
    best_score = -float('inf')
    best_move = None
    use_pruning = True if ai_algorithm == "alphabeta" else False
    
    for r, c in moves:
        board[r][c] = temp_ai
        score = ai_logic.minimax(board, ai_logic.depth - 1, -float('inf'), float('inf'), False, r, c, use_pruning)
        board[r][c] = ai_logic.blank
        if score > best_score:
            best_score = score
            best_move = (r, c)
            
    end_time = time.time()
    
    print(f"\n[{ai_algorithm.upper()}] Tính nước tiếp theo cho: {temp_ai.upper()}")
    print(f"[*] Nước đi gợi ý: {best_move} | Điểm số: {best_score} | Số trạng thái: {ai_logic.get_states()} | Thời gian: {end_time - start_time:.4f}s")
    print("-" * 70)
    
    if best_move:
        br, bc = best_move
        label.config(text=f"GỢI Ý {temp_ai.upper()}: Ô {best_move} | Điểm: {best_score}", fg=TITLE_COLOR)
        buttons[br][bc].config(bg=TITLE_COLOR)
        window.after(1200, lambda: buttons[br][bc].config(bg=BTN_NORMAL) if board[br][bc] == ai_logic.blank else None)

def reset_entire_board():
    global board, current_player, current_selected_mode, check_marker
    board = ai_logic.init_board() 
    for r in range(ai_logic.size):
        for c in range(ai_logic.size):
            buttons[r][c].config(text="", bg=BTN_NORMAL, fg=TEXT_COLOR)
            
    if check_mode:
        check_marker = "x"
        label.config(text="Đã dọn bàn! Click để (X)", fg=TITLE_COLOR)
    else:
        current_player = "x"
        current_selected_mode = None
        btn_human_first.config(bg=BTN_MENU_BG, fg=BTN_MENU_FG)
        btn_ai_first.config(bg=BTN_MENU_BG, fg=BTN_MENU_FG)
        label.config(text="CHỌN CHẾ ĐỘ BẮT ĐẦU VÁN CỜ", fg=TEXT_COLOR)
    print("\n[*] Hệ thống: Bàn cờ đã được làm mới hoàn toàn.")

# Đồ họa
window = Tk()
window.title("Game cờ Caro")
pixel_ratio = PhotoImage(width=1, height=1)
window.configure(bg=BG_COLOR)
window.geometry("460x660")
window.resizable(False, False)

label = Label(window, text="CHỌN CHẾ ĐỘ BẮT ĐẦU", font=FONT_UI, bg=BG_COLOR, fg=TEXT_COLOR)
label.pack(pady=5)

controls_frame = Frame(window, bg=BG_COLOR)
controls_frame.pack(pady=2)

btn_human_first = Button(controls_frame, text="BẠN ĐI TRƯỚC (X)", font=FONT_UI, bg=BTN_MENU_BG, fg=BTN_MENU_FG, activebackground=BTN_MENU_ACTIVE_BG, activeforeground=BTN_MENU_ACTIVE_FG, relief="flat", cursor="hand2", command=lambda: start_game("human"))
btn_human_first.grid(row=0, column=0, padx=5, ipadx=5, ipady=2)
apply_menu_hover_effect(btn_human_first, "human")  

btn_ai_first = Button(controls_frame, text="AI ĐI TRƯỚC (X)", font=FONT_UI, bg=BTN_MENU_BG, fg=BTN_MENU_FG, activebackground=BTN_MENU_ACTIVE_BG, activeforeground=BTN_MENU_ACTIVE_FG, relief="flat", cursor="hand2", command=lambda: start_game("ai"))
btn_ai_first.grid(row=0, column=1, padx=5, ipadx=5, ipady=2)
apply_menu_hover_effect(btn_ai_first, "ai")  

algo_frame = Frame(window, bg=BG_COLOR)
algo_frame.pack(pady=3)
btn_alphabeta = Button(algo_frame, text="AI: Alpha-Beta", font=('Consolas', 10, 'bold'), bg=BTN_MENU_ACTIVE_BG, fg=BTN_MENU_ACTIVE_FG, relief="flat", cursor="hand2", command=lambda: toggle_algo("alphabeta"))
btn_alphabeta.grid(row=0, column=0, padx=5, ipadx=3)
btn_minimax = Button(algo_frame, text="AI: Minimax", font=('Consolas', 10, 'bold'), bg=BTN_MENU_BG, fg=BTN_MENU_FG, relief="flat", cursor="hand2", command=lambda: toggle_algo("minimax"))
btn_minimax.grid(row=0, column=1, padx=5, ipadx=3)

sb_frame = Frame(window, bg=BG_COLOR)
sb_frame.pack(pady=3)
btn_sandbox = Button(sb_frame, text="Chế độ kiểm thử", font=('Consolas', 9, 'bold'), bg=BTN_MENU_BG, fg=BTN_MENU_FG, relief="flat", cursor="hand2", command=toggle_sandbox)
btn_sandbox.grid(row=0, column=0, padx=4, ipady=1)
btn_analyze = Button(sb_frame, text=" Nước đi AI gợi ý", font=('Consolas', 9, 'bold'), bg=TITLE_COLOR, fg="#000000", relief="flat", cursor="hand2", command=run_sandbox_analysis)
btn_analyze.grid(row=0, column=1, padx=4, ipady=1)
btn_reset = Button(sb_frame, text="RESET", font=('Consolas', 9, 'bold'), bg="#FF003C", fg="#FFFFFF", relief="flat", cursor="hand2", command=reset_entire_board)
btn_reset.grid(row=0, column=2, padx=4, ipady=1)

board_bg_frame = Frame(window, bg=FRAME_BG, bd=2)
board_bg_frame.pack(pady=5)
buttons = [[None for _ in range(ai_logic.size)] for _ in range(ai_logic.size)]
for r in range(ai_logic.size):
    for c in range(ai_logic.size):
        btn = Button(board_bg_frame, text="", font=fontboard, image=pixel_ratio, width=42, height=42, compound="center", bg=BTN_NORMAL, fg=TEXT_COLOR, relief="flat", cursor="crosshair", activebackground=BTN_HOVER, command=lambda r=r, c=c: cell_clicked(r, c))
        btn.grid(row=r, column=c, padx=1, pady=1)
        apply_hover_effect(btn)
        buttons[r][c] = btn

window.mainloop()