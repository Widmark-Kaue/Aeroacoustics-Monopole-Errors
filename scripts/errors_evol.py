import numpy as np
import plotly.graph_objects as go
from src.path import PATH_IMAGES
from plotly.colors import DEFAULT_PLOTLY_COLORS as COLORS

x =     [8    ,   16,   32,   64]
w1 =    [68.74, 8.83, 3.93, 1.04]
w2 =    [22.02, 1.52, 3.37, 1.34]
w3 =    [18.62, 2.37, 0.24, 0.79]
Total = [30.99, 3.07, 3.17, 1.23]

fig = go.Figure(layout=go.Layout(
            autosize=False,
            width=1000,
            height=500,
            margin=dict(l=10, r = 10, t = 25, b = 20),
        ))

plotconfig = dict(
        xaxis = dict(
            ticks ='outside',
            linecolor = 'black',
            mirror =True
        ),
        yaxis = dict(
            ticks ='outside',
            linecolor = 'black',
            mirror =True
        )
)

fig.add_traces(
    [
        go.Scatter(x=x, 
                   y=w1, 
                   mode = 'lines+markers',
                   line = dict(color = COLORS[0]),
                   name="Janela 1",
                   opacity=0.85
                   ),
        go.Scatter(x=x,
                   y = w2,
                   mode = 'lines+markers',
                   line = dict(color = COLORS[1]),
                   name = 'Janela 2',
                   opacity=0.85
                   ),
        go.Scatter(x=x,
                   y =w3,
                   mode = 'lines+markers',
                   line = dict(color = COLORS[2]),
                   name = 'Janela 3', 
                   opacity=0.85
                   ),
        go.Scatter(x=x,
                   y = Total,
                   mode = 'lines+markers',
                   line = dict(color = 'black'),
                   name =  'Total',
                   opacity=0.85
                   
                   )
    ]
)

fig.update_layout(
    font = dict(
                color = 'black', 
                family = 'Times New Roman', 
                size = 22
            ),
            template = 'plotly_white',
            legend = dict(
                yanchor = 'top', 
                xanchor = 'right',
                x = 0.95, 
                font = dict(
                    family = 'Times New Roman',
                    size = 16,
                    color = 'black'
                ) 
            ),
            **plotconfig
)
fig.update_xaxes(title_text = r'$PPW$', tickvals = x)
fig.update_yaxes(title_text = r'$Erro \ [\%]$')

fig.show()
fig.write_image(PATH_IMAGES.joinpath('results', 'error', 'erros_spacial_comp_ppw.pdf'), format = 'pdf', scale = 5)
fig.write_html(PATH_IMAGES.joinpath('plotly-interactive', 'error', 'erros_spacial_comp_ppw.html'))