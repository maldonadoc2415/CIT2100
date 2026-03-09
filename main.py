import gamelogic as gl
import ai


def play_game():
    # Setup board
    my_board = [[' ' for _ in range(6)] for _ in range(7)]
    
    print(" Welcome to Connect Four \n AI EDITION ")
    is_ai_game = input("Play against AI? (y/n): ").lower() == 'y'
    
    turn = "X"
    winner = False

    while not gl.game_is_over(my_board):
        gl.print_board(my_board)
        available = gl.available_moves(my_board)

        # Player turn or AI turn
        if turn == "X" or not is_ai_game:
            move = 0
            while move not in available:
                try:
                    move = int(input(f"Player {turn}, choose a column {available}: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    move = 0
        else:
            # AI TURN
            print("AI is thinking (analyzing future moves)...")
            # We pass 'gl' so the AI can use gl.select_space and gl.has_won during simulation
            move = ai.get_ai_move(my_board, gl)
            print(f"AI chose column {move}")

        # Execute the move on the actual board
        gl.select_space(my_board, move, turn)

        # Check for a win
        if gl.has_won(my_board, turn):
            gl.print_board(my_board)
            print(f"\n GAME OVER! Player {turn} wins! ")
            winner = True
            break

        # Switch turns
        turn = "O" if turn == "X" else "X"

    # Handle a tie
    if not winner:
        gl.print_board(my_board)
        print("\n It's a tie! The board is full. ")

if __name__ == "__main__":
    play_game()