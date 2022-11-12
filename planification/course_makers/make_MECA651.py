import json
import copy

# MECA651
# MODULE EN DEUX SOUS PARTIES: SOLIDE ET FLUIDE

from automatic_university_scheduler.scheduling import Activity, Course

course_label = "MECA651"
teachers_acronyms = {
    "EP": "PAIREL ERIC",
    "ER": "ROUX EMILE",
    "CE": "ELMO KULANESAN CHRISTIAN",
    "AB": "BENHEMOU AYA",
}
CM_teacher = teachers_acronyms["EP"]
exam_teachers = [teachers_acronyms[acr] for acr in ["EP", "ER", "CE"]]
TP_rooms = ["A-POLY-B104"]
course = Course(label=course_label, color="Green")
default_rooms = json.load(open("../default_rooms.json"))
big_info_rooms = ["A-POLY-C213", "A-POLY-C214", "A-POLY-C215"]

TD_rooms = {
    1: "default",
    2: "info",
    3: "default",
    4: "default",
    5: "default",
    6: "default",
    7: "default",
    8: "default",
    9: "default",
    10: "default",
    11: "default",
    12: "info",
}

TD_blocks = {
    "solide": [
        ("MM-3-A-TD", ["CE"]),
        ("MM-3-B-TD", ["CE"]),
        ("MM-3-C-TD", ["AB"]),
    ],
    "fluide": [
        ("MM-3-A-TD", ["ER"]),
        ("MM-3-B-TD", ["AB"]),
        ("MM-3-C-TD", ["ER"]),
    ],
}

TP_blocks = {
    1: [
        ("MM-3-A1", ["CE"]),
        ("MM-3-A2", ["CE"]),
        ("MM-3-B1", ["CE"]),
        ("MM-3-B2", ["AB"]),
        ("MM-3-C1", ["AB"]),
        ("MM-3-C2", ["AB"]),
    ],
    2: [
        ("MM-3-A1", ["AB"]),
        ("MM-3-A2", ["AB"]),
        ("MM-3-B1", ["AB"]),
        ("MM-3-B2", ["CE"]),
        ("MM-3-C1", ["CE"]),
        ("MM-3-C2", ["CE"]),
    ],
    3: [
        ("MM-3-A1", ["CE"]),
        ("MM-3-A2", ["AB"]),
        ("MM-3-B1", ["CE"]),
        ("MM-3-B2", ["AB"]),
        ("MM-3-C1", ["CE"]),
        ("MM-3-C2", ["AB"]),
    ],
}


def make_CM(
    index=1,
    after=None,
    min_offset=0,
    max_offset=96 * 5,
    add_to=None,
    teacher=CM_teacher,
    rooms=["A-POLY-B120"],
):
    students = "MM-3"
    if index in range(1, 4):
        part = "solide"
    elif index in range(4, 7):
        part = "fluide"
    label = f"{course_label}_{part}_{students}_CM_{index}"
    activity = Activity(label=label, students=students, kind="CM", duration=6)
    activity.add_ressources(kind="teachers", quantity=1, pool=[CM_teacher])
    activity.add_ressources(kind="rooms", quantity=1, pool=rooms)
    if after != None:
        activity.add_multiple_after(after, min_offset=min_offset, max_offset=max_offset)
    if add_to != None:
        add_to.add_activity(activity)
    return [activity]


def make_TD(
    TD_blocks, index=1, after=None, min_offset=0, max_offset=96 * 5, add_to=None
):
    if index in range(1, 7):
        part = "solide"
    elif index in range(7, 13):
        part = "fluide"
    TD_blocks = TD_blocks[part]
    activities = []
    for students, teacher in TD_blocks:
        activity = Activity(
            label=f"{course_label}_{part}_{students}_TD_{index}",
            students=students,
            duration=6,
        )
        teacher = [teachers_acronyms[t] for t in teacher]
        activity.add_ressources(kind="teachers", quantity=1, pool=teacher)
        room_category = TD_rooms[index]
        if room_category == "default":
            room_pool = default_rooms[students]
        elif room_category == "info":
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
    TP_blocks = TP_blocks[index]
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
    students = "MM-3"
    label = f"{course_label}_{students}_CT_{index}"
    activity = Activity(label=label, students=students, kind="EX", duration=3 + 1)
    activity.add_ressources(kind="teachers", quantity=3, pool=exam_teachers)
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
for index in range(1, 7):
    CM[index] = make_CM(
        index=index,
        after=None,
        add_to=course,
    )
# TD
TD = {}
for index in range(1, 13):
    TD[index] = make_TD(
        TD_blocks=TD_blocks,
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
for index in range(1, 3):
    CC[index] = make_CC(
        index=index,
        after=None,
        add_to=course,
    )

# ENCHAINEMENTS
for act in CM[2]:
    act.add_multiple_after(CM[1], min_offset=48)
for act in CM[3]:
    act.add_multiple_after(CM[2], min_offset=48)
for act in CM[5]:
    act.add_multiple_after(TD[8], min_offset=48)
for act in CM[6]:
    act.add_multiple_after(TD[5], min_offset=48)


for act in TD[1]:
    act.add_multiple_after(CM[2])
for act in TD[2]:
    act.add_multiple_after(CM[3])
for act in TD[3]:
    act.add_multiple_after(TD[2])
for act in TD[4]:
    act.add_multiple_after(TD[3])
for act in TD[5]:
    act.add_multiple_after(TD[4])
for act in TD[6]:
    act.add_multiple_after(TD[5])
for act in TD[7]:
    act.add_multiple_after(CM[4])
for act in TD[8]:
    act.add_multiple_after(TD[7])
for act in TD[9]:
    act.add_multiple_after(CM[6])
for act in TD[10]:
    act.add_multiple_after(TD[9])
for act in TD[11]:
    act.add_multiple_after(TD[10])
for act in TD[12]:
    act.add_multiple_after(TD[11])

for act in TP[2]:
    act.add_multiple_after(TP[1])
for act in TP[3]:
    act.add_multiple_after(TP[2])

for act in CC[1]:
    act.add_multiple_after(TP[3] + TD[6], min_offset=48)
for act in CC[2]:
    act.add_multiple_after(TD[12] + CC[1], min_offset=48)

path = f"../activity_data/{course_label}.json"
with open(path, "w") as f:
    json.dump(course.to_dict(), f)
