"""
Student Grade Analyzer Program
"""

from typing import List, Dict, Union, Optional


def show_menu() -> None:
    """
    Display the main menu 
    """
    print("=== Student Grade Analyzer ===\n")
    print("1. Add a new student")
    print("2. Add grades for a student")
    print("3. Generate a full report")
    print("4. Find the top student")
    print("5. Exit")


def add_student(students: List[Dict[str, Union[str, List[int]]]]) -> None:
    """
    Add a new student to the list
    """
    name = input("Enter student name: ").strip()

    if not name:
        print("Error: Name cannot be empty.")

        return

    name_without_necessary_signs = name.replace(
        " ", "").replace("-", "").replace("'", "")
    if not name_without_necessary_signs.isalpha():
        print("Error: Name can only contain letters, spaces, - and '")

        return

    if len(name_without_necessary_signs) < 2:
        print("Error: Name must contain at least 2 letters.")

        return

    if any(student["name"].lower() == name.lower() for student in students):
        print(f"Error: Student '{name}' already exists")

        return

    students.append({"name": name, "grades": []})

    print(f"Student '{name}' added successfully!")


def add_grades(students: List[Dict[str, Union[str, List[int]]]]) -> None:
    """
    Add grades for an existing student
    """
    name = input("Enter student name: ").strip()

    # next() with generator for efficient search
    student = next(
        (person for person in students if person["name"].lower() == name.lower()), None)

    if not student:
        print(f"Student {name} not found!")

        return

    print(f"Adding grades for {name}. Enter 'done' to finish.")

    while True:
        grade_from_input = input(
            "Enter the grade (0 - 100 or 'done'): ").strip()

        if grade_from_input.lower() == 'done':
            break

        try:
            grade = int(grade_from_input)

            if 0 <= grade <= 100:
                student["grades"].append(grade)
                print(f"Grade {grade} added!")

            else:
                print("Grade must be between 0 and 100.")

        except ValueError:
            print("Invalid input. Please enter a number.")

        except Exception as e:
            print("Another error: ", e)


def show_report(students: List[Dict[str, Union[str, List[int]]]]) -> None:
    """
    Generate comprehensive student report
    """
    if not students:
        print("No students available.")

        return

    print("=== Student report === \n")

    # Get students with grades using filter
    students_with_grades = list(
        filter(lambda students_grades: students_grades["grades"], students))

    # If no students have grades
    if not students_with_grades:

        print("No students with grades available.")

        # Show students without grades
        students_without_grades = list(
            filter(lambda student: not student["grades"], students))

        for student in students_without_grades:
            print(f"{student['name']}'s average grade is N/A (no grades)")

        return

    student_averages = []

    # Process only students with grades
    for student in students_with_grades:
        name = student["name"]
        grades = student["grades"]

        # Calculate average for current student
        try:
            student_avg = sum(grades) / len(grades)

            print(f"{name}'s average grade is {student_avg:.2f}.")

            student_averages.append(student_avg)

        except ZeroDivisionError:
            # This shouldn't happen due to filter, but added for safety
            print(f"{name}'s average grade is N/A (error)")

        except Exception as e:
            print("Another error: ", e)

    # Summary statistics
    print("Summary: ")
    max_avg = max(student_averages)
    min_avg = min(student_averages)
    overall_avg = sum(student_averages) / len(student_averages)

    print(f"Max Average: {max_avg:.2f}")
    print(f"Min Average: {min_avg:.2f}")
    print(f"Overall Average: {overall_avg:.2f}")


def find_top_performer(students: List[Dict[str, Union[str, List[int]]]]) -> None:
    """
    Find student with highest average grade
    """
    if not students:
        print("No students available")
        return

    students_with_grades = [
        student for student in students if student["grades"]]

    if not students_with_grades:
        print("No students with grades available")
        return

    try:
        # Pre-calculate averages once
        student_data = []
        for student in students_with_grades:
            avg = sum(student["grades"]) / len(student["grades"])
            student_data.append((student, avg))

        # Find top performer using pre-calculated averages
        top_student, top_avg = max(student_data, key=lambda x: x[1])
        print(f"Top student: {top_student['name']} with average {top_avg:.2f}")

    except Exception as e:
        print(f"Error finding top performer: {e}")


def main() -> None:
    """
    Main program loop
    """
    students = []

    print("Welcome to the Student Grade Analyzer!")

    menu_actions = {
        '1': add_student,
        '2': add_grades,
        '3': show_report,
        '4': find_top_performer
    }

   # Valid choices as a set for fast lookup
    valid_choices = ('1', '2', '3', '4', '5')

    while True:
        try:
            show_menu()
            choice = input("Enter your choice (1-5): ").strip()

            if choice not in valid_choices:
                print("Error: Please enter a valid number between 1-5.")
                continue

            if choice == '5':
                print("Thank you! Goodbye!")
                break

            menu_actions[choice](students)

        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            break

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()