import streamlit as st
import pandas as pd
import plotly.express as px
# Markdown header with title and short description
header = """
# ALS Clinical Trials Dashboard

This dashboard displays the results of a clinical trial studying the effects of a new treatment on ALS patients. 
We are monitoring mobility improvements over the course of the trial, taking into account factors such as 
family history, prior health issues, and placebo group status. 

Scroll down to view detailed patient data and overall trial results.

[Go to Data Dictionary](#data-dictionary)
"""
# Column names
# Display the header in the app
st.markdown(header)
columns = [
    'Patient_ID', 'Placebo', 'Family_History', 'Prior_Serious_Health_Issues', 'Sex', 'Height_in_inches',
    'Weight_in_pounds', 'Smoker', 'Diagnosis_Length_months', 'Pre_Mobility', 'BMI', 'January_mobility',
    'February_mobility', 'March_mobility', 'April_mobility', 'May_mobility', 'June_mobility', 'July_mobility',
    'August_mobility', 'September_mobility', 'October_mobility', 'November_mobility', 'December_mobility',
    'Trial_Avg_Mobility', 'Improvement'
]

# Existing data for the first 10 patients
data = [
    ['LMWDSTNFR', 1, 1, 0, 0, 63, 226, 1, 34, 3, 40.03, 5, 1, 5, 3, 7, 7, 4, 3, 6, 6, 4, 3, 4.5, 1],
    ['JGNU4WIGI', 0, 0, 0, 1, 68, 243, 0, 48, 6, 36.94, 10, 8, 1, 4, 9, 7, 1, 4, 5, 8, 5, 10, 6.0, 0],
    ['MM7AQTTPW', 0, 0, 0, 1, 74, 181, 0, 40, 10, 23.24, 7, 8, 6, 1, 4, 8, 7, 6, 10, 4, 10, 7, 6.5, 0],
    ['3A2NBUNOU', 1, 0, 1, 0, 62, 157, 1, 44, 9, 28.71, 10, 10, 9, 6, 2, 2, 6, 8, 5, 2, 1, 9, 5.833333333333333, 0],
    ['ET7B8RRFE', 0, 0, 0, 0, 61, 121, 1, 50, 7, 22.86, 5, 3, 8, 3, 3, 6, 8, 9, 1, 5, 7, 6, 5.333333333333333, 0],
    ['BZ25TS3MI', 1, 1, 0, 0, 74, 237, 1, 7, 9, 30.43, 7, 5, 9, 10, 2, 10, 2, 4, 5, 2, 5, 4, 5.416666666666667, 0],
    ['7QJK388YZ', 0, 1, 1, 1, 67, 271, 1, 56, 9, 42.44, 1, 9, 8, 3, 9, 5, 2, 3, 9, 3, 3, 6, 5.083333333333333, 0],
    ['PGQSPP2F3', 0, 1, 0, 0, 61, 172, 0, 33, 4, 32.5, 4, 6, 6, 8, 3, 5, 1, 10, 8, 10, 1, 7, 5.75, 1],
    ['38TKY6II9', 1, 1, 1, 0, 59, 188, 1, 50, 2, 37.97, 3, 2, 5, 6, 2, 9, 2, 5, 7, 9, 5, 3, 4.833333333333333, 1],
    ['JG44G1GWL', 0, 1, 0, 1, 56, 240, 0, 17, 1, 53.8, 3, 8, 2, 3, 5, 4, 7, 9, 10, 1, 2, 8, 5.166666666666667, 1],
]

# Additional data (patients 11-100)
data_string = '''
1UBZU12R1,0,1,1,1,72,128,0,19,10,17.36,1,1,10,7,5,8,8,5,4,10,10,10,6.583333333333333,0
DNN1654MS,1,1,0,1,79,182,1,46,9,20.5,4,8,3,9,3,3,6,8,8,5,2,8,5.583333333333333,0
DMCG7SBD3,1,0,0,0,61,192,1,36,8,36.27,10,6,9,3,8,2,3,10,1,3,1,3,4.916666666666667,0
URVCR84JM,0,1,1,1,78,204,1,18,9,23.57,1,3,10,9,6,5,6,8,7,7,5,1,5.666666666666667,0
7IBUNIEND,1,1,1,1,66,242,1,23,6,39.06,9,5,5,4,5,3,2,6,3,6,2,5,4.583333333333333,0
ET9AOZD5Q,0,0,0,0,72,192,0,56,9,26.04,9,10,2,5,1,9,10,5,1,7,1,3,5.25,0
41TZYJPI4,1,0,0,1,72,197,0,17,10,26.72,8,7,3,3,8,5,8,1,5,6,6,3,5.25,0
P2V91USTA,1,1,1,0,57,136,1,55,9,29.43,1,5,9,6,8,7,8,1,1,10,3,7,5.5,0
RKBH22ABS,1,1,1,0,63,287,1,2,6,50.83,5,5,1,5,10,3,7,5,3,10,6,2,5.166666666666667,0
CARYNYK8O,1,0,0,0,78,261,0,18,3,30.16,8,4,5,9,6,1,9,8,3,5,2,6,5.5,1
MIBVGFU5H,0,0,0,1,73,149,0,36,5,19.66,5,7,8,5,2,5,2,6,8,3,5,1,4.75,0
VOGYMX3XU,1,0,0,0,69,109,0,11,2,16.09,5,2,5,8,4,1,4,9,1,3,5,1,4.0,1
3RO78OVHU,1,0,0,0,70,253,1,22,10,36.3,1,1,2,1,1,8,1,2,1,3,4,10,2.9166666666666665,0
G7EBR4J48,0,1,1,0,75,165,1,32,4,20.62,3,10,8,2,6,5,2,5,3,4,1,4,4.416666666666667,1
FOPTJ4QHG,1,1,1,0,76,244,0,41,9,29.7,7,9,10,7,9,2,2,1,3,7,9,8,6.166666666666667,0
F6KSGTGHA,0,1,1,1,77,179,1,55,4,21.22,6,5,10,7,5,3,9,3,9,1,5,10,6.083333333333333,1
VX6A2JXO4,0,0,1,0,55,155,0,3,1,36.02,2,1,5,3,8,1,5,5,8,5,5,10,4.833333333333333,1
7JNA24UA1,1,1,0,0,65,243,0,49,9,40.43,7,3,8,3,6,1,1,8,7,5,9,4,5.166666666666667,0
IR9KNYH2K,0,0,1,0,74,217,1,57,0,27.86,9,6,8,4,6,7,8,10,9,2,6,10,7.083333333333333,1
MANQLJKQR,1,0,1,1,59,136,1,28,7,27.47,2,5,7,5,7,5,10,8,4,1,5,3,5.166666666666667,0
MOEQVXZ56,0,1,0,0,64,206,1,38,5,35.36,10,8,7,1,6,4,8,5,4,10,3,1,5.583333333333333,1
L89R1YIKJ,1,0,1,1,57,246,1,38,5,53.23,6,1,7,2,7,5,6,1,2,9,1,8,4.583333333333333,0
NYMBNDWGU,1,0,1,1,68,278,0,5,1,42.27,7,3,5,6,5,7,3,9,2,5,4,4,5.0,1
3HOT1LFPC,0,1,0,1,66,116,0,5,8,18.72,4,3,6,7,4,4,5,6,10,4,1,2,4.666666666666667,0
VTA2WKRO2,1,0,1,0,63,272,1,10,2,48.18,1,10,7,2,4,1,8,5,8,8,8,9,5.916666666666667,1
982SK6A8A,1,1,1,0,58,183,1,14,2,38.24,6,1,4,5,4,10,1,2,2,10,5,8,4.833333333333333,1
2Z2W4F3XZ,0,1,1,0,76,161,0,49,1,19.6,10,5,6,8,7,9,1,1,6,5,3,3,5.333333333333333,1
YHNNIKO7A,0,1,1,1,72,119,0,17,4,16.14,4,9,5,2,5,6,2,7,4,5,5,10,5.333333333333333,1
3SGKD3ZTC,1,0,1,0,65,232,1,27,6,38.6,2,9,9,4,6,8,10,1,8,2,2,1,5.166666666666667,0
1XQB38DPC,1,1,1,0,76,281,0,22,10,34.2,2,8,1,3,3,10,2,9,9,2,5,1,4.583333333333333,0
QUFYUATIK,1,0,0,1,58,165,0,46,4,34.48,8,1,10,3,4,9,4,9,1,4,6,6,5.416666666666667,1
HKPCZTUBI,1,0,0,0,58,261,1,5,9,54.54,7,4,9,1,7,9,10,7,10,1,4,5,6.166666666666667,0
USY24S1J4,1,1,1,1,70,103,0,26,7,14.78,4,8,6,5,8,6,4,3,10,7,10,9,6.666666666666667,0
7WJZPGMAB,1,0,1,1,62,141,1,21,0,25.79,3,6,8,10,8,1,10,9,9,1,8,3,6.333333333333333,1
7URZ9A6VQ,1,1,0,0,64,151,1,44,6,25.92,1,2,4,2,4,2,2,9,10,6,4,2,4.0,0
QD1LW4U2S,0,0,1,1,73,165,0,40,5,21.77,4,6,8,1,6,6,9,4,6,2,10,10,6.0,1
Q4RBULEPO,0,1,1,1,55,147,1,37,7,34.16,5,3,6,10,7,4,3,7,3,8,9,5,5.833333333333333,0
H4AJCALVZ,1,0,1,1,62,124,1,17,0,22.68,2,5,7,4,7,9,2,4,3,3,2,9,4.75,1
5LWC5QFR2,0,0,0,1,68,283,1,8,3,43.03,8,9,6,6,4,2,10,9,10,4,10,4,6.833333333333333,1
PH188XYG2,0,1,1,0,58,238,1,25,0,49.74,2,1,2,5,7,4,7,1,1,10,5,9,4.5,1
8XQD9MMNN,0,0,1,0,58,267,1,45,5,55.8,7,2,8,6,10,5,1,5,5,1,7,5,5.166666666666667,1
DVZ7M8YHP,1,1,1,1,61,263,0,55,2,49.69,4,6,8,10,6,4,4,10,10,7,7,1,6.416666666666667,1
MWWDRP6QM,0,1,0,0,75,100,0,43,8,12.5,4,10,2,5,10,7,6,5,5,2,4,10,5.833333333333333,0
46JV4D9SH,1,1,0,0,77,265,0,38,0,31.42,6,2,8,10,8,2,8,1,7,8,3,6,5.75,1
8TI7FUMCX,1,1,0,1,80,147,1,11,8,16.15,7,3,8,3,2,10,5,6,6,6,9,2,5.583333333333333,0
2CZ18JG9F,0,0,0,1,75,194,0,13,8,24.25,3,5,9,2,6,3,8,5,7,8,7,6,5.75,0
RQZA99O4O,1,0,0,0,67,175,0,33,6,27.41,4,5,6,10,8,6,2,1,2,5,5,10,5.333333333333333,0
O9UXIH2AF,0,1,0,0,62,148,1,31,5,27.07,5,2,2,1,1,7,9,1,6,3,8,6,4.25,0
319VEAW9Z,0,1,0,0,63,196,1,31,9,34.72,9,10,9,9,6,3,6,2,7,4,8,7,6.666666666666667,0
J1QKYEJI9,1,0,1,1,68,171,0,40,8,26.0,6,2,2,6,2,4,10,9,7,2,10,8,5.666666666666667,0
BBDBXBVYB,1,0,0,0,75,210,0,3,1,26.25,2,8,1,8,4,1,6,8,9,7,10,8,6.0,1
5D8LZ8PG7,1,1,1,0,61,270,0,20,6,51.01,8,9,3,5,10,7,3,10,3,10,4,8,6.666666666666667,1
9SAB37OIP,0,1,1,1,63,141,0,12,1,24.97,8,8,3,10,3,5,8,4,1,7,2,7,5.5,1
VS1Q5KP6I,0,0,1,1,67,280,0,30,1,43.85,7,8,1,9,7,9,6,9,5,8,9,7,7.083333333333333,1
R2SBR5D3M,0,0,1,1,75,174,1,19,10,21.75,6,7,10,4,7,5,3,6,4,8,4,8,6.0,0
SF7NRXN13,0,0,1,0,57,287,0,39,7,62.1,3,2,3,1,10,9,2,2,10,5,5,5,4.75,0
4LMHMXKS7,1,0,0,1,60,250,0,6,2,48.82,10,8,5,9,8,4,7,3,4,1,1,2,5.166666666666667,1
ETIAEH2J9,0,1,1,1,73,260,0,37,4,34.3,6,3,1,1,1,1,5,2,6,9,10,6,4.25,1
L26P5XXD4,1,1,0,1,64,234,1,26,8,40.16,4,5,10,5,3,8,1,9,6,5,9,2,5.583333333333333,0
943QE6FYW,0,0,1,0,66,131,0,12,9,21.14,4,2,5,8,8,4,1,5,2,1,10,10,5.0,0
HNJASCXJO,0,0,1,1,71,271,0,29,0,37.79,4,5,4,1,6,3,8,7,6,5,3,5,4.75,1
9T2L1SETB,0,1,0,1,77,174,0,2,5,20.63,9,1,4,2,5,9,6,9,5,9,9,10,6.5,1
MF1CXSDO8,0,1,0,1,59,134,0,23,3,27.06,6,1,4,2,6,7,6,10,2,10,4,8,5.5,1
UOMKB5YNZ,1,0,1,0,71,125,1,52,0,17.43,10,6,8,10,6,6,3,9,4,2,3,3,5.833333333333333,1
UR3BTEPVT,1,1,1,0,72,103,0,56,1,13.97,6,8,1,10,2,9,7,9,1,10,3,9,6.25,1
MBUGTTWYU,0,0,1,1,60,212,0,51,9,41.4,2,3,10,2,6,2,10,9,8,3,6,10,5.916666666666667,0
54LOP8JJ4,0,1,0,1,76,153,1,56,6,18.62,5,1,7,5,2,3,4,1,6,4,3,6,3.9166666666666665,0
KCTPF5LK6,0,0,1,0,56,157,0,43,3,35.19,10,5,1,7,5,10,9,3,8,4,10,4,6.333333333333333,1
CZAGKQE4K,1,0,1,1,67,159,1,26,7,24.9,3,4,7,6,6,1,3,9,2,3,10,1,4.583333333333333,0
45AQT5PDY,1,0,0,0,74,220,1,57,5,28.24,4,5,4,3,1,1,4,6,3,7,1,2,3.4166666666666665,0
SGMUZGIYK,0,0,1,1,76,141,0,46,8,17.16,4,10,4,5,5,5,6,5,7,5,8,4,5.666666666666667,0
Z7L5KQ2X3,0,1,0,0,63,93,1,43,8,16.47,6,6,7,10,5,4,6,1,4,1,1,3,4.5,0
WVJJOC38D,0,1,0,1,63,127,0,37,9,22.49,7,9,1,2,8,5,5,7,6,4,10,5,5.75,0
AZ5EX1VAR,1,1,1,0,72,166,0,49,10,22.51,5,3,5,7,2,10,1,3,1,4,4,9,4.5,0
57JOH4HNY,0,1,1,0,67,272,1,55,8,42.6,9,7,10,3,8,7,1,1,7,7,10,8,6.5,0
5H82CGH46,1,0,0,0,63,280,0,48,7,49.59,4,6,6,7,5,3,1,9,8,2,2,3,4.666666666666667,0
HZBT3RWZC,0,0,0,0,61,151,0,58,10,28.53,8,4,7,9,3,5,6,6,9,3,9,10,6.583333333333333,0
EOHZA16SU,1,1,0,0,77,240,0,8,8,28.46,10,1,1,9,1,9,7,5,4,3,7,9,5.5,0
J87Z4U7QT,1,0,0,1,59,296,0,11,9,59.78,6,8,7,2,9,4,5,8,6,5,6,5,5.916666666666667,0
FC7UVZHKD,1,0,0,1,71,234,0,27,0,32.63,2,2,4,7,6,1,4,6,2,1,2,10,3.9166666666666665,1
6WEKOXYX2,0,1,1,1,72,162,1,59,1,21.97,7,5,5,2,10,7,10,9,2,5,4,5,5.916666666666667,1
L1ZSEEPTN,0,1,1,1,78,273,0,23,3,31.54,3,6,5,1,10,7,1,4,1,6,7,3,4.5,1
YUPSIH3W9,0,0,0,0,79,139,0,8,7,15.66,5,7,6,4,6,4,9,1,10,3,8,2,5.416666666666667,0
12DD84FJI,0,0,1,0,57,223,1,47,9,48.25,5,3,9,10,6,6,7,3,5,4,4,9,5.916666666666667,0
VAG6OH8IR,1,1,1,1,65,204,0,57,5,33.94,9,4,1,6,9,10,2,1,6,8,8,3,5.583333333333333,1
58GGIRWSQ,0,0,1,0,73,239,0,27,10,31.53,5,7,1,6,2,10,3,5,8,7,9,9,6.0,0
HLWI54ABX,1,0,1,0,77,167,0,27,0,19.8,4,10,1,10,4,10,4,2,10,6,4,4,5.75,1
Q6HR5ATFB,1,1,1,1,66,288,1,12,2,46.48,4,9,7,1,7,5,3,8,8,9,8,1,5.833333333333333,1
M4KFNH1PJ,0,1,1,1,69,190,1,24,7,28.06,4,10,7,6,1,5,6,5,4,2,7,5,5.166666666666667,0
YXCWZ95MU,1,1,0,1,68,170,0,58,2,25.85,8,7,8,10,4,8,3,4,2,5,6,8,6.083333333333333,1
'''

# Define data types for each column
types = [str, int, int, int, int, int, int, int, int, int, float] + [int]*12 + [float, int]

# Process the additional data
lines = data_string.strip().split('\n')

for line in lines:
    values = line.strip().split(',')
    row = []
    for v, t in zip(values, types):
        row.append(t(v))
    data.append(row)

# Create the DataFrame
df = pd.DataFrame(data, columns=columns)
##################################DASHBOARD##################################

###### Line chart showing the average mobility score over the course of the trial #####
# Prepare the data for the line graph
month_columns = ['January_mobility', 'February_mobility', 'March_mobility', 'April_mobility', 'May_mobility', 
                 'June_mobility', 'July_mobility', 'August_mobility', 'September_mobility', 'October_mobility', 
                 'November_mobility', 'December_mobility']

# Reshape the data for easier plotting
df_melted = pd.melt(df, id_vars=['Patient_ID', 'Placebo'], value_vars=month_columns, 
                      var_name='Month', value_name='Mobility_Score')

# Convert 'Month' to a categorical type for correct ordering
df_melted['Placebo'] = df_melted['Placebo'].map({0: 'Trial Drug', 1: 'Placebo'})

# Calculate the average scores by month for placebo and non-placebo users
avg_scores = df_melted.groupby(['Placebo', 'Month'])['Mobility_Score'].mean().reset_index()

# Plot the average scores by month for placebo and non-placebo groups with updated labels
fig_avg = px.line(avg_scores, x='Month', y='Mobility_Score', color='Placebo',
                  labels={'Placebo': 'Trial Group', 'Mobility_Score': 'Average Mobility Score'},
                  title='Average Mobility Scores by Month for Trial Drug and Placebo Groups')

# Display the plot in the Streamlit app
st.plotly_chart(fig_avg)


# Dropdown to select patients
selected_patient = st.selectbox("Select a Patient to View Individual Mobility Scores", df['Patient_ID'].unique())

# Filter data for the selected patient
patient_data = df_melted[df_melted['Patient_ID'] == selected_patient]

# Plot individual patient's mobility scores
fig_patient = px.line(patient_data, x='Month', y='Mobility_Score', 
                      labels={'Mobility_Score': 'Mobility Score'},
                      title=f'Mobility Scores for Patient {selected_patient}')

# Display the patient's individual mobility scores plot
st.plotly_chart(fig_patient)















##############################################################################
# Display the DataFrame in the Streamlit app
st.write("ALS Trial Data")
st.dataframe(df)


# Markdown data dictionary
data_dictionary = """
### Data Dictionary

- **Patient_ID**: A unique identifier for each patient.
- **Placebo**: Indicates if the patient received a placebo (1 = Yes, 0 = No).
- **Family_History**: Indicates if the patient has a family history of the disease (1 = Yes, 0 = No).
- **Prior_Serious_Health_Issues**: Indicates if the patient had serious health issues prior to the trial (1 = Yes, 0 = No).
- **Sex**: Gender of the patient (0 = Female, 1 = Male).
- **Height_in_inches**: The height of the patient in inches.
- **Weight_in_pounds**: The weight of the patient in pounds.
- **Smoker**: Indicates if the patient is a smoker (1 = Yes, 0 = No).
- **Diagnosis_Length_months**: The length of time since diagnosis in months.
- **Pre_Mobility**: The patient’s mobility score before the trial.
- **Trial_Avg_Mobility**: The average mobility score of the patient across all months of the trial.
- **Improvement**: Indicates if the patient showed improvement in mobility (1 = Yes, 0 = No).
"""

# Add the markdown to the app
st.markdown(data_dictionary)

#