##  Import Standard Libraries
import pandas as pd

# ##  Import Local Libraries
# import model.resource as resource

##  Mapping dictionaries for column-header equivalency.  
##      Used to generate sources and truths.

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

def __processHealthcareData(tgt_mapping:dict[str, str], healthcare_csv:str, output_csv:str, random_id:bool=False) -> None:
    """
        Takes the inputted `heathcare_csv` file and remaps the column header names to the values in tgt_mapping.  
        Writes this file to `output_csv`.

        If `random_id` is specified, then a "Random_ID" column is included
    """
    ##  hard-column alternative
    # healthcare_df = pd.read_csv(healthcare_csv, names=list(__CONST_TRUTH_MAPPING.keys()), header=0)
    
    ##  dynamic-column mapping
    healthcare_df = pd.read_csv(healthcare_csv)
    try:
        healthcare_df.rename(columns=tgt_mapping, inplace=True)
    except KeyError as e:
        print(f"Column not found in healthcare data: {e}")

    ##  add "Random_ID" column
    ##  TODO:: maybe change to avoid collision?
    if random_id:
        healthcare_df["Random_ID"] = range(len(healthcare_df))

    ##  output to desired file
    healthcare_df.to_csv(output_csv, index=False)
def __generateGroundTruth(tgt_mapping: dict[str, str], header_names: list[str], output_csv: str) -> None:
    """
    Creates a ground truth CSV in the form:
        source,target
        source_column,target_column
    by reversing the original mapping dictionary.

    Example:
        "Name": "Patient_Name"
    becomes:
        "Patient_Name": "Name"
    """
    reversed_mapping = {v: k for k, v in tgt_mapping.items()}
    mapped_df = pd.DataFrame(list(reversed_mapping.items()), columns=header_names)
    mapped_df.to_csv(output_csv, index=False)

def initialGeneration() -> None:
    """
        Generates all initial database `.csv` files to be used.
            -   `source_1.csv`
            -   `source_2.csv`
            -   `source_3.csv`
            -   `ground_truth_1.csv`
            -   `ground_truth_2.csv`
            -   `ground_truth_3.csv`

        Uses `__processHealthcareData()` and `__generateGroundTruth()`.
    """
    __ground_truth_headers:list[str] = ["source", "target"]

    ##  mapping 1
    __processHealthcareData(__TRUTH_MAPPING_1, ("healthcare.csv"), ("source_1.csv"))
    __generateGroundTruth(__TRUTH_MAPPING_1, __ground_truth_headers, ("ground_truth_1.csv"))

    ##  mapping 2
    __processHealthcareData(__TRUTH_MAPPING_2, ("healthcare.csv"), ("source_2.csv"), random_id=True)
    ##  handle `random_state` column too?
    __generateGroundTruth(__TRUTH_MAPPING_2, __ground_truth_headers,("ground_truth_2.csv"))

    ##  mapping 3
    __processHealthcareData(__TRUTH_MAPPING_3, ("healthcare.csv"), ("source_3.csv"))
    __generateGroundTruth(__TRUTH_MAPPING_3, __ground_truth_headers, ("ground_truth_3.csv"))
