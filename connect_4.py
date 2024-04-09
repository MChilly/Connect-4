import tkinter as tk


# Παράθυρο για τις οδηγίες του παιχνιδιού
def display_help():
    extra_window = tk.Toplevel()
    extra_window.title("Οδηγίες παιχνιδιού")
    extra_window.geometry('500x500')
    tk.Label(extra_window, text="Παιχνίδι για δύο παίκτες. Ο κάθε παίκτης προσπαθεί να σχηματίσει όσο περισσότερες τετράδες οριζόντια, κάθετα ή διαγώνια,\n"
                                " προσπαθώντας ταυτόχρονα να εμποδίσει τον αντίπαλο να κάνει το ίδιο. ").pack()


def display_about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_text = "Πληροφορίες για το παιχνίδι ή τον προγραμματιστή."
    about_label = tk.Label(about_window, text=about_text)
    about_label.pack()


# GUI Setup
root = tk.Tk()
root.iconbitmap(r"images\game_dice.ico")
root.title = "Connect 4"
root.geometry("800x800")


# Μενού παιχνιδιού
menu = tk.Menu(root)
root.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label='Αρχείο', menu=filemenu)
filemenu.add_command(label="Αποθήκευση ως", command="test")
filemenu.add_command(label="Άνοιγμα αρχείου", command="test")
# Εμφάνιση διαχωριστικής γραμμής
filemenu.add_separator()
filemenu.add_command(label="Έξοδος", command=root.destroy)

helpmenu = tk.Menu(menu)
menu.add_cascade(label="Βοήθεια", menu=helpmenu)
helpmenu.add_cascade(label="Οδηγίες παιχνιδιού", command=display_help)
helpmenu.add_cascade(label="About", command=display_about)



root.mainloop()  # Αρχή βρόχου συμβάντων GUI
