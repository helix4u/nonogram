# Nonogram Generator & Friends
![image](https://github.com/user-attachments/assets/70f5aa32-1300-4dfc-9ac3-7a19f64b9efc)

This repository contains a collection of Python scripts and Kivy applications for generating, playing, and solving Nonograms and other puzzle games. It’s a work in progress, so expect bugs—feel free to break things, fix them, and repeat the process.

## Prerequisites

- **Python 3.x**: Make sure you have Python installed. You can download it from the official Python website.
- **Kivy**: Required for running the Kivy applications. Installation instructions are below.

## Installation

### Clone the Repository

Start by cloning this repository to your local machine:

```bash
git clone https://github.com/helix4u/nonogram.git
cd nonogram
```

### Install Dependencies

If you want to run the Kivy applications, you'll need to install Kivy:

```bash
pip install kivy
```

## Usage

### Running the Command Line Nonogram Generator

You can generate and format Nonograms using the command-line script:

```bash
python nonogram.py
```

This script doesn't require any additional dependencies beyond Python's standard library, so it should run out of the box.

### Running the Kivy Nonogram Apps

There are two Kivy applications for playing and solving Nonograms, each offering different ways to get hints.

#### Standard Kivy App:

```bash
python nonogram_kivy_WIP.py
```

#### Alternative Suggestion Kivy App:

This one is modified to work with Pydroid 3 on android. Tested on a Galaxy S23 Ultra. Functional, not pretty. ![image](https://github.com/user-attachments/assets/ef749d46-2925-4498-a310-77b3ef8bb5cf)



```bash
python nonogram_kivy_alt_suggest_WIP.py
```

#### Sudoku

![image](https://github.com/user-attachments/assets/37ad9dac-231b-4a37-998e-832516e81085)


```bash
python sudoku.py
```

These are works in progress, so you might encounter some bugs. Don’t hesitate to tweak the code, test it, and improve it.

## Contributing

This is a project for those who like to dive in, mess around, and make improvements. If you find any bugs (and you probably will), feel free to fix them and submit a pull request.

## Troubleshooting

If something’s not working, here are a few steps to try:

1. **Dependencies**: Ensure all required dependencies are installed.
2. **Python Version**: Make sure you're using a compatible Python version.
3. **Bug Fixing**: The scripts are in development, so they may need some debugging. Don't hesitate to explore the code and make adjustments.

## License

This project is open-source, so feel free to use, modify, and distribute it as you see fit.
