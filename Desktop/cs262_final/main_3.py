import pandas as pd

df = pd.read_csv("healthcare.csv")
print(df.columns)
df_source3 = df.copy()

# Change values
df_source3["Gender"] = df_source3["Gender"].replace({
    "Male": "M",
    "Female": "F"
})

df_source3["Blood Type"] = df_source3["Blood Type"].str.replace("+", " Positive")

# Rename columns differently
df_source3.columns = [
    "Name",
    "Age",
    "Sex",
    "BloodGroup",
    "Condition",
    "AdmissionDate",
    "DoctorName",
    "Hospital",
    "Insurance",
    "Charge",
    "Room",
    "Type",
    "DischargeDate",
    "Medication",
    "Results"
]
df_source3.to_csv("source_3.csv", index=False)


mapping3 = {
    "Name": "Name",
    "Age": "Age",
    "Sex": "Gender",
    "BloodGroup": "Blood Type",
    "Condition": "Medical Condition",
    "AdmissionDate": "Date of Admission",
    "DoctorName": "Doctor",
    "Hospital": "Hospital",
    "Insurance": "Insurance Provider",
    "Charge": "Billing Amount",
    "Room": "Room Number",
    "Type": "Admission Type",
    "DischargeDate": "Discharge Date",
    "Medication": "Medication",
    "Results": "Test Results"
}

gt3 = pd.DataFrame(list(mapping3.items()), columns=["source", "target"])
gt3.to_csv("ground_truth_3.csv", index=False)

print(gt3)


