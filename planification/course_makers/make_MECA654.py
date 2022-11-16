import json
import copy

# MECA654

from automatic_university_scheduler.scheduling import Activity, Course

course_label = "MECA654"
course = Course(label=course_label, color="Green")
teachers_acronyms = {
    "EP": (["PAIREL ERIC"], 1),
    "ER": (["ROUX EMILE"], 1),
    "CE": (["ELMO KULANESAN CHRISTIAN"], 1),
}

exam_teachers = [teachers_acronyms[acr] for acr in ["EP", "ER", "CE"]]
default_rooms = json.load(open("../default_rooms.json"))
rooms = {
    "amphi_x1": (["A-POLY-B120"], 1),
    "big_info_rooms_x1": (["A-POLY-C213", "A-POLY-C214", "A-POLY-C215"], 1),
    "info_rooms_x1": (
        ["A-POLY-C213", "A-POLY-C214", "A-POLY-C215", "A-POLY-C216", "A-POLY-C217"],
        1,
    ),
}
activities_ressources = {
    "CM": {
        1: [
            ("MM-3", "ER", "amphi"),
        ],
        2: [
            ("MM-3", "ER", "amphi"),
        ],
        3: [
            ("MM-3", "ER", "amphi"),
        ],
        4: [
            ("MM-3", "ER", "amphi"),
        ],
        5: [
            ("MM-3", "ER", "amphi"),
        ],
        6: [
            ("MM-3", "ER", "amphi"),
        ],
        7: [
            ("MM-3", "ER", "amphi"),
        ],
    },
    "TD": {
        1: [
            ("MM-3-A-TD", "CE", "default"),
            ("MM-3-B-TD", "CE", "default"),
            ("MM-3-C-TD", "CE", "default"),
        ],
        2: [
            ("MM-3-A-TD", "CE", "default"),
            ("MM-3-B-TD", "CE", "default"),
            ("MM-3-C-TD", "AB", "default"),
        ],
        3: [
            ("MM-3-A-TD", "CE", "default"),
            ("MM-3-B-TD", "CE", "default"),
            ("MM-3-C-TD", "AB", "default"),
        ],
        4: [
            ("MM-3-A-TD", "CE", "default"),
            ("MM-3-B-TD", "CE", "default"),
            ("MM-3-C-TD", "AB", "default"),
        ],
        5: [
            ("MM-3-A-TD", "CE", "default"),
            ("MM-3-B-TD", "CE", "default"),
            ("MM-3-C-TD", "AB", "default"),
        ],
        6: [
            ("MM-3-A-TD", "CE", "default"),
            ("MM-3-B-TD", "CE", "default"),
            ("MM-3-C-TD", "AB", "default"),
        ],
        7: [
            ("MM-3-A-TD", "CE", "default"),
            ("MM-3-B-TD", "CE", "default"),
            ("MM-3-C-TD", "AB", "default"),
        ],
        8: [
            ("MM-3-A-TD", "CE", "default"),
            ("MM-3-B-TD", "CE", "default"),
            ("MM-3-C-TD", "AB", "default"),
        ],
        9: [
            ("MM-3-A-TD", "CE", "default"),
            ("MM-3-B-TD", "CE", "default"),
            ("MM-3-C-TD", "AB", "default"),
        ],
        10: [
            ("MM-3-A-TD", "CE", "big_info"),
            ("MM-3-B-TD", "CE", "big_info"),
            ("MM-3-C-TD", "AB", "big_info"),
        ],
    },
    "TP": {
        1: [
            ("MM-3-A1", "CE", "info"),
            ("MM-3-A2", "CE", "info"),
            ("MM-3-B1", "CE", "info"),
            ("MM-3-B2", "AB", "info"),
            ("MM-3-C1", "AB", "info"),
            ("MM-3-C2", "AB", "info"),
        ],
        2: [
            ("MM-3-A1", "CE", "info"),
            ("MM-3-A2", "CE", "info"),
            ("MM-3-B1", "CE", "info"),
            ("MM-3-B2", "AB", "info"),
            ("MM-3-C1", "AB", "info"),
            ("MM-3-C2", "AB", "info"),
        ],
        3: [
            ("MM-3-A1", "CE", "info"),
            ("MM-3-A2", "CE", "info"),
            ("MM-3-B1", "CE", "info"),
            ("MM-3-B2", "AB", "info"),
            ("MM-3-C1", "AB", "info"),
            ("MM-3-C2", "AB", "info"),
        ],
    },
}


def make_activities(activities_data, course):
    all_activities = {}
    for kind, activities_kind in activities_data.items():
        all_activities[kind] = {}
        for index, atomic_activities in activities_kind.items():
            all_activities[kind][index] = []
            activities =  all_activities[kind][index]  
            for students, teachers, rooms in atomic_activities:
                activity = Activity(
                    label=f"{course_label}_{students}_{kind}_{index}",
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
    return all_activities


# def make_CM(
#     index=1,
#     after=None,
#     min_offset=0,
#     max_offset=96 * 5,
#     add_to=None,
#     teacher=CM_teacher,
#     rooms=["A-POLY-B120"],
# ):
#     students = "MM-3"
#     if index in range(1, 4):
#         part = "solide"
#     elif index in range(4, 7):
#         part = "fluide"
#     label = f"{course_label}_{part}_{students}_CM_{index}"
#     activity = Activity(label=label, students=students, kind="CM", duration=6)
#     activity.add_ressources(kind="teachers", quantity=1, pool=[CM_teacher])
#     activity.add_ressources(kind="rooms", quantity=1, pool=rooms)
#     if after != None:
#         activity.add_multiple_after(after, min_offset=min_offset, max_offset=max_offset)
#     if add_to != None:
#         add_to.add_activity(activity)
#     return [activity]


# def make_TD(
#     TD_blocks, index=1, after=None, min_offset=0, max_offset=96 * 5, add_to=None
# ):
#     if index in range(1, 7):
#         part = "solide"
#     elif index in range(7, 13):
#         part = "fluide"
#     TD_blocks = TD_blocks[part]
#     activities = []
#     for students, teacher in TD_blocks:
#         activity = Activity(
#             label=f"{course_label}_{part}_{students}_TD_{index}",
#             students=students,
#             duration=6,
#         )
#         teacher = [teachers_acronyms[t] for t in teacher]
#         activity.add_ressources(kind="teachers", quantity=1, pool=teacher)
#         room_category = TD_rooms[index]
#         if room_category == "default":
#             room_pool = default_rooms[students]
#         elif room_category == "info":
#             room_pool = big_info_rooms
#         activity.add_ressources(kind="rooms", quantity=1, pool=room_pool)
#         if after != None:
#             if after != None:
#                 activity.add_multiple_after(
#                     after, min_offset=min_offset, max_offset=max_offset
#                 )
#         course.add_activity(activity)
#         if add_to != None:
#             add_to.add_activity(activity)
#         activities.append(activity)
#     return activities


# def make_TP(
#     TP_blocks, index=1, after=None, min_offset=0, max_offset=96 * 5, add_to=None
# ):
#     TP_blocks = TP_blocks[index]
#     activities = []
#     for students, teacher in TP_blocks:
#         activity = Activity(
#             label=f"{course_label}_{students}_TP_{index}",
#             students=students,
#             duration=16,
#             kind="TP",
#         )
#         teacher = [teachers_acronyms[t] for t in teacher]
#         activity.add_ressources(kind="teachers", quantity=1, pool=teacher)
#         activity.add_ressources(kind="rooms", quantity=1, pool=TP_rooms)
#         if after != None:
#             if after != None:
#                 activity.add_multiple_after(
#                     after, min_offset=min_offset, max_offset=max_offset
#                 )
#         course.add_activity(activity)
#         if add_to != None:
#             add_to.add_activity(activity)
#         activities.append(activity)
#     return activities


# def make_CC(
#     index=1,
#     after=None,
#     min_offset=0,
#     max_offset=96 * 5,
#     add_to=None,
#     teacher=exam_teachers,
#     rooms=["A-POLY-B120"],
# ):
#     students = "MM-3"
#     label = f"{course_label}_{students}_CT_{index}"
#     activity = Activity(label=label, students=students, kind="EX", duration=3 + 1)
#     activity.add_ressources(kind="teachers", quantity=3, pool=exam_teachers)
#     activity.add_ressources(kind="rooms", quantity=1, pool=rooms)
#     if after != None:
#         if after != None:
#             activity.add_multiple_after(
#                 after, min_offset=min_offset, max_offset=max_offset
#             )
#     if add_to != None:
#         add_to.add_activity(activity)
#     return [activity]


# # CM
# CM = {}
# for index in range(1, 9):
#     CM[index] = make_CM(
#         index=index,
#         after=None,
#         add_to=course,
#     )
# # TD
# TD = {}
# for index in range(1, 13):
#     TD[index] = make_TD(
#         TD_blocks=TD_blocks,
#         index=index,
#         after=None,
#         add_to=course,
#     )
# # TP
# TP = {}
# for index in range(1, 4):
#     TP[index] = make_TP(
#         TP_blocks=TP_blocks,
#         index=index,
#         after=None,
#         add_to=course,
#     )
# # CC
# CC = {}
# for index in range(1, 3):
#     CC[index] = make_CC(
#         index=index,
#         after=None,
#         add_to=course,
#     )

# # ENCHAINEMENTS
# for act in CM[2]:
#     act.add_multiple_after(CM[1], min_offset=48)
# for act in CM[3]:
#     act.add_multiple_after(CM[2], min_offset=48)
# for act in CM[5]:
#     act.add_multiple_after(TD[8], min_offset=48)
# for act in CM[6]:
#     act.add_multiple_after(TD[5], min_offset=48)


# for act in TD[1]:
#     act.add_multiple_after(CM[2])
# for act in TD[2]:
#     act.add_multiple_after(CM[3])
# for act in TD[3]:
#     act.add_multiple_after(TD[2])
# for act in TD[4]:
#     act.add_multiple_after(TD[3])
# for act in TD[5]:
#     act.add_multiple_after(TD[4])
# for act in TD[6]:
#     act.add_multiple_after(TD[5])
# for act in TD[7]:
#     act.add_multiple_after(CM[4])
# for act in TD[8]:
#     act.add_multiple_after(TD[7])
# for act in TD[9]:
#     act.add_multiple_after(CM[6])
# for act in TD[10]:
#     act.add_multiple_after(TD[9])
# for act in TD[11]:
#     act.add_multiple_after(TD[10])
# for act in TD[12]:
#     act.add_multiple_after(TD[11])

# for act in TP[2]:
#     act.add_multiple_after(TP[1])
# for act in TP[3]:
#     act.add_multiple_after(TP[2])

# for act in CC[1]:
#     act.add_multiple_after(TP[3] + TD[6], min_offset=48)
# for act in CC[2]:
#     act.add_multiple_after(TD[12] + CC[1], min_offset=48)

path = f"../activity_data/{course_label}.json"
with open(path, "w") as f:
    json.dump(course.to_dict(), f)
