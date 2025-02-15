import random
import string
import os
import json
from datetime import datetime

class UsernameGenerator:
    def __init__(self):
        self.config_file = "username_generator_config.json"
        self.adjectives = [
            "Happy", "Brave", "Mighty", "Swift", "Clever", "Magic", "Cosmic",
            "Wild", "Noble", "Epic", "Shadow", "Crystal", "Thunder", "Silent"
        ]
        
        self.nouns = [
            "Dragon", "Tiger", "Phoenix", "Warrior", "Knight", "Wolf", "Eagle",
            "Falcon", "Lion", "Panther", "Wizard", "Runner", "Hunter", "Legend"
        ]
        
        self.load_word_lists()
        self.letters = string.ascii_letters
        self.digits = string.digits
        self.special_chars = "!@#$%^&*"

    def load_word_lists(self):
        """Load custom word lists from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as file:
                    data = json.load(file)
                    self.adjectives = data.get('adjectives', self.adjectives)
                    self.nouns = data.get('nouns', self.nouns)
                print("Custom word lists loaded successfully!")
        except Exception as e:
            print(f"Error loading word lists: {str(e)}")

    def save_word_lists(self):
        """Save current word lists to file"""
        try:
            data = {
                'adjectives': self.adjectives,
                'nouns': self.nouns
            }
            with open(self.config_file, 'w') as file:
                json.dump(data, file, indent=4)
            print("Word lists saved successfully!")
            return True
        except Exception as e:
            print(f"Error saving word lists: {str(e)}")
            return False

    def add_custom_words(self):
        """Add custom words to the generator"""
        print("\n=== Add Custom Words ===")
        print("Enter 'done' when finished adding words")
        
        print("\nAdd adjectives:")
        while True:
            word = input("Enter an adjective (or 'done'): ").strip()
            if word.lower() == 'done':
                break
            if word:
                self.adjectives.append(word)

        print("\nAdd nouns:")
        while True:
            word = input("Enter a noun (or 'done'): ").strip()
            if word.lower() == 'done':
                break
            if word:
                self.nouns.append(word)
        self.save_word_lists()

    def get_user_preferences(self):
        """Get user preferences for username generation"""
        print("\n=== Username Generator Settings ===")
        
        while True:
            try:
                print("\nGeneration Modes:")
                print("1. Random characters")
                print("2. Word combination")
                mode = input("Choose generation mode (1-2): ").strip()
                if mode not in ['1', '2']:
                    raise ValueError("Please enter 1 or 2")
                if mode == '1':
                    length = int(input("Enter desired username length (4-20): "))
                    if not 4 <= length <= 20:
                        raise ValueError("Length must be between 4 and 20")
                else:
                    length = 0  # Not used in word combination mode
                
                include_numbers = input("Include numbers? (y/n): ").lower().strip()
                if include_numbers not in ['y', 'n']:
                    raise ValueError("Please enter 'y' or 'n'")
                
                include_special = input("Include special characters? (y/n): ").lower().strip()
                if include_special not in ['y', 'n']:
                    raise ValueError("Please enter 'y' or 'n'")
                
                num_usernames = int(input("How many usernames would you like to generate? (1-10): "))
                if not 1 <= num_usernames <= 10:
                    raise ValueError("Please enter a number between 1 and 10")
                return mode, length, include_numbers == 'y', include_special == 'y', num_usernames
            except ValueError as e:
                print(f"Error: {str(e)}")
                print("Please try again.\n")

    def generate_random_username(self, length, include_numbers, include_special):
        """Generate a random username of specified length"""
        characters = self.letters
        if include_numbers:
            characters += self.digits
        if include_special:
            characters += self.special_chars
            
        return ''.join(random.choice(characters) for _ in range(length))

    def generate_word_username(self, include_numbers, include_special):
        """Generate a username by combining words"""
        adj = random.choice(self.adjectives)
        noun = random.choice(self.nouns)
        username = adj + noun
        
        if include_numbers:
            username += str(random.randint(1, 999))
        if include_special:
            username += random.choice(self.special_chars)
            
        return username

    def generate_username(self, mode, length, include_numbers, include_special):
        """Generate a single username based on preferences"""
        if mode == '1':
            return self.generate_random_username(length, include_numbers, include_special)
        else:
            return self.generate_word_username(include_numbers, include_special)

    def save_usernames(self, usernames):
        """Save generated usernames to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"usernames_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as file:
                file.write("Generated Usernames:\n")
                file.write("===================\n\n")
                for i, username in enumerate(usernames, 1):
                    file.write(f"{i}. {username}\n")
            
            print(f"\nUsernames successfully saved to {filename}")
            return True
        except IOError as e:
            print(f"\nError saving usernames: {str(e)}")
            return False

    def show_menu(self):
        """Display main menu"""
        print("\n=== Username Generator Menu ===")
        print("1. Generate usernames")
        print("2. Add custom words")
        print("3. Exit")
        return input("Choose an option (1-3): ").strip()

    def run(self):
        """Main program loop"""
        print("Welcome to the Username Generator!")
        print("=================================")
        
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                try:
                    mode, length, include_numbers, include_special, num_usernames = self.get_user_preferences()
                    
                    generated_usernames = []
                    for _ in range(num_usernames):
                        username = self.generate_username(mode, length, include_numbers, include_special)
                        generated_usernames.append(username)
                    
                    print("\nGenerated Usernames:")
                    print("===================")
                    for i, username in enumerate(generated_usernames, 1):
                        print(f"{i}. {username}")
                    
                    save_option = input("\nWould you like to save these usernames to a file? (y/n): ").lower().strip()
                    if save_option == 'y':
                        self.save_usernames(generated_usernames)
                    
                except KeyboardInterrupt:
                    print("\nUsername generation cancelled.")
                except Exception as e:
                    print(f"\nAn unexpected error occurred: {str(e)}")
                    print("Please try again.")
                    
            elif choice == '2':
                self.add_custom_words()
            elif choice == '3':
                break
            else:
                print("Invalid option. Please try again.")
        print("\nThank you for using the Username Generator!")

if __name__ == "__main__":
    generator = UsernameGenerator()
    generator.run()