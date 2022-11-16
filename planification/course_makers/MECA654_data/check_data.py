import yaml
import markdown
import pandas as pd

name = "MECA654"
data = yaml.safe_load(open(f"{name}.yml"))

# CONSTRAINTS
constraints = data["constraints"]
text_constraints = """
graph TB
"""
for constraint in constraints:
    if constraint["kind"] == "succession":
        offset = ""
        if "min_offset" in constraint.keys():
            min_offset = constraint["min_offset"]
            if min_offset != None:
                offset += f"{min_offset} < t"
        if "max_offset" in constraint.keys():
            max_offset = constraint["max_offset"]
            if max_offset != None:
                if len(offset) == 0:
                    offset +="t"
                offset += f" <{max_offset}"
             
        for start in constraint["start_after"]:
            for end in constraint["activities"]:
                if len(offset) > 0:
                    text_constraints += f"    {start} -- {offset} --> {end}\n"
                else:
                    text_constraints += f"    {start} --> {end}\n"
open(f"{name}_graph.md", "w").write(text_constraints)

# RESSOURCES
activities = data["activities"]
out = {"kind":[], "duration":[], "students":[], "teachers":[], "Nteachers":[], "rooms": [], "Nrooms":[]}
index = []
for label, activity in activities.items():
    index.append(label)
    out["kind"].append(activity["kind"])
    out["duration"].append(activity["duration"])
    out["students"].append(activity["students"])
    out["teachers"].append(str(activity["teachers"]["pool"]))
    out["Nteachers"].append(activity["teachers"]["value"])
    out["rooms"].append(str(activity["rooms"]["pool"]))
    out["Nrooms"].append(activity["rooms"]["value"])
out = pd.DataFrame(out, index = index)
out.index.name = "label"
out.to_csv(f"{name}_ressources.csv")
    