import random
import string

def prompt_user_for_preferences():
    try:
        length = int(input("Please provide the desired password length (min 5): "))
        if length < 5:
            print("Error: Password must be at least 5 characters long.")
            return None, None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None, None

    char_types = {
        'uppercase letters': string.ascii_uppercase,
        'lowercase letters': string.ascii_lowercase,
        'digits': string.digits,
        'special characters': string.punctuation
    }

    selected_char_types = ''
    
    for desc, chars in char_types.items():
        choice = input(f"Do you want to include {desc}? (yes/no or y/n): ").strip().lower()
        if choice in ['yes', 'y']:  # Added 'y' and 'yes' as valid responses
            selected_char_types += chars

    if not selected_char_types:
        print("At least one type of character must be selected.")
        return None, None

    return length, selected_char_types

def create_password(length, char_pool):
    return ''.join(random.choice(char_pool) for _ in range(length))

def show_password(password):
    print(f"\nYour generated password is: {password}")

def start_password_generator():
    length, char_pool = prompt_user_for_preferences()

    if length and char_pool:
        generated_password = create_password(length, char_pool)
        show_password(generated_password)

if __name__ == "__main__":
    start_password_generator()
