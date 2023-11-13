import json
import copy

# PACI 642

from automatic_university_scheduler.scheduling import Activity, Course

students = "SNI-3-D-TD"
course_label = "PACI642"
teachers_acronyms = {"YM": "MUGNIER YANNICK"}
CM_teacher = "YM"
exam_teachers = "YM"
CM_rooms = ["A-POLY-C204"]
course = Course(label=course_label, color="Green")
default_rooms = json.load(open("../default_rooms.json"))


TD_rooms = {
    1: "default",
    2: "default",
    3: "default",
    4: "default",
    5: "default",
    6: ["A-POLY-C214", "A-POLY-C215"],
    7: "default",
    8: "default",
    9: ["A-POLY-C214", "A-POLY-C215"],
    10: "default",
}

CM_rooms = {
    1: "default",
    2: "default",
    3: "default",
    4: "default",
    5: "default",
    6: "default",
    7: ["A-POLY-C214", "A-POLY-C215"],
    8: "default",
    9: "default", 
    10: "default",
}
TP_rooms = ["A-POLY-C116", "A-POLY-C117"]

TD_blocks = [["SNI-3-D-TD", ["YM"]]]
TP_blocks = [["SNI-3-D1", ["YM"]]]


def make_CM(
    index=1,
    after=None,
    min_offset=0,
    max_offset=96 * 5,
    add_to=None,
    teacher=CM_teacher,
    rooms=CM_rooms,
):
    room_pool  = rooms[index]
    if room_pool == "default":
        room_pool = default_rooms[students]
 
        
    label = f"{course_label}_{students}_CM_{index}"
    activity = Activity(label=label, students=students, kind="CM", duration=6)
    activity.add_ressources(kind="teachers", quantity=1, pool=[teachers_acronyms[CM_teacher]])
    activity.add_ressources(kind="rooms", quantity=1, pool=room_pool)
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
        room_pool  = TD_rooms[index]
        if room_pool == "default":
            room_pool = default_rooms[students]
        activity.add_ressources(kind="rooms", quantity=1, pool=room_pool)
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
        activity.add_ressources(kind="rooms", quantity=2, pool=TP_rooms)
        if after != None:
            activity.add_multiple_after(
                after, min_offset=min_offset, max_offset=max_offset
            )
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
    teacher=exam_teachers,
    rooms=["A-POLY-B120"],
):
    students = "SNI-3"
    label = f"{course_label}_{students}_CT_{index}"
    activity = Activity(label=label, students=students, kind="EX", duration=6+2)
    activity.add_ressources(kind="teachers", quantity=1, pool=[teachers_acronyms[exam_teachers]])
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

# CC
CT = {}
for index in range(1, 2):
    CT[index] = make_CT(
        index=index,
        after=None,
        add_to=course,
    )

# ENCHAINEMENTS
for act in CM[2]:
    act.add_multiple_after(CM[1], min_offset=48)
for act in CM[3]:
    act.add_multiple_after(CM[2], min_offset=48)
for act in CM[4]:
    act.add_multiple_after(CM[3], min_offset=48)
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
    act.add_multiple_after(CM[2])
for act in TD[2]:
    act.add_multiple_after(TD[1])
    act.add_multiple_after(CM[3])
for act in TD[3]:
    act.add_multiple_after(TD[1])
    act.add_multiple_after(CM[4])
for act in TD[4]:
    act.add_multiple_after(TD[3])
    act.add_multiple_after(CM[5])
for act in TD[5]:
    act.add_multiple_after(TD[4])
    act.add_multiple_after(CM[6])
for act in TD[6]:
    act.add_multiple_after(TD[5])
    act.add_multiple_after(CM[7], max_offset=1)
for act in TD[7]:
    act.add_multiple_after(TD[6])
    act.add_multiple_after(CM[8])
for act in TD[8]:
    act.add_multiple_after(TD[7])
    act.add_multiple_after(CM[9]) 
for act in TD[9]:
    act.add_multiple_after(TD[8])

for act in TP[2]:
    act.add_multiple_after(TP[1])

for act in CT[1]:
    act.add_multiple_after(TD[9], min_offset=48)
    act.add_multiple_after(TP[2], min_offset=48)

path = f"../activity_data/{course_label}.json"
with open(path, "w") as f:
    json.dump(course.to_dict(), f)
