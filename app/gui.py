# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Creates the GUI for the HEET software.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Created: 12.07.2021
Last Modified: 28.08.2021

@author: Daniel-Alexandru Nistor
"""
# The library that will allow us to create the GUI.
import tkinter as tk
import compute_emissions

def compute():    
    # The values of the input parameters entered by the user.
    latitude = float(entry_lat.get())
    longitude = float(entry_long.get())
    capacity = float(entry_cap.get())
    age = float(entry_age.get())
    trophic_state = var_troph_state.get().lower()

    # Compute the CO2 and CH4 emissions.
    emissions_co2, emissions_ch4 = compute_emissions.get_emissions(latitude,
                                                                   longitude,
                                                                   capacity,
                                                                   age,
                                                                   trophic_state)
    # Change the output labels to display the computed emissions.
    labels_co2[1]['text'] = f'{emissions_co2:.2f}'
    labels_ch4[1]['text'] = f'{emissions_ch4:.2f}'


# The root of the GUI.
root = tk.Tk()
root.geometry('400x300')
root.title('HEET: Hydropower Emissions Estimation Tool')
root.iconbitmap('dam.ico')


# The input frame of the GUI.
input_frame = tk.LabelFrame(root, text='Inputs')
input_frame.pack(pady=5)

# A label asking the user for the dam location in decimal degrees.
label_dam_loc = tk.Label(input_frame, text='Insert Dam Location (DD):')
label_dam_loc.grid(row=0, column=0)

# A label asking the user for the latitude.
label_lat = tk.Label(input_frame, text='Latitude:')
label_lat.grid(row=0, column=1)
# A label asking the user for the longitude.
label_long = tk.Label(input_frame, text='Longitude:')
label_long.grid(row=1, column=1)

# An entry field for the latitude.
entry_lat = tk.Entry(input_frame)
entry_lat.grid(row=0, column=2, padx=10, pady=5)
# An entry field for the longitude.
entry_long = tk.Entry(input_frame)
entry_long.grid(row=1, column=2, pady=5)

# A label asking the user for the dam capacity in megawatts.
label_cap = tk.Label(input_frame, text='Insert Dam Capacity (MW):')
label_cap.grid(row=2, column=0)

# An entry field for the dam capacity.
entry_cap = tk.Entry(input_frame)
entry_cap.grid(row=2, column=2, pady=5)


# A label asking the user for the age of the dam.
label_age = tk.Label(input_frame, text='Insert Age (yrs):')
label_age.grid(row=3, column=0)
# An entry field for the age.
entry_age = tk.Entry(input_frame)
entry_age.grid(row=3, column=2, pady=5)


# A label asking the user for the trophic state.
label_troph_state = tk.Label(input_frame, text='Select Trophic State:')
label_troph_state.grid(row=4, column=0)
# A drop-down menu with the choices of trophic state.
var_troph_state = tk.StringVar()
options = ['Ultra-Oligotrophic', 'Oligotrophic', 'Mesotrophic', 'Eutrophic',
            'Hypertrophic']
var_troph_state.set(options[1])
menu_troph_state = tk.OptionMenu(input_frame, var_troph_state, *options)
menu_troph_state.grid(row=4, column=2, pady=5)


# The output frame of the GUI.
output_frame = tk.LabelFrame(root, text='Outputs')
output_frame.pack(pady=5, ipady=2.5)

# A set of labels outputting the CO2 emissions.
labels_co2 = [tk.Label(output_frame, text='CO2 emissions (tonnes/yr):'),
              tk.Label(output_frame, text='0')]
for index, label in enumerate(labels_co2):
    label.grid(row=0, column=index, padx=2.5)

# A set of labels outputting the CH4 emissions.
labels_ch4 = [tk.Label(output_frame, text='CH4 emissions (tonnes/yr):'),
              tk.Label(output_frame, text='0')]
for index, label in enumerate(labels_ch4):
    label.grid(row=1, column=index)

# A button to press when you want to compute emissions.
button_compute = tk.Button(output_frame, text='Compute Emissions',
                           command=compute)
button_compute.grid(row=2, column=0, columnspan=2, pady=5)

# Display the root and its attachments.
root.mainloop()
