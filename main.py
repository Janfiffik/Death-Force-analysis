import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# Additional libraries
from datetime import datetime
from collections import Counter
import pycountry
from iso3166 import countries
from plotly.graph_objs import Choropleth

# Reading of all dataframes and preliminary data exploration

# Options for terminal -----------------------------------------------
# pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_rows', None)   # Shows all rows
pd.set_option('display.max_columns', None)  # Shows all columns
# --------------------------------------------------------------------

# reading DataFrames
df_hh_income = pd.read_csv('Data/Median_Household_Income_2015.csv', encoding='windows-1252')
df_pct_poverty = pd.read_csv('Data/Pct_People_Below_Poverty_Level.csv', encoding='windows-1252')
df_pct_complete_hs = pd.read_csv('Data/Pct_Over_25_Completed_High_School.csv', encoding='windows-1252')
df_share_race_city = pd.read_csv('Data/Share_of_Race_By_City.csv', encoding='windows-1252')
df_fatalities = pd.read_csv('Data/Deaths_by_Police_US.csv', encoding='windows-1252')

print("---------------Shapes of all dataframes----------------:\n")
hh_income_shape = df_hh_income.shape
print(f"Median household income:  \n{hh_income_shape[0]} rows.\n{hh_income_shape[1]} columns.\n")

pct_poverty_shape = df_pct_poverty.shape
print(f"People below poverty level:\n{pct_poverty_shape[0]} rows.\n{pct_poverty_shape[1]} columns.\n")

pct_complete_hs_shape = df_pct_complete_hs.shape
print(f"Pct over 25 complete high school: \n{pct_complete_hs_shape[0]} rows.\n{pct_complete_hs_shape[1]} columns.\n")

share_race = df_share_race_city.shape
print(f"Share race city has:\n{share_race[0]} rows.\n{share_race[1]} columns.\n")

fatalities = df_fatalities.shape
print(f"Shape of fatalities dataframe:\n{fatalities[0]} rows.\n{fatalities[1]} columns.")

print("----------------------------Nan values---------------------------------\n")
print(f" df_hh_income has:\n {df_hh_income.isna().sum()} Nan values.\n")
print(f"df_pct_poverty has:\n {df_pct_poverty.isna().sum()} Nan values.\n")
print(f"df_pct_complete_hs has:\n {df_pct_complete_hs.isna().sum()} Nan values.\n")
print(f"df_share_race_city has:\n {df_share_race_city.isna().sum()} Nan values.\n")
print(f"df_fatalities has:\n {df_fatalities.isna().sum()} Nan values.\n")

print("---------------Info about all dataframes------------------------\n")
# print(f"df_hh_income info:\n{df_hh_income.info}\n")
# print(f"df_pct_poverty info:\n{df_pct_poverty.info}\n")
# print(f"df_pct_complete_hs info:\n {df_pct_complete_hs.info}\n")
# print(f"df_share_race_city info:\n {df_share_race_city.info}\n")
# print(f"df_fatalities info:\n {df_fatalities.info}\n")

print("-----------------------They have duplicates?-------------------------\n")
print(f"df_hh_income duplicates:\n{df_hh_income.duplicated().sum()}\n")
print(f"df_pct_poverty duplicates:\n{df_pct_poverty.duplicated().sum()}\n")
print(f"df_pct_complete_hs duplicates:\n {df_pct_complete_hs.duplicated().sum()}\n")
print(f"df_share_race_city duplicates:\n {df_share_race_city.duplicated().sum()}\n")
print(f"df_fatalities duplicates:\n {df_fatalities.duplicated().sum()}\n")

print(f"-----------------All column names-------------------------\n")
print(f"df_hh_income columns:\n{df_hh_income.columns}\n")
print(f"df_pct_poverty columns:\n{df_pct_poverty.columns}\n")
print(f"df_pct_complete_hs columns:\n {df_pct_complete_hs.columns}\n")
print(f"df_share_race_city columns:\n {df_share_race_city.columns}\n")
print(f"df_fatalities columns:\n {df_fatalities.columns}\n")

print("------------------------delete Nan value rows-----------------------------------------\n")

cleared_hh_income = df_hh_income.dropna()
cleared_pct_poverty = df_pct_poverty.dropna()
cleared_high_school = df_pct_complete_hs.dropna()
cleared_race_city = df_share_race_city.dropna()
cleared_fatal = df_fatalities.dropna()

print("-----------------------------Nan values left and shapes:")
print(f" df_hh_income has:\n {cleared_hh_income.isna().sum()} Nan values.\n Shape:\n"
      f"{cleared_hh_income.shape[0]}\n")

print(f"df_pct_poverty has:\n {cleared_pct_poverty.isna().sum()} Nan values.\n Shape:"
      f"{cleared_pct_poverty.shape[0]}\n")

print(f"df_pct_complete_hs has:\n {cleared_high_school.isna().sum()} Nan values.\nShape:"
      f"{cleared_high_school.shape[0]}\n")

print(f"df_share_race_city has:\n {cleared_race_city.isna().sum()} Nan values.\nShape:"
      f"{cleared_race_city.shape[0]}\n")

print(f"df_fatalities has:\n {cleared_fatal.isna().sum()} Nan values.\nShape:"
      f"{cleared_fatal.shape[0]}\n")
print("----------------------------------------------------------------------")

print("-----------------ALL converting-----------------------")
# ------converting geographic area to name of State----------
country_codes = cleared_pct_poverty["Geographic Area"]
states = []
for i in country_codes:
    state = pycountry.subdivisions.get(code=f"US-{i}")
    states.append(state.name)

cleared_pct_poverty["States"] = states
del cleared_pct_poverty["Geographic Area"]

# -----------------
country_codes = cleared_high_school["Geographic Area"]
states = []
for i in country_codes:
    state = pycountry.subdivisions.get(code=f"US-{i}")
    states.append(state.name)

cleared_high_school["States"] = states
del cleared_high_school["Geographic Area"]

# -----------------
country_codes = cleared_race_city["Geographic area"]
states = []
for i in country_codes:
    state = pycountry.subdivisions.get(code=f'US-{i}')
    states.append(state.name)
cleared_race_city["States"] = states
del cleared_race_city["Geographic area"]

# -------converting poverty_rate from string to float-------
new_poverty = cleared_pct_poverty['poverty_rate']
poverty = []
for i in new_poverty:
    try:
        pov = float(i)
        poverty.append(pov)
    except ValueError:
        pov = 0
        poverty.append(pov)
cleared_pct_poverty['poverty_rate'] = poverty

# ------------converting percent_completed_hs to float----------------------
new_comp = cleared_high_school["percent_completed_hs"]
completed = []
for i in new_comp:
    try:
        comp = float(i)
        completed.append(comp)
    except ValueError:
        comp = 0
        completed.append(comp)
cleared_high_school["percent_completed_hs"] = completed

# ---------------------converting races from str to float pct---------------------------------------
new_white = cleared_race_city['share_white']
white = []
for i in new_white:
    try:
        white.append(float(i))
    except ValueError:
        white.append(0)

cleared_race_city['white'] = white
del cleared_race_city["share_white"]

print(type(cleared_race_city.white[2]))
# -------------
new_black = cleared_race_city['share_black']
black = []
for i in new_black:
    try:
        black.append(float(i))
    except ValueError:
        black.append(0)

cleared_race_city['black'] = black
del cleared_race_city["share_black"]

print(type(cleared_race_city.black[2]))
# -------------
new_nat_am = cleared_race_city['share_native_american']
nat_am = []
for i in new_nat_am:
    try:
        nat_am.append(float(i))
    except ValueError:
        nat_am.append(0)

cleared_race_city['native_american'] = nat_am
del cleared_race_city["share_native_american"]

print(type(cleared_race_city.native_american[2]))
# -------------
new_asian = cleared_race_city['share_asian']
asian = []
for i in new_asian:
    try:
        asian.append(float(i))
    except ValueError:
        asian.append(0)

cleared_race_city['asian'] = asian
del cleared_race_city["share_asian"]

print(type(cleared_race_city.asian[2]))
# -------------
new_hispanic = cleared_race_city['share_hispanic']
hispanic = []
for i in new_hispanic:
    try:
        hispanic.append(float(i))
    except ValueError:
        hispanic.append(0)

cleared_race_city['hispanic'] = hispanic
del cleared_race_city["share_hispanic"]

print(type(cleared_race_city.hispanic[2]))
# ------------- race converting ----------------------------

# average poverty rate by state for chart_bar
average_poverty = cleared_pct_poverty.groupby("States")['poverty_rate'].mean()

poverty_chart = px.bar(average_poverty,
                       x='poverty_rate',
                       color="poverty_rate")
poverty_chart.update_layout(title="States and Cities poverty rate.")
# poverty_chart.show()

# --------------------Average high school -------------------------------
average_school = cleared_high_school.groupby("States")["percent_completed_hs"].mean()

school_chart = px.bar(average_school,
                      x="percent_completed_hs",
                      color="percent_completed_hs")
school_chart.update_layout(title="the High School Graduation Rate by US State")
school_chart.show()

# the Relationship between Poverty Rates and High School Graduation Rates

school_pov = pd.concat([average_poverty, average_school], axis=1)

relation_pov_school = px.scatter(school_pov,
                                 text=school_pov.index,
                                 x="poverty_rate",
                                 y="percent_completed_hs",
                                 title="Relationship between Poverty Rates and High School Graduation Rates",
                                 labels={'poverty_rate': 'Poverty Rate (%)',
                                         'percent_completed_hs': 'Graduation Rate (%)'},
                                 hover_name=school_pov.index,
                                 color=school_pov.index,
                                 size_max=60)
relation_pov_school.update_layout(showlegend=False)
relation_pov_school.show()

# same data but with seaborn
seab_chart = sns.lmplot(school_pov, x="poverty_rate",
                        y="percent_completed_hs",
                        height=6,
                        aspect=1.5,
                        scatter_kws={'s': 100})
plt.title("Relationship between Poverty Rates and High School Graduation Rates")
plt.show()

# ------------------- racial makeup of each US state -------------------------
# print(cleared_race_city[["States", 'white', 'black', 'native_american',
#                          'asian', 'hispanic']].head(20))

print("-------------Creating new average race groups per states dataframe----------------------")
race_per_state = cleared_race_city.groupby('States')[['white', 'black', 'native_american', 'asian', 'hispanic']]
race_per_state = race_per_state.sum()
Perc_Race = pd.DataFrame(index=race_per_state.index)

states = race_per_state.index
races = race_per_state.columns

for state in states:
    state_bool = cleared_race_city["States"] == state
    for race in races:
        race_average = cleared_race_city.loc[state_bool, race].mean()
        race_average = round(race_average, 3)
        Perc_Race.at[state, race] = race_average

print(Perc_Race.head(5))

# sunburst graph -----------------------------------------------------------------
race_sunburst_graph = px.sunburst(Perc_Race,
                                  path=[Perc_Race.index, Perc_Race.white, 'black', 'native_american',
                                        'asian', 'hispanic'],
                                  title="Races per state",
                                  branchvalues='total',
                                  )
race_sunburst_graph.show()

# Create a Bar Chart with Subsections Showing the Racial Makeup of Each US State

bar_chart_race = px.bar(Perc_Race,
                        x=Perc_Race.index,
                        y=['white', 'black', 'native_american', 'asian', 'hispanic'],
                        barmode='group',
                        )
bar_chart_race.update_layout(annotations=[dict(x=x_val,
                                               y=y_val,
                                               showarrow=False,
                                               text="White",
                                               arrowhead=0,
                                               ax=0,
                                               ay=40
                                               )
                                          for x_val, y_val in zip(range(len(Perc_Race.index)),
                                                                  Perc_Race.white)] +
                                         [dict(
                                                x=x_val,
                                                y=y_val,
                                                showarrow=False,
                                                text="Black",
                                                arrowhead=0,
                                                ax=0,
                                                ay=20
                                               )
                                             for x_val, y_val in zip(range(len(Perc_Race.index)),
                                                                     Perc_Race.black)] +
                                         [dict(
                                                x=x_val,
                                                y=y_val,
                                                showarrow=False,
                                                text="Native American",
                                                arrowhead=0,
                                                ax=0,
                                                ay=0
                                               )
                                             for x_val, y_val, race in zip(range(len(Perc_Race.index)),
                                                                           Perc_Race.native_american, races)] +
                             [dict(
                                                x=x_val,
                                                y=y_val,
                                                showarrow=False,
                                                text="Asian",
                                                arrowhead=0,
                                                ax=0,
                                                ay=-20
                                               )
                                             for x_val, y_val in zip(range(len(Perc_Race.index)),
                                                                     Perc_Race.asian)] +
                             [dict(
                                                x=x_val,
                                                y=y_val,
                                                showarrow=False,
                                                text="Hispanic",
                                                arrowhead=0,
                                                ax=0,
                                                ay=-40
                                               )
                                             for x_val, y_val in zip(range(len(Perc_Race.index)),
                                                                     Perc_Race.hispanic)])

bar_chart_race.show()
# -----------------------------------------------------------------------------------
print("rewrote races from single capital letter to words")

old_race = df_fatalities["race"]

new_race = []
for race in old_race:
    if race == 'B':
        new_race.append('black')
    elif race == 'H':
        new_race.append("hispanic")
    elif race == "A":
        new_race.append("asian")
    elif race == "N":
        new_race.append("native_american")
    elif race == "W":
        new_race.append("white")
    else:
        new_race.append('others')

df_fatalities['race'] = new_race
print(df_fatalities.head(5))

# ----------------donut chart----------------------------
death = []
for i in df_fatalities["manner_of_death"]:
    if i in ["shot", 'shot and Tasered']:
        death.append(1)
df_fatalities["death"] = death

deaths_by_race = df_fatalities.groupby("race")['death'].value_counts()
print(deaths_by_race)

death_race = px.pie(df_fatalities,
                    names='race',
                    values='death',
                    color='race',
                    title="Number of deaths by race",
                    hole=0.5)
death_race.show()

# --------death by gender----------------
death_gender = df_fatalities.groupby("gender")["death"].value_counts()
print(death_gender)

deaths_by_gender = px.bar(df_fatalities,
                          x=df_fatalities.gender,
                          y=df_fatalities.death,
                          title="Death by gender",
                          labels={'death': 'Total Deaths'})
deaths_by_gender.show()

# -------------------Box Plot Showing the Age and Manner of Death------------------------
manner_age = px.box(df_fatalities, x="age",
                    y="manner_of_death",
                    title="Age and Manner of Death")
manner_age.show()

# ----------------------armed pople---------------------
print("weapons as int")
armed = df_fatalities["armed"]
# print(armed.unique())

no_arms = ['unarmed', 'toy weapon', 'flashlight']

short_arms = ['knife', 'shovel', 'hammer',
              'hatchet', 'sword', 'machete', 'box cutter', 'metal object',
              'screwdriver', 'lawn mower blade', 'flagpole', 'cordless drill',
              'metal pole', 'Taser', 'metal pipe', 'metal hand tool', 'blunt object',
              'metal stick', 'sharp object', 'meat cleaver', 'carjack', 'chain',
              "contractor's level", 'stapler', 'beer bottle', 'baseball bat and fireplace poker',
              'straight edge razor', 'gun and knife', 'ax', 'brick', 'baseball bat',
              'hand torch', 'chain saw', 'garden tool', 'scissors', 'pole', 'pick-axe',
              'flashlight', 'baton', 'spear', 'pitchfork', 'rock', 'piece of wood', 'bayonet', 'pipe',
              'glass shard', 'metal rake', 'crowbar', 'oar', 'tire iron', 'air conditioner',
              'pole and knife', 'baseball bat and bottle', 'pen']

long_range_arms = ['gun', 'nail gun', 'guns and explosives', 'bean-bag gun', 'gun and knife', 'hatchet and gun',
                   'machete and gun', "crossbow"]

others_arms = ['fireworks', 'vehicle', 'motorcycle', 'air conditioner']

unknown_arms = ['unknown weapon', 'undetermined']

arms_group = []
for i in armed:
    if i in no_arms:
        arms_group.append("unarmed")
    elif i in short_arms:
        arms_group.append("melee weapon")
    elif i in long_range_arms:
        arms_group.append("firearms and long range weapons")
    elif i in others_arms:
        arms_group.append("wierd objects as arms")
    else:
        arms_group.append("undetermined")

df_fatalities["arms_group"] = arms_group

weapon_used_bar = px.bar(df_fatalities,
                         x="arms_group",
                         title="Weapon usage against police")
weapon_used_bar.show()

print("----------Age of people killed---------------")
grouped_age = df_fatalities.groupby('age')['age'].value_counts()

age_of_dead = px.bar(grouped_age,
                     y=grouped_age,
                     title="Age of killed peoples")
age_of_dead.show()

# ---------------ages by races---------------------------
races_ages = df_fatalities[['race', 'age']]
print(races_ages.head(5))

sns.set(style='whitegrid')  # set style for the plot

plt.figure(figsize=(10, 6))
sns.kdeplot(data=races_ages,
            x='age',
            hue="race",
            fill=True,
            common_norm=False,
            palette='husl')
plt.xlabel('age')
plt.ylabel('Density')
plt.title('Kernel Density estimate of age distribution by age')
plt.show()

# ----------percentages by age of people killed by police----------
death_age = px.pie(df_fatalities,
                   names='age',
                   values='age',
                   color='age',
                   title="Percentage of age",
                   hole=0.5)
death_age.show()

print(" ----what percentage was under age of 25--------")
age_col = df_fatalities['age']

under = []
over = []
for i in age_col:
    if i <= 25:
        under.append(1)
    else:
        over.append(1)

one_perc = (len(under) + len(over))/100

print(f"Percentage of ages under 25 is {round(len(under)/one_perc, 2)}")
print(f"Percentage of ages over 25 is {round(len(over)/one_perc, 2)}\n")

# -----------Mental illness and police killings--------------

ment_pie = px.bar(df_fatalities,
                  x='signs_of_mental_illness',
                  color='signs_of_mental_illness',
                  title='Percentage of mental illness',
                  )
ment_pie.show()

ment_df = df_fatalities['signs_of_mental_illness']
not_mental = []
mental = []

for i in ment_df:
    if i:
        mental.append(1)
    else:
        not_mental.append(1)
one_perc1 = ((len(not_mental) + len(mental)) / 100)

print(f"Percentage of mentally ill people: {round(len(mental)/one_perc1, 2)}")
print(f"Percentage of not mentally ill people: {round(len(not_mental)/one_perc1, 2)}")

# ---------------Most killings in cities------

most_killings_per_citi = df_fatalities["city"].value_counts().head(10)
print(most_killings_per_citi)

violent_cities = px.line(most_killings_per_citi,
                         x=most_killings_per_citi.index,
                         y='count')

violent_cities.show()

# ------------top 10 cities dataframe-------------------
top_10_violent = list(most_killings_per_citi.index)  # for boolean index
top_10_df = df_fatalities[df_fatalities['city'].isin(top_10_violent)]
# print(top_10_df.head(10))

race_deaths = top_10_df.groupby(['city', 'race'])['death'].sum().reset_index()
# print(race_deaths)

city_race_death = px.sunburst(race_deaths,
                              path=['city', 'race'],
                              values='death',
                              title='Rate of death by race in top 10 violent cities',
                              )
city_race_death.show()

# ---------------choropleth map of police killings in us states-----------------
us_states = df_fatalities["state"]
# print(us_states.head(10))

# create country codes for Chorolpleth map
country_codes = []
for i in us_states:
    state = pycountry.subdivisions.get(code=f"US-{i}")
    country_codes.append(state.code)

full_names = []
for j in us_states:
    state = pycountry.subdivisions.get(code=f"US-{j}")
    full_names.append(state.name)

df_fatalities['Country_Codes'] = country_codes
df_fatalities["Country_Names"] = full_names
# ----------------------------------------

death_counts = df_fatalities.groupby('state')['death'].value_counts()
state_names = df_fatalities["Country_Names"].unique()

data = dict(type='choropleth',
            locations=df_fatalities['state'].unique(),
            locationmode='USA-states',
            text=state_names,
            z=death_counts)

layout = dict(geo=dict(scope='usa',
                       showlakes=False))

police_killings = go.Figure(data=[data], layout=layout)
police_killings.show()

# Number of Police Killings Over Time

str_dates = df_fatalities['date']

date = []
for row in str_dates:
    date_string = f"{row[0:2]}-{row[3:5]}-20{row[6:]}"
    date_time = datetime.strptime(date_string, '%d-%m-%Y')
    date.append(date_time)

df_fatalities['date'] = date

killings_over_time = df_fatalities.groupby('date')['death'].value_counts()
print(killings_over_time)

killings_time_line = go.Figure()
killings_time_line.add_trace(go.Scatter(x=df_fatalities['date'].unique(), y=killings_over_time,
                                        mode='lines+markers',
                                        name="Number of deaths over time"))
killings_time_line.update_layout(title='Number of deaths over Time',
                                 xaxis_title='Dates',
                                 yaxis_title='number of deaths')
killings_time_line.show()
