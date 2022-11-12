import json
import copy

# MATH641


from automatic_university_scheduler.scheduling import Activity, Course


course_label = "MATH641"
teacher = "BASCOP ALEXANDRE"
course = Course(label=course_label, color="Blue")
default_rooms = json.load(open("../default_rooms.json"))


TD_blocks = [
        ("SNI-3-D-TD", teacher),
        ("IDU-3-G-TD", teacher),
    ]



def make_CM(
    index=1,
    after=None,
    min_offset=0,
    max_offset=96 * 5,
    add_to=None,
    teacher=teacher,
    rooms=["A-POLY-B120"],
):  
    students = "IDU-3_SNI-3"
    label = f"{course_label}_{students}_CM_{index}"
    activity = Activity(label=label, students=students, kind="CM", duration=6)
    activity.add_ressources(kind="teachers", quantity=1, pool=[teacher])
    activity.add_ressources(kind="rooms", quantity=1, pool=rooms)
    if after != None:
        activity.add_multiple_after(after, min_offset=min_offset, max_offset=max_offset)
    if add_to != None:
        add_to.add_activity(activity)
    return [activity]


def make_TD(
    TD_blocks, index=1, after=None, min_offset=0, max_offset=96 * 5, add_to=None
):
    activities = []
    for students, teacher in TD_blocks:
        activity = Activity(
            label=f"{course_label}_{students}_TD_{index}", students=students, duration=6
        )
        activity.add_ressources(kind="teachers", quantity=1, pool=[teacher])
        activity.add_ressources(kind="rooms", quantity=1, pool=default_rooms[students])
        if after != None:
            if after != None:
                activity.add_multiple_after(after, min_offset=min_offset, max_offset=max_offset)
        course.add_activity(activity)
        if add_to != None:
            add_to.add_activity(activity)
        activities.append(activity)
    return activities

def make_CT(
    index=1,
    after=None,
    min_offset=0,
    max_offset=96 * 5,
    add_to=None,
    teacher=teacher,
    rooms=["A-POLY-B120"],
):  
    students = "IDU-3_SNI-3"
    label = f"{course_label}_{students}_CT_{index}"
    activity = Activity(label=label, students=students, kind="EX", duration=6+2)
    activity.add_ressources(kind="teachers", quantity=1, pool=[teacher])
    activity.add_ressources(kind="rooms", quantity=1, pool=rooms)
    if after != None:
        if after != None:
            activity.add_multiple_after(after, min_offset=min_offset, max_offset=max_offset)    
    if add_to != None:
        add_to.add_activity(activity)
    return [activity]


# CM
CM = {}
for index in range(1,12):
    CM[index] = make_CM(
        index=index,
        after=None,
        add_to=course,
    )
# TD
TD = {}    
for index in range(1,13):   
    TD[index] = make_TD(
        TD_blocks=TD_blocks,
        index=index,
        after=None,
        add_to=course,
    )

# CT
CT = {}
for index in range(1,2):
    CT[index] = make_CT(
        index=index,
        after=None,
        add_to=course,
    )

# ENCHAINEMENTS
for act in CM[2]: act.add_multiple_after(CM[1], min_offset=48)
for act in CM[3]: act.add_multiple_after(CM[2], min_offset=48)
for act in CM[4]: act.add_multiple_after(CM[3], min_offset=48)
for act in CM[5]: act.add_multiple_after(TD[1], min_offset=48)
for act in CM[6]: act.add_multiple_after(TD[2], min_offset=48)
for act in CM[7]: act.add_multiple_after(TD[3], min_offset=48)
for act in CM[8]: act.add_multiple_after(TD[4], min_offset=48)
for act in CM[9]: act.add_multiple_after(TD[5], min_offset=48)
for act in CM[10]: act.add_multiple_after(TD[6], min_offset=48)
for act in CM[11]: act.add_multiple_after(TD[8], min_offset=48)

for act in TD[1]: act.add_multiple_after(CM[4])
for act in TD[2]: act.add_multiple_after(CM[5])
for act in TD[3]: act.add_multiple_after(CM[6])
for act in TD[4]: act.add_multiple_after(CM[7])
for act in TD[5]: act.add_multiple_after(CM[8])
for act in TD[6]: act.add_multiple_after(CM[9])
for act in TD[7]: act.add_multiple_after(CM[10])
for act in TD[8]: act.add_multiple_after(TD[7])
for act in TD[9]: act.add_multiple_after(CM[11])
for act in TD[10]: act.add_multiple_after(TD[9])
for act in TD[11]: act.add_multiple_after(TD[10])
for act in TD[12]: act.add_multiple_after(TD[11])

for act in CT[1]: act.add_multiple_after(TD[12], min_offset=48)

path = f"../activity_data/{course_label}.json"
with open(path, "w") as f:
    json.dump(course.to_dict(), f)
