## Import Standard Libraries
import pandas as pd

## Import Local Libraries
import model.resource as resource
__TRUTH_MAPPING_1:dict[str, str] = {
    "Name": "Patient_Name",
    "Age": "Patient_Age",
    "Gender": "Sex",
    "Blood Type": "Blood_Group",
    "Medical Condition": "Condition",
    "Date of Admission": "Adm_Date",
    "Doctor": "Physician",
    "Hospital": "Hospital_Name",
    "Insurance Provider": "Insurer",
    "Billing Amount": "Total_Charge",
    "Room Number": "Room_No",
    "Admission Type": "Admission_Category",
    "Discharge Date": "Discharge_Date",
    "Medication": "Drug",
    "Test Results": "Lab_Results"
}

__TRUTH_MAPPING_2:dict[str, str] = {
    "Name": "Nm",
    "Age": "Age_yrs",
    "Gender": "Gndr",
    "Blood Type": "Bld_Type",
    "Medical Condition": "Med_Cond",
    "Date of Admission": "AdmDt",
    "Doctor": "Dr_Name",
    "Hospital": "Hosp",
    "Insurance Provider": "InsuranceCo",
    "Billing Amount": "Bill_Amt",
    "Room Number": "Rm_No",
    "Admission Type": "Adm_Type",
    "Discharge Date": "Dschg_Dt",
    "Medication": "Med",
    "Test Results": "Test_Out"
}

__TRUTH_MAPPING_3:dict[str, str] = {
    "Name": "Name",
    "Age": "Age",
    "Gender": "Sex",
    "Blood Type": "BloodGroup",
    "Medical Condition": "Condition",
    "Date of Admission": "AdmissionDate",
    "Doctor": "DoctorName",
    "Hospital": "Hospital",
    "Insurance Provider": "Insurance",
    "Billing Amount": "Charge",
    "Room Number": "Room",
    "Admission Type": "Type",
    "Discharge Date": "DischargeDate",
    "Medication": "Medication",
    "Test Results": "Results"
}

def processHealthcareData(tgt_mapping:dict[str, str], healthcare_csv:str, output_csv:str, random_id:bool=False) -> None:
    ##  hard-column alternative
    # healthcare_df = pd.read_csv(healthcare_csv, names=list(__CONST_TRUTH_MAPPING.keys()), header=0)
    
    ##  dynamic-column mapping
    healthcare_df = pd.read_csv(healthcare_csv)
    try:
        healthcare_df.rename(columns=tgt_mapping, inplace=True)
    except KeyError as e:
        print(f"Column not found in healthcare data: {e}")

    if random_id:
        healthcare_df["Random_ID"] = range(len(healthcare_df))

    healthcare_df.to_csv(output_csv, index=False)

def generateGroundTruth(tgt_mapping:dict[str, str], header_names:list[str], output_csv:str) -> None:
    mapped_df:pd.DataFrame = pd.DataFrame(list(tgt_mapping.items()), columns=header_names)
    mapped_df.to_csv(output_csv, index=False)

def main():
    __ground_truth_headers:list[str] = ["source", "target"]

    ##  mapping 1
    processHealthcareData(__TRUTH_MAPPING_1, resource.getDataFile("healthcare.csv"), resource.getDataFile("source_1.csv"))
    generateGroundTruth(__TRUTH_MAPPING_1, __ground_truth_headers, resource.getDataFile("ground_truth_1.csv"))

    ##  mapping 2
    processHealthcareData(__TRUTH_MAPPING_2, resource.getDataFile("healthcare.csv"), resource.getDataFile("source_2.csv"), random_id=True)

    ##  mapping 3
    processHealthcareData(__TRUTH_MAPPING_3, resource.getDataFile("healthcare.csv"), resource.getDataFile("source_3.csv"))
    generateGroundTruth(__TRUTH_MAPPING_3, __ground_truth_headers, resource.getDataFile("ground_truth_3.csv"))



if __name__ == "__main__":
    main()