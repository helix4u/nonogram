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

def calculate_adjacent_shaded(solved_grid):
    rows, cols = len(solved_grid), len(solved_grid[0])
    adjacent_counts = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            if solved_grid[r][c] == 1:
                # Check all 8 adjacent cells
                for i in range(max(0, r-1), min(r+2, rows)):
                    for j in range(max(0, c-1), min(c+2, cols)):
                        if (i, j) != (r, c):
                            adjacent_counts[r][c] += solved_grid[i][j]

    return adjacent_counts

# Custom widget for interactive Nonogram cell
class NonogramCell(ButtonBehavior, Widget):
    cell_state = NumericProperty(0)  # 0: unshaded, 1: shaded, 2: X

    def __init__(self, quadrant_color, **kwargs):
        super(NonogramCell, self).__init__(**kwargs)
        self.quadrant_color = quadrant_color
        self.darker_shade = [c * 0.6 for c in quadrant_color]  # Darker shade of the vibrant quadrant color
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
                Color(*self.quadrant_color)
            elif self.cell_state == 1:  # Shaded
                Color(*self.darker_shade)
            else:  # Marked with an 'X'
                Color(*self.quadrant_color)
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
        
        # Get screen size at runtime
        self.screen_width = Window.width
        self.screen_height = Window.height
        
        # Main layout with vertical orientation
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Grid layout for the Nonogram
        self.grid_layout = GridLayout(cols=self.grid_width + 1, padding=5, spacing=1, size_hint=(None, None))
        main_layout.add_widget(self.grid_layout)
        
        # Persistent result label (directly below the grid)
        self.result_label = Label(
            text="Correctly shaded cells: 0 / 0 | Incorrectly shaded cells: 0",
            size_hint=(1, None),  
            height=50,  
            text_size=(Window.width - 20, None),  
            font_size='12sp',  
            halign='left',  
            valign='middle',
            padding_y=10  
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))  
        main_layout.add_widget(self.result_label)
        
        # Add button for generating new Nonogram
        generate_button = Button(text='Generate New Nonogram', size_hint=(1, 0.07), height=40)
        generate_button.bind(on_press=self.generate_nonogram)
        main_layout.add_widget(generate_button)
        
        # Add button for checking progress
        check_button = Button(text='Check Progress', size_hint=(1, 0.07), height=40)
        check_button.bind(on_press=self.check_progress)
        main_layout.add_widget(check_button)

        # Add button for move suggestion
        suggest_button = Button(text='Suggest Move', size_hint=(1, 0.07), height=40)
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
        
        # Define vibrant quadrant colors
        quadrant_colors = [
            (0.4, 0.7, 1, 1),  # Vibrant blue
            (0.4, 1, 0.4, 1),  # Vibrant green
            (1, 0.4, 0.4, 1),  # Vibrant red
            (1, 1, 0.4, 1)     # Vibrant yellow
        ]
        
        max_row_clues_len = max(len(clue) for clue in row_clues)
        max_col_clues_len = max(len(clue) for clue in column_clues)

        cell_size = min(self.screen_width // (self.grid_width + max_row_clues_len + 2), 
                        (self.screen_height * 0.6) // (self.grid_height + max_col_clues_len + 2))

        # Ensure that the grid has the correct number of rows and columns
        self.grid_layout.cols = self.grid_width + max_row_clues_len
        self.grid_layout.rows = self.grid_height + max_col_clues_len

        # Add column clues
        for i in range(max_col_clues_len):
            for j in range(max_row_clues_len):
                self.grid_layout.add_widget(Label(text="", size_hint_y=None, height=cell_size // 2))
            for clue in column_clues:
                if i < max_col_clues_len - len(clue):
                    self.grid_layout.add_widget(Label(text="", size_hint_y=None, height=cell_size // 2)) 
                else:
                    self.grid_layout.add_widget(Label(text=str(clue[i - (max_col_clues_len - len(clue))]), font_size='12sp', size_hint_y=None, height=cell_size // 2))

        # Add row clues and grid cells
        self.cells = []  # Store references to the cells for checking progress
        for i, row in enumerate(grid):
            for j in range(max_row_clues_len):
                if j < max_row_clues_len - len(row_clues[i]):
                    self.grid_layout.add_widget(Label(text="", size_hint_y=None, height=cell_size))
                else:
                    self.grid_layout.add_widget(Label(text=str(row_clues[i][j - (max_row_clues_len - len(row_clues[i]))]), font_size='12sp', size_hint_y=None, height=cell_size))

            for j, cell in enumerate(row):
                q_index = (i // (self.grid_height // 2)) * 2 + (j // (self.grid_width // 2))  # Determine quadrant index
                nonogram_cell = NonogramCell(quadrant_colors[q_index], size_hint=(None, None), size=(cell_size, cell_size))
                self.cells.append(nonogram_cell)
                self.grid_layout.add_widget(nonogram_cell)
        
        # Reset the result label
        self.result_label.text = "Correctly shaded cells: 0 / 0 | Incorrectly shaded cells: 0"

        # Calculate adjacent shaded cells for the solution grid
        self.adjacent_counts = calculate_adjacent_shaded(self.solution_grid)

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
        # Find the cell with the most adjacent shaded cells that is not yet shaded
        max_adjacent = -1
        suggestion = None

        for i, cell in enumerate(self.cells):
            row = i // self.grid_width
            col = i % self.grid_width
            if self.solution_grid[row][col] == 1 and cell.cell_state == 0:
                if self.adjacent_counts[row][col] > max_adjacent:
                    max_adjacent = self.adjacent_counts[row][col]
                    suggestion = (row, col)

        if suggestion:
            row, col = suggestion
            move = f"Suggested move: Shade cell in row {row + 1}, column {col + 1}"
            self.result_label.text = move
        else:
            self.result_label.text = "No suggestions available!"

if __name__ == '__main__':
    NonogramApp().run()
