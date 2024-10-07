import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Markdown header with title and short description

st.set_page_config(layout="wide", page_title="ALS Clinical Trials Dashboard")
header = """
# ALS Clinical Trials Dashboard

This dashboard displays the results of a clinical trial studying the effects of a new treatment on ALS patients. 
We are monitoring mobility improvements over the course of the trial, taking into account factors such as 
family history, prior health issues, and placebo group status. 

Scroll down to view detailed patient data and overall trial results.

[Go to Data Dictionary](#data-dictionary)

_This survey has no medical value and was created with synthetic data for demonstration purposes only._
"""

st.markdown(header)




# Load the CSV from the URL
url = "https://raw.githubusercontent.com/Djean3/ALS/main/ALS_trial_data.csv"
df = pd.read_csv(url)

# Rename the month columns for better readability
df.rename(columns={
    'January_mobility': 'January', 
    'February_mobility': 'February',
    'March_mobility': 'March',
    'April_mobility': 'April',
    'May_mobility': 'May',
    'June_mobility': 'June',
    'July_mobility': 'July',
    'August_mobility': 'August',
    'September_mobility': 'September',
    'October_mobility': 'October',
    'November_mobility': 'November',
    'December_mobility': 'December',
}, inplace=True)

# Melt the DataFrame for easier plotting
month_columns = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
                 'August', 'September', 'October', 'November', 'December']

df_melted = pd.melt(df, id_vars=['Patient_ID', 'Placebo'], value_vars=month_columns, 
                    var_name='Month', value_name='Mobility_Score')

# Convert 'Placebo' to readable labels
df_melted['Placebo'] = df_melted['Placebo'].map({0: 'Trial Drug', 1: 'Placebo'})

# Calculate the average scores by month for placebo and non-placebo users
avg_scores = df_melted.groupby(['Placebo', 'Month'])['Mobility_Score'].mean().reset_index()

df['Overweight'] = df['BMI'].apply(lambda x: 1 if x > 25 else 0)
df['Obese'] = df['BMI'].apply(lambda x: 1 if x > 30 else 0)

# Add "All Patients" checkbox
all_patients = st.checkbox("All Patients", value=True, key="all_patients")

# Disable other filters if "All Patients" is selected
if not all_patients:
    gender = st.selectbox("Select Gender", options=["All", "Male", "Female"], key="gender_select")

    # Use columns to arrange checkboxes horizontally
    col1, col2 = st.columns(2)

    with col1:
        family_history = st.checkbox("Has Family History", value=False, key="family_history")
        is_obese = st.checkbox("Is Obese (BMI > 30)", value=False, key="is_obese")

    with col2:
        prior_health_issues = st.checkbox("Had Prior Serious Health Issues", value=False, key="prior_health_issues")
        smoker = st.checkbox("Is Smoker", value=False, key="smoker")

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

all_diagnosis_years = st.checkbox("All Diagnosis Lengths", value=True, key="all_diagnosis_years")
min_years = int(df['Diagnosis_Length_Years'].min())
max_years = int(df['Diagnosis_Length_Years'].max())

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

if not all_pre_mobility:
    pre_mobility = st.slider(
        "Select Pre Mobility Score (Before Trial)", 
        min_mobility, max_mobility, (min_mobility, max_mobility), 
        key="pre_mobility_slider"
    )
    df = df[(df['Pre_Mobility'] >= pre_mobility[0]) & (df['Pre_Mobility'] <= pre_mobility[1])]

############################################

# Function to generate dynamic statement with clarity on minimal improvements
def generate_dynamic_statement(df, placebo_group, group_name):
    # Filter the group data (0: Trial Drug, 1: Placebo)
    group_df = df[df['Placebo'] == placebo_group]
    total_patients = group_df.shape[0]
    improved_patients = group_df[group_df['Improvement'] == 1].shape[0]

    # Calculate improvement percentage
    if total_patients > 0:
        improvement_percentage = (improved_patients / total_patients) * 100
    else:
        improvement_percentage = 0

    # Create a list of selected filters for display
    selected_filters = []
    # Only show filters if "All Patients" is unchecked
    if not all_patients:
        if gender != "All":
            selected_filters.append(f"{gender.lower()} patients")
        if family_history:
            selected_filters.append("with a family history")
        if prior_health_issues:
            selected_filters.append("with prior serious health issues")
        if smoker:
            selected_filters.append("who are smokers")
        if is_obese:
            selected_filters.append("who are obese")
        if not all_diagnosis_years:
            selected_filters.append(f"who have been diagnosed for {diagnosis_years[0]}-{diagnosis_years[1]} years")
        if not all_pre_mobility:
            selected_filters.append(f"with a pre-mobility score range of {pre_mobility[0]}-{pre_mobility[1]}")
    else:
        selected_filters.append("all patients in the study")

    # Check if there are any selected filters before trying to join them
    if len(selected_filters) > 1:
        filter_str = " and ".join([", ".join(selected_filters[:-1]), selected_filters[-1]])
    elif len(selected_filters) == 1:
        filter_str = selected_filters[0]
    else:
        filter_str = "all patients in the study"

    # Generate the result statement based on the effect
    if improvement_percentage > 50:
        return f"The {group_name} had a positive effect on mobility, with {improvement_percentage:.1f}% improvement for {total_patients} patients {filter_str}."
    elif improvement_percentage == 50:
        return f"The {group_name} had a neutral effect on mobility, with 50% of {total_patients} patients {filter_str} showing improvement."
    else:
        return (
            f"The {group_name} was ineffective on the selected patients, with only {improvement_percentage:.1f}% ({improved_patients} of {total_patients} patients) experiencing mobility improvement "
            f"{filter_str}."
        )

# Generate statements
trial_drug_statement = generate_dynamic_statement(df, placebo_group=0, group_name="trial drug")
placebo_statement = generate_dynamic_statement(df, placebo_group=1, group_name="placebo")

##########################################################################
# Group data by Placebo and Improvement for the first chart
grouped_data = df.groupby(['Placebo', 'Improvement']).size().reset_index(name='Count')
grouped_data['Total'] = grouped_data.groupby('Placebo')['Count'].transform('sum')
grouped_data['Percentage'] = (grouped_data['Count'] / grouped_data['Total']) * 100
grouped_data['Improvement'] = grouped_data['Improvement'].map({0: 'Not Improved', 1: 'Improved'})
grouped_data['Placebo'] = grouped_data['Placebo'].map({0: 'Trial Drug', 1: 'Placebo'})
grouped_data['text'] = grouped_data.apply(lambda row: f"{row['Percentage']:.1f}% - {row['Count']} patients", axis=1)

# Chart 1: Improvement Based on Placebo and Trial Groups (stacked bar chart)
fig1 = px.bar(grouped_data, 
             x='Placebo', 
             y='Count', 
             color='Improvement', 
             barmode='stack',  # Stacked bar chart
             text=grouped_data['text'],  # Display percentage and patient count
             labels={'Count': 'Number of Patients', 'Placebo': 'Trial Group'},
             title='Patient Improvement Based on Clinical Trial Groups and Health Factors')

# Plot the average mobility scores by month (filtered based on user selections)
df_melted_filtered = pd.melt(df, id_vars=['Patient_ID', 'Placebo'], value_vars=month_columns, 
                             var_name='Month', value_name='Mobility_Score')

df_melted_filtered['Placebo'] = df_melted_filtered['Placebo'].map({0: 'Trial Drug', 1: 'Placebo'})
avg_scores_filtered = df_melted_filtered.groupby(['Placebo', 'Month'])['Mobility_Score'].mean().reset_index()

# Line chart: Average mobility scores by month for Trial Drug and Placebo groups
fig_avg_filtered = px.line(avg_scores_filtered, x='Month', y='Mobility_Score', color='Placebo',
                           labels={'Placebo': 'Trial Group', 'Mobility_Score': 'Average Mobility Score'},
                           title='Average Mobility Scores by Month for Trial Drug and Placebo Groups')

# Create a bar chart showing average pre-trial and post-trial mobility scores
avg_pre_mobility = df['Pre_Mobility'].mean()
avg_trial_mobility = df['Trial_Avg_Mobility'].mean()
if avg_pre_mobility != 0:
    percent_change = ((avg_trial_mobility - avg_pre_mobility) / avg_pre_mobility) * 100
else:
    percent_change = 0

mobility_data = pd.DataFrame({
    'Mobility Stage': ['Pre-Trial Mobility', 'Post-Trial Mobility'],
    'Average Score': [avg_pre_mobility, avg_trial_mobility]
})

fig_mobility = px.bar(mobility_data, 
                      x='Mobility Stage', 
                      y='Average Score', 
                      text=[f"{avg_pre_mobility:.2f}", f"{avg_trial_mobility:.2f}"],
                      labels={'Average Score': 'Average Mobility Score'},
                      title=f'Average Pre-Trial vs Post-Trial Mobility Scores\nPercentage Change: {percent_change:.2f}%',
                      color_discrete_sequence=['#636EFA', '#EF553B'])
##########################################
# Group the data by Gender and Improvement after filters are applied
filtered_gender_improvement_data = df.groupby(['Sex', 'Improvement']).size().reset_index(name='Count')

# Map gender values for better labeling (0: Female, 1: Male)
filtered_gender_improvement_data['Sex'] = filtered_gender_improvement_data['Sex'].map({0: 'Female', 1: 'Male'})

# Map Improvement values for better labeling (0: Not Improved, 1: Improved)
filtered_gender_improvement_data['Improvement'] = filtered_gender_improvement_data['Improvement'].map({0: 'Not Improved', 1: 'Improved'})

# Check the gender filter and adjust the data accordingly
if gender == 'Male':
    filtered_gender_improvement_data = filtered_gender_improvement_data[filtered_gender_improvement_data['Sex'] == 'Male']
elif gender == 'Female':
    filtered_gender_improvement_data = filtered_gender_improvement_data[filtered_gender_improvement_data['Sex'] == 'Female']

# Define color mapping when all genders are selected
if gender == 'All':
    color_map = {'Male': '#1f77b4', 'Female': '#aec7e8'}  # Dark blue and light blue
else:
    color_map = None  # Let Plotly use default colors if a specific gender is selected

# ---------------------- Pie Chart ----------------------
fig_gender_pie = px.pie(
    filtered_gender_improvement_data,
    names='Sex',
    values='Count',
    color='Sex',
    title='Gender Distribution of Improvement',
    hole=0.4,  # Making it a donut chart
    color_discrete_map=color_map,  # Apply custom colors when all genders are selected
    labels={'Sex': 'Gender', 'Count': 'Number of Patients', 'Improvement': 'Mobility Status'}
)


##########################################
# Container for displaying the charts
with st.container():
    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(fig1, use_container_width=True)  # Improvement stacked bar chart

    with col2:
        st.plotly_chart(fig_avg_filtered, use_container_width=True)  # Line chart for mobility scores by month

# New row for the additional charts
with st.container():
    col3, col4 = st.columns([1, 1])

    with col3:
        st.plotly_chart(fig_mobility, use_container_width=True)  # Bar chart for pre and post-trial mobility

    # Optionally, add another chart or analysis in col4
    with col4:
        st.plotly_chart(fig_gender_pie, use_container_width=True)  # Display pie chart

st.write(placebo_statement)
st.write(trial_drug_statement)
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



#######################################################
#############################################################################################
 #Calculate the average pre-mobility and trial average mobility for filtered patients
# avg_pre_mobility = filtered_df['Pre_Mobility'].mean()
# avg_trial_mobility = filtered_df['Trial_Avg_Mobility'].mean()
# ###################################





# # Calculate the percentage change
# if avg_pre_mobility != 0:
#     percent_change = ((avg_trial_mobility - avg_pre_mobility) / avg_pre_mobility) * 100
# else:
#     percent_change = 0

# # Create a dataframe to hold this data for visualization
# mobility_data = pd.DataFrame({
#     'Mobility Stage': ['Pre-Trial Mobility', 'Post-Trial Mobility'],
#     'Average Score': [avg_pre_mobility, avg_trial_mobility]
# })
# # Generate the statement for the trial drug group
# trial_drug_statement = generate_dynamic_statement(df, placebo_group=0, group_name="trial drug")
# # Display the trial drug statement


# # Group data by Placebo and Improvement for the first chart
# grouped_data = df.groupby(['Placebo', 'Improvement']).size().reset_index(name='Count')

# # Calculate the total count for each Placebo group
# grouped_data['Total'] = grouped_data.groupby('Placebo')['Count'].transform('sum')

# # Calculate the percentage of patients in each group
# grouped_data['Percentage'] = (grouped_data['Count'] / grouped_data['Total']) * 100

# # Map Improvement values for better labeling
# grouped_data['Improvement'] = grouped_data['Improvement'].map({0: 'Not Improved', 1: 'Improved'})

# # Map Placebo values for better labeling (0: Trial Drug, 1: Placebo)
# grouped_data['Placebo'] = grouped_data['Placebo'].map({0: 'Trial Drug', 1: 'Placebo'})

# # Create the stacked bar chart with percentages and patient count as text on the bars
# grouped_data['text'] = grouped_data.apply(lambda row: f"{row['Percentage']:.1f}% - {row['Count']} patients", axis=1)

# df_melted_filtered = pd.melt(df, id_vars=['Patient_ID', 'Placebo'], value_vars=month_columns, 
#                              var_name='Month', value_name='Mobility_Score')

# # Convert 'Placebo' to readable labels
# df_melted_filtered['Placebo'] = df_melted_filtered['Placebo'].map({0: 'Trial Drug', 1: 'Placebo'})

# # Calculate the average scores by month for placebo and non-placebo users based on filtered data
# avg_scores_filtered = df_melted_filtered.groupby(['Placebo', 'Month'])['Mobility_Score'].mean().reset_index()

# # Chart 1: Improvement Based on Placebo and Trial Groups (stacked bar chart)
# fig1 = px.bar(grouped_data, 
#              x='Placebo', 
#              y='Count', 
#              color='Improvement', 
#              barmode='stack',  # Stacked bar chart
#              text=grouped_data['text'],  # Display percentage and patient count
#              labels={'Count': 'Number of Patients', 'Placebo': 'Trial Group'},
#              title='Patient Improvement Based on Clinical Trial Groups and Health Factors')

# # Plot the dynamically updated average mobility scores by month (line chart)
# fig_avg_filtered = px.line(avg_scores_filtered, x='Month', y='Mobility_Score', color='Placebo',
#                            labels={'Placebo': 'Trial Group', 'Mobility_Score': 'Average Mobility Score'},
#                            title='Average Mobility Scores by Month for Trial Drug and Placebo Groups')


# ### % imrpovement
# filtered_df = df.copy()

# # Calculate the average pre-mobility and trial average mobility for filtered patients
# avg_pre_mobility = filtered_df['Pre_Mobility'].mean()
# avg_trial_mobility = filtered_df['Trial_Avg_Mobility'].mean()

# # Calculate the percentage change
# if avg_pre_mobility != 0:
#     percent_change = ((avg_trial_mobility - avg_pre_mobility) / avg_pre_mobility) * 100
# else:
#     percent_change = 0

# # Create a dataframe to hold this data for visualization
# mobility_data = pd.DataFrame({
#     'Mobility Stage': ['Pre-Trial Mobility', 'Post-Trial Mobility'],
#     'Average Score': [avg_pre_mobility, avg_trial_mobility]
# })

# # Create a bar chart showing average pre-trial and post-trial mobility scores
# fig_mobility = px.bar(mobility_data, 
#                       x='Mobility Stage', 
#                       y='Average Score', 
#                       text=[f"{avg_pre_mobility:.2f}", f"{avg_trial_mobility:.2f}"],
#                       labels={'Average Score': 'Average Mobility Score'},
#                       title=f'Average Pre-Trial vs Post-Trial Mobility Scores\n'
#                             f'Percentage Change: {percent_change:.2f}%',
#                       color_discrete_sequence=['#636EFA', '#EF553B'])

# # Map the phases to more descriptive names
# df_mobility['Phase'] = df_mobility['Phase'].map({'Pre_Mobility': 'Pre-Trial Mobility', 'Trial_Avg_Mobility': 'Post-Trial Mobility'})

# # Create a box plot to show the distribution of mobility scores
# fig_mobility_distribution = px.box(
#     df_mobility,
#     x='Phase',
#     y='Mobility_Score',
#     color='Placebo',
#     labels={'Mobility_Score': 'Mobility Score', 'Phase': 'Phase'},
#     title='Distribution of Pre-Trial and Post-Trial Mobility Scores by Trial Group'
# )

# # Containerizing the two charts
# with st.container():
#     # Adjust column width by specifying different fractions (e.g., 5:5 for equal width)
#     col1, col2 = st.columns([1, 1])  # Equal width for both columns

#     # Display the bar chart in the first column, using full container width
#     with col1:
#         st.plotly_chart(fig1, use_container_width=True)  # Make the chart fill the column width

#     # Display the dynamically updated line chart in the second column, using full container width
#     with col2:
#         st.plotly_chart(fig_avg_filtered, use_container_width=True)  # Make the chart fill the column width

# # Display the chart in a new container
# with st.container():
#     # Adjust column width for new row of charts
#     col3, col4 = st.columns([1, 1])  # Equal width for both columns

#     # Display the percentage improvement on the left as a chart
#     with col3:
#         st.plotly_chart(fig_mobility, use_container_width=True)

#     # Optionally, keep another chart or analysis on the right
#     with col4:
#         st.plotly_chart(fig_mobility_distribution, use_container_width=True)

# # Add a space before the placebo statement
# st.write("")

# # Generate the statement for the placebo group
# placebo_statement = generate_dynamic_statement(df, placebo_group=1, group_name="placebo")
# Display the placebo statement
















###############################


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