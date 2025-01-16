import os
import random


def load_txt(filename):
    # to read the contents of responses.txt and put the keyword as dictionary and random response as list
    config = {"keywords": {}, "random_responses": []}
    # Ensure the directory exists before trying to read the file
    directory = os.path.dirname(filename)
    os.makedirs(directory, exist_ok=True)

    if not os.path.exists(filename):
        print(f"file '{filename}' not found. Creating a new one.")
        # Create a new empty responses.txt file if it doesn't exist
        with open(filename, "w") as file:
            pass  # This just creates an empty file
        return config  # Return an empty config as the file was empty

    try:
        with open(filename, "r") as file:
            section = None
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.endswith(":"):
                    section = line[:-1].strip().lower()
                elif section == "keywords":
                    key, value = map(str.strip, line.split(":", 1))
                    config["keywords"][key.lower()] = value
                elif section == "random_responses":
                    config["random_responses"].append(line)
    except FileNotFoundError:
        print(f"file '{filename}' not found.")
    return config


def signup_login():
    # set up UI for login and signup
    print("If you are an old user, please log in. If new, sign up first.")
    action = input("enter 'login' or 'signup':").strip().lower()

    if action == "signup":
        username = input("enter username:")
        password = input("enter password:")

        # Ensure the directory exists for user.txt
        os.makedirs("project2", exist_ok=True)

        # Open file in append mode
        with open("project2/user.txt", "a") as file:
            file.write(f"{username},{password}\n")
        print(f"sign up successful! Please log in now with your username {username}.")

        # After signup, redirect to login page by calling signup_login() again
        return signup_login()

    elif action == "login":
        username = input("username=")
        password = input("password=")

        # Ensure the file exists before attempting to read
        if not os.path.exists("project2/user.txt"):
            print("user not found. please sign in!")
            return None

        try:
            with open("project2/user.txt", "r") as file:
                for line in file:
                    saved_username, saved_password = line.strip().split(",")
                    if username == saved_username and password == saved_password:
                        print(f"login successful! welcome {username}")
                        return username
        except FileNotFoundError:
            print("user not found. please sign in!")
        print("invalid username or password.")
    else:
        print("invalid input. please try again.")
    return None


def chatbot(username, config):
    # List of possible agent names
    agent_names = ["Ava", "Bobo", "Charlie", "Zara", "Echo", "Nova"]
    agent_name = random.choice(agent_names)  # Randomly select an agent name

    print(f"Your agent's name is {agent_name}. Type 'bye' to exit.")
    print(f"Hello, {username}! My name is {agent_name}. How can I assist you today?")

    # List of ignored questions (to be treated with no response)
    ignored_questions = [
        "i hate you",
        "who are you?",
        "you are boring"
    ]

    while True:
        user_input = input(f"{username}:").strip().lower()

        if user_input in {"bye", "exit", "quit"}:
            print(f"chatbot: goodbye, {username}!")
            break

        # Check if the question is in the ignored list
        if any(ignored_question in user_input for ignored_question in ignored_questions):

            continue

        responded = False
        for keyword, response in config["keywords"].items():
            if keyword in user_input:
                print(f"chatbot:{response}")
                responded = True
                break

        if not responded:
           
            if config["random_responses"]:
                random_response = random.choice(config["random_responses"])
                print(f"chatbot: {random_response.replace('{name}', username)}")
            else:
                print(f"chatbot: I do not understand what you want.")


def ai_page():
    # main page where all functions are called and put together
    username = signup_login()
    if username:
        config = load_txt("project2/responses.txt")
        if config["keywords"] or config["random_responses"]:
            chatbot(username, config)
        else:
            print("chatbot response file is empty.")
    else:
        print("please log in to use chatbot.")


ai_page()
