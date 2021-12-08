import application.db.people as people
import application.salary as salary
import datetime

if __name__ == '__main__':
    people.get_employees()
    salary.calculate_salary()
    print(datetime.datetime.now())