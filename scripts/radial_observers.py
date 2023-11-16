import numpy as np 
import plotly.graph_objects as go 

lambdaD = 48
theta = np.linspace(0,np.pi, 15)
r = np.array([0.5, 1, 1.5, 2])*lambdaD

x = lambda r: r*np.cos(theta)
y = lambda r: r*np.sin(theta)

fig = go.Figure()

for ri in r:
    fig.add_trace(
        go.Scatter(
            x = x(ri),
            y = y(ri),
            mode = 'lines+markers',
            line = dict(color = 'black', dash = 'dash'),
            opacity = 0.7,
            showlegend=False
        )
        
    )

r2  = np.arange(-2,-2.5, 0.5)

fig.update_xaxes(title_text = r'$\lambda_D$', tickvals = lambdaD*r2, ticktext = [f'{i}' for i in r])
fig.update_yaxes(title_text = '', showticklabels = False)

fig.show()