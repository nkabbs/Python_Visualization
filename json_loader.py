import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

f = open('multiple_channel_example.json', 'r')
write_file = open('array_output.txt', 'a')
json_data = json.loads(f.read())

signal_absorption_data = json_data["signal_absorption_time_series_data"]

df2 = pd.DataFrame(signal_absorption_data)
regions = df2.region.unique()

hide_zeroes = True
exploratory = True
combine_channels = True

example_timestamp_data = df2['channels'].values[0][0]['timestamp_data']

selected_start_time = 0#20550 #20550 ~ when first clip starts
selected_end_time = 33000#33000 #24000~ when first clip ends, 28500 ~ end of 3 samples
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
    region_data = df2.loc[df2['region'] == region]#.sort_values('name')
    if region == "Pitch Transforms":
        region_data['name_length'] = region_data['name'].map(len)
        region_data = region_data.sort_values(['name_length', 'name'])

    data_by_density = []
    data_by_channel = []
    density_names = []
    i = 0
    num_channels = len(df2['channels'].values[0])
    while i < num_channels:
        data_by_channel.extend(o[i] for o in region_data['channels'].values)
        density_names.extend(o + str(':') + str(i) for o in region_data['name'])
        i += 1
    data_by_channel.reverse()
    density_names.reverse()

    preserved_density_names = []
    for i in range(len(data_by_channel)):
        channel_signal_absorption_data = []
        signal_absorption_index = timestamp_selection_start_index
        if exploratory:
            while signal_absorption_index < timestamp_selection_end_index:
                channel_signal_absorption_data.append(data_by_channel[i]['exploratory_signal_absorption'][signal_absorption_index])
                signal_absorption_index += 1
        else:
            while signal_absorption_index < timestamp_selection_end_index:
                channel_signal_absorption_data.append(data_by_channel[i]['activating_signal_absorption'][signal_absorption_index])
                signal_absorption_index += 1
        if not hide_zeroes or len([num for num in channel_signal_absorption_data if num > 0]) > 0:
            preserved_density_names.append(density_names[i])
            data_by_density.append(channel_signal_absorption_data)

    plt.xlabel('Phoneme')
    plt.ylabel('Density')
    ylabels = []
    yticks = []
    guids = np.unique(df2['guid'])
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
    for i in range(num_rows):
        for j in range(num_cols):
            change_row_color = random.getrandbits(1)
            #if change_row_color:
            #    mask_values[i][j] = 0
    maskArr = np.ma.masked_array(data_by_density, mask=mask_values)
    ax.imshow(data_by_density, cmap='Blues', aspect="auto", interpolation="nearest")
    ax.imshow(maskArr, cmap='Reds', aspect="auto", interpolation="nearest")
    plt.savefig(region + '.png')
    plt.show()

