import json
import copy

# EASI642

from automatic_university_scheduler.scheduling import Activity, Course

course_label = "EASI642"
teachers_acronyms = {
    "YY": "YAN YAJING",
    "GG": "GINOLHAC GUILLAUME",
    "MG": "GALLET MATTHIEU",
    "MB": "BOHM MARTIN",
}
CM_teacher = {
    1: "YY",
    2: "YY",
    3: "YY",
    4: "YY",
    4: "YY",
    5: "YY",
    6: "YY",
    7: "YY",
    8: "YY",
    9: "MB",
}
TD_teacher = {
    1: "YY",
    2: "YY",
    3: "YY",
    4: "YY",
    4: "YY",
    5: "YY",
    6: "YY",
    7: "YY",
    8: "YY",
    9: "MB",
}

exam_teachers = [teachers_acronyms[acr] for acr in ["YY"]]
TP_rooms = ["A-POLY-C213", "A-POLY-C214", "A-POLY-C215", "A-POLY-C216", "A-POLY-C217"]
big_info_rooms = ["A-POLY-C213", "A-POLY-C214", "A-POLY-C215"]
course = Course(label=course_label, color="Green")
default_rooms = json.load(open("../default_rooms.json"))


TD_rooms = {
    1: "default",
    2: "default",
    3: "default",
    4: "default",
    5: "default",
    6: "default",
    7: "default",
    8: "default",
    9: "big_info_room",
}

TP_blocks = [["SNI-3-D1", ["GG"]], ["SNI-3-D2", ["MG"]]]


def make_CM(
    index=1,
    after=None,
    min_offset=0,
    max_offset=96 * 5,
    add_to=None,
    teacher=CM_teacher,
    rooms=["A-POLY-C204"],
):
    teacher = teachers_acronyms[teacher[index]]
    students = "SNI-3"
    label = f"{course_label}_{students}_CM_{index}"
    activity = Activity(label=label, students=students, kind="CM", duration=6)
    activity.add_ressources(kind="teachers", quantity=1, pool=[teacher])
    activity.add_ressources(kind="rooms", quantity=1, pool=rooms)
    if after != None:
        activity.add_multiple_after(after, min_offset=min_offset, max_offset=max_offset)
    if add_to != None:
        add_to.add_activity(activity)
    return [activity]


def make_TD(index=1, after=None, min_offset=0, max_offset=96 * 5, add_to=None):
    activities = []
    students = "SNI-3-D-TD"
    teacher = teachers_acronyms[TD_teacher[index]]
    activity = Activity(
        label=f"{course_label}_{students}_TD_{index}",
        students=students,
        duration=6,
    )
    activity.add_ressources(kind="teachers", quantity=1, pool=[teacher])
    room_category = TD_rooms[index]
    if room_category == "default":
        room_pool = default_rooms[students]
    elif room_category == "big_info_room":
        room_pool = big_info_rooms
    activity.add_ressources(kind="rooms", quantity=1, pool=room_pool)
    if after != None:
        if after != None:
            activity.add_multiple_after(
                after, min_offset=min_offset, max_offset=max_offset
            )
    course.add_activity(activity)
    if add_to != None:
        add_to.add_activity(activity)
    activities.append(activity)
    return activities


def make_TP(
    TP_blocks, index=1, after=None, min_offset=0, max_offset=96 * 5, add_to=None
):
    activities = []
    for students, teacher in TP_blocks:
        activity = Activity(
            label=f"{course_label}_{students}_TP_{index}",
            students=students,
            duration=16,
            kind="TP",
        )
        teacher = [teachers_acronyms[t] for t in teacher]
        activity.add_ressources(kind="teachers", quantity=1, pool=teacher)
        activity.add_ressources(kind="rooms", quantity=1, pool=TP_rooms)
        if after != None:
            if after != None:
                activity.add_multiple_after(
                    after, min_offset=min_offset, max_offset=max_offset
                )
        course.add_activity(activity)
        if add_to != None:
            add_to.add_activity(activity)
        activities.append(activity)
    return activities


def make_CC(
    index=1,
    after=None,
    min_offset=0,
    max_offset=96 * 5,
    add_to=None,
    teacher=exam_teachers,
    rooms=["A-POLY-B120"],
):
    students = "SNI-3"
    label = f"{course_label}_{students}_CT_{index}"
    activity = Activity(label=label, students=students, kind="EX", duration=3 + 1)
    activity.add_ressources(kind="teachers", quantity=1, pool=exam_teachers)
    activity.add_ressources(kind="rooms", quantity=1, pool=rooms)
    if after != None:
        if after != None:
            activity.add_multiple_after(
                after, min_offset=min_offset, max_offset=max_offset
            )
    if add_to != None:
        add_to.add_activity(activity)
    return [activity]


# CM
CM = {}
for index in range(1, 10):
    CM[index] = make_CM(
        index=index,
        after=None,
        add_to=course,
    )
# TD
TD = {}
for index in range(1, 10):
    TD[index] = make_TD(
        index=index,
        after=None,
        add_to=course,
    )
# TP
TP = {}
for index in range(1, 4):
    TP[index] = make_TP(
        TP_blocks=TP_blocks,
        index=index,
        after=None,
        add_to=course,
    )
# CC
CC = {}
for index in range(1, 2):
    CC[index] = make_CC(
        index=index,
        after=None,
        add_to=course,
    )

# ENCHAINEMENTS
for act in CM[2]:
    act.add_multiple_after(CM[1], min_offset=48)
    act.add_multiple_after(TD[1], min_offset=48)
for act in CM[3]:
    act.add_multiple_after(CM[2], min_offset=48)
    act.add_multiple_after(TD[2], min_offset=48)
for act in CM[4]:
    act.add_multiple_after(CM[3], min_offset=48)
    act.add_multiple_after(TD[3], min_offset=48)    
for act in CM[5]:
    act.add_multiple_after(CM[4], min_offset=48)
for act in CM[6]:
    act.add_multiple_after(CM[5], min_offset=48)
for act in CM[7]:
    act.add_multiple_after(CM[6], min_offset=48)
for act in CM[8]:
    act.add_multiple_after(CM[7], min_offset=48)
for act in CM[9]:
    act.add_multiple_after(CM[8], min_offset=48)
   

for act in TD[1]:
    act.add_multiple_after(CM[1])
for act in TD[2]:
    act.add_multiple_after(CM[2])
    act.add_multiple_after(TD[1])
for act in TD[3]:
    act.add_multiple_after(CM[3])
    act.add_multiple_after(TD[2])
for act in TD[4]:
    act.add_multiple_after(TD[3])
    act.add_multiple_after(CM[4])
for act in TD[5]:
    act.add_multiple_after(TD[4])
    act.add_multiple_after(CM[5])
for act in TD[6]:
    act.add_multiple_after(CM[6])
    act.add_multiple_after(TD[5])
for act in TD[7]:
    act.add_multiple_after(CM[7])
    act.add_multiple_after(TD[6])
for act in TD[8]:
    act.add_multiple_after(TD[7])
    act.add_multiple_after(CM[8])
for act in TD[9]:
    act.add_multiple_after(CM[9])
    act.add_multiple_after(TD[8])


for act in TP[2]:
    act.add_multiple_after(TP[1])
for act in TP[3]:
    act.add_multiple_after(TP[2])

for act in CC[1]:
    act.add_multiple_after(TP[3] + TD[9], min_offset=48)


path = f"../activity_data/{course_label}.json"
with open(path, "w") as f:
    json.dump(course.to_dict(), f)
