# Topic: Class Variables vs Instance Variables

class Student:
    # Class Variable: Shared by all students
    school_name = "Python Academy"

    def __init__(self, name):
        # Instance Variable: Unique to each student
        self.name = name

if __name__ == "__main__":
    s1 = Student("Alice")
    s2 = Student("Bob")

    print(f"{s1.name} studies at {s1.school_name}")

    # TRAP: If you change a Class Variable via the Class, it changes for EVERYONE.
    Student.school_name = "Global Tech"
    print(f"After change: {s2.name} also studies at {s2.school_name}")

    # TRAP: You can add a new property to only ONE specific object on the fly.
    s1.grade = "A"
    print(f"{s1.name}'s grade: {s1.grade}")
    # print(s2.grade) # ERROR: s2 doesn't have a 'grade'!