import nflreadpy as nfl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
from scipy.stats import t

# Importing as polars df
print("Loading Data . . .")
ps = nfl.load_player_stats(seasons=(2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024), summary_level=("reg"))

# Transferring to pandas
player_stats = ps.to_pandas()

# Picking and filtering columns
player_stats = player_stats[[
'player_id',
'player_display_name',
'position',
'season',
'games',
'fantasy_points',
'carries'
]]
player_stats = player_stats[player_stats['position'].str.contains('RB', na=False)]
player_stats = player_stats[player_stats['carries'] > 75]

# Creating fantasy points per game average column
player_stats['fantasy_points_per_game'] = player_stats['fantasy_points']/player_stats['games']

# Sorting values
player_stats = player_stats.sort_values(by='fantasy_points_per_game', ascending=False)

# Just the FPTS/G
fppg_data = player_stats['fantasy_points_per_game']

# Calcs
median_fppg = fppg_data.median()
mean_fppg = fppg_data.mean()
q1_fppg = fppg_data.quantile(0.25)
q3_fppg = fppg_data.quantile(0.75)
iqr_fppg = q3_fppg - q1_fppg
lower_fence = q1_fppg - (1.5 * iqr_fppg)
upper_fence = q3_fppg + (1.5 * iqr_fppg)
min_fppg = fppg_data.min()
max_fppg = fppg_data.max()
outliers = fppg_data[(fppg_data < lower_fence) | (fppg_data > upper_fence)]
outlier_percentage = (len(outliers) / len(fppg_data)) * 100
std_dev_fppg = fppg_data.std()
t_statistic = (mean_fppg - 8) / (std_dev_fppg/(445**0.5))
degrees_of_freedom = len(fppg_data) - 1
p_value = 2 * t.sf(abs(t_statistic), degrees_of_freedom)

# Print Statements
print("\n----------------------")
print("\n| Summary Statistics |")
print("\n----------------------\n")
print (f"Median FP/G: {median_fppg:.2f}")
print (f"Mean FP/G: {mean_fppg:.2f}")
print (f"Min: {min_fppg:.2f}")
print (f"Max: {max_fppg:.2f}")
print (f"Q1 (25th Pctl): {q1_fppg:.2f}")
print (f"Q3 (75th Pctl): {q3_fppg:.2f}")
print (f"IQR: {iqr_fppg:.2f}")
print (f"Lower Outlier Fence: {lower_fence:.2f}")
print (f"Upper Outlier Fence: {upper_fence:.2f}")
print (f"Outliers Found (#): {len(outliers)}")
print (f"Outliers Found (%): {outlier_percentage:.2f}%")
print (f"Data Points: {len(fppg_data)}")
print (f"Standard Deviation: {std_dev_fppg:.2f}")
print (f"T Statistic: {t_statistic:.2f}")
print (f"P-value: {p_value:.4e}")
input("\nPress Enter to view graphs. . .")

# Histogram
plt.figure(figsize=(10, 6))

sns.histplot(fppg_data, bins=25, kde=False, color='#816EC7', alpha=1.0)

plt.axvline(median_fppg, color='red', linestyle='--', linewidth=2, label=f'Median: {median_fppg:.2f}')
plt.axvline(mean_fppg, color='darkorange', linestyle='-', linewidth=2, label=f'Mean: {mean_fppg:.2f}')

plt.title('Distribution of Fantasy Points Per Game (Min 75 Carries)', fontsize=16)
plt.xlabel('Fantasy Points Per Game', fontsize=12)
plt.ylabel('Frequency (Players)', fontsize=12)
plt.legend(loc='upper right')
plt.grid(axis='y', alpha=0.5)

plt.tight_layout()
#plt.savefig('fppg_histogram.png', bbox_inches='tight')
plt.show()

#Box Plot
plt.figure(figsize=(10, 6))

sns.boxplot(x=fppg_data, showmeans=True, meanline=False, meanprops={'marker':'D', 
                                                                    'markerfacecolor':'yellow', 
                                                                    'markeredgecolor':'darkorange', 
                                                                    'markersize':'8'}, 
                                                                    color='#816EC7')

plt.title('Fantasy Points Per Game (Min 75 Carries)', fontsize=16)
plt.xlabel('Fantasy Points Per Game', fontsize=12)

custom_lines = [
    Line2D([0], [0], color='red', lw=0, label=f'Median: {median_fppg:.2f}'),
    Line2D([0], [0], color='darkorange', marker='D', markerfacecolor='yellow', markeredgecolor='darkorange', markersize=8, lw=0, label=f'Mean: {mean_fppg:.2f}'),
    Line2D([0], [0], color='black', marker='o', lw=0, label='Outliers'),
    Line2D([0], [0], color='blue', linestyle='--', label=f'Upper Fence: {upper_fence:.2f}'),
    Line2D([0], [0], color='blue', linestyle=':', label=f'Lower Fence: {lower_fence:.2f}'),
]

# Manually adding the IQR range and Quartiles to the legend
plt.text(
    0.95, 0.95,
    f'Q1: {q1_fppg:.2f}\nQ3: {q3_fppg:.2f}\nIQR: {iqr_fppg:.2f}\nLower Fence: {lower_fence:.2f}\nUpper Fence: {upper_fence:.2f}\nOutliers in Data: {outlier_percentage:.2f}%',
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment='top',
    horizontalalignment='right',
    bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.7)
)

plt.tight_layout()
#plt.savefig('fppg_boxplot.png', bbox_inches='tight')
plt.show()