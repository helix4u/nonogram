from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from random import sample
from copy import deepcopy


class SudokuGrid(GridLayout):
    def __init__(self, **kwargs):
        super(SudokuGrid, self).__init__(**kwargs)
        self.cols = 9
        self.rows = 9
        self.padding = [10, 10, 10, 10]  # Padding around the grid
        self.spacing = [5, 5]  # Slightly larger spacing for better visibility
        self.puzzle, self.solution = self.generate_sudoku()
        self.inputs = []

        self.create_grid()

    def create_grid(self):
        """Create and initialize the Sudoku grid."""
        self.clear_widgets()

        # Create grid with increased size, scaling with window width
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] != 0:
                    ti = TextInput(text=str(self.puzzle[i][j]), readonly=True,
                                   font_size=40,  # Increased font size
                                   halign='center', padding_y=(20, 20),  # Increased padding for better visual
                                   foreground_color=(0, 0, 0, 1),
                                   background_color=(0.8, 0.8, 0.8, 1),
                                   multiline=False, size_hint=(None, None), height=100, width=self.width * 0.1)  # Scaling
                    ti.cursor = (0, 0)
                    ti.disabled = True
                else:
                    ti = TextInput(font_size=40,
                                   halign='center', padding_y=(20, 20),
                                   foreground_color=(0, 0, 0, 1), multiline=False,
                                   size_hint=(None, None), height=100, width=self.width * 0.1)  # Scaling
                    ti.focus = False

                self.inputs.append(ti)
                self.add_widget(ti)

    def on_size(self, *args):
        """Handle resizing for the grid elements."""
        for ti in self.inputs:
            ti.width = self.width * 0.1

    def generate_sudoku(self):
        """Generates a random Sudoku puzzle and its solution"""
        base = 3
        side = base * base

        def pattern(r, c): return (base * (r % base) + r // base + c) % side
        def shuffle(s): return sample(s, len(s))
        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        solution = [[nums[pattern(r, c)] for c in cols] for r in rows]

        puzzle = deepcopy(solution)
        for i in sample(range(side * side), side * side // 2):
            puzzle[i // side][i % side] = 0

        return puzzle, solution

    def update_grid(self):
        """Updates the grid with a new puzzle and clears all cells."""
        self.puzzle, self.solution = self.generate_sudoku()

        self.clear_widgets()
        self.inputs.clear()

        self.create_grid()

    def check_solution(self):
        """Checks the current user input against the solution and provides feedback."""
        correct_count = 0
        total_filled = 0

        for i in range(9):
            for j in range(9):
                input_value = self.inputs[i * 9 + j].text

                if input_value and input_value.isdigit():
                    total_filled += 1
                    if int(input_value) == self.solution[i][j]:
                        correct_count += 1

        if total_filled == 0:
            self.show_popup("No cells have been filled in yet.")
        else:
            self.show_popup(f"Correct: {correct_count}/{total_filled} filled cells.")

    def show_popup(self, message):
        """Show a popup with a message and wrap the text if necessary."""
        label = Label(text=message, halign="center", valign="middle", text_size=(300, None))
        label.bind(size=lambda *x: label.setter('text_size')(label, (label.width, None)))

        self.popup = Popup(title="Result", content=label, size_hint=(0.7, 0.3))
        self.popup.open()

    def show_confirm_new_puzzle(self):
        """Show confirmation popup to generate a new puzzle"""
        content = GridLayout(cols=2)
        yes_button = Button(text="Yes")
        no_button = Button(text="No")

        content.add_widget(yes_button)
        content.add_widget(no_button)

        self.confirm_popup = Popup(title="Generate new puzzle?", content=content, size_hint=(0.6, 0.3))

        yes_button.bind(on_press=lambda x: self.new_puzzle())
        yes_button.bind(on_press=lambda x: self.confirm_popup.dismiss())
        no_button.bind(on_press=self.confirm_popup.dismiss)

        self.confirm_popup.open()

    def new_puzzle(self):
        """Generates and updates the grid with a new puzzle"""
        self.update_grid()


class SudokuApp(App):
    def build(self):
        layout = GridLayout(cols=1, padding=[10, 10, 10, 10], spacing=[10, 10])

        sudoku_grid = SudokuGrid(size_hint=(1, None))
        sudoku_grid.bind(minimum_height=sudoku_grid.setter('height'))
        layout.add_widget(sudoku_grid)

        check_button = Button(text="Check Solution", size_hint=(1, 0.1))
        check_button.bind(on_press=lambda x: sudoku_grid.check_solution())
        layout.add_widget(check_button)

        new_puzzle_button = Button(text="New Puzzle", size_hint=(1, 0.1))
        new_puzzle_button.bind(on_press=lambda x: sudoku_grid.show_confirm_new_puzzle())
        layout.add_widget(new_puzzle_button)

        return layout


if __name__ == "__main__":
    SudokuApp().run()
