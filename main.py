import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
file_path = r'C:\Users\kamsj\Downloads\suicide-rate-male-female-who-mdb.csv'
data = pd.read_csv(file_path)

# Function to map country names to continents
def map_country_to_continent(country_name):
    try:
        import pycountry_convert as pc
        country_alpha = pc.country_name_to_country_alpha2(country_name)
        continent_code = pc.country_alpha2_to_continent_code(country_alpha)
        continent_map = {
            'AF': 'Africa', 'AN': 'Antarctica', 'AS': 'Asia', 'EU': 'Europe',
            'OC': 'Oceania', 'NA': 'North America', 'SA': 'South America'
        }
        return continent_map.get(continent_code, 'Unknown')
    except:
        return 'Unknown'

# Apply the function to create a new 'Continent' column
data['Continent'] = data['Entity'].apply(map_country_to_continent)

# Drop rows where 'Continent' or suicide rates are missing
data_cleaned = data.dropna(subset=[
    'Age-standardized death rate from self-inflicted injuries per 100,000 population - Sex: Males - Age group: all ages',
    'Age-standardized death rate from self-inflicted injuries per 100,000 population - Sex: Females - Age group: all ages'
])

# Rename columns for easier reference
data_cleaned = data_cleaned.rename(columns={
    'Age-standardized death rate from self-inflicted injuries per 100,000 population - Sex: Males - Age group: all ages': 'Male Suicide Rate',
    'Age-standardized death rate from self-inflicted injuries per 100,000 population - Sex: Females - Age group: all ages': 'Female Suicide Rate'
})

# Remove the rows where the Continent is 'Unknown'
data_cleaned = data_cleaned[data_cleaned['Continent'] != 'Unknown']

# Calculate the average suicide rates by continent
continent_avg = data_cleaned.groupby('Continent')[['Male Suicide Rate', 'Female Suicide Rate']].mean()

# Plotting
plt.figure(figsize=(10, 6))

# Bar plot for average suicide rates by continent
continent_avg.plot(kind='bar', figsize=(12, 6), color=['green', 'pink'])

# Add titles and labels
plt.title('Average Suicide Rates by Gender for Each Continent', fontsize=16)
plt.xlabel('Continent', fontsize=14)
plt.ylabel('Average Suicide Rate (per 100,000 population)', fontsize=14)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the plot
plt.tight_layout()
plt.show()
