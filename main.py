from dash import Dash, html, Input, Output, State, dcc, ctx
from dash import dash_table

app = Dash(__name__)


def load_initial_data():
	return [
		{"id": 1, "z_re": 0.0, "z_im": 0.0, "type": "init", "status": "pending", "button": "[Run](https://google.com)"},
		{"id": 2, "z_re": 1.0, "z_im": 1.0, "type": "init", "status": "done", "button": "[Run](https://google.com)"},
	]


initial_data = load_initial_data()

app.layout = html.Div([
	html.H2("Click to Add Rows to Table"),
	html.Button("Click Anywhere to Add Row", id="add-row-btn", n_clicks=0),
	dcc.Interval(
		id='interval',
		interval=1000,  # 1000 ms = 1 second
		n_intervals=0  # counts how many times triggered
	),
	dash_table.DataTable(
		id='table',
		columns=[
			{"name": "id", "id": "id"},
			{"name": "z_re", "id": "z_re"},
			{"name": "z_im", "id": "z_im"},
			{"name": "type", "id": "type"},
			{"name": "status", "id": "status"},
			{"name": "button", "id": "button", "presentation": "markdown"},
		],
		data=initial_data,
		style_table={'overflowX': 'auto'},
		style_cell={'textAlign': 'center'},
	),
	# Keep track of row count
	html.Div(str(len(initial_data)), id='row-counter', style={'display': 'none'}),
	html.Div(id='dummy', style={'display': 'none'})
])


@app.callback(
	Output('table', 'data'),
	Output('row-counter', 'children'),
	Input('add-row-btn', 'n_clicks'),
	Input('interval', 'n_intervals'),
	State('table', 'data'),
	State('row-counter', 'children'),
	prevent_initial_call=True
)
def manage_table(n_clicks, n_intervals, table_data, counter):
	"""
	Combined callback for:
	  1. Adding a row when button clicked
	  2. Updating links every second
	"""
	# Ensure table_data and counter are initialized
	table_data = table_data or []
	counter = int(counter) if counter else 0

	triggered = ctx.triggered_id

	# Handle Add Row button
	if triggered == 'add-row-btn':
		new_id = counter + 1
		new_row = {
			"id": new_id,
			"z_re": 0.0,
			"z_im": 0.0,
			"type": "default",
			"status": "pending",
			"button": f"[Run](https://google.com)"
		}
		table_data.append(new_row)
		counter = new_id

	# Handle Interval (update links dynamically)
	elif triggered == 'interval':
		for row in table_data:
			row_id = row["id"]
			row["button"] = f'[Run](https://www.google.com/search?q={row_id})'

	return table_data, counter


@app.callback(
	Output('dummy', 'children'),
	Input('table', 'active_cell'),
	State('table', 'data')
)
def on_button_click(active_cell, rows):
	if active_cell and active_cell['column_id'] == 'button':
		# Get row index
		row_idx = active_cell['row']
		# Update status for that row
		rows[row_idx]['status'] = "RUNNING"
		print(f"cliked {row_idx}")

	return ""


if __name__ == '__main__':
	app.run_server(debug=True)
