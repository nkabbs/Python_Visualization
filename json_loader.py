import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

f = open('multiple_channel_example.json', 'r')
write_file = open('array_output.txt', 'a')
json_data = json.loads(f.read())

signal_absorption_data = json_data["signal_absorption_time_series_data"]

df = pd.DataFrame(signal_absorption_data)
regions = df.region.unique()

hide_zeroes = True
exploratory = False
combine_channels = True

example_timestamp_data = df['channels'].values[0][0]['timestamp_data']

selected_start_time = 0
selected_end_time = 38000
timestamp_selection_start_index = 0
timestamp_selection_end_index = 0
#multiply by 2 because currently the timestamps are recorded at half-millisecond intervals (should somehow change that maybe?...)
while timestamp_selection_start_index < len(example_timestamp_data) and example_timestamp_data[timestamp_selection_start_index] < selected_start_time and timestamp_selection_start_index < selected_end_time * 2:
    timestamp_selection_start_index += 1
while timestamp_selection_end_index < len(example_timestamp_data) and example_timestamp_data[timestamp_selection_end_index] < selected_end_time and timestamp_selection_end_index < selected_end_time * 2:
    timestamp_selection_end_index += 1

for region in regions:
    if region == "Phoneme Density":
        exploratory = False
        #region_data = region_data.sort_values(['layer'])
    fig, ax = plt.subplots()
    region_data = df.loc[df['region'] == region]#.sort_values('name')
    if region == "Pitch Transforms":
        region_data['name_length'] = region_data['name'].map(len)
        region_data = region_data.sort_values(['name_length', 'name'])

    data_by_density = []
    consolidated_signal_activation_data = []
    density_names = []
    num_channels = len(df['channels'].values[0])
    if combine_channels:
        for density_data in region_data['channels'].values:
            highest_exploratory_signal_absorption = []
            highest_activating_signal_absorption = []
            highest_exploratory_signal_channel = []
            highest_activating_signal_channel = []
            for i in range(len(density_data[0]['timestamp_data'])):
                timestamp_highest_exploratory_signal_absorption = 0
                timestamp_highest_activating_signal_absorption = 0
                j = 0
                highest_exploratory_signal_channel.append(0)
                highest_activating_signal_channel.append(0)
                highest_exploratory_signal_absorption.append(0)
                highest_activating_signal_absorption.append(0)
                while j < num_channels:
                    current_exploratory_signal_absorption = density_data[j]['exploratory_signal_absorption'][i]
                    current_activating_signal_absorption = density_data[j]['activating_signal_absorption'][i]
                    if current_exploratory_signal_absorption > timestamp_highest_exploratory_signal_absorption:
                        highest_exploratory_signal_channel[i] = j
                        highest_exploratory_signal_absorption[i] = current_exploratory_signal_absorption
                        timestamp_highest_exploratory_signal_absorption = current_exploratory_signal_absorption
                    if current_activating_signal_absorption > timestamp_highest_activating_signal_absorption:
                        highest_activating_signal_channel[i] = j
                        highest_activating_signal_absorption[i] = current_activating_signal_absorption
                        timestamp_highest_activating_signal_absorption = current_activating_signal_absorption
                    j += 1
            consolidated_signal_activation_data.append({"timestamp_data": density_data[0]["timestamp_data"], "highest_exploratory_signal_channel": highest_exploratory_signal_channel, "highest_activating_signal_channel": highest_activating_signal_channel, "exploratory_signal_absorption": highest_exploratory_signal_absorption, "activating_signal_absorption": highest_activating_signal_absorption})
            density_names.extend(o + str(':') + str(i) for o in region_data['name'])
    else:
        i = 0
        while i < num_channels:
            consolidated_signal_activation_data.extend(o[i] for o in region_data['channels'].values) #[{'primary_channel': [0,1], 'timestamp_data': [0, 0.5], 'exploratory_signal_absorption': [1, .1], 'activating_signal_absorption': [.1, .2]
            density_names.extend(o + str(':') + str(i) for o in region_data['name'])
            i += 1
    consolidated_signal_activation_data.reverse()
    density_names.reverse()

    preserved_density_names = []
    for i in range(len(consolidated_signal_activation_data)):
        channel_signal_absorption_data = []
        signal_absorption_index = timestamp_selection_start_index
        if exploratory:
            while signal_absorption_index < timestamp_selection_end_index:
                channel_signal_absorption_data.append(consolidated_signal_activation_data[i]['exploratory_signal_absorption'][signal_absorption_index])
                signal_absorption_index += 1
        else:
            while signal_absorption_index < timestamp_selection_end_index:
                channel_signal_absorption_data.append(consolidated_signal_activation_data[i]['activating_signal_absorption'][signal_absorption_index])
                signal_absorption_index += 1
        if not hide_zeroes or len([num for num in channel_signal_absorption_data if num > 0]) > 0:
            preserved_density_names.append(density_names[i])
            data_by_density.append(channel_signal_absorption_data)

    plt.xlabel('Phoneme')
    plt.ylabel('Density')
    ylabels = []
    yticks = []
    guids = np.unique(df['guid'])
    # for i in range(len(data_by_density)):
    for i in range(len(preserved_density_names)):
        ylabels.append(preserved_density_names[i])
        yticks.append(i)

    phoneme_timestamps = json_data["phoneme_timestamps"]
    xticks = []
    xlabels = []
    h_starred = False
    for phoneme_timestamp in phoneme_timestamps:
        average_timestamp = round((int(phoneme_timestamp["start_time"]) + int(phoneme_timestamp["end_time"])) / 2)
        if average_timestamp > selected_start_time and average_timestamp < selected_end_time:
            # doubled because each index is only a half ms, so if we want to convert from ms to index we x2
            if phoneme_timestamp["phoneme"] == "h#" or h_starred:
                xticks.append((average_timestamp - selected_start_time) * 2)
                xlabels.append(phoneme_timestamp["phoneme"])
    plt.xticks(xticks, xlabels)
    plt.yticks(yticks, ylabels)

    plt.title(("Exploratory " if exploratory else "Activating ") + "Signal Activation Mapping ("
              + str(region) + ": " + str(selected_start_time) + "ms to " + str(selected_end_time) + "ms)")

    num_cols = len(data_by_density[0])
    num_rows = len(data_by_density)
    mask_values = [[1]*num_cols for i in range(num_rows)]
    if combine_channels:
        for i in range(num_rows):
            current_density_data = consolidated_signal_activation_data[i]
            for j in range(num_cols):
                if (exploratory and current_density_data['highest_exploratory_signal_channel'][j] == 1) or (not exploratory and current_density_data['highest_activating_signal_channel'][j] == 1):
                    mask_values[i][j] = 0
    maskArr = np.ma.masked_array(data_by_density, mask=mask_values)
    ax.imshow(data_by_density, cmap='Blues', aspect="auto", interpolation="nearest")
    ax.imshow(maskArr, cmap='Reds', aspect="auto", interpolation="nearest")
    plt.savefig(region + '.png')
    plt.show()

