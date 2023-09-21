board = [[' ' for _ in range(3)] for _ in range(3)]
    players = ['X', 'O']
    current_player = 0
    
    print("Welcome to Tic-Tac-Toe!")
    print_positions()
    
    while True:
        print_board(board)
        print(f"Player {players[current_player]}'s turn.")
        
        try:
            position = int(input("Enter a position (1-9): ")) - 1
            row, col = divmod(position, 3)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")
            continue
        
        if position < 0 or position > 8 or board[row][col] != ' ':
            print("Invalid move. Try again.")
            continue
        
        board[row][col] = players[current_player]
        
        if check_win(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} wins!")
            break
        elif is_full(board):
            print_board(board)
            print("It's a tie!")
            break
        
        current_player = 1 - current_player
