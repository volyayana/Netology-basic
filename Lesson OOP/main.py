def get_course_avg_grade(course_name, class_name, people_list):
    sum_grades = 0
    people_len = 0
    for i in people_list:
        if isinstance(i, class_name) and course_name in i.grades.keys():
            sum_grades += sum(i.grades[course_name])
            people_len += len(i.grades[course_name])
    return sum_grades / people_len

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
 
    def add_courses(self, course_name):
        self.finished_courses.append(course_name)  

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка' 
    
    def get_avg_rate(self):
        grades_list =  [i for j in self.grades.values() for i in j]
        return sum(grades_list) / len(grades_list)

    def __str__(self):
        return (f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {self.get_avg_rate()}\n'
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\nЗавершенные курсы: {", ".join(self.finished_courses)}\n'
        )
    
    def __lt__(self, other):
        if isinstance(other, Student):
            return self.get_avg_rate() < self.get_avg_rate()
 
     
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def get_avg_rate(self):
        grades_list =  [i for j in self.grades.values() for i in j]
        return sum(grades_list) / len(grades_list)

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.get_avg_rate()}\n'

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self.get_avg_rate() < other.get_avg_rate()

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\n'
 
best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python', 'Git', 'Ansible']
best_student.add_courses('Maths')

other_student = Student('Test', 'Student', 'your_gender')
other_student.courses_in_progress += ['Python', 'Git']
 
best_reviewer = Reviewer('Some', 'Buddy')
best_reviewer.courses_attached += ['Python']

other_reviewer = Reviewer('Other', 'Buddy')
other_reviewer.courses_attached += ['Git']

best_lecturer = Lecturer('Some', 'Lector')
best_lecturer.courses_attached += ['Python', 'Git']

other_lecturer = Lecturer('Other', 'Lector')
other_lecturer.courses_attached += ['Ansible', 'Python']

best_mentor = Mentor('Some', 'Mentor')
best_mentor.courses_attached += ['Maths']

other_mentor = Mentor('Some', 'Mentor')
other_mentor.courses_attached += ['Python']
 

best_reviewer.rate_hw(best_student, 'Python', 10)
other_reviewer.rate_hw(best_student, 'Git', 9)

best_reviewer.rate_hw(other_student, 'Python', 9)

best_student.rate_lecturer(best_lecturer, 'Python', 9)
best_student.rate_lecturer(best_lecturer, 'Git', 10)

other_student.rate_lecturer(other_lecturer, 'Python', 10)
best_student.rate_lecturer(best_lecturer, 'Git', 5)


print(best_student < other_student)  # false
print(best_student)
print(other_student)

print(best_lecturer < other_lecturer)  # true
print(best_lecturer)
print(other_lecturer)

print(best_reviewer)

print(get_course_avg_grade('Git', Lecturer, [best_student, other_student, other_lecturer, best_lecturer]))