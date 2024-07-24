# LinkedIn N-Queens Solver

This project provides an automated solution for the "Queens" game on LinkedIn, implementing a solver for the classic N-Queens problem.

## Description

The LinkedIn N-Queens Solver is a Python script that automates the process of solving the N-Queens puzzle in LinkedIn's "Queens" game. It uses web scraping techniques to interact with the game interface, solves the puzzle programmatically, and inputs the solution automatically.

Key features:
- Automated login to LinkedIn
- Web scraping to extract the game board
- Implementation of a backtracking algorithm to solve the N-Queens problem
- Automated input of the solution to the game interface

## Requirements

- Python 3.x
- Playwright
- BeautifulSoup4
- NumPy
- Matplotlib

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/JavierHiruelo/linkedin-n-queens-solver.git
   ```

2. Install the required packages:
   ```
   pip install playwright beautifulsoup4 numpy matplotlib
   ```

3. Install the Playwright browsers:
   ```
   playwright install
   ```

## Usage

1. Run the script:
   ```
   python N_Queens_Solver.py
   ```

2. When prompted, enter your LinkedIn username and password.

3. The script will automatically log in to LinkedIn, navigate to the Queens game, solve the puzzle, and input the solution.

## How it works

1. The script uses Playwright to automate browser interactions.
2. It logs into LinkedIn using the provided credentials.
3. The game board is extracted using BeautifulSoup.
4. The N-Queens problem is solved using a backtracking algorithm.
5. The solution is automatically input into the game interface.

## Note

This project is for educational purposes only. Be aware that automated interactions with websites may violate terms of service. Use responsibly and at your own risk.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/JavierHiruelo/linkedin-n-queens-solver/issues) if you want to contribute.

## License

MIT License

Copyright (c) [2024] [Javier Hiruelo Pérez]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
