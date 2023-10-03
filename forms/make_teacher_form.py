# MAKE TEACHER FORM
import xlsxwriter
import numpy as np

workbook = xlsxwriter.Workbook("Indisponibilites_Enseignant_NOM_PRENOM.xlsx")

static_data_format = workbook.add_format(
    {
        "bold": True,
        "font_color": "black",
        "align": "center",
        "valign": "vcenter",
        "bg_color": "#C0C0C0",
    }
)
must_complete_format = workbook.add_format(
    {
        "bold": False,
        "font_color": "black",
        "align": "center",
        "valign": "vcenter",
        "bg_color": "#FF6600",
    }
)
completed_format = workbook.add_format(
    {
        "bold": False,
        "font_color": "black",
        "align": "center",
        "valign": "vcenter",
        "bg_color": "#99CC00",
    }
)
optional_format = workbook.add_format(
    {
        "bold": False,
        "font_color": "black",
        "align": "center",
        "valign": "vcenter",
        "bg_color": "#FFCC00",
    }
)
do_not_fill_format = workbook.add_format(
    {
        "bold": False,
        "font_color": "#FFCC00",
        "align": "center",
        "valign": "vcenter",
        "bg_color": "#808080",
    }
)

my_email = "ludovic.charleux@univ-smb.fr"
allowed_weeks = np.arange(4, 23).tolist()
allowed_days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
allowed_hours = np.concatenate(
    [[f"{h}:{m}".zfill(5) for m in ["00", "30", ]] for h in range(8, 20)]
).tolist()
repetitions = ["Aucune", "Toutes les semaines", "Tous les jours"]

worksheet = workbook.add_worksheet("Mode Emploi")
worksheet.write(0, 0, "Etape 1", static_data_format)
worksheet.write(
    0, 1, "Remplir les cellules oranges dans chaque onglet", static_data_format
)
worksheet.write(1, 0, "Etape 2", static_data_format)
worksheet.write(
    1, 1, "Remplir les cellules jaunes si besoin dans chaque onglet", static_data_format
)
worksheet.write(2, 0, "Etape 3", static_data_format)
worksheet.write(2, 1, f"Renvoyer cette feuille (une seule fois) à:", static_data_format)
worksheet.write_url(
    2,
    2,
    f"external:mailto:{my_email}?subject=[Indisponibilités] Nom Prénom",
    string=my_email,
)


worksheet.set_column(0, 0, width=20)
worksheet.set_column(1, 1, width=100)


worksheet = workbook.add_worksheet("Données")
worksheet.write(0, 0, "Nom", static_data_format)
worksheet.write(1, 0, "Prénom", static_data_format)
worksheet.write(2, 0, "E-mail", static_data_format)
worksheet.write(3, 0, "Tel.", static_data_format)
worksheet.set_column(0, 0, width=20)
worksheet.set_column(1, 1, width=100)

worksheet.conditional_format(
    f"B1:B4",
    {"type": "blanks", "format": must_complete_format},
)
worksheet.conditional_format(
    f"B1:B4",
    {"type": "no_blanks", "format": completed_format},
)


worksheet = workbook.add_worksheet("Indisponibilités")
worksheet.merge_range(
    "A1:C1",
    "Indisponible depuis:",
    static_data_format,
)
worksheet.merge_range(
    "D1:F1",
    "Et jusqu'à:",
    static_data_format,
)
for i in range(2):
    worksheet.write(1, 3 * i, "Semaine", static_data_format)
    worksheet.write(1, 3 * i + 1, "Jour", static_data_format)
    worksheet.write(1, 3 * i + 2, "Heure", static_data_format)
worksheet.write(1, 6, "Répétition ?", static_data_format)

worksheet.set_column(0, 5, width=10)
worksheet.set_column(6, 6, width=20)

worksheet.conditional_format(
    f"A3:G100",
    {"type": "blanks", "format": optional_format},
)
worksheet.conditional_format(
    f"A3:G100",
    {"type": "no_blanks", "format": completed_format},
)

for i in range(2):
    worksheet.data_validation(
        2,3*i,100,3*i,
        {
            "validate": "list",
            "source": allowed_weeks,
            "input_message": "Numéro de semaine",
        },
    )
    worksheet.data_validation(
        2,3*i+1,100,3*i+1,
        {
            "validate": "list",
            "source": allowed_days,
            "input_message": "Jour de la semaine",
        },
    )
    worksheet.data_validation(
        2,3*i+2,100,3*i+2,
        {
            "validate": "list",
            "source": allowed_hours,
            "input_message": "Heure",
        },
    )
worksheet.data_validation(
    2,6,100,6,
    {
        "validate": "list",
        "source": repetitions,
        "input_message": "Voulez vous répéter cette indisponiblité plusieurs fois ?",
    },
)    
workbook.close()
