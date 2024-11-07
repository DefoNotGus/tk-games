import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import time

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fun Game")
        self.root.geometry("400x300")
        self.score = 0  # Initialize the score
        self.start_time = None
        self.player_name = ""

        # Main menu setup
        self.main_menu()

    def main_menu(self):
        # Clear the window for the main menu
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title = tk.Label(self.root, text="Welcome to the Fun Game!", font=("Arial", 16))
        title.pack(pady=20)

        # Start Button
        start_button = tk.Button(self.root, text="Start", command=self.get_player_name, font=("Arial", 14))
        start_button.pack(pady=10)

        # Score Button
        score_button = tk.Button(self.root, text="Score", command=self.show_score, font=("Arial", 14))
        score_button.pack(pady=10)

    def get_player_name(self):
        # Prompt for the player's name
        self.player_name = simpledialog.askstring("Name", "Enter your name:")
        if self.player_name:
            self.start_time = time.time()  # Start the timer
            self.start_level_1()

    def show_score(self):
        # Read scores from score.txt and display them sorted by time
        try:
            with open("score.txt", "r") as file:
                scores = [line.strip().split(",") for line in file]
            # Sort scores by time (second column, as float)
            scores.sort(key=lambda x: float(x[1]))
            # Display scores
            score_message = "\n".join([f"{name}: {time}s" for name, time in scores])
            messagebox.showinfo("Scores", score_message)
        except FileNotFoundError:
            messagebox.showinfo("Scores", "No scores recorded yet.")

    def start_level_1(self):
        # Move to level 1
        self.level_1()

    def level_1(self):
        # Clear the window for level 1
        for widget in self.root.winfo_children():
            widget.destroy()

        # Question and options for level 1
        question_label = tk.Label(self.root, text="What is the capital of France?", font=("Arial", 14))
        question_label.pack(pady=20)

        # Options for the quiz question
        options = [("Berlin", False), ("Paris", True), ("London", False), ("Rome", False)]
        for option_text, is_correct in options:
            button = tk.Button(self.root, text=option_text, command=lambda correct=is_correct: self.check_answer(correct, next_level=self.level_2))
            button.pack(pady=5)

    def check_answer(self, is_correct, next_level):
        if is_correct:
            self.score += 1
            messagebox.showinfo("Correct!", "Well done!")
            next_level()
        else:
            messagebox.showinfo("Incorrect", "Try again!")
            self.main_menu()

    def level_2(self):
        # Clear the window for level 2
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set up a question with multiple answers
        question_label = tk.Label(self.root, text="Select the two largest planets:", font=("Arial", 14))
        question_label.pack(pady=20)

        # Options for multiple-choice question
        options = [
            ("Earth", False), ("Jupiter", True), ("Mars", False),
            ("Venus", False), ("Saturn", True), ("Mercury", False)
        ]
        self.selected_options = []

        for option_text, is_correct in options:
            button = tk.Checkbutton(self.root, text=option_text, command=lambda text=option_text, correct=is_correct: self.select_option(text, correct, next_level=self.level_3))
            button.pack(pady=5)

    def select_option(self, text, is_correct, next_level):
        if text not in self.selected_options:
            self.selected_options.append((text, is_correct))
        else:
            self.selected_options.remove((text, is_correct))

        # Check if two choices have been made
        if len(self.selected_options) == 2:
            # Check if both answers are correct
            if all(correct for _, correct in self.selected_options):
                self.score += 1
                messagebox.showinfo("Correct!", "Nice job!")
                next_level()
            else:
                messagebox.showinfo("Incorrect", "That's not quite right!")
                self.main_menu()

    def level_3(self):
        # Clear the window for level 3
        for widget in self.root.winfo_children():
            widget.destroy()

        # Instruction Label
        instruction_label = tk.Label(self.root, text="Find the hidden Monkey in the image", font=("Arial", 14))
        instruction_label.pack(pady=20)

        # Load the full image and overlay the smaller image in the center
        self.full_image = Image.open("forrest.png")
        self.overlay_image = Image.open("monkey.png")
        
        # Center coordinates for the overlay image on the 100x100 image
        x = (self.full_image.width - self.overlay_image.width) // 2
        y = (self.full_image.height - self.overlay_image.height) // 2
        
        # Paste the overlay image onto the full image at the calculated center
        self.full_image.paste(self.overlay_image, (x, y))
        
        # Convert to a format that Tkinter can use
        self.display_image = ImageTk.PhotoImage(self.full_image)
        
        # Display the image
        self.image_label = tk.Label(self.root, image=self.display_image)
        self.image_label.pack(pady=10)

        # Bind a click event to check if the user clicked the right spot
        self.image_label.bind("<Button-1>", self.check_click)

    def check_click(self, event):
        # Check if the click is within the bounds of the overlayed "monkey" area
        x_start = (self.full_image.width - self.overlay_image.width) // 2
        y_start = (self.full_image.height - self.overlay_image.height) // 2
        x_end = x_start + self.overlay_image.width
        y_end = y_start + self.overlay_image.height

        if x_start <= event.x <= x_end and y_start <= event.y <= y_end:
            self.score += 1
            end_time = time.time()
            time_taken = round(end_time - self.start_time, 2)  # Calculate time taken
            messagebox.showinfo("Found!", "You found the Monkey!")
            self.save_score(self.player_name, time_taken)
            self.main_menu()  # Return to the main menu
        else:
            messagebox.showinfo("Try Again", "That's not the right spot!")

    def save_score(self, name, time_taken):
        # Append the player's name and time taken to score.txt
        with open("score.txt", "a") as file:
            file.write(f"{name},{time_taken}\n")

# Create the Tkinter window and run the app
root = tk.Tk()
app = GameApp(root)
root.mainloop()
