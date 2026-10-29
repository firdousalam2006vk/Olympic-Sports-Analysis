"""
Script 04: Generate High-Resolution Visualizations for Report & Presentation
===========================================================================
Project: Global Olympic Sports Performance Analysis
Design System: Navy Blue (#1B365D), Slate Blue (#2E6B9E), Accent Gold (#D4AF37),
               and Clean Background (#F8FAFC).
"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

NAVY = "#1B365D"
SLATE = "#2E6B9E"
SKY = "#4A90E2"
GOLD = "#D4AF37"
SILVER = "#A0AAB2"
BRONZE = "#CD7F32"
BG_COLOR = "#F8FAFC"
TEXT_DARK = "#1E293B"

CHARTS_DIR = os.path.join("exports", "charts")
PROCESSED_DIR = os.path.join("data", "processed")
os.makedirs(CHARTS_DIR, exist_ok=True)

def generate_charts():
    print("Loading processed data for chart generation...")
    athletes_df = pd.read_csv(os.path.join(PROCESSED_DIR, "athletes.csv"), low_memory=False)
    medals_df = pd.read_csv(os.path.join(PROCESSED_DIR, "medal_results.csv"))
    host_df = pd.read_csv(os.path.join(PROCESSED_DIR, "host_nation_performance.csv"))
    reg_df = pd.read_csv(os.path.join(PROCESSED_DIR, "regional_sports_efficiency.csv"))
    funding_df = pd.read_csv(os.path.join(PROCESSED_DIR, "sports_funding_benchmark.csv"))

    # -------------------------------------------------------------
    # Chart 1: All-Time Top 15 Countries by Medal Distribution
    # -------------------------------------------------------------
    print("Generating Chart 1: Top 15 Countries Medal Distribution...")
    top_nations = medals_df.groupby(['noc', 'country']).agg(
        gold=('gold', 'sum'),
        silver=('silver', 'sum'),
        bronze=('bronze', 'sum'),
        total=('total_medals', 'sum')
    ).reset_index().sort_values('gold', ascending=False).head(15).iloc[::-1]

    fig, ax = plt.subplots(figsize=(11, 7), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    y_pos = np.arange(len(top_nations))
    b_bronze = ax.barh(y_pos, top_nations['bronze'], color=BRONZE, label='Bronze', height=0.65, edgecolor='none')
    b_silver = ax.barh(y_pos, top_nations['silver'], left=top_nations['bronze'], color=SILVER, label='Silver', height=0.65, edgecolor='none')
    b_gold = ax.barh(y_pos, top_nations['gold'], left=top_nations['bronze'] + top_nations['silver'], color=GOLD, label='Gold', height=0.65, edgecolor='none')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_nations['country'], fontsize=11, fontweight='bold', color=TEXT_DARK)
    ax.set_xlabel("Official Event Medals Won", fontsize=11, fontweight='bold', color=NAVY, labelpad=10)
    ax.set_title("All-Time Top 15 Olympic Nations by Medal Type (1896-2016)", fontsize=14, fontweight='heavy', color=NAVY, pad=15)
    ax.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='#CBD5E1', fontsize=10)
    
    # Value annotations on total
    for i, (_, row) in enumerate(top_nations.iterrows()):
        ax.text(row['total'] + 25, i, f"{int(row['total']):,} ({int(row['gold'])}G)", va='center', fontsize=9.5, fontweight='bold', color=NAVY)

    ax.set_xlim(0, top_nations['total'].max() + 350)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')
    plt.tight_layout()
    chart1_path = os.path.join(CHARTS_DIR, "01_top_15_countries_medals.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Chart 2: Athlete Participation & Gender Trajectory (Summer)
    # -------------------------------------------------------------
    print("Generating Chart 2: Gender Participation Trajectory...")
    summer_athletes = athletes_df[athletes_df['season'] == 'Summer']
    gender_agg = summer_athletes.groupby(['year', 'sex'])['athlete_id'].nunique().unstack(fill_value=0).reset_index()
    gender_agg.columns = ['year', 'female', 'male']
    gender_agg['total'] = gender_agg['female'] + gender_agg['male']
    gender_agg['female_pct'] = (gender_agg['female'] / gender_agg['total']) * 100

    fig, ax1 = plt.subplots(figsize=(11, 6), facecolor=BG_COLOR)
    ax1.set_facecolor(BG_COLOR)

    ax1.plot(gender_agg['year'], gender_agg['male'], color=SLATE, linewidth=2.5, marker='o', markersize=4, label='Male Athletes')
    ax1.plot(gender_agg['year'], gender_agg['female'], color=GOLD, linewidth=2.5, marker='s', markersize=4, label='Female Athletes')
    ax1.set_xlabel("Olympic Year", fontsize=11, fontweight='bold', color=NAVY, labelpad=10)
    ax1.set_ylabel("Number of Participating Athletes", fontsize=11, fontweight='bold', color=NAVY, labelpad=10)
    ax1.set_title("Evolution of Athlete Participation and Gender Parity (Summer Games)", fontsize=14, fontweight='heavy', color=NAVY, pad=15)
    ax1.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='#CBD5E1', fontsize=10)

    # Secondary axis for female % share
    ax2 = ax1.twinx()
    ax2.plot(gender_agg['year'], gender_agg['female_pct'], color='#E11D48', linestyle='--', linewidth=2, label='Female Share (%)')
    ax2.set_ylabel("Female Athlete Share (%)", fontsize=11, fontweight='bold', color='#E11D48', labelpad=10)
    ax2.yaxis.set_major_formatter(ticker.PercentFormatter(100, decimals=0))
    ax2.set_ylim(0, 60)
    ax2.legend(loc='center left', frameon=True, facecolor='white', edgecolor='#CBD5E1', fontsize=10)

    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    plt.tight_layout()
    chart2_path = os.path.join(CHARTS_DIR, "02_gender_participation_trajectory.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Chart 3: Host Nation Advantage (Host Bump Analysis)
    # -------------------------------------------------------------
    print("Generating Chart 3: Host Nation Advantage...")
    host_clean = host_df.dropna(subset=['pre_medals', 'host_medals', 'post_medals']).tail(8).copy()
    
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    x = np.arange(len(host_clean))
    width = 0.26

    rects1 = ax.bar(x - width, host_clean['pre_medals'], width, label='Pre-Host Games (t-1)', color=SILVER)
    rects2 = ax.bar(x, host_clean['host_medals'], width, label='Host Year (t=0)', color=NAVY)
    rects3 = ax.bar(x + width, host_clean['post_medals'], width, label='Post-Host Games (t+1)', color=SLATE)

    ax.set_xticks(x)
    labels = [f"{row['country']}\n({int(row['host_year'])})" for _, row in host_clean.iterrows()]
    ax.set_xticklabels(labels, fontsize=10, fontweight='bold', color=TEXT_DARK)
    ax.set_ylabel("Official Medals Won", fontsize=11, fontweight='bold', color=NAVY, labelpad=10)
    ax.set_title("The 'Host Nation Advantage': Pre vs. Host vs. Post Performance", fontsize=14, fontweight='heavy', color=NAVY, pad=15)
    ax.legend(frameon=True, facecolor='white', edgecolor='#CBD5E1', fontsize=10)

    # Highlight bump percentages
    for i, (_, row) in enumerate(host_clean.iterrows()):
        bump = int(row['medal_bump'])
        pct = row['medal_bump_pct']
        sign = "+" if bump > 0 else ""
        ax.annotate(f"{sign}{bump} ({sign}{pct:.0f}%)",
                    xy=(i, row['host_medals']),
                    xytext=(0, 6), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='heavy', color='#0F766E')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    chart3_path = os.path.join(CHARTS_DIR, "03_host_nation_advantage.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Chart 4: Regional Medal Conversion Efficiency
    # -------------------------------------------------------------
    print("Generating Chart 4: Regional Sports Efficiency...")
    reg_clean = reg_df[~reg_df['continent'].isin(['Other', 'Special'])].sort_values('medals_per_100_athletes', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    bars = ax.bar(reg_clean['continent'], reg_clean['medals_per_100_athletes'], color=[NAVY, SLATE, SKY, GOLD, '#F97316'], width=0.55)
    ax.set_ylabel("Medal Conversion Rate (Medals / 100 Athletes)", fontsize=11, fontweight='bold', color=NAVY, labelpad=10)
    ax.set_title("Continental Sports Efficiency: Medals Won per 100 Participating Athletes", fontsize=14, fontweight='heavy', color=NAVY, pad=15)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10.5, fontweight='bold', color=NAVY)

    ax.set_ylim(0, 14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    chart4_path = os.path.join(CHARTS_DIR, "04_regional_conversion_efficiency.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Chart 5: Sports Investment vs. Medal Return (UK Sport Benchmark)
    # -------------------------------------------------------------
    print("Generating Chart 5: Sports Investment vs. Medal Return Scatter...")
    rio_f = funding_df[funding_df['cycle'] == 'Rio 2016'].copy()

    fig, ax = plt.subplots(figsize=(11, 6.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    scatter = ax.scatter(rio_f['funding_millions_gbp'], rio_f['medals_won'],
                         s=rio_f['funding_millions_gbp'] * 18, c=NAVY, alpha=0.85, edgecolors='white', linewidth=1.5)

    # Trendline
    m, b = np.polyfit(rio_f['funding_millions_gbp'], rio_f['medals_won'], 1)
    x_vals = np.linspace(0, 36, 100)
    ax.plot(x_vals, m * x_vals + b, color='#DC2626', linestyle='--', linewidth=2, label=f'Linear Fit (r = 0.752)')

    # Labels for notable sports
    for _, r in rio_f.iterrows():
        offset_y = 0.3 if r['sport'] not in ['Rowing', 'Cycling'] else -0.7
        ax.text(r['funding_millions_gbp'] + 0.5, r['medals_won'] + offset_y, r['sport'], fontsize=9, fontweight='bold', color=TEXT_DARK)

    ax.set_xlabel("High-Performance Investment (Million £ GBP)", fontsize=11, fontweight='bold', color=NAVY, labelpad=10)
    ax.set_ylabel("Olympic Medals Won (Rio 2016)", fontsize=11, fontweight='bold', color=NAVY, labelpad=10)
    ax.set_title("Capital vs. Podium: UK Sport High-Performance Funding vs. Medal Returns", fontsize=14, fontweight='heavy', color=NAVY, pad=15)
    ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='#CBD5E1', fontsize=10)

    ax.text(0.98, 0.04, "Data Source: UK Sport Official Rio 2016 High Performance Allocations (Verified Benchmark)",
            transform=ax.transAxes, ha='right', fontsize=8.5, fontstyle='italic', color='#64748B')

    ax.set_xlim(0, 36)
    ax.set_ylim(-1, 14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    chart5_path = os.path.join(CHARTS_DIR, "05_sports_funding_vs_medals_scatter.png")
    plt.savefig(chart5_path, dpi=300)
    plt.close()

    print("\n[SUCCESS] All 5 high-resolution charts generated in exports/charts/")

if __name__ == "__main__":
    generate_charts()

