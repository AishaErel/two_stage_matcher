import pandas as pd

df = pd.read_csv("healthcare.csv")
print(df.columns)

df_source = df.copy()

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

df_source.to_csv("source_1.csv", index=False) #source_1 file has the same patient info with different column names (gender = sex etc)

mapping = {
    "Patient_Name": "Name",
    "Patient_Age": "Age",
    "Sex": "Gender",
    "Blood_Group": "Blood Type",
    "Condition": "Medical Condition",
    "Adm_Date": "Date of Admission",
    "Physician": "Doctor",
    "Hospital_Name": "Hospital",
    "Insurer": "Insurance Provider",
    "Total_Charge": "Billing Amount",
    "Room_No": "Room Number",
    "Admission_Category": "Admission Type",
    "Discharge_Date": "Discharge Date",
    "Drug": "Medication",
    "Lab_Results": "Test Results"
}

gt = pd.DataFrame(list(mapping.items()), columns=["source", "target"])
gt.to_csv("ground_truth.csv", index=False)