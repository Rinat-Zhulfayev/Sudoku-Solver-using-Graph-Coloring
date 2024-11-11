import csv
import random
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

# Definition of the SudokuGraph class to handle the logic of a Sudoku game
class SudokuGraph:
    def __init__(self, initial_board=None):
        self.size = 9  # The size of the Sudoku grid
        self.graph = {}  # Dictionary to store connections between cells
        self.board = [[0] * 9 for _ in range(9)]  # The Sudoku grid
        self.initialize_graph()  # Initialize graph connections
        if initial_board:
            self.set_initial_board(initial_board)  # Set up the initial board state if provided

    def initialize_graph(self):
        # Initializes the Sudoku board
        for row in range(self.size):
            for col in range(self.size):
                vertex = (row, col)
                self.graph[vertex] = []
                # Add row and column connections
                for k in range(self.size):
                    if k != col:
                        self.graph[vertex].append((row, k))
                    if k != row:
                        self.graph[vertex].append((k, col))
                # Add 3x3 block connections
                start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                for i in range(start_row, start_row + 3):
                    for j in range(start_col, start_col + 3):
                        if (i, j) != (row, col):
                            self.graph[vertex].append((i, j))

    def set_initial_board(self, board):
        # Set the initial board from the provided grid
        for r in range(self.size):
            for c in range(self.size):
                value = board[r][c]
                if 1 <= value <= 9:
                    self.board[r][c] = value

    def is_valid(self, row, col, num):
        # Check if it's valid to place a number in a cell
        block_row, block_col = 3 * (row // 3), 3 * (col // 3)
        for k in range(9):
            if self.board[row][k] == num or self.board[k][col] == num:
                return False
            if self.board[block_row + k // 3][block_col + k % 3] == num:
                return False
        return True

    def solve_sudoku(self):
        # Recursive function to solve the Sudoku using backtracking
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.solve_sudoku():
                                return True
                            self.board[row][col] = 0
                    return False
        return True

    def get_board(self):
        # Get the current state of the board
        return self.board

# Definition of a simple Sudoku data class
class Sudoku:
    def __init__(self, puzzle, difficulty):
        self.puzzle = puzzle
        self.difficulty = difficulty

# Load Sudoku puzzles from a CSV file
sudoku_list = []
with open('shuffled_sudo2.csv', newline='') as file:
    rows = csv.DictReader(file)
    for row_num, row in enumerate(rows, start=1):
        if row_num > 100:
            break
        puzzle = row['puzzle']
        difficulty = float(row['difficulty'])
        sudoku_object = Sudoku(puzzle, difficulty)
        sudoku_list.append(sudoku_object)

# Definition of the SudokuUI class to handle the user interface
class SudokuUI:
    def __init__(self, master):
        self.master = master
        self.color_toggle = True  # Toggle for switching colors in the UI
        self.previous_board = None  # Store the previous board state
        self.previous_colors = None  # Store the previous colors of the board
        self.bold_font = tkFont.Font(family="Arial", size=18, weight="bold")
        self.difficulty_font = tkFont.Font(family="Arial", size=12, weight="bold")
        self.selected_sudoku = None
        self.initial_puzzle = self.getSudoku()  # Load a random Sudoku puzzle
        self.sudoku_graph = SudokuGraph(self.initial_puzzle)  # Initialize the Sudoku logic

        self.entries = [[tk.Entry(master, width=2, font=('Arial', 18), justify='center') for _ in range(9)] for _ in range(9)]
        self.initialize_ui()

    def initialize_ui(self):
        # Set up the UI components for the Sudoku grid
        self.master.title("DEU Sudoku Solver")
        for r in range(9):
            for c in range(9):
                value = self.sudoku_graph.get_board()[r][c]
                entry = self.entries[r][c]
                entry.grid(row=r+1, column=c, sticky='nsew', padx=1, pady=1)
                entry.bind('<Key>', lambda e, r=r, c=c: self.check_entry(e, r, c))  # Bind key events
                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(state='readonly')

        for i in range(0, 9, 3):  # Loop over each 3x3 subgrid
            for j in range(0, 9, 3):
                # Check if the current subgrid is in the specified positions
                if (i // 3, j // 3) in [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]:
                    color = '#D3D3D3'
                    border_color = 'lemon chiffon'
                else:
                    color = 'white'
                    border_color = 'SeaGreen3'

                for m in range(3):
                    for n in range(3):
                        self.entries[i + m][j + n].config(highlightbackground=border_color, highlightthickness=2)
                        self.entries[i + m][j + n].config(font=self.bold_font)

        form_width = self.master.winfo_width()

        self.header_label = tk.Label(self.master, text="Sudoku Solver", font=('Arial', 16, 'bold'), bg='lightgrey', padx=0, pady=0)
        self.header_label.grid(row=0, column=0, columnspan=30, sticky='ew')
        for i in range(9):
            self.master.grid_columnconfigure(i, weight=1)

        solve_button = tk.Button(self.master, text='Solve', font=('Arial', 10), bg='green', fg='white', command=self.solve, relief='ridge', borderwidth=3)
        solve_button.grid(row=10, column=1, columnspan=2, sticky='nsew', padx=(0, 10), pady=(15, 15))

        clear_button = tk.Button(self.master, text='Clear', font=('Arial', 10), bg='orangered', fg='white', command=self.resetSudoku, relief='ridge', borderwidth=3)
        clear_button.grid(row=10, column=3, columnspan=2, sticky='nsew', padx=(0, 10), pady=(15, 15))

        self.color_button = tk.Button(self.master, text='Change Color', font=('Arial', 10), bg='CadetBlue3', fg='white', command=self.change_color, relief='ridge', borderwidth=3)
        self.color_button.grid(row=10, column=5, columnspan=3, sticky='nsew', pady=(15, 15))
        self.color_button.config(state="disabled")

        new_button = tk.Button(self.master, text='New Sudoku', command=self.newSudoku, relief='ridge', bg='CadetBlue3', fg='white',borderwidth=3)
        new_button.grid(row=4, column=13, columnspan=2, sticky='nsew', padx=(20, 20))

        self.difficulty_value_label = tk.Label(self.master, text="Difficulty: "+str(self.selected_sudoku.difficulty),  fg='red', font=self.difficulty_font)
        self.difficulty_value_label.grid(row=5, column=13, columnspan=2, sticky='nsew', padx=(20, 20))

    def getSudoku(self):
        # Load a random Sudoku puzzle from the list
        ready_puzzle_format = []
        self.selected_sudoku = random.choice(sudoku_list)
        for i in range(0, 81, 9):
            alt_liste = self.selected_sudoku.puzzle[i:i+9]
            alt_liste = [int(char) if char != '.' else 0 for char in alt_liste]
            ready_puzzle_format.append(alt_liste)
        return ready_puzzle_format

    def newSudoku(self):
        # Load a new Sudoku puzzle
        self.clear()
        self.initial_puzzle = self.getSudoku()
        self.difficulty_value_label.config(text="Difficulty: "+str(self.selected_sudoku.difficulty))
        self.resetSudoku()

    def resetSudoku(self):
        # Reset the current Sudoku board
        self.clear()
        self.sudoku_graph = SudokuGraph(self.initial_puzzle)
        self.changeDefaultColor()
        self.initialize_ui()

    def solve(self):
        # Attempt to solve the current Sudoku puzzle
        puzzle = [[0 for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                entry = self.entries[r][c]
                value = entry.get()
                if value.isdigit() and 1 <= int(value) <= 9:
                    puzzle[r][c] = int(value)
        print(puzzle)
        self.sudoku_graph = SudokuGraph(puzzle)
        if self.sudoku_graph.solve_sudoku():
            self.update_board()
            self.color_button.config(state="normal")
        else:
            messagebox.showinfo("Result", "No solution exists.")

    def update_board(self):
        # Update the UI with the solved puzzle
        for r in range(9):
            for c in range(9):
                entry = self.entries[r][c]
                if entry.get() == '':
                    value = self.sudoku_graph.get_board()[r][c]
                    entry.insert(0, str(value))
                    entry.config(fg='blue')
                    entry.config(state='readonly')

    def changeDefaultColor(self):
        # Change the default text color in entries
        for r in range(9):
            for c in range(9):
                entry = self.entries[r][c]
                entry.config(fg='black')

    def clear(self):
        # Clear all entries in the UI
        for r in range(9):
            for c in range(9):
                entry = self.entries[r][c]
                entry.config(state='normal')
                entry.delete(0, tk.END)
        self.color_button.config(state="disabled")

    def check_entry(self, event, row, col):
        # Handle entry input validation
        if event.char.isdigit() and 1 <= int(event.char) <= 9:
            entry = self.entries[row][col]
            if entry.get() != '':
                entry.delete(0, tk.END)
            entry.insert(0, event.char)
            entry.config(fg='blue')
        elif event.keycode == 8:  # Backspace key
            entry = self.entries[row][col]
            entry.delete(0, tk.END)
        return 'break'  # Prevent invalid input

    def change_color(self):
        # Toggle the color scheme of the Sudoku entries
        if self.color_toggle:
            color_map = {}
            color_list = ['red', 'green', 'blue', 'orange', 'DeepPink2', 'brown', 'black', 'dark slate gray', 'dark violet']
            self.previous_board = [row[:] for row in self.sudoku_graph.get_board()]
            self.previous_colors = [[entry.cget('fg') for entry in row] for row in self.entries]
            for r in range(9):
                for c in range(9):
                    entry = self.entries[r][c]
                    value = entry.get()
                    if value != '':
                        if value not in color_map:
                            color_map[value] = color_list.pop(0)
                        entry.config(fg=color_map[value])

            self.color_toggle = False
        else:
            if self.previous_board and self.previous_colors:
                for r in range(9):
                    for c in range(9):
                        entry = self.entries[r][c]
                        entry.delete(0, tk.END)
                        entry.insert(0, str(self.previous_board[r][c]))
                        entry.config(fg=self.previous_colors[r][c])

            self.color_toggle = True

root = tk.Tk()
root.minsize(480,430)
root.resizable(False, False)
icon = tk.PhotoImage(file="icon5.png")
root.iconphoto(False, icon)
app = SudokuUI(root)
root.mainloop()