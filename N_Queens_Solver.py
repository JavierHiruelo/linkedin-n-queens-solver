from playwright.sync_api import Playwright, sync_playwright
from bs4 import BeautifulSoup
import time
import numpy as np
import matplotlib.pyplot as plt

# We need to ask for the LinkedIn username and password to the user
#! YOU CAN ADD YOUR LINKEDIN USERNAME AND PASSWORD HERE
username = input("Enter username:")
password = input("Enter password:")

def get_board_size(soup: BeautifulSoup) -> int:
    """
    Get the size of the board from the HTML content of the n-queens game.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the HTML content of the n-queens game.

    Returns:
        int: The size of the board.
    """
    
    # Find the div with class 'queens-grid'
    queens_grid_div = soup.find('div', class_='queens-grid')

    # Extract the style attribute
    style_attribute = queens_grid_div.get('style')

    return int(style_attribute.split(';')[0].split(':')[1])


def get_board(soup: BeautifulSoup, board_size: int) -> np.array:
    """
    Given a BeautifulSoup object representing an HTML document, extracts the board from the document and returns it as a 9x9 numpy array.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing an HTML document.

    Returns:
        numpy.ndarray: A board_size x board_size numpy array representing the board. Each element of the array is a string representing the color of the corresponding cell on the board.
    """
    # Initialize an empty list to store the colors of the cells
    board = []
    
    # Iterate over each div element in the document
    for div in soup.select(selector="div"):
        
        # Check if the div has a class attribute and if it contains the class "queens-cell"
        if div.has_attr("class") and "queens-cell" in div["class"]:
            # Extract the color of the cell by splitting the class attribute and taking the second element
            color = div["class"][1].split("-")[-1]
            # Append the color to the board list
            board.append(color)
    
    # Convert the board list to a numpy array and 
    # reshape it to a board_size x board_size matrix
    return np.asarray(board).reshape(board_size, board_size)



def normalize_board(board: np.array) -> np.array:
    """
    Normalizes a board_size x board_size board by converting each unique integer value to a value between 0 and board_size - 1.

    Parameters:
        board (np.array): A board_size x board_size numpy array representing the board.

    Returns:
        np.array: A board_size x board_size numpy array with normalized values between 0 and board_size - 1.

    The function converts the board, which is represented as a numpy array, to a range of
    values between 0 and board_size - 1. It does this by first converting all values to integers,
    then iterating over all unique values in the board and replacing all occurrences of that value
    with its corresponding index in the range [0, board_size - 1]. The resulting numpy array is returned.
    """
    
    # We want to normalize the board to be in the range [0, 8]
    board = board.astype(int)
    
    # Find all unique values in the board
    uniques = np.unique(board)
    
    # Iterate over each unique value and replace all occurrences with its index
    for i in range(len(uniques)):
        board[board == uniques[i]] = i
        
    return board

    

def plot_board(board: np.array) -> None:
    """
    Plots a matrix visualization of the given numpy array board.

    Args:
        board (np.array): A numpy array representing the board.

    Returns:
        None: This function does not return anything.

    This function plots a matrix visualization of the given numpy array board.
    The matrix is plotted using matplotlib's imshow function. The colors used for
    each integer value in the board are defined in the colors list. The colorbar is
    added to the plot to show the corresponding integer values. The title of the plot
    is set to 'Matrix Visualization'.
    """
    
    # Plot the matrix
    plt.imshow(board, 
               interpolation='nearest')
    
    # Add a colorbar with ticks for each integer
    plt.colorbar(ticks=range(np.max(board) + 1))
    
    # Set the title of the plot
    plt.title('Matrix Visualization')
    
    # Show the plot
    plt.show()



class Solver:
    def __init__(self, board, board_size):
        self.board = board
        self.board_size = board_size
        self.solution = np.zeros((board_size, board_size))
    
    
    
    def solve(self):
        """
        Solves the n-queens problem by recursively placing queens on the board.

        Returns:
            numpy.ndarray or None: A 2D numpy array representing the solution 
            board if a valid solution is found.
            None: If no valid solution is found.
        """
        if self.place_queen(0):
            return self.solution
        else:
            return None  # No valid solution found
    
    
    
    def place_queen(self, row):
        """
        Place a queen on the board at the given row index.

        Args:
            row (int): The row index to place the queen.

        Returns:
            bool: True if a valid solution is found, False otherwise.

        This function recursively places a queen on the board at the given row 
        index. It checks if the row index is greater than or equal to 9, in 
        which case it returns True to indicate that a valid solution has been 
        found. Otherwise, it iterates over each column index and checks if the 
        given row and column are valid for placing a queen. If a valid position 
        is found, the queen is placed on the board and the function recursively 
        calls itself with the next row index. If a valid solution is found, the 
        function returns True. Otherwise, it resets the queen at the current 
        position and continues to the next column. If no valid solution is found, 
        the function returns False.

        Note: This function assumes that the `self.solution` attribute is a 2D 
        numpy array representing the current solution board.
        """
        if row >= self.board_size:
            return True
        
        for col in range(self.board_size):
            if self.is_valid(row, col):
                self.solution[row, col] = 1
                if self.place_queen(row + 1):
                    return True
                self.solution[row, col] = 0
        
        return False
    
    
    
    def is_valid(self, row, col):
        """
        Check if the given row and column are valid for placing a queen in the current solution.

        Parameters:
            row (int): The row index of the queen.
            col (int): The column index of the queen.

        Returns:
            bool: True if the given row and column are valid, False otherwise.

        This function checks if the given row and column are valid for placing a queen in 
        the current solution. It first checks if there is already a queen in the same column 
        by summing the values in the corresponding column of the solution matrix. If the sum 
        is greater than 0, it means there is already a queen in that column, and the function 
        returns False.

        Then, it checks if there is already a queen in the same row by summing the values in 
        the corresponding row of the solution matrix. If the sum is greater than 0, it means 
        there is already a queen in that row, and the function returns False.

        Next, it checks if there is already a queen in the diagonally adjacent cells by checking 
        the values in the diagonally adjacent cells of the solution matrix. If any of the 
        adjacent cells have a value of 1, it means there is already a queen in that cell, and 
        the function returns False.

        If none of the above conditions are met, it calls the `is_color_valid` method to check 
        if the color of the queen at the given row and column is valid. If the color is valid, 
        the function returns True. Otherwise, it returns False.

        Note: This function assumes that the `self.solution` attribute is a 2D numpy array 
        representing the current solution.
        """
        # Check for queens in the same column
        if np.sum(self.solution[:, col]) > 0:
            return False
        
        # Check for queens in the same row
        if np.sum(self.solution[row, :]) > 0:
            return False
        
        # Check for queens adjacent diagonally
        if row > 0 and col > 0 and self.solution[row - 1, col - 1] == 1:
            return False
        if row > 0 and col < self.board_size-1 and self.solution[row - 1, col + 1] == 1:
            return False
        if row < self.board_size-1 and col > 0 and self.solution[row + 1, col - 1] == 1:
            return False
        if row < self.board_size-1 and col < self.board_size-1 and self.solution[row + 1, col + 1] == 1:
            return False
        
        return self.is_color_valid(row, col)



    def is_color_valid(self, row, col):
        """
        Check if the color at the given row and column is valid.

        Parameters:
            row (int): The row index of the color.
            col (int): The column index of the color.

        Returns:
            bool: True if the color is valid, False otherwise.

        This function checks if the color at the given row and column is valid by 
        comparing the number of unique colors in the solution board with the number 
        of unique colors after adding the color at the given row and column. If the 
        two numbers are equal, it means that the color is not valid and the function 
        returns False. Otherwise, it returns True.

        The function first retrieves the colors from the solution board using the 
        condition `self.solution == 1`. It then converts the resulting array of colors
        into two sets, `colors1` and `colors2`, to remove duplicates. The color at 
        the given row and column is added to `colors1` using `colors1.add(self.board[row, col])`. 
        Finally, the function checks if the length of `colors1` is equal to the length of `colors2`, 
        and returns False if they are equal, indicating that the color is not valid. Otherwise, 
        it returns True.

        Note: This function assumes that the `self.board` attribute is a 2D array 
        representing the solution board, and the `self.solution` attribute is a 2D array 
        representing the solution.
        """
        colores = self.board[self.solution == 1]
        colors1 = set(colores)
        colors2 = set(colores)
        colors1.add(self.board[row, col])
        if len(colors1) == len(colors2):
            return False
        else:
            return True



def is_valid(board, solution, board_size):
    """
    Check if a given solution is valid for the n-queens problem.

    Args:
        board (numpy.ndarray): The board representing the n-queens problem.
        solution (numpy.ndarray): The solution to be checked.

    Returns:
        bool: True if the solution is valid, False otherwise.

    This function checks if a given solution is valid for the n-queens problem. It first checks if the number of queens is correct, then checks if there are queens in the same column, same row, and adjacent diagonally. Finally, it checks if there are queens in the same color.

    The function takes a board and a solution as input. The board is a 2D numpy array representing the n-queens problem, where each cell contains a color. The solution is a 2D numpy array representing the position of the queens on the board, where each cell contains a 1 if there is a queen at that position, and a 0 otherwise.

    The function returns True if the solution is valid, and False otherwise. If the solution is not valid, the function prints the reason why it is not valid.

    The function uses numpy to perform the necessary calculations and checks.
    """
    # First we need to check that the number of queens is correct
    if np.sum(solution) != board_size:
        print("Number of queens is not {board_size}")
        return False
    
    # Check for queens in the same column
    for col in range(board_size):
        if np.sum(solution[:, col]) > 1:
            print("Queens in the same column")
            return False
        
    # Check for queens in the same row
    for row in range(board_size):
        if np.sum(solution[row, :]) > 1:
            print("Queens in the same row")
            return False
        
    queens = np.argwhere(solution == 1)

    # Check for queens adjacent diagonally (they are not queens really they are like a king + bishop)
    for queen in queens:
        row, col = queen
        if row > 0 and col > 0 and solution[row - 1, col - 1] == 1:
            print("Queens adjacent diagonally")
            return False
        if row > 0 and col < board_size-1 and solution[row - 1, col + 1] == 1:
            print("Queens adjacent diagonally")
            return False
        if row < board_size-1 and col > 0 and solution[row + 1, col - 1] == 1:
            print("Queens adjacent diagonally")
            return False
        if row < board_size-1 and col < board_size-1 and solution[row + 1, col + 1] == 1:
            print("Queens adjacent diagonally")
            return False
        
    # Check for queens in the same color
    for queen in queens:
        row, col = queen
        color = board[row, col]
        for i in range(board_size):
            for j in range(board_size):
                if solution[i, j] == 1 and board[i, j] == color and (i != row or j != col):
                    print("Queens in the same color")
                    print(f"Queen at ({i}, {j}) and queen at ({row}, {col})")
                    return False
                
    return True



def get_solution_positions(solution: np.array, board_size: int) -> list:
    """
    Get the positions of the queens in the solution.

    Args:
        solution (numpy.ndarray): The solution to the n-queens problem.

    Returns:
        list: A list of positions where the queens are located.

    This function takes a solution to the n-queens problem as input and returns a list of positions where the queens are located.

    The function iterates over the indices where the solution array is equal to 1, which correspond to the positions of the queens. It then converts the row and column indices into a single index and appends it to the positions list.

    The function returns the positions list.
    """

    # Initialize an empty list to store the positions
    positions = []

    # Iterate over the indices where the solution array is equal to 1
    for row, col in np.argwhere(solution == 1):
        # Convert the row and column indices into a single index
        position = row * board_size + col
        # Append the position to the positions list
        positions.append(position)

    # Return the positions list
    return positions

  

def run(playwright: Playwright) -> None:
    """
    Runs a Playwright script to solve the n-queens problem on LinkedIn.

    Args:
        playwright (Playwright): The Playwright object used to launch the browser.

    Returns:
        None

    This function launches a Chromium browser using the Playwright library and performs the following steps:
    1. Opens the LinkedIn page for the n-queens game.
    2. Waits for the session key and session password inputs to be available on the page.
    3. Fills in the session key and session password inputs with the provided username and password.
    4. Submits the form to log in.
    5. Waits for the "Start" button to be available on the page.
    6. Clicks the "Start" button to start the game.
    7. Waits for the game grid to be available on the page.
    8. Retrieves the HTML content of the game grid.
    9. Parses the HTML content to obtain the game board.
    10. Normalizes the game board.
    11. Solves the n-queens problem using the Solver class.
    12. Retrieves the positions of the queens on the board.
    13. Double-clicks on each cell containing a queen on the game grid.
    14. Waits for 10 seconds.
    15. Closes the browser context and browser.

    Note: The function assumes that the username and password variables are defined and contain the appropriate values.
    """
    
    browser = playwright.chromium.launch(
        headless=False, 
        slow_mo=50,
        args=["--start-maximized"]
    )
    context = browser.new_context()
    page = context.new_page()
    
    # Open the LinkedIn page for the n-queens game
    page.goto("https://www.linkedin.com/games/queens/")
    
    # Ensure the page has fully loaded and the input is available
    page.wait_for_selector('input[name="session_key"]')
    page.wait_for_selector('input[name="session_password"]')
    
    # Fill in the session key and session password inputs
    page.fill("input[name=\"session_key\"]", username)
    page.fill("input[name=\"session_password\"]", password)
    page.click("button[type=\"submit\"]")
    
    
    page.wait_for_selector('div[class="launch-footer "]')
    
    if page.is_visible("button[id=\"ember34\"]"):
        page.click("button[id=\"ember34\"]")
    if page.is_visible("button[id=\"ember35\"]"):
        page.click("button[id=\"ember35\"]")
    if page.is_visible("button[id=\"ember36\"]"):
        page.click("button[id=\"ember36\"]")
    if page.is_visible("button[id=\"ember37\"]"):
        page.click("button[id=\"ember37\"]")
    
    # Wait for the game grid to be available
    page.wait_for_selector('div[class="queens-grid"]')

    grid_html = page.inner_html('div[class="queens-board-wrapper game-board"]')
    soup = BeautifulSoup(grid_html, 'html.parser')
    board_size = get_board_size(soup)    # Returns an integer
    
    # Retrieve the HTML content of the game grid
    grid_html = page.inner_html('div[class="queens-grid"]')
    soup = BeautifulSoup(grid_html, 'html.parser')
    
    # Parse the HTML content to obtain the game board
    board = get_board(soup, board_size)  # Returns a numpy array of size (board_size, board_size)
    board = normalize_board(board)       # Returns the array with values between 0 and board_size - 1
    
    # Solve the n-queens problem
    solver = Solver(board, board_size)
    solution = solver.solve()    
    positions = get_solution_positions(solution, board_size)  # Returns a list of positions where the queens are located
    
    # Double-click on each cell containing a queen
    for position in positions:
        page.dblclick(f"div[data-cell-idx=\"{position}\"]")
    
    time.sleep(10)
    
    # ---------------------
    context.close()
    browser.close()
    
    
with sync_playwright() as playwright:
    run(playwright)