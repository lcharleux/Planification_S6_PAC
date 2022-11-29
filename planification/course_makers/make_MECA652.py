import json
import copy

# MECA652

from automatic_university_scheduler.scheduling import Activity, Course

course_label = "MECA652"
teachers_acronyms = {
    "PS": "SAFFRE PHILIPPE",
}


CM_teacher = teachers_acronyms["PS"]
exam_teachers = [teachers_acronyms[acr] for acr in ["PS"]]

course = Course(label=course_label, color="Green")
default_rooms = json.load(open("../default_rooms.json"))
big_info_rooms = ["A-POLY-C213", "A-POLY-C214", "A-POLY-C215"]
info_rooms = ["A-POLY-C213", "A-POLY-C214", "A-POLY-C215", "A-POLY-C216", "A-POLY-C217"]
TP_rooms = info_rooms

TD_rooms = {
    1: "default",
    2: "default",
    3: "default",
    4: "default",
    5: "default",
    6: "default",
    7: "default",
    8: "default",
    9: "default",
    10: "default",
}

TD_blocks = [
    ("MM-3-A-TD", ["PS"]),
    ("MM-3-B-TD", ["PS"]),
    ("MM-3-C-TD", ["PS"]),
]

TP_blocks = {
    1: [
        ("MM-3-A1", ["PS"]),
        ("MM-3-A2", ["PS"]),
        ("MM-3-B1", ["PS"]),
        ("MM-3-B2", ["PS"]),
        ("MM-3-C1", ["PS"]),
        ("MM-3-C2", ["PS"]),
    ],
    2: [
        ("MM-3-A1", ["PS"]),
        ("MM-3-A2", ["PS"]),
        ("MM-3-B1", ["PS"]),
        ("MM-3-B2", ["PS"]),
        ("MM-3-C1", ["PS"]),
        ("MM-3-C2", ["PS"]),
    ],
    3: [
        ("MM-3-A1", ["PS"]),
        ("MM-3-A2", ["PS"]),
        ("MM-3-B1", ["PS"]),
        ("MM-3-B2", ["PS"]),
        ("MM-3-C1", ["PS"]),
        ("MM-3-C2", ["PS"]),
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
    label = f"{course_label}_{students}_CM_{index}"
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
    activities = []
    for students, teacher in TD_blocks:
        activity = Activity(
            label=f"{course_label}_{students}_TD_{index}",
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
for index in range(1, 11):
    CM[index] = make_CM(
        index=index,
        after=None,
        add_to=course,
    )
# TD
TD = {}
for index in range(1, 11):
    TD[index] = make_TD(
        TD_blocks=TD_blocks,
        index=index,
        after=None,
        add_to=course,
    )
# TP
TP = {}
for index in range(1, 3):
    TP[index] = make_TP(
        TP_blocks=TP_blocks,
        index=index,
        after=None,
        add_to=course,
    )
# # CC
# CC = {}
# for index in range(1, 2):
#     CC[index] = make_CC(
#         index=index,
#         after=None,
#         add_to=course,
#     )

# ENCHAINEMENTS
for act in CM[2]:
    act.add_multiple_after(CM[1], min_offset=0, max_offset=1)
for act in CM[3]:
    act.add_multiple_after(CM[2], min_offset=48)
    act.add_multiple_after(TD[1], min_offset=48)
for act in CM[4]:
    act.add_multiple_after(CM[3], min_offset=48)
    act.add_multiple_after(TD[2], min_offset=48)    
for act in CM[5]:
    act.add_multiple_after(CM[4], min_offset=48)
    act.add_multiple_after(TD[3], min_offset=48)
for act in CM[6]:
    act.add_multiple_after(CM[5], min_offset=48)
    act.add_multiple_after(TD[4], min_offset=48)
for act in CM[7]:
    act.add_multiple_after(CM[6], min_offset=48)
    act.add_multiple_after(TD[5], min_offset=48)
for act in CM[8]:
    act.add_multiple_after(CM[7], min_offset=48)
    act.add_multiple_after(TD[6], min_offset=48)    
for act in CM[9]:
    act.add_multiple_after(CM[8], min_offset=48)
    act.add_multiple_after(TD[7], min_offset=48)
for act in CM[10]:
    act.add_multiple_after(CM[9], min_offset=48)
    act.add_multiple_after(TD[8], min_offset=48)

# TD par blocs de 3:
for index, TDi in TD.items():
    for i in range(1, len(TDi)):
        TDi[i].add_after(TDi[i-1], max_offset = 40, min_offset = -40)


# TD enchainement général
TD_CM_offset = 40
for act in TD[1]:
    act.add_multiple_after(CM[2], max_offset=TD_CM_offset)
for act in TD[2]:
    act.add_multiple_after(CM[3], max_offset=TD_CM_offset)
    act.add_multiple_after(TD[1])
for act in TD[3]:
    act.add_multiple_after(TD[2])
    act.add_multiple_after(CM[4], max_offset=TD_CM_offset)
for act in TD[4]:
    act.add_multiple_after(TD[3])
    act.add_multiple_after(CM[5], max_offset=TD_CM_offset)
for act in TD[5]:
    act.add_multiple_after(TD[4])
    act.add_multiple_after(CM[6], max_offset=TD_CM_offset)
for act in TD[6]:
    act.add_multiple_after(TD[5])
    act.add_multiple_after(CM[7], max_offset=TD_CM_offset)
for act in TD[7]:
    act.add_multiple_after(TD[6])
    act.add_multiple_after(CM[8], max_offset=TD_CM_offset)
for act in TD[8]:
    act.add_multiple_after(TD[7])
    act.add_multiple_after(CM[9], max_offset=TD_CM_offset)
for act in TD[9]:
    act.add_multiple_after(TD[8])
    act.add_multiple_after(CM[10], max_offset=TD_CM_offset)
for act in TD[10]:
    act.add_multiple_after(TD[9])
    act.add_multiple_after(TP[1])    

# TP par blocs de 2:
for index, TPi in TP.items():
     TPi[1].add_after(TPi[0], max_offset = 16)
     TPi[3].add_after(TPi[2], max_offset = 16)
     TPi[5].add_after(TPi[4], max_offset = 16)


for act in TP[1]:
    act.add_multiple_after(TD[9])
for act in TP[2]:
    act.add_multiple_after(TP[1])
    act.add_multiple_after(TD[10])

# for act in CC[1]:
#     act.add_multiple_after(TP[3] + TD[6], min_offset=48)

path = f"../activity_data/{course_label}.json"
with open(path, "w") as f:
    json.dump(course.to_dict(), f)
