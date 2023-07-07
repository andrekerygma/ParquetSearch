import PySimpleGUI as sg
import pandas as pd

# Panda's display settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Function to load the file and return the columns
def load_file(filepath):
    df = pd.concat([pd.read_parquet(fp) for fp in filepath])
    return df, df.columns.tolist()

# Function to perform the search
def search(df, column, search_term, exact_match):
    if exact_match:
        results = df[df[column] == search_term]
    else:
        results = df[df[column].str.contains(search_term, na=False)]
    return results[[column]]

# Function to calculate the size of the longest text
def calculate_size(columns):
    return max(len(c) for c in columns)

# Interface layout
layout = [
    [sg.Text("Parquet Files:", font='Helvetica 14'), sg.Input(enable_events=True, key='-FILES-', font='Helvetica 14'), sg.FilesBrowse(font='Helvetica 14')],
    [sg.Text("Column:", font='Helvetica 14'), sg.Combo([], key='-COLUMN-', size=(None, None), font='Helvetica 14')],
    [sg.Text("Search Term:", font='Helvetica 14'), sg.Input(key='-TERM-', font='Helvetica 14')],
    [sg.Checkbox("Exact Match", default=True, key='-EXACT-', font='Helvetica 14')],
    [sg.Button("Search", font='Helvetica 14'), sg.Button("Export", font='Helvetica 14')],
    [sg.Output(size=(50, 20), key='-OUTPUT-', font='Courier 14', expand_x=True, expand_y=True)]
]

# Creates the window
window = sg.Window("Parquet File Search", layout, resizable=True)

df = None
results = None

# Event loop
while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        break
    elif event == '-FILES-':
        if values['-FILES-']:
            df, columns = load_file(values['-FILES-'].split(';'))
            window['-COLUMN-'].update(values=columns)
            window['-COLUMN-'].set_size((calculate_size(columns), None))
    elif event == "Search":
        if df is not None and values['-COLUMN-']:
            window['-OUTPUT-'].update('')  # Clear the output box
            results = search(df, values['-COLUMN-'], values['-TERM-'], values['-EXACT-'])
            print(results.to_string(index=False))
        else:
            print("Please select parquet files and a column.")
    elif event == "Export":
        if results is not None:
            filename = sg.popup_get_file('Save the results as', save_as=True, default_extension=".txt", file_types=(('Text', '.txt'),))
            if filename:
                with open(filename, 'w') as f:
                    f.write(results.to_string(index=False))
        else:
            print("No results to export. Please do a search first.")

window.close()
