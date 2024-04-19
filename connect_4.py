# Importing necessary libraries
import tkinter as tk
from tkinter import *
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

        self.start_button = Button(self.root, text="Έναρξη Παιχνιδιού", bg="red", fg="white", font=("Helvetica", 14), command='test')
        self.start_button.pack(pady=10, side="top")

        self.credits_label = Label(self.root, text=" Ομαδικό Project ΠΛΗΠΡΟ-ΕΑΠ(2023-2024): Ασήμης Γ. | Ορμανίδου Μ.| Σαρρέας Γ. | Τσιλιγκάνου Μ.",
                                   font=("Helvetica", 10, "italic"), bg="#f8f8f8", fg="gray")
        self.credits_label.pack(side="bottom", pady=(5, 20))  # Adjust the padding as needed

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
    # root.geometry("800x800+520+20")
    game = Game(root)  # instance of the Game class
    game.create_menu()
    # The window is not allowed to grow when we drag it.
    root.resizable(width=False, height=False)
    root.mainloop()  # Start GUI event loop
