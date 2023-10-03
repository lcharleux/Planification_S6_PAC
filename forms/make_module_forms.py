import yaml
from scheduling_forms.core import make_modules_forms
import os

eval_activities = ["cc", "ct", "ci", "et"]

groups = {
    "MM4": {
        "cm": ["MM4"],
        "td": ["MM4-" + g for g in list("ABC")],
        "tp": [
            "MM4-" + g
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
    "SNI4": {
        "cm": ["SNI4"],
        "td": ["SNI4-E"],
        "tp": [
            "SNI4-E1",
            "SNI4-E2",
        ],
    },
    "IDU4": {
        "cm": ["IDU4"],
        "td": ["IDU4-G"],
        "tp": [
            "IDU4-G1",
            "IDU4-G2",
        ],
    },
    "IDU4-SNI4": {
        "cm": ["IDU4-SNI4"],
        "td": ["IDU4-G", "SNI4-E"],
        "tp": [
            "IDU4-G1",
            "IDU4-G2",
            "SNI4-E1",
            "SNI4-E2",
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
make_modules_forms(data, groups, rooms, eval_activities, root_path=root_path)
