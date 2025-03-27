import string

dictionnaire = {f"KEY_{lettre}": lettre for lettre in string.ascii_uppercase}
print(dictionnaire)