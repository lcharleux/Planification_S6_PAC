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
from automatic_university_scheduler.scheduling import (
    read_json_data,
    get_unique_teachers_and_rooms,
    create_unavailable_constraints,
    create_weekly_unavailable_intervals,
    SolutionPrinter,
    export_solution,
    get_atomic_students_groups,
    DAYS_NAMES,
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
MAX_WEEKS = 80
TIME_SLOTS_PER_WEEK = TIME_SLOTS_PER_DAY * DAYS_PER_WEEK
horizon = MAX_WEEKS * TIME_SLOTS_PER_WEEK
START_DAY = datetime.date.fromisocalendar(2023, 1, 1)
STOP_DAY = START_DAY + datetime.timedelta(
    weeks=MAX_WEEKS
)

# ACTIVITY GENERATION

print("Horizon = %i" % horizon)

activity_data_dir = "activity_data/"
teacher_data_dir = "teacher_data/"
room_data_dir = "room_data/"
student_data_dir = "student_data/"
teacher_data = read_json_data(teacher_data_dir)
activity_data = read_json_data(activity_data_dir)  # , contains="Meca501")
room_data = read_json_data(room_data_dir)
calendar_data = read_json_data(student_data_dir)


# STUDENTS GROUPS
students_groups = {
    "EPU-3-S6": [
        "MM-3-A1",
        "MM-3-A2",
        "MM-3-B1",
        "MM-3-B2",
        "MM-3-C1",
        "MM-3-C2",
        "SNI-3-D1",
        "SNI-3-D2",
        "IDU-3-G1",
        "IDU-3-G2",
    ],
    "MM-3": ["MM-3-A1", "MM-3-A2", "MM-3-B1", "MM-3-B2", "MM-3-C1", "MM-3-C2"],
    "SNI-3": ["SNI-3-D1", "SNI-3-D2"],
    "IDU-3": ["IDU-3-G1", "IDU-3-G2"],
    "IDU-3_SNI-3": ["IDU-3-G1", "IDU-3-G2","SNI-3-D1", "SNI-3-D2"], # POUR LES MATH641
    "MM-3-A-TD": ["MM-3-A1", "MM-3-A2"],
    "MM-3-B-TD": ["MM-3-B1", "MM-3-B2"],
    "MM-3-C-TD": ["MM-3-C1", "MM-3-C2"],
    "SNI-3-D-TD": ["SNI-3-D1", "SNI-3-D2"],
    "IDU-3-G-TD": ["IDU-3-G1", "IDU-3-G2"],
    "MM-3-A1": ["MM-3-A1"],
    "MM-3-A2": ["MM-3-A2"],
    "MM-3-B1": ["MM-3-B1"],
    "MM-3-B2": ["MM-3-B2"],
    "MM-3-C1": ["MM-3-C1"],
    "MM-3-C2": ["MM-3-C2"],
    "SNI-3-D1": ["SNI-3-D1"],
    "SNI-3-D2": ["SNI-3-D2"],
    "IDU-3-G1": ["IDU-3-G1"],
    "IDU-3-G2": ["IDU-3-G2"],
}


model = cp_model.CpModel()

# TEACHER UNAVAILABILITY
teacher_unavailable_intervals = create_unavailable_constraints(
    model, data=teacher_data, start_day=START_DAY, horizon=horizon
)
# ROOM UNAVAILABILITY
room_unavailable_intervals = create_unavailable_constraints(
    model, data=room_data, start_day=START_DAY, horizon=horizon
)

# NIGHT SHIFTS & LUNCH BREAKS AND WEEK-ENDS!
weekly_unavailable_intervals = create_weekly_unavailable_intervals(
    model, WEEK_STRUCTURE, MAX_WEEKS
)

# STUDENT CALENDAR
students_unavailable_intervals = create_unavailable_constraints(
    model, data=calendar_data, start_day=START_DAY, horizon=horizon
)


create_activities(
    activity_data,
    model,
    students_groups,
    horizon=horizon,
    teacher_unavailable_intervals=teacher_unavailable_intervals,
    room_unavailable_intervals=room_unavailable_intervals,
    students_unavailable_intervals=students_unavailable_intervals,
    weekly_unavailable_intervals=weekly_unavailable_intervals,
    cm_td_allowed_slots = [32, 39, 46, 53, 60, 67]
)

# MINIMIZE SEMESTER DURATION
# Makespan objective
activities_ends = []
for file, module in activity_data.items():
    for label, activity in module["activities"].items():
        if activity["kind"] != "lunch":
            activities_ends.append(activity["model"]["end"])

makespan = model.NewIntVar(0, horizon, "makespan")
model.AddMaxEquality(makespan, activities_ends)
model.Minimize(makespan)

# Solve model.
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 300.0


solution_printer = SolutionPrinter(limit=10)
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
    module_solution = module_solution[["label", "week", "weekday", "weekdayname", "starttime", "endtime", "kind", "students", "teachers", "rooms", "year", "month", "day", "daystart", "dayend"]]
    sheet_name = f"{module}"
    module_solution.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
    worksheet = writer.sheets[sheet_name]
    workbook = writer.book
    my_format = workbook.add_format(
        {"align": "center", "valign": "vcenter", "border": 0, "font_size": 11}
    )
    worksheet.set_column('A:A', 50, my_format)
    worksheet.set_column('B:G', 12, my_format)
    worksheet.set_column('H:H', 20, my_format)
    worksheet.set_column('I:J', 70, my_format)
    worksheet.set_column('K:N', 12, my_format)

writer.close()    

# RESSOURCES
for ressources in ["teachers", "rooms"]:
    writer = pd.ExcelWriter(f"outputs/{ressources}_activities.xlsx", engine="xlsxwriter")
    unique_ressources = np.unique(np.concatenate(solution[ressources].values))
    unique_ressources.sort()
    for ressource in unique_ressources:
        loc = solution[ressources].apply(lambda a: ressource in a)
        ressource_solution = solution[loc].sort_values(["start"])
        ressource_solution = ressource_solution[["module", "label", "week", "weekday", "weekdayname", "starttime", "endtime", "kind", "students", "teachers", "rooms", "year", "month", "day", "daystart", "dayend"]]
        sheet_name = f"{ressource}"
        ressource_solution.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
        worksheet = writer.sheets[sheet_name]
        workbook = writer.book
        my_format = workbook.add_format(
            {"align": "center", "valign": "vcenter", "border": 0, "font_size": 11}
        
        )
        worksheet.set_column('A:A', 20, my_format)
        worksheet.set_column('B:B', 50, my_format)
        worksheet.set_column('C:H', 12, my_format)
        worksheet.set_column('I:I', 20, my_format)
        worksheet.set_column('J:K', 70, my_format)
        worksheet.set_column('L:N', 12, my_format)

    writer.close()  