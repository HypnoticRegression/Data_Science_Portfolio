#3d Modeling with plotly

#Import needed packages
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px 
from scipy.interpolate import griddata



doc = pd.read_csv(r'S:\Data\federal_funding_rates.csv')

df = doc.copy()
df.head()


x = df['Month']
y = df['Year']
z = df['Federal Funding Rate']

####Create meshgrid for x,y
xi = np.linspace(min(x), max(x), num=100)
yi = np.linspace(min(y), max(y), num=100)

x_grid, y_grid = np.meshgrid(xi,yi)

#Grid data
z_grid = griddata((x,y),z,(x_grid,y_grid),method='nearest')

# Plotly 3D Surface
fig = go.Figure(go.Surface(x=x_grid,y=y_grid,z=z_grid,
                       colorscale='turbo'))

fig.update_layout(width= 900, height = 700,scene=dict(xaxis_title='Month',yaxis_title='Year',zaxis_title='Federal Funds Rate'))

fig.show()
