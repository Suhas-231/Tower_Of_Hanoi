import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TowerOfHanoi:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi Game")
        
        # Set window size to be slightly smaller than full screen
        self.root.geometry("1200x800")
        self.root.configure(bg='#282c34')
        
        self.player_name = None
        self.difficulty = None
        self.num_disks = 3
        self.selected_disk = None
        self.replay_button = None
        self.exit_button = None

        self.create_initial_screen()

    def create_initial_screen(self):
        self.initial_frame = tk.Frame(self.root, bg='#282c34')
        self.initial_frame.pack(expand=True)

        tk.Label(self.initial_frame, text="Tower of Hanoi Game", font=("Helvetica", 24), fg='white', bg='#282c34').pack(pady=20)
        tk.Label(self.initial_frame, text="Enter Player Name:", font=("Helvetica", 16), fg='white', bg='#282c34').pack(pady=10)
        
        self.name_entry = tk.Entry(self.initial_frame, font=("Helvetica", 16))
        self.name_entry.pack(pady=10)

        play_button = tk.Button(self.initial_frame, text="Play", command=self.show_difficulty_selection, font=("Helvetica", 16), bg='#61afef', fg='white', activebackground='#98c379', activeforeground='black')
        play_button.pack(pady=20)

    def show_difficulty_selection(self):
        self.player_name = self.name_entry.get()
        self.initial_frame.destroy()
        
        self.difficulty_frame = tk.Frame(self.root, bg='#282c34')
        self.difficulty_frame.pack(expand=True)
        
        tk.Label(self.difficulty_frame, text="Select Difficulty Level", font=("Helvetica", 24), fg='white', bg='#282c34').pack(pady=20)
        
        tk.Button(self.difficulty_frame, text="Easy", command=lambda: self.start_game(3), font=("Helvetica", 16), bg='#61afef', fg='white', activebackground='#98c379', activeforeground='black').pack(pady=10)
        tk.Button(self.difficulty_frame, text="Medium", command=lambda: self.start_game(5), font=("Helvetica", 16), bg='#61afef', fg='white', activebackground='#98c379', activeforeground='black').pack(pady=10)
        tk.Button(self.difficulty_frame, text="Hard", command=lambda: self.start_game(7), font=("Helvetica", 16), bg='#61afef', fg='white', activebackground='#98c379', activeforeground='black').pack(pady=10)

    def start_game(self, num_disks):
        self.num_disks = num_disks
        self.max_moves = (2 ** self.num_disks) - 1
        self.remaining_moves = self.max_moves

        self.difficulty_frame.destroy()
        self.create_game_screen()

    def create_game_screen(self):
        self.canvas = tk.Canvas(self.root, width=1200, height=600, bg='#abb2bf')
        self.canvas.pack()

        self.rods = [[], [], []]
        self.disk_widths = []
        self.disk_height = 40
        self.disk_gap = 10
        self.lives = 3

        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        control_frame = tk.Frame(self.root, bg='#282c34')
        control_frame.pack(pady=10)

        tk.Label(control_frame, text=f"Player: {self.player_name}", font=("Helvetica", 16), fg='white', bg='#282c34').grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(control_frame, text=f"Difficulty: {self.num_disks} Disks", font=("Helvetica", 16), fg='white', bg='#282c34').grid(row=1, column=0, columnspan=2)

        self.step_description = tk.Label(self.root, text="", font=("Helvetica", 16), bg='#abb2bf')
        self.step_description.pack(pady=10)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.selected_rod = None

    def reset_game(self):
        self.canvas.delete("all")

        self.rods = [list(range(self.num_disks, 0, -1)), [], []]
        self.disk_widths = [i * 40 for i in range(1, self.num_disks + 1)]
        self.lives = 3
        self.remaining_moves = self.max_moves

        self.step_description.config(text="")
        self.selected_disk = None

        self.draw_rods()
        self.draw_disks()
        self.update_status_labels()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        if self.replay_button:
            self.replay_button.destroy()
            self.replay_button = None
        if self.exit_button:
            self.exit_button.destroy()
            self.exit_button = None

    def on_canvas_click(self, event):
        rod_width = 20
        rod_height = 400
        rod_x_positions = [300, 600, 900]
        x = event.x

        for i, rod_x in enumerate(rod_x_positions):
            if rod_x - rod_width // 2 <= x <= rod_x + rod_width // 2:
                if self.selected_rod is None:
                    if self.rods[i]:
                        self.selected_rod = i
                        self.selected_disk = self.rods[i][-1]
                        self.draw_disks()
                else:
                    if self.valid_move(self.selected_rod, i):
                        self.move_disk(self.selected_rod, i)
                        self.remaining_moves -= 1
                        self.selected_rod = None
                        self.selected_disk = None
                        self.update_status_labels()
                    else:
                        self.lives -= 1
                        self.update_status_labels()
                        if self.lives == 0:
                            self.end_game("Game Over! You have lost all your lives.")
                            self.show_result_page("Game Over! You have lost all your lives.")
                        else:
                            self.show_invalid_move_message()
                        self.selected_rod = None
                        self.selected_disk = None
                    self.draw_disks()
                break

    def valid_move(self, src, dest):
        if not self.rods[src]:
            return False
        if not self.rods[dest]:
            return True
        return self.rods[src][-1] < self.rods[dest][-1]

    def move_disk(self, src, dest):
        disk = self.rods[src].pop()
        self.rods[dest].append(disk)
        self.draw_rods()
        self.draw_disks()

        self.step_description.config(text=f"Last Disk Moved: {disk}")

        if self.rods == [[], [], list(range(self.num_disks, 0, -1))]:
            self.end_game(f"Congratulations, {self.player_name}! You have won the game.")
            self.show_result_page(f"Congratulations, {self.player_name}! You have won the game.")
        elif self.remaining_moves == 0:
            self.end_game("Game Over! You have exceeded the maximum number of moves.")
            self.show_result_page("Game Over! You have exceeded the maximum number of moves.")

    def end_game(self, message):
        self.step_description.config(text=message)
        self.canvas.unbind("<Button-1>")

    def show_result_page(self, message):
        self.canvas.pack_forget()
        self.step_description.pack_forget()

        result_frame = tk.Frame(self.root, bg='#282c34')
        result_frame.pack(expand=True)

        tk.Label(result_frame, text=message, font=("Helvetica", 24), fg='white', bg='#282c34').pack(pady=20)

        replay_button = tk.Button(result_frame, text="Replay", command=self.reset_game, font=("Helvetica", 16), bg='#61afef', fg='white', activebackground='#98c379', activeforeground='black')
        replay_button.pack(pady=10)

        exit_button = tk.Button(result_frame, text="Exit", command=self.root.quit, font=("Helvetica", 16), bg='#61afef', fg='white', activebackground='#98c379', activeforeground='black')
        exit_button.pack(pady=10)


    def show_invalid_move_message(self):
        messagebox.showerror("Invalid Move", "You cannot place a larger disk on a smaller disk!")
        self.root.after(5000, lambda: messagebox.showinfo("Invalid Move", "You cannot place a larger disk on a smaller disk!"))

    def draw_rods(self):
        rod_width = 20
        rod_height = 400
        rod_x_positions = [300, 600, 900]
        for x in rod_x_positions:
            self.canvas.create_rectangle(x - rod_width // 2, 600 - rod_height, x + rod_width // 2, 600, fill='black')

        self.canvas.create_text(300, 100, text="Source", font=("Helvetica", 16), fill='blue', tags="rod_label")
        self.canvas.create_text(900, 100, text="Destination", font=("Helvetica", 16), fill='red', tags="rod_label")

    def draw_disks(self):
        self.canvas.delete("disk")
        rod_x_positions = [300, 600, 900]
        for i, rod in enumerate(self.rods):
            for j, disk in enumerate(rod):
                disk_width = self.disk_widths[disk - 1]
                x = rod_x_positions[i]
                y = 600 - (j + 1) * (self.disk_height + self.disk_gap)
                color = '#007bff'
                if self.selected_disk == disk:
                    color = '#ff7f7f'  # Color when disk is selected
                self.canvas.create_rectangle(x - disk_width // 2, y - self.disk_height, x + disk_width // 2, y,
                                             fill=color, tags="disk")

    def update_status_labels(self):
        self.canvas.delete("status")
        self.canvas.create_text(600, 20, text=f"Lives: {'❤️' * self.lives}", font=("Helvetica", 16), tags="status")
        self.canvas.create_text(600, 50, text=f"Remaining Moves: {self.remaining_moves}", font=("Helvetica", 16, "bold"), tags="status")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TowerOfHanoi(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
