import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from signal_absorption_time_series_helper import get_timestamp_start_and_end_index, consolidate_combined_channel_signal_activation_data, \
    parse_consolidated_signal_activation_data_into_densities, plot_x_and_y_axis_labels, get_mask_from_signal_activation_data

json_data = json.loads(open('5_4_5.json', 'r').read())
df = pd.DataFrame(json_data["signal_absorption_time_series_data"])
phoneme_timestamps = json_data["phoneme_timestamps"]
regions = df.region.unique()

hide_zeroes = False
exploratory = True
combine_channels = True

example_timestamp_data = df['channels'].values[0][0]['timestamp_data']
selected_start_time = 0
selected_end_time = 38000
timestamp_selection_start_index, timestamp_selection_end_index = get_timestamp_start_and_end_index(selected_start_time, selected_end_time, example_timestamp_data)
selected_end_time = min(round(example_timestamp_data[len(example_timestamp_data) - 1]), selected_end_time)

for region in regions:
    region_data = df.loc[df['region'] == region]

    if region == "Phoneme Density":
        exploratory = False
    if region == "Pitch Transforms":
        region_data['name_length'] = region_data['name'].map(len)
        region_data = region_data.sort_values(['name_length', 'name'])

    density_names = []
    consolidated_signal_activation_data = []

    num_channels = len(region_data['channels'].values[0])

    if combine_channels:
        consolidated_signal_activation_data = consolidate_combined_channel_signal_activation_data(num_channels, region_data)
        density_names.extend(o for o in region_data['name'])
    else:
        i = 0
        while i < num_channels:
            consolidated_signal_activation_data.extend(o[i] for o in region_data['channels'].values)
            density_names.extend(o + (str(':') + str(i) if region == "Phoneme Density" else "") for o in region_data['name'])
            i += 1

    consolidated_signal_activation_data.reverse()
    density_names.reverse()

    data_by_density, preserved_density_names = parse_consolidated_signal_activation_data_into_densities(consolidated_signal_activation_data, timestamp_selection_start_index, timestamp_selection_end_index, exploratory, hide_zeroes, density_names)

    fig, ax = plt.subplots()

    plot_x_and_y_axis_labels("Phoneme", "Density", preserved_density_names, phoneme_timestamps, selected_start_time,
                             selected_end_time, exploratory, region)

    num_cols = len(data_by_density[0])
    num_rows = len(data_by_density)
    mask_values = [[1]*num_cols for i in range(num_rows)]

    ax.imshow(data_by_density, cmap='Blues', aspect="auto", interpolation="nearest")

    if combine_channels:
        mask_arr = get_mask_from_signal_activation_data(consolidated_signal_activation_data, exploratory, hide_zeroes, data_by_density)
        ax.imshow(mask_arr, cmap='Reds', aspect="auto", interpolation="nearest")

    plt.savefig(region + '.png')
    plt.show()
