import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from adjustText import adjust_text

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.linewidth': 0.5,
    'figure.dpi': 200,
})

MIRO = '#7AA383'
OPENAI = '#555555'
KIMI = '#D4714E'
MANUS = '#A3C4E0'
OTHER = '#C8C8C8'
TXT_COL = '#5B9BD5'
MM_COL = '#ED7D31'

OUT = 'images/'

# ═══════════════════════════════════════════════════════════════
# Fig 1: Dimension-Level Rank Bump Chart
# ═══════════════════════════════════════════════════════════════
models = [
    dict(name="Kimi-K2.5", short="Kimi", report=75.7, factuality=65.4, process=64.2, group="kimi"),
    dict(name="Doubao", short="Doubao", report=64.2, factuality=64.9, process=53.1, group="other"),
    dict(name="Grok", short="Grok", report=58.7, factuality=63.7, process=58.3, group="other"),
    dict(name="Qwen-3.5-Plus", short="Qwen", report=60.0, factuality=73.1, process=61.1, group="other"),
    dict(name="Manus", short="Manus", report=55.4, factuality=72.6, process=64.2, group="manus"),
    dict(name="ChatGLM", short="ChatGLM", report=63.2, factuality=68.6, process=65.6, group="other"),
    dict(name="MiniMax-M2.5", short="MiniMax", report=63.3, factuality=71.8, process=67.1, group="other"),
    dict(name="Claude-Opus-4.6", short="Claude", report=67.3, factuality=69.8, process=66.0, group="other"),
    dict(name="Gemini-3.1-Pro", short="Gemini", report=71.2, factuality=71.3, process=67.1, group="other"),
    dict(name="OpenAI Deep Research", short="OpenAI", report=73.8, factuality=83.3, process=73.1, group="openai"),
    dict(name="MiroThinker-1.7-mini", short="MT-1.7-mini", report=74.0, factuality=76.2, process=68.5, group="miro"),
    dict(name="MiroThinker-1.7", short="MT-1.7", report=74.3, factuality=79.4, process=72.7, group="miro"),
    dict(name="MiroThinker-H1", short="MT-H1", report=76.7, factuality=81.1, process=74.7, group="miro"),
]

dims = ['report', 'factuality', 'process']
for dim in dims:
    sorted_m = sorted(models, key=lambda m: -m[dim])
    for i, m in enumerate(sorted_m):
        m[dim + '_rank'] = i + 1

color_map = {'miro': MIRO, 'openai': OPENAI, 'kimi': KIMI, 'manus': MANUS, 'other': OTHER}
lw_map = {'miro': 2.5, 'openai': 2.0, 'kimi': 2.5, 'manus': 2.5, 'other': 1.0}
dot_map = {'miro': 6, 'openai': 5, 'kimi': 6, 'manus': 6, 'other': 4}
alpha_map = {'miro': 0.9, 'openai': 0.85, 'kimi': 0.9, 'manus': 0.9, 'other': 0.4}
z_map = {'other': 0, 'openai': 1, 'kimi': 2, 'manus': 2, 'miro': 3}

fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(-0.3, 2.3)
ax.set_ylim(len(models) + 0.5, 0.5)

dim_labels = ['Report', 'Factuality', 'Process']
for i, lbl in enumerate(dim_labels):
    ax.text(i, 0.15, lbl, ha='center', va='bottom', fontsize=13, fontweight='bold', color='#555')
    ax.axvline(i, color='#f0f0f0', lw=0.5, zorder=0)

for r in range(1, len(models) + 1):
    ax.axhline(r, color='#f5f5f5', lw=0.3, zorder=0)

sorted_models = sorted(models, key=lambda m: z_map[m['group']])
for m in sorted_models:
    ranks = [m['report_rank'], m['factuality_rank'], m['process_rank']]
    c = color_map[m['group']]
    a = alpha_map[m['group']]
    lw = lw_map[m['group']]
    dr = dot_map[m['group']]

    xs = [0, 1, 2]
    ax.plot(xs, ranks, color=c, lw=lw, alpha=a, zorder=z_map[m['group']] + 1, solid_capstyle='round')
    for xi, ri in zip(xs, ranks):
        ax.plot(xi, ri, 'o', color=c, markersize=dr, zorder=z_map[m['group']] + 2,
                markeredgecolor='white', markeredgewidth=0.8)

    # left label
    fw = 'bold' if m['group'] in ('miro', 'kimi', 'manus') else 'normal'
    fs = 10 if m['group'] != 'other' else 9
    ax.text(-0.08, m['report_rank'], m['short'], ha='right', va='center',
            fontsize=fs, fontweight=fw, color=c)
    # right label
    ax.text(2.08, m['process_rank'], m['short'], ha='left', va='center',
            fontsize=fs, fontweight=fw, color=c)

ax.set_xticks([])
ax.set_yticks([])
ax.spines[:].set_visible(False)
ax.set_title('Dimension-Level Rank Shifts (Text-Only)', fontsize=16, fontweight='bold',
             color='#1a1a2e', pad=35)

# Legend
legend_items = [
    mpatches.Patch(color=MIRO, label='MiroThinker'),
    mpatches.Patch(color=OPENAI, label='OpenAI'),
    mpatches.Patch(color=KIMI, label='Kimi-K2.5'),
    mpatches.Patch(color=MANUS, label='Manus'),
    mpatches.Patch(color=OTHER, label='Others'),
]
ax.legend(handles=legend_items, loc='lower center', bbox_to_anchor=(0.5, -0.06),
          ncol=5, frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig(OUT + 'fig1_dimension_rank_bump.png', bbox_inches='tight', facecolor='white')
plt.close()
print('✓ fig1_dimension_rank_bump.png')


# ═══════════════════════════════════════════════════════════════
# Fig 2: Process Quality vs. Overall Outcome Scatter
# ═══════════════════════════════════════════════════════════════
scatter_data = [
    dict(name="Kimi-K2.5", short="Kimi", x=64.2, y=68.4, group="other"),
    dict(name="Doubao", short="Doubao", x=53.1, y=60.7, group="other"),
    dict(name="Grok", short="Grok", x=58.3, y=60.2, group="other"),
    dict(name="Qwen-3.5-Plus", short="Qwen", x=61.1, y=64.7, group="other"),
    dict(name="Manus", short="Manus", x=64.2, y=64.0, group="other"),
    dict(name="ChatGLM", short="ChatGLM", x=65.6, y=65.8, group="other"),
    dict(name="MiniMax-M2.5", short="MiniMax", x=67.1, y=67.4, group="other"),
    dict(name="Claude-Opus-4.6", short="Claude", x=66.0, y=67.7, group="other"),
    dict(name="Gemini-3.1-Pro", short="Gemini", x=67.1, y=69.9, group="other"),
    dict(name="OpenAI Deep Research", short="OpenAI", x=73.1, y=76.7, group="openai"),
    dict(name="MiroThinker-1.7-mini", short="MT-1.7-mini", x=68.5, y=72.9, group="miro"),
    dict(name="MiroThinker-1.7", short="MT-1.7", x=72.7, y=75.5, group="miro"),
    dict(name="MiroThinker-H1", short="MT-H1", x=74.7, y=77.5, group="miro"),
]

scatter_colors = {'miro': MIRO, 'openai': OPENAI, 'other': '#B0B0B0'}
scatter_sizes = {'miro': 80, 'openai': 70, 'other': 45}
scatter_alpha = {'miro': 0.9, 'openai': 0.85, 'other': 0.6}
scatter_edge = {'miro': '#5A8A63', 'openai': '#333', 'other': '#999'}

fig, ax = plt.subplots(figsize=(9, 6.5))

xs = np.array([d['x'] for d in scatter_data])
ys = np.array([d['y'] for d in scatter_data])

# Linear regression
coeffs = np.polyfit(xs, ys, 1)
poly = np.poly1d(coeffs)
ss_res = np.sum((ys - poly(xs)) ** 2)
ss_tot = np.sum((ys - np.mean(ys)) ** 2)
r2 = 1 - ss_res / ss_tot

x_range = np.linspace(50, 78, 100)
ax.plot(x_range, poly(x_range), color=KIMI, ls='--', lw=1.5, alpha=0.7, zorder=1)

# Points
for d in sorted(scatter_data, key=lambda d: 0 if d['group'] == 'other' else 1):
    g = d['group']
    ax.scatter(d['x'], d['y'], s=scatter_sizes[g], c=scatter_colors[g],
               alpha=scatter_alpha[g], edgecolors=scatter_edge[g], linewidths=0.8, zorder=3)

# Labels — placed by adjustText to avoid overlaps
texts = []
for d in scatter_data:
    g = d['group']
    fw = 'bold' if g == 'miro' else 'normal'
    lc = MIRO if g == 'miro' else (OPENAI if g == 'openai' else '#777')
    t = ax.text(d['x'], d['y'], d['short'], fontsize=9, fontweight=fw, color=lc)
    texts.append(t)

adjust_text(texts, x=[d['x'] for d in scatter_data], y=[d['y'] for d in scatter_data],
            arrowprops=dict(arrowstyle='-', color='none', lw=0),
            force_text=(0.8, 0.8), force_points=(1.5, 1.5),
            expand_text=(1.2, 1.4), expand_points=(1.6, 1.6),
            only_move={'text': 'xy', 'points': 'xy'},
            max_move=30)

ax.text(0.97, 0.05, f'R² = {r2:.3f}', transform=ax.transAxes, ha='right',
        fontsize=12, fontstyle='italic', color=KIMI)

ax.set_xlabel('Process Score (Text-Only)', fontsize=13)
ax.set_ylabel('Overall Score (Text-Only)', fontsize=13)
ax.set_title('Process Quality vs. Overall Outcome', fontsize=16, fontweight='bold',
             color='#1a1a2e', pad=15)

ax.grid(True, alpha=0.15)
ax.spines['top'].set_color('#ddd')
ax.spines['right'].set_color('#ddd')
ax.spines['bottom'].set_color('#ddd')
ax.spines['left'].set_color('#ddd')
ax.tick_params(colors='#888')

plt.tight_layout()
plt.savefig(OUT + 'fig2_process_outcome_scatter.png', bbox_inches='tight', facecolor='white')
plt.close()
print('✓ fig2_process_outcome_scatter.png')


# ═══════════════════════════════════════════════════════════════
# Fig 3: Text-Only vs. Multimodal Dumbbell Chart
# ═══════════════════════════════════════════════════════════════
dumbbell_data = [
    dict(short="MT-H1", textOnly=77.5, multi=74.5, group="miro"),
    dict(short="OpenAI", textOnly=76.7, multi=70.2, group="openai"),
    dict(short="MT-1.7", textOnly=75.5, multi=71.6, group="miro"),
    dict(short="Gemini", textOnly=69.9, multi=68.1, group="other"),
    dict(short="Claude", textOnly=67.7, multi=66.4, group="other"),
    dict(short="MiniMax", textOnly=67.4, multi=63.3, group="other"),
    dict(short="ChatGLM", textOnly=65.8, multi=63.6, group="other"),
    dict(short="Qwen", textOnly=64.7, multi=56.1, group="other"),
    dict(short="Manus", textOnly=64.0, multi=62.0, group="other"),
    dict(short="Grok", textOnly=60.2, multi=60.5, group="other"),
]

for d in dumbbell_data:
    d['delta'] = d['multi'] - d['textOnly']

fig, ax = plt.subplots(figsize=(9, 5.5))

n = len(dumbbell_data)
y_pos = list(range(n))

for i, d in enumerate(dumbbell_data):
    is_miro = d['group'] == 'miro'
    line_c = MIRO if is_miro else '#D0D0D0'
    line_w = 2.5 if is_miro else 1.5

    lo = min(d['textOnly'], d['multi'])
    hi = max(d['textOnly'], d['multi'])
    ax.plot([lo, hi], [i, i], color=line_c, lw=line_w, solid_capstyle='round', zorder=2)
    ax.plot(d['textOnly'], i, 'o', color=TXT_COL, markersize=8,
            markeredgecolor='white', markeredgewidth=0.8, zorder=3)
    ax.plot(d['multi'], i, 'o', color=MM_COL, markersize=8,
            markeredgecolor='white', markeredgewidth=0.8, zorder=3)

    # Delta annotation
    delta_c = '#4CAF50' if d['delta'] > 0 else ('#D9534F' if d['delta'] < -5 else '#888')
    sign = '+' if d['delta'] > 0 else ''
    ax.text(82, i, f"{sign}{d['delta']:.1f}", ha='center', va='center',
            fontsize=10, fontweight='bold', color=delta_c)

ax.set_yticks(y_pos)
ax.set_yticklabels([d['short'] for d in dumbbell_data])
for i, d in enumerate(dumbbell_data):
    is_miro = d['group'] == 'miro'
    ax.get_yticklabels()[i].set_color(MIRO if is_miro else '#555')
    ax.get_yticklabels()[i].set_fontweight('bold' if is_miro else 'normal')

ax.invert_yaxis()
ax.set_xlim(53, 80)
ax.set_xlabel('Overall Score', fontsize=13)
ax.set_title('Text-Only vs. Multimodal: Overall Score Comparison', fontsize=16,
             fontweight='bold', color='#1a1a2e', pad=15)

# Delta header
ax.text(82, -0.8, 'Δ Drop', ha='center', va='center', fontsize=10,
        fontweight='bold', color='#888')

ax.grid(True, axis='x', alpha=0.15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#ddd')
ax.spines['left'].set_color('#ddd')
ax.tick_params(axis='y', length=0, pad=8)
ax.tick_params(axis='x', colors='#888')

# Legend
ax.plot([], [], 'o', color=TXT_COL, markersize=7, label='Text-Only')
ax.plot([], [], 'o', color=MM_COL, markersize=7, label='Multimodal')
ax.legend(loc='lower right', frameon=False, fontsize=10)

# Subtitle
ax.text(0.5, 1.02, 'Sorted by Text-Only overall score (descending)',
        transform=ax.transAxes, ha='center', fontsize=10, fontstyle='italic', color='#999')

plt.tight_layout()
plt.savefig(OUT + 'fig3_textonly_multimodal_dumbbell.png', bbox_inches='tight', facecolor='white')
plt.close()
print('✓ fig3_textonly_multimodal_dumbbell.png')

print('\nAll 3 figures generated.')
