import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# Mandelbrot generation function
def mandelbrot(xmin, xmax, ymin, ymax, width=500, height=500, max_iter=100):
	x = np.linspace(xmin, xmax, width)
	y = np.linspace(ymin, ymax, height)
	X, Y = np.meshgrid(x, y)
	C = X + 1j * Y
	Z = np.zeros(C.shape, dtype=complex)
	div_time = np.zeros(C.shape, dtype=int)

	for i in range(max_iter):
		Z = Z ** 2 + C
		diverge = np.abs(Z) > 2
		div_now = diverge & (div_time == 0)
		div_time[div_now] = i
		Z[diverge] = 2

	return div_time


# Generate Mandelbrot data
mandelbrot_data = mandelbrot(-2.0, 1.0, -1.5, 1.5)

# Create Plotly figure
fig = px.imshow(
	mandelbrot_data,
	color_continuous_scale="turbo",
	origin="lower",
	title="Mandelbrot Set",
	labels={"color": "Iterations"}
)
# Fix axes labels for coordinate mapping
fig.update_layout(
	dragmode=False,

	xaxis=dict(
		scaleanchor="y",
		scaleratio=1,
		range=[0, mandelbrot_data.shape[1] - 1],
		showticklabels=False,
		fixedrange=True
	),
	yaxis=dict(
		autorange="reversed",
		showticklabels=False,
		fixedrange=True
	)
)

app = Dash(__name__)

app.layout = html.Div([
	html.H1("Mandelbrot Set Visualization"),
	dcc.Graph(id="mandelbrot-graph", figure=fig),
	html.Div(id="click-output", style={"marginTop": "20px", "fontSize": "20px"}),
])


@app.callback(
	Output("click-output", "children"),
	Input("mandelbrot-graph", "clickData")
)
def display_click_data(clickData):
	if clickData is None:
		return "Click on the plot to see coordinates."
	# Extract pixel coordinates from clickData
	point = clickData["points"][0]
	px_x = point["x"]
	px_y = point["y"]
	# Map pixel coordinates back to complex plane coordinates
	# Original plane ranges:
	xmin, xmax = -2.0, 1.0
	ymin, ymax = -1.5, 1.5
	width, height = mandelbrot_data.shape[1], mandelbrot_data.shape[0]
	x_coord = xmin + (xmax - xmin) * (px_x / width)
	y_coord = ymin + (ymax - ymin) * (px_y / height)
	return f"Clicked at pixel coords: ({px_x:.1f}, {px_y:.1f}) → Mandelbrot coords: ({x_coord:.5f}, {y_coord:.5f})"


if __name__ == "__main__":
	app.run_server(host="0.0.0.0", port=8050, debug=True)
