import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the data
df = pd.read_csv('amb_csv/amb.csv', encoding='latin-1')

# Display basic info
print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nData types:")
print(df.dtypes)

# Convert numerical columns (some might be strings)
numeric_cols = ['Altitude', 'Decl1', 'Decl2', 'Decl3', 'Decl4', 'Aspecto',
                'Prof1', 'Prof2', 'Prof3', 'Prof4', 'Rocha1', 'Rocha2', 'Rocha3', 'Rocha4',
                'Solo1', 'Solo2', 'Solo3', 'Solo4', 'Biom1', 'Biom2', 'Biom3', 'Biom4',
                'Serra1', 'Serra2', 'Serra3', 'Serra4', 'esp_serra1', 'esp_serra2', 'esp_serra3', 'esp_serra4',
                'grimpa1', 'grimpa2', 'grimpa3', 'grimpa4', 'hmax', 'dossel', 'agua', 'Gado', 'Veg', 'Fogo']

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Handle missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# Fill missing values with median for numerical columns
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

# Basic statistics
print("\nDescriptive statistics:")
print(df[numeric_cols].describe())

# Vegetation types
print("\nVegetation types:")
print(df['tipo.veg'].value_counts())

# Altitude distribution
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Altitude', bins=30, kde=True)
plt.title('Distribution of Altitude')
plt.xlabel('Altitude (m)')
plt.ylabel('Frequency')
plt.savefig('altitude_distribution.png')
plt.close()

# Biomass vs Altitude
plt.figure(figsize=(10, 6))
biomass_cols = ['Biom1', 'Biom2', 'Biom3', 'Biom4']
df['Biomass_mean'] = df[biomass_cols].mean(axis=1)
sns.scatterplot(x='Altitude', y='Biomass_mean', data=df, hue='tipo.veg')
plt.title('Biomass vs Altitude by Vegetation Type')
plt.xlabel('Altitude (m)')
plt.ylabel('Mean Biomass (%)')
plt.savefig('biomass_vs_altitude.png')
plt.close()

# Canopy cover vs Altitude
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Altitude', y='dossel', data=df, hue='tipo.veg')
plt.title('Canopy Cover vs Altitude by Vegetation Type')
plt.xlabel('Altitude (m)')
plt.ylabel('Canopy Cover (%)')
plt.savefig('canopy_vs_altitude.png')
plt.close()

# Litter (Serra) vs Altitude
serra_cols = ['Serra1', 'Serra2', 'Serra3', 'Serra4']
df['Serra_mean'] = df[serra_cols].mean(axis=1)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Altitude', y='Serra_mean', data=df, hue='tipo.veg')
plt.title('Litter Cover vs Altitude by Vegetation Type')
plt.xlabel('Altitude (m)')
plt.ylabel('Mean Litter Cover (%)')
plt.savefig('litter_vs_altitude.png')
plt.close()

# Correlations
corr_cols = ['Altitude', 'Biomass_mean', 'dossel', 'Serra_mean', 'hmax', 'Gado', 'Fogo']
correlation_matrix = df[corr_cols].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.savefig('correlation_matrix.png')
plt.close()

# Group by vegetation type
veg_stats = df.groupby('tipo.veg')[numeric_cols].mean()
print("\nMean values by vegetation type:")
print(veg_stats)

# Altitude gradients
altitude_bins = pd.cut(df['Altitude'], bins=5)
altitude_groups = df.groupby(altitude_bins)[['Biomass_mean', 'dossel', 'Serra_mean']].mean()
print("\nVegetation characteristics by altitude range:")
print(altitude_groups)

# Impact of disturbances
# Check if disturbance columns have data
if df['Gado'].notna().sum() > 10 and df['Fogo'].notna().sum() > 10 and df['Veg'].notna().sum() > 10:
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    sns.boxplot(x='Gado', y='Biomass_mean', data=df)
    plt.title('Biomass vs Cattle Presence')

    plt.subplot(1, 3, 2)
    sns.boxplot(x='Fogo', y='Biomass_mean', data=df)
    plt.title('Biomass vs Fire Presence')

    plt.subplot(1, 3, 3)
    sns.boxplot(x='Veg', y='Biomass_mean', data=df)
    plt.title('Biomass vs Vegetation Disturbance')

    plt.tight_layout()
    plt.savefig('disturbance_impacts.png')
    plt.close()
else:
    print("Disturbance columns have insufficient data for analysis")

# Species richness (esp_serra) analysis
esp_cols = ['esp_serra1', 'esp_serra2', 'esp_serra3', 'esp_serra4']
df['Species_richness'] = df[esp_cols].sum(axis=1)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Altitude', y='Species_richness', data=df, hue='tipo.veg')
plt.title('Species Richness vs Altitude by Vegetation Type')
plt.xlabel('Altitude (m)')
plt.ylabel('Species Richness')
plt.savefig('species_richness_vs_altitude.png')
plt.close()

# Save processed data
df.to_csv('processed_amb_data.csv', index=False)

print("\nAnalysis complete. Plots saved as PNG files.")