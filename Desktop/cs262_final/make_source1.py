import pandas as pd

df = pd.read_csv("healthcare.csv")

df_source = df.copy() #takes the same data but creates different column names

df_source.columns = [
    "Patient_Name",
    "Patient_Age",
    "Sex",
    "Blood_Group",
    "Condition",
    "Adm_Date",
    "Physician",
    "Hospital_Name",
    "Insurer",
    "Total_Charge",
    "Room_No",
    "Admission_Category",
    "Discharge_Date",
    "Drug",
    "Lab_Results"
]

df_source.to_csv("source_1.csv", index=False)

print("Created source_1.csv")