import streamlit as st
from tinydb import TinyDB, Query
import random
import requests


PISTON_URL = "https://emkc.org/api/v2/piston/execute"  # Replace with the actual API URL


# Initialize TinyDB database
db = TinyDB('student_database.json')

# Create a list to store the student codes and their scores
student_codes = []
student_scores = {}

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def print_positions():
    positions = [[str(3 * i + j + 1) for j in range(3)] for i in range(3)]
    print_board(positions)

def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(row[col] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell != ' ' for row in board for cell in row)


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





# Function to simulate the rock-paper-scissors game
def rps(player1, player2):
    choices = ['rock', 'paper', 'scissors']

    if player1 == player2:
        return 0
    
    if player1 not in choices:
        return 2
    
    if player2 not in choices:
        return 1
    
    elif (player1 == 'rock' and player2 == 'scissors') or \
         (player1 == 'paper' and player2 == 'rock') or \
         (player1 == 'scissors' and player2 == 'paper'):
        return 1
    else:
        return 2


import requests

# Function to execute code using Piston API
def execute_code(code):
    # Prepare the payload for the Piston API
    payload = {
        "language": "py3",
        "version": "3.10.0",
        "files": [
            {
                "name": "my_cool_code.py",  # You can change the filename if needed
                "content": code  # Pass the code as content
            }
        ],
        "compile_timeout": 10000,
        "run_timeout": 3000,
        "compile_memory_limit": -1,
        "run_memory_limit": -1,
    }

    # Make a POST request to the Piston API
    piston_api_url = "https://emkc.org/api/v2/piston/execute"  # Replace with the actual API URL
    response = requests.post(piston_api_url, json=payload)
        
    if response.status_code == 200:
        data = response.json()
        output = data.get("run", {}).get("output", "").strip()
        return output
    else:
        return None


# Streamlit UI
page = st.sidebar.selectbox("Select a page:", ("Home", "Upload Student Code", "Start Tournament"))

if page == "Upload Student Code":
    st.title("Upload Student Code")
    st.write("Please enter your student ID and Python code with the rps() function below.")

    student_id = st.text_input("Student ID:")
    student_code = st.text_area("Enter Python code with rps() function:")

    if st.button("Upload Code"):
        if student_id and student_code:
            # Store student ID and code in TinyDB
            db.insert({"student_id": student_id, "code": student_code})
            st.success("Code uploaded successfully!")

elif page == "Start Tournament":
    st.title("Rock-Paper-Scissors Tournament")
    
    hello_world = execute_code("print('Hello World!')")
    st.write(hello_world)

    # Load student codes from TinyDB
    student_records = db.all()
    st.write("We have {} student codes.".format(len(student_records)))
    
    # Show participants
    st.markdown("### Participants")
    for record in student_records:
        st.markdown("- {}".format(record["student_id"]))
        
    if len(student_records) < 2:
        st.warning("Need at least two student codes to start the tournament.")
    else:
        st.header("Tournament Results")
        random.shuffle(student_records)
        winner = student_records[0]
        for i in range(1, len(student_records)):
            st.markdown("### Round {}".format(i))
            player1 = winner
            player2 = student_records[i]

            # Execute the student code to get their choice
            player1_choice = execute_code(player1["code"])
            player2_choice = execute_code(player2["code"])
            
            player_1_student_id = player1["student_id"]
            player_2_student_id = player2["student_id"]

            st.write(f"{player_1_student_id}: {player1_choice}")
            st.write(f"{player_2_student_id}: {player2_choice}")

            result = rps(player1_choice, player2_choice)

            # Update the scores
            
            if result == 1 or result == 0:    
                player1["score"] = player1.get("score", 0) + 1
                winner = player1
            elif result == 2:
                player2["score"] = player2.get("score", 0) + 1
                winner = player2
                
            st.write(f"Winner: {winner['student_id']}, Score: {winner['score']}")
                
        st.header("Tournament Standings")
        # Order the student records by score
        student_records = sorted(student_records, key=lambda x: x.get("score", 0), reverse=True)
        for record in student_records:
            st.write(f"{record['student_id']}: {record.get('score', 0)}")
            
            
elif page == "Tic-Tac-Toe":
    st.title("Tic-Tac-Toe")
    
    hello_world = execute_code("print('Hello World!')")
    st.write(hello_world)

    # Load student codes from TinyDB
    student_records = db.all()
    st.write("We have {} student codes.".format(len(student_records)))
    
    # Show participants
    st.markdown("### Participants")
    for record in student_records:
        st.markdown("- {}".format(record["student_id"]))
        
    if len(student_records) < 2:
        st.warning("Need at least two student codes to start the tournament.")
    else:
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

# Display the student codes
elif page == "Home":
    st.title("Home Page")
    st.write("Welcome to the Rock-Paper-Scissors Tournament platform!")
