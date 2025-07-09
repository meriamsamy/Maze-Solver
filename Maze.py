import random
import tkinter as tk
# Generate a random maze
def generate_maze():
    maze = []

    for i in range(10): #rows
        row = []
        for j in range(10): #cols
            cell = 0 if random.random() < 0.7 else 1 #70% path ,30% walls
            row.append(cell)
        maze.append(row)
    
    for col in range(10): #choose start
        if maze[0][col] == 0:  
            maze[0][col] = 'S'  
            break

    for col in range(10):  #choose goal
        if maze[10-1][col] == 0: 
            maze[10-1][col] = 'G'  
            break

    solved, path = solver(maze) #make sure generated maze has path,(base case)
    if solved:
        return maze, path
    else: 
        return generate_maze() #recursion case

# Find position of S or G
def find(maze, target):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == target:
                return (i, j)
    return None

# Print the maze with optional path highlighting
def printMaze(maze, path=None):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if path and (i, j) in path and maze[i][j] not in ['S', 'G']:
                print('0', end=' ')  # path
            elif maze[i][j] == 'S':
                print('S', end=' ')
            elif maze[i][j] == 'G':
                print('G', end=' ')
            elif maze[i][j] == 1:
                print('#', end=' ')  # Walls
            else:
                print('.', end=' ')  # Open spaces
        print()

# BFS Maze Solver
def solver(maze):
    row, col = len(maze), len(maze[0])
    start = find(maze, 'S')
    goal = find(maze, 'G')

    if not start or not goal:
        return False, []

    q = [start]  
    visited = {start}  
    parent = {start: None}  # Track shortest path
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    path = []
    path_print=[] # to print the shortest path step by step in correct order

    print("\nExploring the maze step by step:")
    while q: 
        x, y = q.pop(0) 

        # Print maze step by step
        printMaze(maze, visited)
        print()

        # If goal is reached
        if (x, y) == goal:
            print("\nPath found!")

            while (x, y) is not None: 
                path.append((x, y))
                x, y = parent[(x, y)]
                if (x,y)==start:break
            path.reverse() # to correct order
            for(x,y) in path[:-1]: # we removed the last index because it rfers to the goal and repeats printing the maze with the same state
                path_print.append((x,y))
                printMaze(maze,path_print)
                print()    
            return True, path

        #  find all possible moves
        for dx, dy in directions:
            nx, ny = x + dx, y + dy 
            if 0 <= nx < row and 0 <= ny < col and maze[nx][ny] != 1 and (nx, ny) not in visited:
                q.append((nx, ny))  
                visited.add((nx, ny))  
                parent[(nx, ny)] = (x, y)  
                
    return False, []

# GUI Application
class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver Adventure")
        self.root.geometry("800x600")  # Adjusted window size
        self.root.resizable(False, False)
        self.cell_size = 40  # Adjusted cell size for 400x400 canvas (10x40)
        self.maze = None
        self.path = None
        self.canvas = None
        self.solving_label = None
        self.final_label = None
        self.solve_button = None
        self.end_button = None
        self.playagain_button = None
        
        # Custom font styles (adjusted sizes)
        self.title_font = ("Impact", 34, "bold")  
        self.button_font = ("Gill Sans MT", 10, "bold") 
        self.label_font = ("Arial Rounded MT Bold", 16, "bold")  
        
        # Main title
        self.title_label = tk.Label(root, text="Maze Solver Adventure", font=self.title_font, bg="#700b55", fg="black") #dark pink bg
        self.title_label.pack(pady=100)  
        
        # Start button
        self.start_button = tk.Button(root, text="START GAME", command=self.show_maze, width=10, font=self.title_font,
            bg="#700b55", #dark pink
            fg="white",     
            activebackground="#4f093c", #very dark pink
            activeforeground="white",
            relief="raised"
        )
        self.start_button.pack(pady=10)  
        # Initialize final_label
        self.final_label = tk.Label(
            self.root, text="Maze Solved!", fg="white", bg="#a8145c", font=("Arial", 18, "bold"), relief="ridge", padx=5, pady=3) #pink bg
    
    def draw_maze(self):
        self.canvas.delete("all")
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if self.maze[row][col] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#2d3436", outline="#636e72") #fill dark gray outline gray
                elif self.maze[row][col] == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#dfe6e9", outline="#b2bec3") #fill light gray outline gray
                elif self.maze[row][col] == 'S':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#a82113", outline="#78160c")#fill dark red outline outline very dark red
                elif self.maze[row][col] == 'G':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#065407", outline="#034204")#fill dark green outline very dark green

    def animate_path(self, path, index=0):
        if index >= len(path):
            self.root.after(500, self.show_final_message)
            return
        row, col = path[index]
        if self.maze[row][col] not in ['S', 'G']:
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#f1c40f", outline="#f39c12") #fill yellow outline orange
        self.root.after(200, self.animate_path, path, index + 1)

    def show_maze(self):
        self.title_label.pack_forget()
        self.start_button.pack_forget()
        # Generate maze
        self.maze, self.path = generate_maze()
        # Create canvas
        self.canvas = tk.Canvas(
            self.root, 
            width=400,  # 10x40=400px
            height=400, 
            bg="#34495e", #dark blue
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.pack(pady=15)  
        # Draw maze
        self.draw_maze()
        # Create solving label
        self.solving_label = tk.Label(
            self.root, 
            text="Ready to Solve", 
            font=self.label_font, 
            bg="#700b55", #dark pink
            fg="white",
            relief="ridge", 
            padx=5,  
            pady=3   
        )
        self.solving_label.pack(before=self.canvas, pady=10)  
        # Solve button
        self.solve_button = tk.Button(
            self.root, 
            text="SOLVE MAZE", 
            command=self.solve_maze_action,
            width=10,  
            font=self.button_font,
            bg="#700b55", #dark pink
            fg="white",
            activebackground="#4f093c", #very dark pink
            activeforeground="white",
            relief="raised"
        )
        self.solve_button.pack(pady=15)  

    def solve_maze_action(self):
        self.solve_button.pack_forget()
        self.solving_label.config(text="Solving Maze..")
        self.solving_label.pack(before=self.canvas, pady=10)  
        # Start path animation
        self.animate_path(self.path)
      

    def show_final_message(self):
        self.solving_label.pack_forget()
        self.final_label.pack(pady=15)  
        # Play Again button
        self.playagain_button = tk.Button(
            self.root, 
            text="PLAY AGAIN", 
            command=self.play_again,
            width=10,  
            font=self.button_font,
            bg="#700b55", #dark pink
            fg="white",
            activebackground="#4f093c", #very dark pink
            activeforeground="white",
            relief="raised"
        )
        self.playagain_button.pack(pady=10)  
        # End button
        self.end_button = tk.Button(
            self.root, 
            text="EXIT GAME", 
            command=self.root.destroy,
            width=10,  
            font=self.button_font,
            bg="#700b55", #dark pink
            fg="white",
            activebackground="#4f093c", #very dark pink
            activeforeground="white",
            relief="raised"
        )
        self.end_button.pack(pady=10)  

    def play_again(self):
        # Hide final UI elements
        self.final_label.pack_forget()
        self.end_button.pack_forget()
        self.playagain_button.pack_forget()
        # Reset canvas
        self.canvas.delete("all")
        self.canvas.pack_forget()
        # Generate new maze
        self.maze, self.path = generate_maze()
        # Create new canvas
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="#34495e", relief="ridge") #dark blue bg
        self.canvas.pack(pady=15)  
        # Draw new maze
        self.draw_maze()
        # Create new solving label
        self.solving_label = tk.Label(
            self.root, 
            text="Ready to Solve", 
            font=self.label_font, 
            bg="#700b55", #dark pink
            fg="white",
            relief="ridge", 
            padx=5,  
            pady=3   
        )
        self.solving_label.pack(before=self.canvas, pady=10)  
        # Create new solve button
        self.solve_button = tk.Button(
            self.root, 
            text="SOLVE MAZE",  
            command=self.solve_maze_action, 
            width=10,  
            font=self.button_font,
            bg="#700b55", fg="white", #dark pink
            activebackground="#4f093c", #very dark pink
            activeforeground="white",
            relief="raised"                    
        )
        self.solve_button.pack(pady=15)  
# Run the application
window = tk.Tk()
app = MazeApp(window)

# Run the maze in console
maze, path = generate_maze()
print("\nSolving Maze : ")
printMaze(maze, path)

window.mainloop()