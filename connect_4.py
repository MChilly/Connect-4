import tkinter as tk


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
        self.root.iconbitmap(r"images\game_dice.ico")
        self.root.configure(bg='black')  # Setting a black background
        self.current_player_index = 0
        self.players = [
            Player("παίκτης 1", "red", "1"),
            Player("παίκτης 2", "green", "2")
        ]


# Display help information in a new window
def display_help():
    extra_window = tk.Toplevel()
    extra_window.title("Οδηγίες παιχνιδιού")
    extra_window.geometry('500x500')
    tk.Label(extra_window, text="Παιχνίδι για δύο παίκτες. Ο κάθε παίκτης προσπαθεί να σχηματίσει όσο περισσότερες τετράδες οριζόντια, κάθετα ή διαγώνια,\n"
                                " προσπαθώντας ταυτόχρονα να εμποδίσει τον αντίπαλο να κάνει το ίδιο. ").pack()


# Display about information in a new window
def display_about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_text = "Πληροφορίες για το παιχνίδι ή τον προγραμματιστή."
    about_label = tk.Label(about_window, text=about_text)
    about_label.pack()


#  main program
if __name__ == "__main__":
    root = tk.Tk()
    # Window dimensions 800x800. Position: +520pixels right + 20 pixels down.
    root.geometry("800x800+520+20")

    # Game main menu
    menu = tk.Menu(root)
    root.config(menu=menu)
    filemenu = tk.Menu(menu)
    menu.add_cascade(label='Αρχείο', menu=filemenu)
    filemenu.add_command(label="Αποθήκευση ως", command="test")
    filemenu.add_command(label="Άνοιγμα αρχείου", command="test")
    filemenu.add_separator()  # Εμφάνιση διαχωριστικής γραμμής
    filemenu.add_command(label="Έξοδος", command=root.destroy)

    # Help menu
    helpmenu = tk.Menu(menu)
    menu.add_cascade(label="Βοήθεια", menu=helpmenu)
    helpmenu.add_cascade(label="Οδηγίες παιχνιδιού", command=display_help)
    helpmenu.add_cascade(label="Πληροφορίες", command=display_about)

    # The window is not allowed to grow when we drag it.
    root.resizable(width=False, height=False)
    root.mainloop()  # Start GUI event loop
