import json
import copy

# MECA653


from automatic_university_scheduler.scheduling import Activity, Course


course_label = "MECA653"
course = Course(label=course_label, color="magenta")


def make_TD_blocks(teacher):
    TD_blocks = [
        ("MM-3-A-TD", teacher),
        ("MM-3-B-TD", teacher),
        ("MM-3-C-TD", teacher),
    ]
    return TD_blocks


def make_TP_blocks(teacher1, teacher2="CHARLEUX LUDOVIC"):
    TP_blocks = [
        ("MM-3-A-TD", [teacher1, teacher2]),
        ("MM-3-B-TD", [teacher1, teacher2]),
        ("MM-3-C-TD", [teacher1, teacher2]),
    ]
    return TP_blocks


TD_rooms = ["A-POLY-C213", "A-POLY-C214", "A-POLY-C215", "A-POLY-C216"]
TP_rooms = ["A-POLY-C213", "A-POLY-C214", "A-POLY-C215", "A-POLY-C216"]
last_act = None


def make_CM(
    index=1,
    after=None,
    min_offset=0,
    max_offset=96 * 5,
    add_to=None,
    teacher="CHARLEUX LUDOVIC",
    rooms=["A-POLY-B120"],
):
    students = "MM-3"
    label = f"{course_label}_{students}_CM_{index}"
    activity = Activity(label=label, students=students, kind="CM", duration=6)
    activity.add_ressources(kind="teachers", quantity=1, pool=[teacher])
    activity.add_ressources(kind="rooms", quantity=1, pool=rooms)
    if after != None:
        for other in after:
            activity.add_after(other, min_offset=min_offset, max_offset=max_offset)
    if add_to != None:
        add_to.add_activity(activity)
    return activity


def make_TD(
    TD_blocks, index=1, after=None, min_offset=0, max_offset=96 * 5, add_to=None
):
    activities = []
    for students, teacher in TD_blocks:
        activity = Activity(
            label=f"{course_label}_{students}_TD_{index}", students=students, duration=6
        )
        activity.add_ressources(kind="teachers", quantity=1, pool=[teacher])
        activity.add_ressources(kind="rooms", quantity=1, pool=TD_rooms)
        if after != None:
            for other in after:
                activity.add_after(other, min_offset=min_offset, max_offset=max_offset)
        course.add_activity(activity)
        if add_to != None:
            add_to.add_activity(activity)
        activities.append(activity)
    return activities


def make_TP(
    TP_blocks, index=1, after=None, min_offset=0, max_offset=96 * 5, add_to=None
):
    activities = []
    for students, teachers in TP_blocks:
        activity = Activity(
            label=f"{course_label}_{students}_TP_{index}",
            students=students,
            duration=16,
            kind="TP",
        )
        activity.add_ressources(kind="teachers", quantity=2, pool=teachers)
        activity.add_ressources(kind="rooms", quantity=1, pool=TP_rooms)
        if after != None:
            for other in after:
                activity.add_after(other, min_offset=min_offset, max_offset=max_offset)
        course.add_activity(activity)
        if add_to != None:
            add_to.add_activity(activity)
        activities.append(activity)
    return activities


# BLOC IMAGE
index = "Image"
CM_Image = make_CM(
    index=index,
    after=None,
    min_offset=0,
    teacher="ELMO KULANESAN CHRISTIAN",
    rooms=["A-POLY-B120"],
    add_to=course,
)
TD_Image = make_TD(
    make_TD_blocks("ELMO KULANESAN CHRISTIAN"),
    index=index,
    after=[CM_Image],
    min_offset=0,
    max_offset=None,
    add_to=course,
)
TP_Image = make_TP(
    make_TP_blocks("ELMO KULANESAN CHRISTIAN"),
    index=index,
    after=TD_Image,
    min_offset=0,
    max_offset=None,
    add_to=course,
)

# BLOC DATA
index = "Data"
CM_Data = make_CM(
    index=index,
    after=TP_Image,
    min_offset=0,
    teacher="ROUX EMILE",
    rooms=["A-POLY-B120"],
    add_to=course,
)
TD_Data = make_TD(
    make_TD_blocks("ROUX EMILE"),
    index=index,
    after=[CM_Data],
    min_offset=0,
    max_offset=None,
    add_to=course,
)
TP_Data = make_TP(
    make_TP_blocks("ROUX EMILE"),
    index=index,
    after=TD_Data,
    min_offset=0,
    max_offset=None,
    add_to=course,
)

# BLOC ODE
index = "ODE"
CM_ODE = make_CM(
    index=index,
    after=TP_Data,
    min_offset=0,
    teacher="CHARLEUX LUDOVIC",
    rooms=["A-POLY-B120"],
    add_to=course,
)
TD_ODE = make_TD(
    make_TD_blocks("CHARLEUX LUDOVIC"),
    index=index,
    after=[CM_ODE],
    min_offset=0,
    max_offset=None,
    add_to=course,
)
TP_ODE = make_TP(
    make_TP_blocks("ROUX EMILE"),
    index=index,
    after=TD_ODE,
    min_offset=0,
    max_offset=None,
    add_to=course,
)

# BLOC LEARN
index = "Learn"
CM_Learn = make_CM(
    index=index,
    after=TP_ODE,
    min_offset=0,
    teacher="CHARLEUX LUDOVIC",
    rooms=["A-POLY-B120"],
    add_to=course,
)
TD_Learn = make_TD(
    make_TD_blocks("CHARLEUX LUDOVIC"),
    index=index,
    after=[CM_Learn],
    min_offset=0,
    max_offset=None,
    add_to=course,
)
TP_Learn = make_TP(
    make_TP_blocks("ELMO KULANESAN CHRISTIAN"),
    index=index,
    after=TD_Learn,
    min_offset=0,
    max_offset=None,
    add_to=course,
)

# BLOC Opti
index = "Opti"
CM_Opti = make_CM(
    index=index,
    after=TP_Learn,
    min_offset=0,
    teacher="CHARLEUX LUDOVIC",
    rooms=["A-POLY-B120"],
    add_to=course,
)
TD_Opti = make_TD(
    make_TD_blocks("CHARLEUX LUDOVIC"),
    index=index,
    after=[CM_Opti],
    min_offset=0,
    max_offset=None,
    add_to=course,
)
TP_Opti = make_TP(
    make_TP_blocks("ROUX EMILE"),
    index=index,
    after=TD_Opti,
    min_offset=0,
    max_offset=None,
    add_to=course,
)

# PROJETS
index = "Proj"
TP_Projet = make_TP(
    make_TP_blocks("ELMO KULANESAN CHRISTIAN"),
    index=index,
    after=TP_Opti,
    min_offset=0,
    max_offset=None,
    add_to=course,
)


path = f"../activity_data/{course_label}.json"
with open(path, "w") as f:
    json.dump(course.to_dict(), f)
