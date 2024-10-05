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

#############################################################################
######## IMPROVEMENT DONUT CHART ##################################
# Group data by Placebo and Improvement
grouped_data = df.groupby(['Placebo', 'Improvement']).size().reset_index(name='Count')

# Map Improvement values for better labeling
grouped_data['Improvement'] = grouped_data['Improvement'].map({0: 'Not Improved', 1: 'Improved'})

# Map Placebo values for better labeling (0: Trial Drug, 1: Placebo)
grouped_data['Placebo'] = grouped_data['Placebo'].map({0: 'Trial Drug', 1: 'Placebo'})

# Create the stacked bar chart
fig = px.bar(grouped_data, 
             x='Placebo', 
             y='Count', 
             color='Improvement', 
             barmode='stack',  # Switch to stacked bar chart
             labels={'Count': 'Number of Patients', 'Placebo': 'Trial Group'},
             title='Improvement Across Placebo and Trial Groups')

# Display the bar chart in the Streamlit app
st.plotly_chart(fig)


































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