import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Markdown header with title and short description
header = """
# ALS Clinical Trials Dashboard

This dashboard displays the results of a clinical trial studying the effects of a new treatment on ALS patients. 
We are monitoring mobility improvements over the course of the trial, taking into account factors such as 
family history, prior health issues, and placebo group status. 

Scroll down to view detailed patient data and overall trial results.

[Go to Data Dictionary](#data-dictionary)
"""



url = "https://raw.githubusercontent.com/Djean3/ALS/main/ALS_trial_data.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(url)

st.markdown(header)





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


# # Dropdown to select patients
# selected_patient = st.selectbox("Select a Patient to View Individual Mobility Scores", df['Patient_ID'].unique())

# # Filter data for the selected patient
# patient_data = df_melted[df_melted['Patient_ID'] == selected_patient]

# # Plot individual patient's mobility scores
# fig_patient = px.line(patient_data, x='Month', y='Mobility_Score', 
#                       labels={'Mobility_Score': 'Mobility Score'},
#                       title=f'Mobility Scores for Patient {selected_patient}')

# # Display the patient's individual mobility scores plot
# st.plotly_chart(fig_patient)

#############################################################################
######## IMPROVEMENT DONUT CHART ##################################




#####################################################################

# Calculate new feature: Overweight and Obese based on BMI
# Add gender filter (All, Male, Female) with a unique key
gender = st.selectbox("Select Gender", options=["All", "Male", "Female"], key="gender_select")

# Use columns to arrange checkboxes horizontally
col1, col2 = st.columns(2)

with col1:
    # Checkbox in the first column
    family_history = st.checkbox("Has Family History", value=True, key="family_history")
    is_obese = st.checkbox("Is Obese (BMI > 30)", value=True, key="is_obese")

with col2:
    # Checkboxes in the second column
    prior_health_issues = st.checkbox("Had Prior Serious Health Issues", value=True, key="prior_health_issues")
    smoker = st.checkbox("Is Smoker", value=True, key="smoker")

# Apply filters based on checkboxes and dropdowns
if gender == "Male":
    df = df[df['Sex'] == 1]  # 1 represents Male
elif gender == "Female":
    df = df[df['Sex'] == 0]  # 0 represents Female

if family_history:
    df = df[df['Family_History'] == 1]
if prior_health_issues:
    df = df[df['Prior_Serious_Health_Issues'] == 1]
if smoker:
    df = df[df['Smoker'] == 1]
if is_obese:
    df = df[df['Obese'] == 1]

# Filter by diagnosis length (convert to years)
df['Diagnosis_Length_Years'] = df['Diagnosis_Length_months'] // 12

# Diagnosis Length Checkbox and Slider
all_diagnosis_years = st.checkbox("All Diagnosis Lengths", value=True, key="all_diagnosis_years")

min_years = int(df['Diagnosis_Length_Years'].min())
max_years = int(df['Diagnosis_Length_Years'].max())

# Disable slider if "All Diagnosis Lengths" is checked
if not all_diagnosis_years:
    diagnosis_years = st.slider(
        "Select Diagnosis Length (Years)", 
        min_years, max_years, (min_years, max_years), 
        key="diagnosis_years_slider"
    )
    df = df[(df['Diagnosis_Length_Years'] >= diagnosis_years[0]) & (df['Diagnosis_Length_Years'] <= diagnosis_years[1])]

# Pre Mobility Checkbox and Slider
all_pre_mobility = st.checkbox("All Pre Mobility Scores", value=True, key="all_pre_mobility")

min_mobility = int(df['Pre_Mobility'].min())
max_mobility = int(df['Pre_Mobility'].max())

# Disable slider if "All Pre Mobility Scores" is checked
if not all_pre_mobility:
    pre_mobility = st.slider(
        "Select Pre Mobility Score (Before Trial)", 
        min_mobility, max_mobility, (min_mobility, max_mobility), 
        key="pre_mobility_slider"
    )
    df = df[(df['Pre_Mobility'] >= pre_mobility[0]) & (df['Pre_Mobility'] <= pre_mobility[1])]

# Group data by Placebo and Improvement for the first chart
grouped_data = df.groupby(['Placebo', 'Improvement']).size().reset_index(name='Count')

# Calculate the total count for each Placebo group
grouped_data['Total'] = grouped_data.groupby('Placebo')['Count'].transform('sum')

# Calculate the percentage of patients in each group
grouped_data['Percentage'] = (grouped_data['Count'] / grouped_data['Total']) * 100

# Map Improvement values for better labeling
grouped_data['Improvement'] = grouped_data['Improvement'].map({0: 'Not Improved', 1: 'Improved'})

# Map Placebo values for better labeling (0: Trial Drug, 1: Placebo)
grouped_data['Placebo'] = grouped_data['Placebo'].map({0: 'Trial Drug', 1: 'Placebo'})

# Create the stacked bar chart with percentages and patient count as text on the bars
grouped_data['text'] = grouped_data.apply(lambda row: f"{row['Percentage']:.1f}% - {row['Count']} patients", axis=1)

# Chart 1: Improvement Based on Placebo and Trial Groups
fig1 = px.bar(grouped_data, 
             x='Placebo', 
             y='Count', 
             color='Improvement', 
             barmode='stack',  # Stacked bar chart
             text=grouped_data['text'],  # Display percentage and patient count
             labels={'Count': 'Number of Patients', 'Placebo': 'Trial Group'},
             title='Patient Improvement Based on Clinical Trial Groups and Health Factors')

# Chart 2: Line chart showing average BMI by Placebo group
avg_bmi = df.groupby('Placebo')['BMI'].mean().reset_index()
fig2 = px.line(avg_bmi, 
               x='Placebo', 
               y='BMI', 
               title='Average BMI by Trial Group',
               labels={'BMI': 'Average BMI', 'Placebo': 'Trial Group'})

# Display both charts
st.plotly_chart(fig1)
st.plotly_chart(fig2)
##################################################################



























#######################################################################
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