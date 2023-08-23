from utils import *

# Project: Building a website
"""
I am creating a team of 4 to build a website and they must have the following skills
"""
skills = ["JavaScript", "Python", "Flask", "HTML & CSS",
          "UI/UX", "MongoDB", "Project Management"]

project_1 = Project(skills, 4)

# Creating 5 employees
skills_1 = ["Java", "Project Management"]
skills_2 = ["JavaScript", "HTML & CSS", "PHP", "Python", "Django"]
skills_3 = ["Python", "PHP", "Laravel", "SQL"]
skills_4 = ["UI/UX", "Project Management", "HTML & CSS"]
skills_5 = ["MongoDB", "PHP", "JavaScript", "SQL", "NoSQL"]

emp_1 = Employees(1, 7, 5, 9, 4, skills_1)
emp_2 = Employees(2, 5, 8, 8, 9, skills_2)
emp_3 = Employees(3, 2, 7, 2, 7, skills_3)
emp_4 = Employees(4, 7, 6, 9, 6, skills_4)
emp_5 = Employees(5, 2, 9, 9, 4, skills_5)


# Creating 3 interns
skills_6 = ["C++", "Python"]
skills_7 = ["SQL", "Python", "MongoDB"]
skills_8 = ["JavaScript", "HTML & CSS"]

intern_1 = Interns(6, 7, 4, 4, skills_6)
intern_2 = Interns(7, 6, 6, 6, skills_7)
intern_3 = Interns(8, 9, 5, 5, skills_8)

# print(emp_1)
e_1 = emp_1.profile()
print(e_1)

print("Skills covered by employee 2 is :", emp_2.skills_covered(skills))

# Employee list
employee_list = [emp_1, emp_2, emp_3, emp_4, emp_5]
intern_list = [intern_1, intern_2, intern_3]

random_team_1, ids = random_team(intern_list, employee_list, project_1.desired_size_of_team, 3)

team_one_score = evaluate_team(random_team_1)
print("")
print("======== RANDOM ========")
print("This is team 1:", ids) #Return the IDs of the selected people 
print("The score for team 1 is :", team_one_score)
print("")
print("======== TEAM GREEDY ========")
greedy_team_1, id_greedy = team_greedy(5, 3, project_1.skills_required, employee_list, intern_list)
print("THis is the greedy team list", ids)
print("This is team greedy's score: ", evaluate_team(greedy_team_1))