import pandas as pd

df = pd.read_csv("healthcare.csv")
print(df.columns)
df_source2 = df.copy()

df_source2.columns = [
    "Nm",
    "Age_yrs",
    "Gndr",
    "Bld_Type",
    "Med_Cond",
    "AdmDt",
    "Dr_Name",
    "Hosp",
    "InsuranceCo",
    "Bill_Amt",
    "Rm_No",
    "Adm_Type",
    "Dschg_Dt",
    "Med",
    "Test_Out"
]

# Add noise column (IMPORTANT for realism)
df_source2["Random_ID"] = range(len(df_source2))

df_source2.to_csv("source_2.csv", index=False)