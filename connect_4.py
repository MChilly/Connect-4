# Importing necessary libraries and classes
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, Label, Button, Entry
from PIL import Image, ImageTk
import csv


# Define a Player class with attributes for name, color, symbol, and score
class Player:
    """Class representing a player in the Connect 4 game.

    Attributes:
        name (str): The name of the player.
        color (str): The color representing the player.
        symbol (str): The symbol representing the player on the board.
        score (int): The score of the player.
    """
    def __init__(self, name, color, symbol):
        self.name = name  # Player's name
        self.color = color  # Color to represent player in the game
        self.symbol = symbol  # Symbol to represent player on the board
        self.score = 0  # Initial score set to 0


class Board:
    """Class representing the Connect 4 game board.

    Attributes:
        game (Game): Reference to the game object.
        rows (int): Number of rows in the game board.
        cols (int): Number of columns in the game board.
        grid (list): 2D list representing the game board.
        winning_cells (list): List of cells that are part of a winning combination.
        canvas (tk.Canvas): Canvas widget for drawing the game board.
    """
    def __init__(self, game, rows, cols):
        self.game = game  # A reference to the main game class
        self.rows = rows  # Number of rows in the game board
        self.cols = cols # Number of columns in the game board
        self.grid = [["" for _ in range(cols)] for _ in range(rows)]  # Initialize a grid with empty strings
        self.winning_cells = []  # List to keep track of winning cells after game ends
        # Creating a Canvas widget for drawing game elements
        self.canvas = tk.Canvas(game.root, width=cols * 50, height=rows * 50, bg='blue')
        self.canvas.pack()

    # Method to draw or redraw the game board
    def draw(self):
        """Draw or redraw the game board on the canvas."""
        self.canvas.delete("all")  # Clear the canvas
        # Loop through each cell in the grid to draw the pieces
        for row in range(self.rows):
            for col in range(self.cols):
                # Calculating coordinates for each piece
                x1, y1 = col * 50 + 10, row * 50 + 10
                x2, y2 = x1 + 40, y1 + 40
                color = "white" # Default color for empty cells
                if (row, col) in self.winning_cells:
                    color = "yellow"  # Highlight winning cells with yellow
                elif self.grid[row][col]:
                    # Fetch player color if cell is not empty
                    player_symbol = self.grid[row][col]
                    color = self.game.players[int(player_symbol) - 1].color
                    # Draw an oval (piece) in the calculated coordinates
                self.canvas.create_oval(x1, y1, x2, y2, fill=color, tags=("piece", row, col))
                # Bind mouse click on piece to place_piece method
        self.canvas.tag_bind("piece", "<Button-1>", self.place_piece)

    def create_board(self):
        """Initialize the game board by drawing it for the first time.

        This method is responsible for setting up the initial state of the game board.
        It calls the `draw` method to render the empty game board on the canvas.
        """
        self.draw()

    def place_piece(self, event):
        """Handle placing a piece on the board when a cell is clicked.

        Args:
            event (tk.Event): The event object containing details about the mouse click.
        """
        if self.game.game_over:  # Do nothing if the game is over
            print("Game is over, cannot place piece.")
            return

        col = (event.x - 10) // 50  # Calculate column from mouse click coordinates
        if col >= self.cols or col < 0:
            # Display warning if click is out of bounds
            messagebox.showwarning("Invalid Move", "Column is out of bounds. Try again.")
            return

        # Place piece in the first empty cell from the bottom
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == "":
                self.grid[row][col] = self.game.current_player().symbol
                print(f"Placed piece for {self.game.current_player().name} at row {row}, column {col}.")
                self.game.total_moves += 1 # Increment the total moves after placing a piece
                self.draw()
                if self.game.check_win(row, col):
                    print(f"{self.game.current_player().name} has won.")
                    self.game.end_round()
                else:
                    print(f"Moves made:{self.game.total_moves}")
                    self.game.switch_player()
                break
        else:
            # Display warning if all cells in the column are filled
            messagebox.showwarning("Invalid Move", "Column is full. Try another one.")


# Game class to manage overall game settings and states
class Game:
    """Class representing the Connect 4 game.

    Attributes:
        root (tk.Tk): The main window for the application.
        current_player_index (int): Index of the current player.
        players (list): List of Player objects representing the players.
        game_over (bool): Flag to check if the game has ended.
        total_moves (int): Total number of moves made in the game.
        turn_label (tk.Label): Label to display the current player's turn.
    """
    def __init__(self, root):
        self.root = root  # Main window for the application
        self.root.title("Connect 4")  # Set window title
        self.root.geometry("800x800+500+10")  # Window dimensions 800x800. Position: +520pixels right + 20 pixels down
        self.root.iconbitmap(r"images\game_dice.ico") # Set icon for the game window
        self.root.resizable(width=False, height=False) # The window is not allowed to grow when we drag it.
        self.root.configure(bg='black')  # Set background color of the window
        self.current_player_index = 0
        self.players = [ # List of two Player objects
            Player("παίκτης 1", "red", "1"),
            Player("παίκτης 2", "green", "2")
        ]
        self.game_over = False  # A boolean flag to check if the game has ended either due to a win or a draw.
        self.start_screen()  # Initialize start screen

        # initializing a move counter
        self.total_moves = 0

        # Label to display current player's turn
        self.turn_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="black", fg="white")
        self.turn_label.pack(pady=(10, 0))  # Pack label with padding

    def start_screen(self):
        """Set up the start screen with game instructions and player inputs."""
        self.start_image = Image.open(r'images\red_green_pawn3.png')  # Background image for the start screen
        self.start_photo_image = ImageTk.PhotoImage(self.start_image)
        self.start_background_label = tk.Label(self.root, image=self.start_photo_image)
        self.start_background_label.place(relwidth=1, relheight=1)

        # Labels and Entry for number of columns
        self.title_label = Label(self.root, text="Connect 4", font=("Helvetica", 30, "bold"), fg="blue", bg="white")
        self.title_label.pack(pady=(50, 10))  # Adjust the padding as needed

        self.entry_label = Label(self.root, text="Επιλογή Στηλών Παιχνιδιού (10-20)", font=("Helvetica", 14), bg="white")
        self.entry_label.pack()

        self.column_entry = Entry(self.root, font=("Helvetica", 14), width=8)
        self.column_entry.pack(pady=10)

        self.p1= Label(self.root, text="Παίκτης 1", font=("Helvetica", 20), bg="#f9f1f1")
        self.p1.place(x=170, y=580)

        self.p2 = Label(self.root, text="Παίκτης 2", font=("Helvetica", 20), bg="#f1f9f1")
        self.p2.place(x=520, y=580)

        self.start_button = Button(self.root, text="Έναρξη Παιχνιδιού", bg="red", fg="white", font=("Helvetica", 14), command=self.setup_ui)
        self.start_button.pack(pady=10, side="top")

        self.credits_label = Label(self.root, text=" Ομαδικό Project ΠΛΗΠΡΟ-ΕΑΠ(2023-2024): Ορμανίδου Μαρία. |  Σαρρέας Γεώργιος. | Τσιλιγκάνου Μαρία.",
                                   font=("Helvetica", 10, "italic"), bg="#f8f8f8", fg="gray")
        self.credits_label.pack(side="bottom", pady=(5, 20))  # Adjust the padding as needed

    # Setup user interface, read number of columns and initialize game board
    def setup_ui(self):
        """This method is triggered by the start button and sets up the user interface,

         read the number of columns and initialize the game board with these dimensions,
         Clears the start screen widgets from the display"""
        try:
            num_cols = int(self.column_entry.get())
            if not 10 <= num_cols <= 20:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Entry", "Please enter a valid number between 10 and 20.")
            return

        # Adjust the size of the root window to accommodate the board size
        cell_size = 50  # The size of a single cell in the game grid
        padding = 120  # Additional padding for the canvas/Extra space for menu and margins
        window_size = num_cols * cell_size + padding
        self.root.geometry(f"{window_size}x{window_size}")

        # Destroy/Remove the start screen widgets
        self.title_label.destroy()
        self.entry_label.destroy()
        self.column_entry.destroy()
        self.start_button.destroy()
        self.p1.destroy()
        self.p2.destroy()
        self.start_background_label.destroy()
        self.credits_label.destroy()

        # Initialize and display the game board
        self.board = Board(self, num_cols, num_cols)
        self.board.draw()
        self.create_menu()

        # Setup score labels for players
        self.score_labels = {
            player.name: tk.Label(self.root, text=f"Score {player.name}: {player.score}", font=("Helvetica", 14),
                                  bg='black', fg=player.color)
            for player in self.players
        }

        self.score_labels[self.players[0].name].pack(side="left", padx=10)
        self.score_labels[self.players[1].name].pack(side="right", padx=10)

        # After setting up the UI, call update_turn_label to set the initial text
        self.update_turn_label()

    def create_menu(self):
        """Create the main menu for the game."""
        menu = tk.Menu(root)
        self.root.config(menu=menu)

        # File menu
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='Αρχείο', menu=filemenu)
        filemenu.add_command(label="Νέο παιχνίδι", command=self.new_game)
        filemenu.add_command(label="Αποθήκευση ως", command=self.save_game)
        filemenu.add_command(label="Άνοιγμα αρχείου", command=self.load_game)
        filemenu.add_separator()  # Εμφάνιση διαχωριστικής γραμμής
        filemenu.add_command(label="Έξοδος", command=self.root.destroy)

        # Help menu
        helpmenu = tk.Menu(menu)
        menu.add_cascade(label="Βοήθεια", menu=helpmenu)
        helpmenu.add_cascade(label="Οδηγίες παιχνιδιού", command=self.display_help)
        helpmenu.add_cascade(label="Πληροφορίες", command=self.display_about)

    # Display help information in a new window
    def display_help(self):
        """Opens a new window to show game rules or help, related to how to play the game."""
        extra_window = tk.Toplevel()
        extra_window.title("Οδηγίες παιχνιδιού")
        extra_window.geometry('640x600')
        extra_window.configure(bg='white')

        heading = tk.Label(extra_window, text="Οδηγίες Παιχνιδιού Connect 4", font=("Helvetica", 18, "bold"),
                           bg="white")
        heading.pack(pady=10)

        instructions = ("Το Connect 4 είναι ένα παιχνίδι στρατηγικής για δύο παίκτες.\n"
                        "Στόχος είναι να σχηματίσετε μια γραμμή από τέσσερα κομμάτια\n"
                        "του χρώματός σας είτε οριζόντια, κάθετα ή διαγώνια.\n\n"
                        "Οδηγίες:\n"
                        "1. Κάθε παίκτης επιλέγει μια στήλη για να ρίξει ένα κομμάτι.\n"
                        "2. Τα κομμάτια πέφτουν στο χαμηλότερο διαθέσιμο κενό της στήλης.\n"
                        "3. Το παιχνίδι συνεχίζεται μέχρι κάποιος παίκτης να σχηματίσει\n"
                        "   τέσσερα κομμάτια στη σειρά ή να γεμίσει ο πίνακας χωρίς νικητή.\n"
                        "4. Εάν ένας παίκτης σχηματίσει τετράδα, τα κομμάτια αυτά\n"
                        "   αφαιρούνται και ο παίκτης κερδίζει πόντους.\n"
                        "5. Ο γύρος τελειώνει και ξεκινά νέος γύρος.\n\n"
                        "Καλή διασκέδαση!")

        instructions_label = tk.Label(extra_window, text=instructions, font=("Helvetica", 12), justify="left",
                                      bg="white")
        instructions_label.pack(padx=20, pady=10)

    # Display about information in a new window
    def display_about(self):
        """Opens a new window providing information about the game or the developers"""
        about_window = tk.Toplevel(root)
        about_window.title("Πληροφορίες")
        about_window.geometry('600x600')
        about_window.configure(bg='white')

        heading = tk.Label(about_window, text="Σχετικά με το Project", font=("Helvetica", 18, "bold"), bg="white")
        heading.pack(pady=10)

        about_text = ("Αυτό το παιχνίδι Connect 4 δημιουργήθηκε ως μέρος του ομαδικού project\n"
                      "για το μάθημα ΠΛΗΠΡΟ στο ΕΑΠ κατά το ακαδημαϊκό έτος 2023-2024.\n\n"

                      "Τεχνικές Πληροφορίες:\n"
                      "Έκδοση Python: 3.10.9\n"
                      "Βιβλιοθήκες που Χρησιμοποιήθηκαν:\n"
                      "1. tkinter\n"
                      "2. PIL (Pillow)\n"
                      "3. csv\n\n"
                      "Προγραμματιστές:\n"
                      "1. Ορμανίδου Μαρία\n"
                      "2. Σαρρέας Γεώργιος\n"
                      "3. Τσιλιγκάνου Μαρία\n\n"
                      "Ελπίζουμε να απολαύσετε το παιχνίδι!\n\n")

        about_label = tk.Label(about_window, text=about_text, font=("Helvetica", 12), justify="left", bg="white")
        about_label.pack(padx=20, pady=10)

    # Returns the current player object
    def current_player(self):
        """Returns the current player object."""
        return self.players[self.current_player_index]

    # Switch to the other player
    def switch_player(self):
        """Toggles the current_player_index to switch turns between Player 1 and Player 2.
        Updates the game's title bar and turn label to reflect whose turn it is."""
        self.current_player_index = 1 - self.current_player_index
        self.root.title(f"Connect 4 - παίζει ο {self.current_player().name}")
        self.update_turn_label()  # Update the turn label text after switching players

    # Update the label to show which player's turn it is
    def update_turn_label(self):
        """Updates the turn label to show which player's turn is currently active"""
        # Update the label with the name of the current player
        self.turn_label.config(fg=f"{self.current_player().color}", text=f"Επιλέγει ο {self.current_player().name}")

    # Update the score labels after a game
    def update_scores(self):
        """Update the score labels after a game."""
        for player in self.players:
            self.score_labels[player.name].config(text=f"Score {player.name}: {player.score}")

    # Check if the current player has won after placing a piece
    def check_win(self, row, col):
        """Check if the current player has won after placing a piece.

                Args:
                    row (int): The row index of the last placed piece.
                    col (int): The column index of the last placed piece.
                Returns:
                    bool: True if the current player has won, False otherwise.
                """
        # Define all possible directions for connecting four pieces:
        # Horizontal (0,1), Vertical (1,0), Diagonal from top-left to bottom-right (1,1),
        # and Diagonal from bottom-left to top-right (1,-1), and their opposites
        directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]

        # Retrieve the symbol of the current player (e.g., "1" or "2")
        player_symbol = self.current_player().symbol

        # Loop through each direction to check for a line of four consecutive piece
        for row_direction, col_direction in directions:
            count = 0

            # Check for four pieces in a line around the placed piece
            for i in range(-3, 4):  # Range from -3 to 3 includes the placed piece and 3 additional pieces in both directions
                # Calculate row and column indices for checking pieces
                # current_row,  current_col = row + i * row_direction, col + i * col_direction
                current_row = row + i * row_direction  # Row index adjusted by direction and step
                current_col = col + i * col_direction  # Column index adjusted by direction and step

                # Check if the indices are within the board boundaries and the cell has the current player's symbol
                if 0 <= current_row < self.board.rows and 0 <= current_col < self.board.cols and self.board.grid[current_row][current_col] == player_symbol:
                    count += 1  # Increment count if a piece of the current player is found
                    # Check if there are four in a line
                    if count >= 4:
                        # If four in a row are found, store the winning cells' positions
                        self.board.winning_cells = [(row + j * row_direction, col + j * col_direction) for j in range(i, i - 4, -1)]
                        return True  # Return True indicating the current player has won
                else:
                    count = 0  # Reset count if a piece is not part of a consecutive line
        return False  # If no winning line is found after checking all directions, return False

    # End the current round of the game
    def end_round(self):
        """End the current round of the game."""
        self.game_over = True
        winner = self.current_player()

        # Initialize a set to keep track of cells that are removed
        removed_cells = set()

        # Iterate over the winning cells and check for adjacent cells of the same color
        for row, col in self.board.winning_cells:
            if self.board.grid[row][col] == winner.symbol:
                # Add the winning cell to the set of removed cells
                removed_cells.add((row, col))
                # Check adjacent cells in all directions
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if (dr != 0 or dc != 0) and 0 <= row + dr < self.board.rows and 0 <= col + dc < self.board.cols:
                            # If the adjacent cell has the same color, add it to the set of removed cells
                            if self.board.grid[row + dr][col + dc] == winner.symbol:
                                removed_cells.add((row + dr, col + dc))

        # Count the number of removed pieces
        pieces_removed = len(removed_cells)
        # Update the player's score
        winner.score += pieces_removed

        # Remove the winning pieces AND adjacent
        for row, col in removed_cells:
            self.board.grid[row][col] = ""

        # Clear the winning cells list
        self.board.winning_cells = []

        # Adjust the pieces above the removed ones
        for col in range(self.board.cols):
            new_col = []
            # Collect all non-empty cells in the column
            for row in range(self.board.rows):
                if self.board.grid[row][col]:
                    new_col.append(self.board.grid[row][col])

            # Fill the column from bottom to top with collected pieces
            for row in range(self.board.rows - len(new_col)):
                self.board.grid[row][col] = ""  # Fill with empty strings at the top
            for row in range(len(new_col)):
                self.board.grid[self.board.rows - len(new_col) + row][col] = new_col[row]  # Place the collected pieces at the bottom

        self.update_scores()  # Update the score display
        self.board.draw()  # Redraw the board to reflect the changes
        messagebox.showinfo("Round Over", f"{winner.name} wins this round! {pieces_removed} pieces removed.")
        self.game_over = False  # Allow the game to continue
        self.switch_player()  # Switch to the other player for the next round
        # print("End of round - Scores updated.") #prints to debug

    # End the game and show the winner
    def end_game(self):
        self.game_over = True
        winner = self.current_player()

        # Count the number of winning pieces and update the player's score
        pieces_removed = len(self.board.winning_cells)
        winner.score += pieces_removed

        # Remove the winning pieces
        for row, col in self.board.winning_cells:
            self.board.grid[row][col] = ""  # Clear the winning cells

        self.board.winning_cells = []  # Clear the winning cells list
        self.board.draw()  # Redraw the board to reflect the changes
        messagebox.showinfo("Round Over", f"{winner.name} wins this round! {pieces_removed} pieces removed.")
        self.game_over = False  # Allow the game to continue
        self.switch_player()  # Switch to the other player for the next round
        #print("End of game - Scores updated.") #print to debug

    def save_game(self):
        """Save the current game state to a CSV file."""
        filename = filedialog.asksaveasfilename(
            title="Save game",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            )
        if not filename:  # User cancelled save
            return

        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)
            # Directly write the board's grid to the CSV
            for row in self.board.grid:
                writer.writerow(row)
            # Save player scores in the last row
            writer.writerow([player.score for player in self.players])
        messagebox.showinfo("Save Game", "Το παιχνίδι αποθηκεύτηκε με επιτυχία!")

    # Load a game state from a CSV fil
    def load_game(self):
        """Load a game state from a CSV file."""
        filename = filedialog.askopenfilename(
            title="Load game",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not filename:   # User cancelled the dialog, so don't load.
            return  # Cancel load if no filename is given

        with open(filename, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            # Assume the last row contains the scores
            scores = rows.pop()  # The last row contains the scores
            self.board.grid = [row for row in rows]
            for i, score in enumerate(scores):
                self.players[i].score = int(score)

        # Redraw the board with the loaded state and update the game
        self.update_scores()
        self.board.draw()
        self.game_over = False  # Reset the game over status if necessary
        messagebox.showinfo("Load Game", "Το παιχνίδι φορτώθηκε με επιτυχία!\nΜπορείτε να συνεχίσετε το γύρο σας.")

    # New game method resets the board and score
    def new_game(self):
        """Start a new game by resetting the board and scores."""
        self.game_over = False
        self.current_player_index = 0
        self.players[0].score = 0
        self.players[1].score = 0
        self.update_scores()
        # Reset the grid
        self.board.grid = [["" for _ in range(self.board.cols)] for _ in range(self.board.rows)]
        self.board.winning_cells = []  # Clears winning cells after selecting new game
        self.board.draw()
        self.update_turn_label()  # Update the turn label to the first player

#  main program
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)  # instance of the Game class
    root.mainloop()  # Start GUI event loop
