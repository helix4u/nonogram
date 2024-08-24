import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty
from kivy.core.window import Window
import random

Window.size = (420, 768)

# Core Nonogram logic
def generate_structured_grid(height, width, density=0.5):
    grid = [[0 for _ in range(width)] for _ in range(height)]
    for i in range(height):
        for j in range(width):
            grid[i][j] = 1 if random.random() < density else 0
    return grid

def calculate_clues(line):
    clues = []
    count = 0
    for cell in line:
        if cell == 1:
            count += 1
        else:
            if count > 0:
                clues.append(count)
                count = 0
    if count > 0:
        clues.append(count)
    return clues or [0]

def generate_nonogram(height, width, density=0.5):
    grid = generate_structured_grid(height, width, density)
    row_clues = [calculate_clues(row) for row in grid]
    column_clues = [calculate_clues([grid[r][c] for r in range(height)]) for c in range(width)]
    return grid, row_clues, column_clues

# Custom widget for interactive Nonogram cell
class NonogramCell(ButtonBehavior, Widget):
    cell_state = NumericProperty(0)  # 0: unshaded, 1: shaded, 2: X

    def __init__(self, **kwargs):
        super(NonogramCell, self).__init__(**kwargs)
        self.bind(pos=self.update_rect, size=self.update_rect, cell_state=self.update_rect)
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.update_rect()

    def on_press(self):
        self.cell_state = (self.cell_state + 1) % 3
        self.update_rect()

    def update_rect(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self.cell_state == 0:  # Unshaded
                Color(0.8, 0.8, 0.8, 1)
            elif self.cell_state == 1:  # Shaded
                Color(0.2, 0.2, 0.2, 1)
            else:  # Marked with an 'X'
                Color(1, 1, 1, 1)
                self.rect = Rectangle(pos=self.pos, size=self.size)
                Color(0, 0, 0, 1)
                Line(points=[self.x, self.y, self.right, self.top], width=2)
                Line(points=[self.x, self.top, self.right, self.y], width=2)
                return
            self.rect = Rectangle(pos=self.pos, size=self.size)

class NonogramApp(App):
    def build(self):
        self.grid_height = 10
        self.grid_width = 10
        
        # Main layout with vertical orientation
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Grid layout for the Nonogram
        self.grid_layout = GridLayout(cols=self.grid_width + 1, rows=self.grid_height + 1, padding=10, spacing=5, size_hint=(None, None))
        main_layout.add_widget(self.grid_layout)
        
        # Persistent result label (directly below the grid)
        self.result_label = Label(text="Correctly shaded cells: 0 / 0 | Incorrectly shaded cells: 0", size_hint=(1, 0.1), height=40)
        main_layout.add_widget(self.result_label)
        
        # Add button for generating new Nonogram (below the result label)
        generate_button = Button(text='Generate New Nonogram', size_hint=(1, 0.1), height=50)
        generate_button.bind(on_press=self.generate_nonogram)
        main_layout.add_widget(generate_button)
        
        # Add button for checking progress at the bottom
        check_button = Button(text='Check Progress', size_hint=(1, 0.1), height=50)
        check_button.bind(on_press=self.check_progress)
        main_layout.add_widget(check_button)

        # Add button for move suggestion
        suggest_button = Button(text='Suggest Move', size_hint=(1, 0.1), height=50)
        suggest_button.bind(on_press=self.suggest_move)
        main_layout.add_widget(suggest_button)

        # Generate the initial Nonogram
        self.generate_nonogram()

        return main_layout

    def generate_nonogram(self, *args):
        # Clear grid before generating a new one
        self.grid_layout.clear_widgets()

        # Generate the grid and clues
        grid, row_clues, column_clues = generate_nonogram(self.grid_height, self.grid_width, density=0.5)
        self.solution_grid = grid  # Store the correct solution grid
        
        max_row_clues_len = max(len(clue) for clue in row_clues)
        max_col_clues_len = max(len(clue) for clue in column_clues)
        
        cell_size = min(Window.width // (self.grid_width + max_row_clues_len + 2), 
                        (Window.height * 0.7) // (self.grid_height + max_col_clues_len + 2))

        # Ensure that the grid has the correct number of rows and columns
        self.grid_layout.cols = self.grid_width + max_row_clues_len
        self.grid_layout.rows = self.grid_height + max_col_clues_len

        # Add column clues
        for i in range(max_col_clues_len):
            for j in range(max_row_clues_len):
                self.grid_layout.add_widget(Label(text=""))
            for clue in column_clues:
                if i < max_col_clues_len - len(clue):
                    self.grid_layout.add_widget(Label(text="", size_hint_y=None, height=cell_size // 2))  # Adjusted vertical space
                else:
                    self.grid_layout.add_widget(Label(text=str(clue[i - (max_col_clues_len - len(clue))]), font_size='14sp', size_hint_y=None, height=cell_size // 2))

        # Add row clues and grid cells
        self.cells = []  # Store references to the cells for checking progress
        for i, row in enumerate(grid):
            for j in range(max_row_clues_len):
                if j < max_row_clues_len - len(row_clues[i]):
                    self.grid_layout.add_widget(Label(text=""))
                else:
                    self.grid_layout.add_widget(Label(text=str(row_clues[i][j - (max_row_clues_len - len(row_clues[i]))]), font_size='14sp', size_hint_y=None, height=cell_size))

            for cell in row:
                nonogram_cell = NonogramCell(size_hint=(None, None), size=(cell_size, cell_size))
                self.cells.append(nonogram_cell)
                self.grid_layout.add_widget(nonogram_cell)
        
        # Reset the result label
        self.result_label.text = "Correctly shaded cells: 0 / 0 | Incorrectly shaded cells: 0"

        # Update grid layout size
        self.grid_layout.size = (self.grid_width * cell_size + max_row_clues_len * cell_size, self.grid_height * cell_size + max_col_clues_len * cell_size)

    def check_progress(self, *args):
        correct_count = 0
        incorrect_count = 0
        total_correct = sum(sum(row) for row in self.solution_grid)  # Total number of correct shaded cells
        
        for i, cell in enumerate(self.cells):
            row = i // self.grid_width
            col = i % self.grid_width
            if self.solution_grid[row][col] == 1:
                if cell.cell_state == 1:
                    correct_count += 1
                elif cell.cell_state == 0:
                    pass  # Unshaded and should be unshaded, so do nothing
                else:
                    incorrect_count += 1  # X-ed or shaded when it shouldn't be
            elif cell.cell_state == 1:
                incorrect_count += 1  # Shaded when it should be unshaded

        # Update result label with the latest count
        self.result_label.text = f"Correctly shaded cells: {correct_count} / {total_correct} | Incorrectly shaded cells: {incorrect_count}"

    def suggest_move(self, *args):
        # A basic suggestion algorithm that looks for the first unshaded square that should be shaded
        for i, cell in enumerate(self.cells):
            row = i // self.grid_width
            col = i % self.grid_width
            if self.solution_grid[row][col] == 1 and cell.cell_state == 0:
                # Suggest this move
                move = f"Suggested move: Shade cell in row {row + 1}, column {col + 1}"
                self.result_label.text = move
                return
        self.result_label.text = "No suggestions available!"

if __name__ == '__main__':
    NonogramApp().run()
