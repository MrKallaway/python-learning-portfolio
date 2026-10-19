def show_banner():
    print("=" * 40)
    print("     STUDENT DEVELOPER PROFILE")
    print("=" * 40)

def get_profile():
    name = input("Enter your name: ")
    language = input("Enter your language: ")
    interest = input("Enter your interests: ")
    career = input("Enter your career goal: ")
    level_valid = False
    while not level_valid:
        level = input("Choose skill level (1-3): ")
        if level in ("1", "2", "3"):
            level_valid = True
        else:
            print("Invalid input, enter 1-3")
    return name, language, interest, career, level

def display_profile(name, language, interest, career, level):
    print("\nMY DEVELOPER PROFILE")
    print("Name:", name)
    print("Language:", language)
    print("Interest:", interest)
    print("Career Goal:", career)

    if level == "1":
        print("Skill Level: Beginner Developer")
    elif level == "2":
        print("Skill Level: Intermediate Developer")
    elif level == "3":
        print("Skill Level: Advanced Developer")

SKILLS = []

def add_skill():
    skill = input("Enter skill: ")
    SKILLS.append(skill)

def display_skills():
    if not SKILLS:
        print("\nNo skills to display, add a skill first")
    else:
        print("\nProgramming skills: ")
        for skill in SKILLS:
            print("-", skill)

def display_github():
    print("\nWelcome to my GitHub portfolio!")
    print("Link to GitHub: https://github.com/MrKallaway/python-learning-portfolio/tree/main")

show_banner()
profile = get_profile()

running = True
while running:
    
    print("\nChoose an option:")
    print("1. View Developer Profile")
    print("2. Add Programming Skill")
    print("3. View Skills")
    print("4. View Github")
    print("5. Exit")

    choice_valid = False
    while not choice_valid:
        choice = input("Enter 1-5: ")
        if choice in ("1", "2", "3", "4", "5"):
            choice_valid = True
        else:
            print("Invalid input, enter 1-5")

    if choice == "1": # view developer profile
        display_profile(*profile)
    elif choice == "2": # add programming skill
        add_skill()
    elif choice == "3": # view skills
        display_skills()
    elif choice == "4": # view github
        display_github()
    elif choice == "5": # exit
        running = False
