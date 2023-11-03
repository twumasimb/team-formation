# Importing libraries
import pickle
from utils import greedy_cardinality, random_team, greedy, separate_members, Project, demographics
# from utils import Project


url_list = ["https://www.guru.com/d/freelancers/srt/earn/", "https://www.guru.com/d/freelancers/srt/earn/pg/2/",
            "https://www.guru.com/d/freelancers/srt/earn/pg/3/", "https://www.guru.com/d/freelancers/srt/earn/pg/4/",
            "https://www.guru.com/d/freelancers/srt/earn/pg/5/", "https://www.guru.com/d/freelancers/srt/earn/pg/6/",
            "https://www.guru.com/d/freelancers/srt/earn/pg/7/", "https://www.guru.com/d/freelancers/srt/earn/pg/8/",
            "https://www.guru.com/d/freelancers/srt/earn/pg/9/", "https://www.guru.com/d/freelancers/srt/earn/pg/10/"]

data_path = "usr_data/data.pkl"
network_path = "networks\\network_data.pkl"
data = pickle.load(open(data_path, "rb"))  # Load data
network = pickle.load(open(network_path, "rb"))  # Load network


# Creating a project instance
skills = ['C', 'C++', 'App Development', 'Business Planning', 'Ecommerce',
          'Back End Development', 'Marketing', 'Swift', 'Android', 'Apple',
          'Design', 'Graphics', 'Front End Development', 'Data Analytics',
          'Hosting Services', 'Startup Consulting', 'Amazon AWS', 'Accounting']

team_size = 15

project_appy = Project(skills, team_size)

# Running cardinality constraint only
print("====== Cardinality Greedy ======")

Team, score = greedy_cardinality(data, project_appy.desired_size_of_team)
print("This is your team: ", [Team[i]['id'] for i in range(len(Team))])
print(f"There are {len(Team)} members in your team")
print("Your team score is: ", score)

print()
print("====== Random ======")
Random_Team, Random_Team_score = random_team(
    data, project_appy.desired_size_of_team)
print("This is your team: ", [Random_Team[i]['id']
      for i in range(len(Random_Team))])
print(f"There are {len(Random_Team)} members in your team")
print("Your team score is: ", Random_Team_score)

print()
print("====== Greedy ======")
# Put members with score 10 and upwards into the experienced category
exp_min = 4
exp_max = 7
inexp_min = 3
inexp_max = 5
exp, inexp = separate_members(data, 14.6)
exp_tuple = (exp, exp_min, exp_max)
inexp_tuple = (inexp, inexp_min, inexp_max)
Greedy_Team, Greedy_Team_score = greedy(exp_tuple=exp_tuple,
                                        inexp_tuple=inexp_tuple, team_size=project_appy.desired_size_of_team)
print("This is your team: ", [Greedy_Team[i]['id']
      for i in range(len(Greedy_Team))])
print(f"There are {len(Greedy_Team)} members in your team")
print("Your team score is: ", Greedy_Team_score)

demographics(data)