# script used to combine data of all csv files into one csv output file 
import os
import pandas as pd

input_dir = r"C:\Users\Tanisha Iyer\Desktop\corporate comp\2023"    # put desired input file directory here  
output_file = os.path.join(input_dir, "2023_combined.csv")   # desired output file here 

dfs = []

for file in os.listdir(input_dir):
    if file.endswith(".csv"):
        filepath = os.path.join(input_dir, file)
        df = pd.read_csv(filepath)
        dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined data to a new CSV file
combined_df.to_csv(output_file, index=False)
