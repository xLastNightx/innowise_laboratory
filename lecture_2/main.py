# we need it to calculate the current year
from datetime import date

# calculating the current year
today = date.today()
current_year = today.year

user_name = input("Hello, dear! Enter your name: ")
birth_year = int(input("Enter your birth year: "))

if birth_year > 2025 or birth_year <= 1920:
    trulyBirth = False
    while trulyBirth == False:
        birth = int(input("enter your truly birth year: "))
        if birth <= 2025 and birth > 1920:
            birth_year = birth
            trulyBirth = True

current_age = current_year - birth_year

# calculating the life_stage
def generate_profile(age):
    if age <= 12:
        life_stage = "Child"
    elif age < 19:
        life_stage = "Teenager"
    else:
        life_stage = "Adult"
    return life_stage

stage = generate_profile(current_age)

# user profile and set, that we will fill in future
user_profile = {}
hobbies = set()
desire_to_input_another_hobby = True

# adding user hobbies into the dict
while desire_to_input_another_hobby:
    hobby = input(
        "Enter your favorite hobby or type 'stop' to finish it: ").lower()
    if hobby == "stop":
        desire_to_input_another_hobby = False
    else:
        hobbies.add(hobby)

user_profile = {"name": user_name, "age": current_age,
                "stage": stage, "hobbies": hobbies}

# printing everything in the terminal
print(
    f"\nYour name is {user_profile["name"]} and you are {user_profile["age"]} years old, it means, that you are {user_profile["stage"]}.")
print(
    f"\nProfile Summary: \nname: {user_profile["name"]} \nage: {user_profile["age"]} \nstage: {user_profile["stage"]} \n")

if len(hobbies) == 0:
    print("Your list of hobbies is empty")
else:
    print(f"Your favorite hobbies ({len(hobbies)}): ")
    for item in user_profile["hobbies"]:
        print(f"- {item}")