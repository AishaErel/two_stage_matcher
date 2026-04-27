import pandas as pd

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
gt.to_csv("ground_truth_1.csv", index=False)

print("Created ground_truth_1.csv")