import plotly.graph_objects as go

# Dados
x = [1, 2, 3, 4, 5]
y = [10, 11, 9, 12, 8]

# Criar figura
fig = go.Figure()

# Adicionar linha ao gráfico
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Dados de Exemplo'))

# Configurações do layout
fig.update_layout(title='Gráfico de Linhas',
                  xaxis_title=r'$Eixo X$',
                  yaxis_title=r'$Eixo Y$')

# Mostrar gráfico
fig.show()
