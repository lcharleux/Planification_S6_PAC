# INFO642
from automatic_university_scheduler.scheduling import Activity, Course
from automatic_university_scheduler.validation import constraints_to_graph, activities_to_dataframe
from automatic_university_scheduler.preprocessing import courses_from_yml
import yaml
import pandas as pd
import json

# SETUP
course_label = "INFO642"
yml_path = f"../course_models/{course_label}.yml"
data = yaml.safe_load(open(yml_path))
data = data[course_label]
default_rooms = json.load(open("../default_rooms.json"))
room_pools = {
    "big_info_rooms": ["A-POLY-C213", "A-POLY-C214", "A-POLY-C215"],
    "info_rooms": [
        "A-POLY-C209",
        "A-POLY-C202",
        "A-POLY-C210",
        "A-POLY-A030",
        "A-POLY-C217",
    ],
    "amphi": ["A-POLY-B120"],
    "TD_room": ["A-POLY-C109"]
}

# CONSTRAINTS VALIDATION
constraints = data["constraints"]
constraints_graph = constraints_to_graph(constraints)
open(f"../courses_graphs/{course_label}_graph.md", "w").write(constraints_graph)

# RESSOURCES VALIDATION
activities = data["activities"]
out_df = activities_to_dataframe(activities)
out_df.to_csv(f"../courses_activities_dataframes/{course_label}_ressources.csv")
out_df.to_html(f"../courses_activities_dataframes/{course_label}_ressources.html")

# ACTIVITIES
courses = courses_from_yml(yml_path, room_pools = room_pools, default_rooms= default_rooms)
for course_label, course in courses.items():
    path = f"../activity_data/{course_label}.json"
    with open(path, "w") as f:
        json.dump(course.to_dict(), f)