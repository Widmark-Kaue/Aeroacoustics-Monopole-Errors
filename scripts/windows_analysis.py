#%% lib
import numpy as np 
import plotly.graph_objects as go

from src.path import PATH_DATA, PATH_IMAGES
from json import load
#%%
with open(PATH_DATA.joinpath('monopoleFlow','analytical', 'monopole_10Hz_M0.2.json'), 'r') as file:
    mono = load(file)

nx   = mono['nx']
ny   = mono['ny']
ypos = np.linspace(mono['ylim'][0], mono['ylim'][1], ny).searchsorted(0) 
x    = np.linspace(mono['xlim'][0], mono['xlim'][1], nx)
p    = np.array(mono['time']['2']).T[ypos] 
#%% plot
lambdaD = 42
vals = [-3, -1, 0, 1, 3]
vals_without_0 = vals.remove(0)

#figure layout
layout = go.Layout(
    autosize=False,
    width=1000,
    height=500,
    margin=dict(l=10, r = 10, t = 25, b = 20),
)

fig = go.Figure(layout=layout)

fig.add_trace(
    go.Scatter(
        x = x,
        y = p,
        line = dict(color = 'black'),
        showlegend=False,
        name='Monopole flow'
    )
)

for ni,i in enumerate(vals):
    if not i==0:
        fig.add_vline(
            x = i*lambdaD,
            line = dict(color = 'blue', dash = 'dash'),
            opacity = 0.5,
            annotation = dict(text = f'Janela {ni+1}' if ni < len(vals)-1 else ''),
        )

fig.update_xaxes(
    title_text  = r'$x/\lambda_d$', 
    tickvals = np.array(vals)*lambdaD,
    ticktext = [f'{i}' for i in vals],
    ticks = 'outside',
    linecolor = 'black',
    mirror = True)

fig.update_yaxes(
    # title_text = r'$P \ [Pa]$', 
    showgrid = True,
    showticklabels = False,
    )

fig.update_layout(
    template = 'plotly_white',
    font = dict(color = 'black', family = 'Times', size = 22)
)

fig.show()
fig.write_image(PATH_IMAGES.joinpath('windows_analysis.png'),format = 'png', scale = 5)
# %%
