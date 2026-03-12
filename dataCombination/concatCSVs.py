import pandas as pd

new_students = pd.read_csv("csvfiles/sepCSVfiles/new.csv", encoding="utf-8")
graduates = pd.read_csv("csvfiles/sepCSVfiles/graduated.csv", encoding="utf-8")
# enrolled = pd.read_csv("csvfiles/sepCSVfiles/enrolled.csv", encoding="utf-8")

new_students["حالة_الطالب"] = "مستجد"
graduates["حالة_الطالب"] = "خريج"
# enrolled["حالة_الطالب"] = "مقيد"

# dataset = pd.concat([new_students, graduates, enrolled])
dataset = pd.concat([new_students, graduates])

dataset.to_csv("csvfiles/final_dataset_noenro.csv", encoding="utf-8", index=False)