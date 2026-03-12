import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

# =========================================================
#  Loading Data
# =========================================================
try:
    df = pd.read_csv('users.csv')
    print("--- Data Loaded from CSV Successfully ---")
except FileNotFoundError:
    print("Error: 'users.csv' not found. Please run read.py first!")
    exit()

# =========================================================
#  Basic Data Exploration
# =========================================================

print("       BASIC DATA EXPLORATION REPORT       ")
print(f"[•] Shape: {df.shape}")
print(f"\n[•] Column Names:\n{df.columns.tolist()}")
print(f"\n[•] Data Types:\n{df.dtypes}")
print(f"\n[•] Missing Values:\n{df.isnull().sum()}")
print(f"\n[•] Number of Duplicate Rows: {df.duplicated().sum()}")
print("\n[•] Summary Statistics (Numeric):")
print(df.describe())

print("\n[•] Categorical Value Counts:")
for col in ['gender', 'bloodGroup', 'eyeColor', 'role']:
    if col in df.columns:
        print(f"\n- {col}:\n{df[col].value_counts()}")

# =========================================================
# 3. Data Cleaning / Preparation
# =========================================================
def extract_address_info(addr, key):
    try:
        if isinstance(addr, str):
            addr = json.loads(addr.replace("'", "\""))
        return addr.get(key, 'Unknown')
    except: return 'Unknown'

if 'address' in df.columns:
    df['country'] = df['address'].apply(lambda x: extract_address_info(x, 'country'))
    df['city'] = df['address'].apply(lambda x: extract_address_info(x, 'city'))
    print(f"\n[•] Value counts for country (Extracted):\n{df['country'].value_counts()}")

# Handle missing values in age, height, and weight
df['age'] = df['age'].fillna(df['age'].median())
df['height'] = df['height'].fillna(df['height'].mean())
df['weight'] = df['weight'].fillna(df['weight'].mean())

# Handling maidenName if missing 
if 'maidenName' in df.columns:
    df['maidenName'] = df['maidenName'].fillna('Unknown')

print("\n--- Data Cleaning Complete ---")

# =========================================================
# 4. Project Analysis Questions
# =========================================================

print("          ANALYSIS ANSWERS           ")
print(f"1. Average age of users: {df['age'].mean():.2f}")
print(f"\n2. Average age by gender:\n{df.groupby('gender')['age'].mean()}")
print(f"\n3. Number of users per gender:\n{df['gender'].value_counts()}")
print(f"\n4. Top 10 cities with most users:\n{df['city'].value_counts().head(10)}")
print(f"\n5. Average Height: {df['height'].mean():.2f}, Average Weight: {df['weight'].mean():.2f}")
print("\n6. Relationship Analysis: Check Visualizations (Scatter/Regression plots)")

# =========================================================
# Visualizations 
# =========================================================
sns.set_theme(style="whitegrid")
plt.figure(figsize=(18, 12)) 

# Plot 1: Gender 
plt.subplot(2, 3, 1) 
sns.countplot(data=df, x='gender', hue='gender', palette='pastel', legend=False)
plt.title('Users per Gender', fontweight='bold', fontsize=12)

# Plot 2: Top 10 Cities
plt.subplot(2, 3, 2)
city_counts = df['city'].value_counts().head(10)
sns.barplot(x=city_counts.values, y=city_counts.index, hue=city_counts.index, palette='viridis', legend=False)
plt.title('Top 10 Cities', fontweight='bold', fontsize=12)

# Plot 3: Blood Group 
plt.subplot(2, 3, 3) 
sns.countplot(data=df, x='bloodGroup', hue='bloodGroup', palette='magma', order=df['bloodGroup'].value_counts().index, legend=False)
plt.title('Users by Blood Group', fontweight='bold', fontsize=12)
plt.xticks(rotation=45)

# Plot 4: Age vs Weight 
plt.subplot(2, 3, 4) 
sns.scatterplot(data=df, x='age', y='weight', hue='gender', alpha=0.7)
plt.title('Relationship: Age vs Weight', fontweight='bold', fontsize=12)

# Plot 5: Height vs Weight 
plt.subplot(2, 3, 5) 
sns.regplot(data=df, x='height', y='weight', scatter_kws={'alpha':0.4}, line_kws={'color':'red'})
plt.title('Relationship: Height vs Weight', fontweight='bold', fontsize=12)

plt.tight_layout(pad=4.0)
plt.subplots_adjust(hspace=0.4, wspace=0.3)
print("\n--- Generating Visualization Dashboard ---")

# =========================================================
#  Export Formatting
# =========================================================


# Saving the final cleaned and sorted CSV
df.to_csv('cleaned_users.csv', index=False)
print("\n[SUCCESS] Cleaned data saved to 'cleaned_users.csv'")
plt.show()