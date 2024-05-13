from utils.date_time import get_formatted_datetime

import os
import random
from .score import Score
from .user_manager import UserManager

class DiceGame:
    def __init__(self):
        self.user_manager = UserManager()
        self.scores = []
        self.current_user = None

    def save_scores(self, score):
        file_path = 'data/rankings.txt'
        if os.path.exists(file_path):
            with open(file_path, 'a') as file:
                file.write(f"{score.username}, {score.formatted_datetime}, {score.game_id}, {score.points}, {score.wins}\n")
            print("Score saved.")
        else:
            print("File path doesn't exist.")

    def load_scores(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if os.path.exists('data/rankings.txt'):
            with open('data/rankings.txt', 'r') as file:
                self.scores = []
                for line in file:
                    data = line.strip().split(', ')
                    if len(data) == 5:
                        username, formatted_datetime, game_id, points, wins = data
                        self.scores.append(Score(username, formatted_datetime, game_id, int(points), int(wins)))
                    else:
                        print(f"Issue reading line: {line.strip()}")

    def show_top_scores(self):
        self.load_scores()
        if not self.scores:
            print("No games played yet. Play a game to see top scores.")
        else:
            sorted_scores = sorted(self.scores, key=lambda x: (x.points, x.wins), reverse = True)
            print("Top Scores:")
            for i, score in enumerate(sorted_scores[:10], 1):
                print(f"{i}. {score.username}: Points - {score.points}, Wins - {score.wins} ({score.formatted_datetime})")

    def play_game(self):
        print(f"Starting game as {self.current_user.username}...")
        stage = 1
        total_points = 0
        stages_won = 0

        while True:
            print(f"Stage {stage}:")
            points, win = self.play_stage()
            total_points += points

            if win:
                stages_won += 1
                total_points += 3
                print(f"You won this round, {self.current_user.username}!")
                print(f"Total Points: {total_points}, Stages Won: {stages_won}")
                choice = input("Do you want to continue to the next stage? (1 for YES, 0 for NO: ")

                while choice not in ["0", "1"]:
                    print("Invalid input. Please enter 1 for YES or 0 for NO.")
                    choice = input("Do you want to continue to the next stage? (1 for YES, 0 for NO): ")

                if choice == "0":
                    print(f"Game over. You won {stages_won} stage(s) with a total of {total_points} points.")
                    formatted_datetime = get_formatted_datetime()
                    self.save_scores(Score(self.current_user.username, formatted_datetime, "game_id", total_points, stages_won))
                    break
                stage += 1

            else:
                print(f"You lost this game, {self.current_user.username}")
                print("Game over. You didn't win any stages.")
                formatted_datetime = get_formatted_datetime()
                self.save_scores(Score(self.current_user.username, formatted_datetime, "game_id", total_points, stages_won))
                break

    def play_stage(self):
        player_points = 0
        cpu_points = 0
        win = False

        for _ in range(3):
            player_roll = random.randint(1, 6)
            cpu_roll = random.randint(1, 6)
            print(f"{self.current_user.username} rolled: {player_roll}")
            print("CPU rolled: ", cpu_roll)

            if player_roll == cpu_roll:
                print("It's a tie!")
            elif player_roll > cpu_roll:
                player_points += 1
                print(f"You win this round, {self.current_user.username}!")
            else:
                cpu_points += 1
                print("CPU wins this round!")

        if player_points > cpu_points:
            win = True
        return player_points, win
    
    def menu(self):
        while True:
            print("Welcome to Dice ROll Game!")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice, or leave blank to cancel: ")
            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = self.user_manager.register(username, password)
            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = self.user_manager.login(username, password)
                if user:
                    self.current_user = user
                    self.logged_in_menu()
                else:
                    print("Login failed. Invalid username or password.")
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    def register(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = self.user_manager.register(username, password)

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = self.user_manager.login(username, password)
        if user:
            self.current_user = user
            self.logged_in_menu()
        else:
            print("Login failed. Invalid username or password.")

    def logged_in_menu(self):
        while True:
            print(f"Welcome, {self.current_user.username}!")
            print("Menu: ")
            print("1. Start game")
            print("2. Show top scores")
            print("3. Logout")
            choice = input("Enter your choice, or leave blank to cancel: ")
            if choice == "1":
                start_choice = input("Are you sure you want to start a new game? (1 for YES, 0 for NO): ")
                if start_choice == "1":
                    self.play_game()
                else:
                    print("Returning to main menu.")
            elif choice == "2":
                self.show_top_scores()
            elif choice == "3":
                self.logout()
                break
            else:
                print("Invalid choice. Please try again.")

    def logout(self):
        self.current_user = None
        print("Logged out successfully.")