import datetime
from ortools.sat.python import cp_model
import numpy as np
from collections import OrderedDict
import itertools
import pandas as pd
import os
from scipy import ndimage
import json
import os
import time
import yaml
import string
from automatic_university_scheduler.scheduling import (
    read_json_data,
    # get_unique_teachers_and_rooms,
    create_unavailable_constraints,
    create_weekly_unavailable_intervals,
    SolutionPrinter,
    export_solution,
    # get_atomic_students_groups,
    create_activities,
    export_student_schedule_to_xlsx,
)


WEEK_STRUCTURE = np.array(
    #    0h   1h   2h   3h   4h   5h   6h   7h   8h   9h   10h  11h  12h  13h  14h  15h  16h  17h  18h  19h  20h  21h  22h  23h
    [
        "0000 0000 0000 0000 0000 0000 0000 0000 1111 1111 1111 1111 0000 1111 1111 1111 1111 1111 1111 0000 0000 0000 0000 0000",  # MONDAY
        "0000 0000 0000 0000 0000 0000 0000 0000 1111 1111 1111 1111 1111 0000 1111 1111 1111 1111 1111 0000 0000 0000 0000 0000",  # TUESDAY
        "0000 0000 0000 0000 0000 0000 0000 0000 1111 1111 1111 1111 0000 1111 1111 1111 1111 1111 1111 0000 0000 0000 0000 0000",  # WEDNESDAY
        "0000 0000 0000 0000 0000 0000 0000 0000 1111 1111 1111 1111 1111 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000",  # THURSDAY
        "0000 0000 0000 0000 0000 0000 0000 0000 1111 1111 1111 1111 0000 1111 1111 1111 1111 1111 1111 0000 0000 0000 0000 0000",  # FRIDAY
        "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000",  # SATRUDAY
        "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000",  # SUNDAY
    ]
)

WEEK_STRUCTURE = np.array(
    [list(day.replace(" ", "")) for day in WEEK_STRUCTURE]
).astype(int)

DAYS_PER_WEEK, TIME_SLOTS_PER_DAY = WEEK_STRUCTURE.shape
MAX_WEEKS = 21
TIME_SLOTS_PER_WEEK = TIME_SLOTS_PER_DAY * DAYS_PER_WEEK
horizon = MAX_WEEKS * TIME_SLOTS_PER_WEEK
START_DAY = datetime.date.fromisocalendar(2024, 1, 1)
STOP_DAY = START_DAY + datetime.timedelta(weeks=MAX_WEEKS)

# ACTIVITY GENERATION

print("Horizon = %i" % horizon)

activity_data_dir = "activity_data/"
teacher_data_dir = "teacher_data/"
room_data_dir = "room_data/"
student_data_dir = "student_data/"
teacher_data = [read_json_data(teacher_data_dir)]
activity_data = read_json_data(activity_data_dir)
room_data = read_json_data(room_data_dir)
calendar_data = read_json_data(student_data_dir)


# STUDENTS GROUPS
students_groups = {
    None: [],
    "EPU-3-S6": [
        "MM-3-A1",
        "MM-3-A2",
        "MM-3-B1",
        "MM-3-B2",
        "MM-3-C1",
        "MM-3-C2",
        "SNI-3-D1",
        # "SNI-3-D2",
        "IDU-3-G1",
        "IDU-3-G2",
    ],
    "MM-3": ["MM-3-A1", "MM-3-A2", "MM-3-B1", "MM-3-B2", "MM-3-C1", "MM-3-C2"],
    "SNI-3": ["SNI-3-D1"],
    "IDU-3": ["IDU-3-G1", "IDU-3-G2"],
    "IDU-3_SNI-3": ["IDU-3-G1", "IDU-3-G2", "SNI-3-D1"],  # POUR LES MATH641
    "MM-3-A-TD": ["MM-3-A1", "MM-3-A2"],
    "MM-3-B-TD": ["MM-3-B1", "MM-3-B2"],
    "MM-3-C-TD": ["MM-3-C1", "MM-3-C2"],
    "SNI-3-D-TD": ["SNI-3-D1"],
    "IDU-3-G-TD": ["IDU-3-G1", "IDU-3-G2"],
    "MM-3-A1": ["MM-3-A1"],
    "MM-3-A2": ["MM-3-A2"],
    "MM-3-B1": ["MM-3-B1"],
    "MM-3-B2": ["MM-3-B2"],
    "MM-3-C1": ["MM-3-C1"],
    "MM-3-C2": ["MM-3-C2"],
    "SNI-3-D1": ["SNI-3-D1"],
    # "SNI-3-D2": ["SNI-3-D2"],
    # "SN-3-D2": ["SNI-3-D2"],  # BUG EXTRACTION ADE
    "IDU-3-G1": ["IDU-3-G1"],
    "IDU-3-G2": ["IDU-3-G2"],
}


model = cp_model.CpModel()


# EXISTING ACTIVIITIES
def get_unique_ressources_in_activities(data, kind="teachers"):
    """
    Gets the unique ressources of a given kind in activity data
    """
    unique_ressources = []
    for module, mdata in data.items():
        for act_key, act in mdata["activities"].items():
            for ress in act[kind]:
                unique_ressources += ress[1]

    return np.unique(unique_ressources)



# EXISTING ACTIVITIES
# 1. ROOMS & TEACHERS
tracked_ressources = {
    "teachers": get_unique_ressources_in_activities(activity_data, kind="teachers"),
    "rooms": get_unique_ressources_in_activities(activity_data, kind="rooms"),
}
existing_data = pd.read_csv("existing_activities/extraction_data.csv").fillna("")
ressource_existing_intervals = {
    k: {t: [] for t in tracked_ressources[k]} for k in ["teachers", "rooms"]
}

with open("outputs/tracked_ressources.yml", "w") as ymldump:
    yaml.dump({k: v.tolist() for k, v in tracked_ressources.items()}, ymldump)


# 2. STUDENTS
school = "POLYTECH Annecy"
unique_students = list(students_groups.keys())
students_existing_intervals = {k: [] for k in students_groups.keys()}


for index, row in existing_data.iterrows():
    year = row.year
    week = row.week
    weekday = row.weekday
    from_dayslot = row.from_dayslot
    to_dayslot = row.to_dayslot
    act = {
        "kind": "isocalendar",
        "from_year": year,
        "from_week": week,
        "from_weekday": weekday,
        "from_dayslot": from_dayslot,
        "to_year": year,
        "to_week": week,
        "to_weekday": weekday,
        "to_dayslot": to_dayslot,
    }
    for ressource_kind in ["teachers", "rooms"]:
        tracked_ress = tracked_ressources[ressource_kind]
        ressources = row[ressource_kind]
        if ressources == "":
            ressources = []
        else:
            ressources = [t.strip() for t in ressources.split(",")]
        for ressource in ressources:
            if ressource in tracked_ress:
                ressource_existing_intervals[ressource_kind][ressource].append(act)

    if row.school == school:
        for students in [s.strip() for s in row.students.split(",")]:
            if students in students_existing_intervals.keys():
                students_existing_intervals[students].append(act)

# 3. MERGE THE FUCK
teacher_data.append({})
for teacher, acts in ressource_existing_intervals["teachers"].items():
    if teacher not in teacher_data[-1].keys():
        teacher_data[-1][teacher] = {"unavailable": []}
    teacher_data[-1][teacher]["unavailable"] += acts

for room, acts in ressource_existing_intervals["rooms"].items():
    if room not in room_data.keys():
        room_data[room] = {"unavailable": []}
    room_data[room]["unavailable"] += acts

students_data = [calendar_data, {}]

for students, acts in students_existing_intervals.items():
    if students not in students_data[-1].keys():
        students_data[-1][students] = {"unavailable": []}
    students_data[-1][students]["unavailable"] += acts


# 4. CHECK STUFF
for teacher, intervals in ressource_existing_intervals["teachers"].items():
    duration = 0
    for interval in intervals:
        start = interval["from_dayslot"]
        end = interval["to_dayslot"]
        start = max(32, start)
        end = min(73, end)
        duration += max(0, end - start)
    print(teacher, duration)


# TEACHER UNAVAILABILITY
teacher_unavailable_intervals = [
    create_unavailable_constraints(
        model, data=teacher_data[i], start_day=START_DAY, horizon=horizon
    )
    for i in range(len(teacher_data))
]
# ROOM UNAVAILABILITY
room_unavailable_intervals = create_unavailable_constraints(
    model, data=room_data, start_day=START_DAY, horizon=horizon
)

# NIGHT SHIFTS & LUNCH BREAKS AND WEEK-ENDS!
weekly_unavailable_intervals = create_weekly_unavailable_intervals(
    model, WEEK_STRUCTURE, MAX_WEEKS
)

# STUDENT UNAVAILABILITY
# students_data = students_data[:1] # ATTENTION TEST A RETIRER
students_unavailable_intervals = [
    create_unavailable_constraints(
        model, data=students_data[i], start_day=START_DAY, horizon=horizon
    )
    for i in range(len(students_data))
]


# CHECK UNAVAILABILITY
students_atomic_groups = np.unique(
    np.concatenate([v for k, v in students_groups.items()])
)
matrices = {
    k: np.zeros(96 * 7 * MAX_WEEKS).astype(np.int32) for k in students_atomic_groups
}
for i in range(len(students_data)):
    for group, intervals in students_data[i].items():
        for interval in intervals["unavailable"]:
            from_week = interval["from_week"]
            to_week = interval["to_week"]
            from_weekday = interval["from_weekday"]
            to_weekday = interval["to_weekday"]
            start = (
                672 * (from_week - 1)
                + 96 * (from_weekday - 1)
                + interval["from_dayslot"]
            )
            end = 672 * (to_week - 1) + 96 * (to_weekday - 1) + interval["to_dayslot"]
            for student in students_groups[group]:
                matrices[student][start:end] += 1

for agroup, matrix in matrices.items():
    d = 1
    w = 1
    with open(f"./outputs/students_unavailability_matrix_{agroup}.txt", "w", encoding="utf-8") as f:
        for r in matrix.reshape(-1, 96):
            f.write(f"w{w}-d{d} " + "".join([str(rr) for rr in r]) + "\n")
            d += 1
            if d == 8:
                w += 1
                d = 1

atomic_students_unavailable_intervals = create_activities(
    activity_data,
    model,
    students_groups,
    horizon=horizon,
    teacher_unavailable_intervals=teacher_unavailable_intervals,
    room_unavailable_intervals=room_unavailable_intervals,
    students_unavailable_intervals=students_unavailable_intervals,
    weekly_unavailable_intervals=weekly_unavailable_intervals,
    cm_td_allowed_slots=[33, 40, 53, 60, 67],
)

# MINIMIZE SEMESTER DURATION or WEEK DURATION

# 1. SEMESTER DURATION 
def get_semester_duration(model, activity_data, students_groups, horizon):
    activities_ends = []
    for file, module in activity_data.items():
        for label, activity in module["activities"].items():
            if activity["kind"] != "lunch":
                activities_ends.append(activity["model"]["end"])
    makespan = model.NewIntVar(0, horizon, "makespan")
    model.AddMaxEquality(makespan, activities_ends)
    return makespan



# 2. WEEK DURATION AND ABSOLUTE DEVIATION FROM MEAN WEEK DURATION
def get_absolute_week_duration_deviation(model, activity_data, students_groups, horizon, MAX_WEEKS):
    week_duration = {group:[[] for i in range(MAX_WEEKS)] for group in students_atomic_groups}
    total_activities_duration = {group:0 for group in students_atomic_groups}
    for file, module in activity_data.items():
        for label, activity in module["activities"].items():
            # if activity["kind"] != "lunch":
            #     activities_ends.append(activity["model"]["end"])
            start = activity["model"]["start"]
            end = activity["model"]["end"]
            #duration = end - start
            duration = activity["duration"]
            for group in students_groups[activity["students"]]:
                total_activities_duration[group] += duration 
            week = model.NewIntVar(0, 100, "makespan")
            model.AddDivisionEquality(week, start, 672)
            #week_duration[model.getOr ] += duration
            # for i, c in enumerate(week_duration):
            for i in range(MAX_WEEKS):
                is_week = model.NewBoolVar("is_week")
                model.Add(week == i).OnlyEnforceIf(is_week) 
                model.Add(week != i).OnlyEnforceIf(is_week.Not()) 
                duration_on_week = model.NewIntVar(0, 672, "duration_on_week")
                model.Add(duration_on_week == duration ).OnlyEnforceIf(is_week)
                model.Add(duration_on_week == 0).OnlyEnforceIf(is_week.Not())
                #model.Add(duration_on_week == 0 )
                for group in students_groups[activity["students"]]:
                    week_duration[group][i].append(duration_on_week)
    # Remove empty groups:
    week_duration_curated = {}
    for group, wd in week_duration.items():
        l = sum([len(d) for d in wd])
        if l != 0:
            week_duration_curated[group] = wd

    #week_duration_sums = [sum([d for d in wd]) for group, wd in week_duration.items()]
    week_duration_sums = []
    week_duration_residuals = []
    for group, wd in week_duration_curated.items():
        total_duration_per_group = 0
        for nw, w in enumerate(wd):
            if len(w) != 0:
                week_duration_sums.append(sum(w))
                total_duration_per_group += sum(w)
            else:
                week_duration_sums.append(0)
        mean_week_duration = model.NewIntVar(0, 672, f"mean_week_duration_{group}")
        #print(group, wd)
        #print(group, len(wd), total_duration_per_group)
        model.AddDivisionEquality(mean_week_duration, total_activities_duration[group], len(wd))
        for w in wd:
            week_duration = sum(w)
            abs_week_residual = model.NewIntVar(0, 672, "mean_week_duration")
            positive_residual = model.NewBoolVar("mean_week_duration")
            model.Add( week_duration - mean_week_duration >= 0).OnlyEnforceIf(positive_residual)
            model.Add( week_duration - mean_week_duration < 0).OnlyEnforceIf(positive_residual.Not())
            model.Add(abs_week_residual == week_duration - mean_week_duration).OnlyEnforceIf(positive_residual)
            model.Add(abs_week_residual == mean_week_duration - week_duration).OnlyEnforceIf(positive_residual.Not())
            week_duration_residuals.append(abs_week_residual)
    makespan = model.NewIntVar(0, horizon, "makespan")
    model.Add(makespan == sum(week_duration_residuals))
    
    return makespan    
        

# makespan = model.NewIntVar(0, horizon, "makespan")
# #model.AddMaxEquality(makespan, activities_ends)
# #model.AddMaxEquality(makespan, week_duration_sums)
# #makespan = sum([d**2 for d in week_duration_sums])
# model.Add(makespan == sum(week_duration_residuals))
makespan = get_absolute_week_duration_deviation(model, activity_data, students_groups, horizon, MAX_WEEKS=MAX_WEEKS)
model.Minimize(makespan)

# Solve model.
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 3600.0
solver.parameters.num_search_workers = 16
#solver.parameters.log_search_progress = True


solution_printer = SolutionPrinter(limit=400)
t0 = time.time()
status = solver.Solve(model, solution_printer)
t1 = time.time()
print(f"Elapsed time: {t1-t0:.2f} s")

solution = export_solution(
    activity_data,
    model,
    solver,
    students_groups,
    week_structure=WEEK_STRUCTURE,
    start_day=START_DAY,
)
xlsx_path = "outputs/schedule.xlsx"
if not os.path.isdir("./outputs"):
    os.mkdir("outputs")

export_student_schedule_to_xlsx(
    xlsx_path,
    solution,
    students_groups,
    week_structure=WEEK_STRUCTURE,
    row_height=15,
    column_width=25,
)
# MODULES
writer = pd.ExcelWriter(f"outputs/modules_activities.xlsx", engine="xlsxwriter")
unique_modules = solution.module.unique()
unique_modules.sort()
for module in unique_modules:
    module_solution = solution[solution.module == module].sort_values(["start"])
    module_solution = module_solution[
        [
            "label",
            "week",
            "weekday",
            "weekdayname",
            "starttime",
            "endtime",
            "kind",
            "students",
            "teachers",
            "rooms",
            "year",
            "month",
            "day",
            "daystart",
            "dayend",
        ]
    ]
    sheet_name = f"{module}"
    module_solution.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
    worksheet = writer.sheets[sheet_name]
    workbook = writer.book
    my_format = workbook.add_format(
        {"align": "center", "valign": "vcenter", "border": 0, "font_size": 11}
    )
    worksheet.set_column("A:A", 50, my_format)
    worksheet.set_column("B:G", 12, my_format)
    worksheet.set_column("H:H", 20, my_format)
    worksheet.set_column("I:J", 70, my_format)
    worksheet.set_column("K:N", 12, my_format)

if not os.path.isdir("./outputs"):
    os.mkdir("outputs")

writer.close()

# MODULES PLANIFICATION
writer = pd.ExcelWriter("outputs/modules_activities_planification.xlsx", engine="xlsxwriter")
unique_modules = solution.module.unique()
unique_modules.sort()

for module in unique_modules:
    module_solution = solution[solution.module == module].sort_values(["kind", "start"])
    module_solution = module_solution[
        [
            "label",
            "week",
            "weekday",
            "weekdayname",
            "starttime",
            "endtime",
            "kind",
            "students",
            "teachers",
            "rooms",
            "year",
            "month",
            "day",
            "daystart",
            "dayend",
        ]
    ]
    sheet_name = f"{module}"
    module_solution.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
    worksheet = writer.sheets[sheet_name]
    workbook = writer.book
    my_format = workbook.add_format(
        {"align": "center", "valign": "vcenter", "border": 0, "font_size": 11}
    )
    worksheet.set_column("A:A", 50, my_format)
    worksheet.set_column("B:G", 12, my_format)
    worksheet.set_column("H:H", 20, my_format)
    worksheet.set_column("I:J", 30, my_format)
    worksheet.set_column("K:N", 12, my_format)

writer.close()


# RESSOURCES
for ressources in ["teachers", "rooms"]:
    writer = pd.ExcelWriter(
        f"outputs/{ressources}_activities.xlsx", engine="xlsxwriter"
    )
    unique_ressources = np.unique(np.concatenate(solution[ressources].values))
    unique_ressources.sort()

    for ressource in unique_ressources:
        loc = solution[ressources].apply(lambda a: np.isin(ressource, a))
        ressource_solution = solution[loc].sort_values(["start"])
        ressource_solution = ressource_solution[
            [
                "module",
                "label",
                "week",
                "weekday",
                "weekdayname",
                "starttime",
                "endtime",
                "kind",
                "students",
                "teachers",
                "rooms",
                "year",
                "month",
                "day",
                "daystart",
                "dayend",
            ]
        ]
        sheet_name = f"{ressource}"
        ressource_solution.to_excel(
            writer, sheet_name=sheet_name, index=False, startrow=1
        )
        worksheet = writer.sheets[sheet_name]
        workbook = writer.book
        my_format = workbook.add_format(
            {"align": "center", "valign": "vcenter", "border": 0, "font_size": 11}
        )
        worksheet.set_column("A:A", 20, my_format)
        worksheet.set_column("B:B", 50, my_format)
        worksheet.set_column("C:H", 12, my_format)
        worksheet.set_column("I:I", 20, my_format)
        worksheet.set_column("J:K", 70, my_format)
        worksheet.set_column("L:N", 12, my_format)
        nrows = ressource_solution.shape[0] +2
        tag = f"A2:P{nrows}"
        worksheet.autofilter(tag)
        
    writer.close()
