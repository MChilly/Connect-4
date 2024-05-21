# Importing necessary libraries
import tkinter as tk
from tkinter import messagebox, filedialog, Label, Button, Entry
from PIL import Image, ImageTk

# Define a Player class with attributes for name, color, symbol, and score
class Player:
    def __init__(self, name, color, symbol):
        self.name = name  # Player's name
        self.color = color  # Color to represent player in the game
        self.symbol = symbol  # Symbol to represent player on the board
        self.score = 0  # Initial score set to 0

    # Board class represents the game board
class Board:
    def __init__(self, game, rows, cols):
        self.game = game  # A reference to the main game class
        self.rows = rows  # Number of rows in the game board
        self.cols = cols  # Number of columns in the game board
        self.grid = [["" for _ in range(cols)] for _ in range(rows)]  # Initialize a grid with empty strings
        self.winning_cells = []  # List to keep track of winning cells after game ends
        # Creating a Canvas widget for drawing game elements
        self.canvas = tk.Canvas(game.root, width=cols * 50, height=rows * 50, bg='blue')
        self.canvas.pack()

        # Method to draw or redraw the game board
        def draw(self):
            self.canvas.delete("all")  # Clear the canvas
            # Loop through each cell in the grid to draw the pieces
            for row in range(self.rows):
                for col in range(self.cols):
                    # Calculating coordinates for each piece
                    x1, y1 = col * 50 + 10, row * 50 + 10
                    x2, y2 = x1 + 40, y1 + 40
                    color = "white"  # Default color for empty cells
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
            # Initially draw the board
            self.draw()


# Game class to manage overall game settings and states
class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")
        self.root.geometry("800x800+520+20")  # Window dimensions 800x800. Position: +520pixels right + 20 pixels down
        self.root.iconbitmap(r"images\game_dice.ico")
        self.root.configure(bg='black')  # Setting a black background
        self.current_player_index = 0
        self.players = [
            Player("παίκτης 1", "red", "1"),
            Player("παίκτης 2", "green", "2")
        ]
        self.start_screen()  # Initialize start screen


    def start_screen(self):
        # Set up the start screen with game instructions and player inputs
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

        self.start_button = Button(self.root, text="Έναρξη Παιχνιδιού", bg="black", fg="white", font=("Helvetica", 14), command=self.setup_ui)
        self.start_button.pack(pady=10, side="top")

        self.credits_label = Label(self.root, text=" Ομαδικό Project ΠΛΗΠΡΟ-ΕΑΠ(2023-2024): Ασήμης Γ. | Ορμανίδου Μ.| Σαρρέας Γ. | Τσιλιγκάνου Μ.",
                                   font=("Helvetica", 10, "italic"), bg="#f8f8f8", fg="gray")
        self.credits_label.pack(side="bottom", pady=(5, 20))  # Adjust the padding as needed

    # Setup user interface, read number of columns and initialize game board
    def setup_ui(self):
        """This method is triggered by the start button.Reads the number of columns for the game board.
        Initializes the game board with these dimensions.
        Sets up the game area, including a menu for new game, save, load, and exit actions.
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
        # self.o_red_label.destroy()
        self.p2.destroy()
        # self.x_green_label.destroy()
        self.start_background_label.destroy()
        self.credits_label.destroy()

        # Initialize and display the game board
        # self.root.title("Connect 4")
        self.board = Board(self, num_cols, num_cols)
        # self.board.draw()

        # Setup score labels for players
        self.score_labels = {
            player.name: tk.Label(self.root, text=f"Score {player.name}: {player.score}", font=("Helvetica", 14),
                                  bg='black', fg=player.color)
            for player in self.players
        }

        # Create menu for game options --THE LOAD functions has to be adjusted!!!
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="Αρχείο", menu=filemenu)
        filemenu.add_command(label="Νέο παιχνίδι", command=self.new_game)
        filemenu.add_command(label="Αποθήκευση ως", command=self.save_game)
        filemenu.add_command(label="Άνοιγμα αρχείου", command=self.load_game)
        filemenu.add_separator()
        filemenu.add_command(label="Έξοδος", command=self.root.quit)

        helpmenu = tk.Menu(menu)
        menu.add_cascade(label="Βοήθεια", menu=helpmenu)
        helpmenu.add_cascade(label="Οδηγίες παιχνιδιού", command=self.display_help)
        helpmenu.add_cascade(label="About", command=self.display_about)

    def create_menu(self):
        # Game main menu
        menu = tk.Menu(root)
        self.root.config(menu=menu)

        # File menu
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='Αρχείο', menu=filemenu)
        filemenu.add_command(label="Νέο παιχνίδι", command="test")
        filemenu.add_command(label="Αποθήκευση ως", command="test")
        filemenu.add_command(label="Άνοιγμα αρχείου", command="test")
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
        extra_window.geometry('500x500')
        tk.Label(extra_window,
                 text="Παιχνίδι για δύο παίκτες. Ο κάθε παίκτης προσπαθεί να σχηματίσει όσο περισσότερες τετράδες οριζόντια, κάθετα ή διαγώνια,\n"
                      " προσπαθώντας ταυτόχρονα να εμποδίσει τον αντίπαλο να κάνει το ίδιο. ").pack()

    # Display about information in a new window
    def display_about(self):
        """Opens a new window providing information about the game or the developers"""
        about_window = tk.Toplevel(root)
        about_window.title("About")
        about_text = "Πληροφορίες για το παιχνίδι ή τον προγραμματιστή."
        about_label = tk.Label(about_window, text=about_text)
        about_label.pack()



#  main program
if __name__ == "__main__":
    root = tk.Tk()
    # Window Dimensions 800x800. Position:+ 520 pixels right + 20 pixels down.
    root.geometry("800x800+520+20")
    game = Game(root)  # instance of the Game class
    game.create_menu()
    # The window is not allowed to grow when we drag it.
    root.resizable(width=False, height=False)
    root.mainloop()  # Start GUI event loop
