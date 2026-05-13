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

def __processHealthcareData(
    tgt_mapping: dict[str, str],
    healthcare_csv: str,
    output_csv: str,
    random_id: bool = False,
    n_distractors: int = 0
) -> None:

    healthcare_df = pd.read_csv(healthcare_csv)
    healthcare_df.rename(columns=tgt_mapping, inplace=True)

    if random_id:
        healthcare_df["Random_ID"] = range(len(healthcare_df))

    if n_distractors > 0:
        healthcare_df = add_distractor_columns(healthcare_df, n_extra=n_distractors)

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

def add_distractor_columns(df: pd.DataFrame, n_extra: int = 50) -> pd.DataFrame:
    df = df.copy()
    n = len(df)

    for i in range(n_extra):
        if i % 5 == 0:
            df[f"Fake_Numeric_{i}"] = range(n)

        elif i % 5 == 1:
            values = (["A", "B", "C", "D"] * ((n // 4) + 1))[:n]
            df[f"Fake_Category_{i}"] = values

        elif i % 5 == 2:
            df[f"Fake_Text_{i}"] = [f"text_{j % 10}" for j in range(n)]

        elif i % 5 == 3:
            df[f"Fake_Date_{i}"] = pd.date_range("2020-01-01", periods=n, freq="D").astype(str)

        else:
            df[f"Fake_ID_{i}"] = [f"ID_{j}" for j in range(n)]

    return df
def generateWideTarget(n_distractors: int = 100) -> None:
    target_df = pd.read_csv("healthcare.csv")
    target_wide = add_distractor_columns(target_df, n_extra=n_distractors)
    target_wide.to_csv("target_wide.csv", index=False)
def initialGeneration() -> None:
    __ground_truth_headers: list[str] = ["source", "target"]

    __processHealthcareData(__TRUTH_MAPPING_1, "healthcare.csv", "source_1.csv")
    __generateGroundTruth(__TRUTH_MAPPING_1, __ground_truth_headers, "ground_truth_1.csv")

    __processHealthcareData(__TRUTH_MAPPING_2, "healthcare.csv", "source_2.csv", random_id=True)
    __generateGroundTruth(__TRUTH_MAPPING_2, __ground_truth_headers, "ground_truth_2.csv")

    __processHealthcareData(__TRUTH_MAPPING_3, "healthcare.csv", "source_3.csv")
    __generateGroundTruth(__TRUTH_MAPPING_3, __ground_truth_headers, "ground_truth_3.csv")

    generateWideTarget(n_distractors=100)

if __name__ == "__main__":
    initialGeneration()
