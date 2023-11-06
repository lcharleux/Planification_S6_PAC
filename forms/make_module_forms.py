import yaml
from scheduling_forms.core import make_modules_forms, export_emails
import os
import pandas as pd

eval_activities = ["cc", "ct", "ci", "et"]

groups = {
    "MM3": {
        "cm": ["MM3"],
        "td": ["MM3-" + g for g in list("ABC")],
        "tp": [
            "MM3-" + g
            for g in [
                "A1",
                "A2",
                "B1",
                "B2",
                "C1",
                "C2",
            ]
        ],
    },
    "SNI3": {
        "cm": ["SNI3"],
        "td": ["SNI3-E"],
        "tp": [
            "SNI3-E1",
            # "SNI3-E2",
        ],
    },
    "IDU3": {
        "cm": ["IDU3"],
        "td": ["IDU3-G"],
        "tp": [
            "IDU3-G1",
            "IDU3-G2",
        ],
    },
    "IDU3-SNI3": {
        "cm": ["IDU3-SNI3"],
        "td": ["IDU3-G", "SNI3-E"],
        "tp": [
            "IDU3-G1",
            "IDU3-G2",
            "SNI3-E1",
            # "SNI3-E2",
        ],
    },
    "TC": {
        "cm": ["IDU3-SNI3-MM3"],
        "td": ["IDU3-G", "SNI3-E", "MM3-A", "MM3-B", "MM3-C"],
        "tp": [
            "IDU3-G1",
            "IDU3-G2",
            "SNI3-E1",
            # "SNI3-E2",
        ] + 
        [
            "MM3-" + g
            for g in [
                "A1",
                "A2",
                "B1",
                "B2",
                "C1",
                "C2",
            ]
        ],
    },
}

rooms = [
    "Amphi",
    "Amphi x2",
    "TD",
    "Info",
    "Info (Grande)",
    "Info (Partagée)",
    "Gymnase",
    "TP-A202",
    "TP-B104",
    "TP-C114",
    "TP-C115",
    "TP-C117",
    "TP-C119",
    "TP-C120",
    "TP-C121",
]


data = yaml.load(open("mccc.yml"), Loader=yaml.FullLoader)
root_path="generated_forms/"
if not os.path.exists(root_path):
    os.makedirs(root_path)
make_modules_forms(data, groups, rooms, eval_activities, year="2324", root_path=root_path)


# E-mails
emails_file = "managers_emails.txt"
emails = export_emails(data)
with open(emails_file, "w") as out:
    out.write(emails)

# Tabular output
out = {"module":[], "responsable":[], "spécialité":[]}

for module, mdata in data.items():
    out["module"].append(module)
    out["responsable"].append(mdata["responsable"])
    out["spécialité"].append(mdata["specialite"])

out = pd.DataFrame(out).sort_values(["spécialité", "module"]).set_index("module")
out.columns = [s.capitalize() for s in out.columns]
out.to_html("managers.html")