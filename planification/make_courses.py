import os

makers_dir = "course_makers"
makers = sorted([f for f in os.listdir(makers_dir) if f.endswith(".py")])
for maker in makers:
    print(f"Runnning: {maker}")
    os.system(f"cd {makers_dir} && python {maker}")
