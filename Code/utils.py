import requests
from bs4 import BeautifulSoup
import demjson
import pickle
import random
import networkx as nx
import matplotlib.pyplot as plt


class UsrClass():
    def __init__(self):
        # Define class attributes to hold values from the dictionary
        self.id = None
        self.rating = 0
        self.reviews = 0
        self.revenue = 0
        self.country = None
        self.services = 0
        self.skills = None

    def assign_values(self, data):
        # Assign values from the dictionary to the class attributes
        self.id = data.get("GuruId")
        self.rating = data.get("AvgFeedback12")
        self.reviews = data.get("FeedbackReviews") or 0
        self.revenue = data.get("Revenue12")
        self.country = data.get("Country")
        self.services = data.get("ServiceCount")

    def assign_skills(self, skills):
        """
        Assign each user his/her skillsets.
        """
        self.skills = skills

    def __str__(self):
        dictionary = {
            'id': self.id,
            'rating': self.rating,
            'reviews': self.reviews,
            'revenue': self.revenue,
            'country': self.country,
            'services': self.services,
            'skills': self.skills
        }
        return f"{dictionary}"

    def get_score(self):
        experience_score = ((self.reviews*self.rating)/100)
        skill_score = (0.5*(len(self.skills)) + self.services)
        score = experience_score + skill_score
        return round(score, 1)

    def usr(self):
        dictionary = {
            'id': self.id,
            'score': self.get_score(),
            'skills': self.skills
        }
        return dictionary


class Project():
    """ We define a project by the skills required to complete it """

    def __init__(self, skills_required, desired_size_of_team) -> None:
        self.skills_required = skills_required
        self.desired_size_of_team = desired_size_of_team


def get_data(url_list):
    """ 
        This function takes a list of urls from the Guru freelancer site
        and create a list of dictionaries of the freelancer data. 
    """
    users_profile = []

    for url in url_list:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup1 = BeautifulSoup(response.content, 'html.parser')

            file_path = f"webpages\webpage_{url_list.index(url)}.html"

            # Save the HTML data to a file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(soup1.prettify())
        else:
            print("Failed to retrieve the web page.")

        # Read the local webpage
        try:
            # Open the file for reading
            with open(file_path, "r", encoding="utf-8") as file:
                # Read the content of the file
                html_content = file.read()

        except FileNotFoundError:
            print("File not found:", file_path)
        except Exception as e:
            print("An error occurred:", str(e))

        soup = BeautifulSoup(html_content, 'html.parser')

        # Get the user profile dictionary from the webpage
        job_data = [list[':data']
                    for list in soup.find_all('freelancer-record')]

        # Taking out the first item (It is not relevant to our work).
        job_data.pop(job_data.index(job_data[0]))

        # Get the skills from other parts of the website
        all_skills = []
        for freelancer in soup.find_all('freelancer-record'):
            individual_skill = [skill.get_text().strip() for skill in freelancer.select(
                ".skillsList__skill--hasHover")]
            all_skills.append(individual_skill)

        # Here too we take out the first item because it is irrelevant to us.
        all_skills.pop(all_skills.index(all_skills[0]))

        # Convert the data to a dictionary
        job_dicts = [demjson.decode(item) for item in job_data]

        # Create an instance of UsrClass
        user_profile = []

        for data in job_dicts:
            user = UsrClass()  # Create an instance for each user.

            # Assign values from the dictionary to the instance attributes
            user.assign_values(data)
            user_profile.append(user)

        i = 0
        for i in range(len(all_skills)):
            user_profile[i].assign_skills(all_skills[i])
            users_profile.append(user_profile[i].usr())

        # Add this set of users to all the users
        # users_profile.extend(user_profile)

    print(f"Here are all the top 10 users out of {len(users_profile)}")

    for i in range(10):
        print(users_profile[i])

    pickle.dump(users_profile, open("usr_data\data.pkl", "wb"))

    print(pickle.load(open("usr_data\data.pkl", "rb")))


def sort_data(data):
    """
        This function will return a sorted list from the highest score to the lowest.
    """
    return sorted(data, key=lambda x: x["score"], reverse=True)


def separate_members(data, threshold_score):
    """
        This function takes the list of members and a threshold score
        then returns two lists of members (experienced and inexperienced)
    """

    experienced = []
    inexperienced = []

    for user in data:
        try:
            if user["score"] >= threshold_score:
                experienced.append(user)
            else:
                inexperienced.append(user)
        except Exception as e:
            print("There was an error appending. Check the error below!")
            print()
            print(e)

    print("The number of experienced personnels are: ", len(experienced))
    print("The number of inexperienced personnels are: ", len(inexperienced))

    # sorting the groups
    experienced = sort_data(experienced)
    inexperienced = sort_data(inexperienced)

    return experienced, inexperienced


def score_function(team):
    """
        This function sums up the scores the list of teams passed through it.
        This function takes in the list of dictionaries as an argument and returns the score (floating point)
    """
    score = round(sum([data['score'] for data in team]), 1)
    return score


def random_team(list_of_members, team_size):
    """ 
        This function takes in a list of members and randomly choose members to meet the cardinality constraint. 
        The function returns the list of selected members and the score.
    """
    Team = random.sample(list_of_members, team_size)
    score = score_function(Team)
    return Team, score


def greedy_cardinality(list_of_members, team_size):
    """
        This function will take the following arguments.
            1. The list of employees
            2. The size required for the project
        the function will then sort the list
        and return a list of the best candidates that meet the cardinality constraint.

        The algorithm
        1. create a list for the team to be returned
        2. create a score variable
    """
    sorted_data = sort_data(list_of_members)
    Team = [sorted_data[i] for i in range(team_size)]
    score = score_function(Team)
    return Team, score


def greedy(exp_tuple, inexp_tuple, team_size):
    """
        algorithm is going to return a list of the top experienced and inexperienced 
        persons for a defined project. The arguments are:
            1. The least and most number from each group, 
            2. The size of the group
            3. The each team list, minimum size and maximum size as a tuple

        The algorithm is pretty simple
            1. add the best members till the minimum required for each is met. 
            2. Select members from the experienced group to top up the till the team size is met. 
    """
    # Extracting the data from the tuple
    Team = []
    exp_members = []
    inexp_members = []
    exp_list, exp_min, exp_max = exp_tuple
    inexp_list, inexp_min, inexp_max = inexp_tuple

    # phase 1 of the algo: meet the minimum of each group.
    # For the experienced group
    for i in range(exp_min):
        Team.append(exp_list[i])
        exp_members.append(exp_list[i])

    # For the inexperienced group
    for i in range(inexp_min):
        Team.append(inexp_list[i])
        inexp_members.append(inexp_list[i])

    # Phase 2: Top up with the experienced group till max
    if len(Team) < team_size:
        for i in range(exp_min, exp_max):
            Team.append(exp_list[i])
            exp_members.append(exp_list[i])

    # if the max team size is still not reached, top up with the inexperienced group
    if len(Team) < team_size:
        for i in range(inexp_min, inexp_max):
            Team.append(inexp_list[i])
            inexp_members.append(inexp_list[i])

    print(
        f"There are {len(exp_members)} members from the experienced group in the team")
    print(
        f"There are {len(inexp_members)} members from the inexperienced group in the team")

    return Team, score_function(Team)


def penalty_function(team, expected_team_size):
    """
        This function will introduce a penalty to the objective function if it violates the cardinality constraint
    """
    return len(team) - expected_team_size


def obj_fxn(k, team, expected_team_size):
    """
        The objective is to return the team that gives the maximum score.
        k is the penalty factor
    """
    return score_function(team) - k*penalty_function(team, expected_team_size)


def constrained_greedy():
    pass


"""
    Creating a network...
"""


def create_network(data):

    # Create an empty undirected graph
    G = nx.Graph()

    # Add nodes with id as the node name
    for person in data:
        G.add_node(person["id"], score=person["score"],
                   skills=person['skills'])

    # Add edges based on common skills with weights
    for i, person1 in enumerate(data):
        for j, person2 in enumerate(data[i+1:], start=i+1):
            common_skills = set(person1["skills"]) & set(person2["skills"])
            if len(common_skills) >0:
                weight = len(common_skills)
                G.add_edge(person1["id"], person2["id"],
                           common_skills=common_skills, weight=(1/weight))
            else:
                G.add_edge(person1["id"], person2["id"],
                           common_skills=None, weight=100)

    # Draw the graph with weighted edges
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): data["weight"] for u, v, data in G.edges(data=True)}
    nx.draw(G, pos, with_labels=True, node_size=1000,
            font_size=12, font_color="black", font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Store the graph in a pickle file
    pickle.dump(G, open("networks\\network_data.pkl", "wb"))

    # Display the graph
    plt.show()


def cover_greedy():

    pass


def demographics(data):
    """
    This will take the data and return some stats on some special values.
    """
    total_score = 0
    max_score = 0
    min_score = 100
    for person in data:
        total_score += person['score']
        if person['score'] > max_score:
            max_score = person['score']
        if person['score'] < min_score:
            min_score = person['score']
    avg_score = total_score/len(data)

    print("=== Score Statistics ===")
    print(f"Average Score = {avg_score}")
    print(f"Maximum Score = {max_score}")
    print(f"Minimum Score = {min_score}")
