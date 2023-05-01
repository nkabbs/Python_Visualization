import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

f = open('5_1_2.json', 'r')
write_file = open('array_output.txt', 'a')
json_data = json.loads(f.read())

# def parse_signal_absorption_data(signal_absorption_data):
#     parsed_data = []
#     for i in range(len(signal_absorption_data)):
#         density_data = signal_absorption_data[i]
#         channels = density_data["channels"]
#         guid = density_data["guid"]
#         name = density_data["name"]
#         region = density_data["region"]
#         j = 0
#         while j < len(channels):
#             channel_data = channels[j]
#             channel = channel_data["channel"]
#             timestamp_data = channel_data["timestamp_data"]
#             exploratory_signal_absorption = channel_data["exploratory_signal_absorption"]
#             activating_signal_absorption = channel_data["activating_signal_absorption"]
#             k = 0
#             while k < len(timestamp_data):
#                 parsed_data.append({"guid": guid, "name": name, "channel": channel, "timestamp": timestamp_data[k], "exploratory_signal_absorption": float(exploratory_signal_absorption[k]), "activating_signal_absorption": float(activating_signal_absorption[k])})
#                 k += 1
#             j += 1
#     return parsed_data

signal_absorption_data = json_data["signal_absorption_time_series_data"]
#parsed_data = parse_signal_absorption_data(signal_absorption_data)

df2 = pd.DataFrame(signal_absorption_data)

regions = df2.region.unique()


data_by_region = {}
hide_zeroes = False
exploratory = True

for region in regions:
    region_data = df2.loc[df2['region'] == region]
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
    for i in range(len(data_by_channel)):
        channel_signal_absorption_data = []
        if exploratory:
            for j in range(len(data_by_channel[i]['exploratory_signal_absorption'])):
                channel_signal_absorption_data.append(data_by_channel[i]['exploratory_signal_absorption'][j])
        else:
            for j in range(len(data_by_channel[i]['activating_signal_absorption'])):
                channel_signal_absorption_data.append(data_by_channel[i]['activating_signal_absorption'][j])
        if not hide_zeroes or len([num for num in channel_signal_absorption_data if num > 0]) > 0:
            data_by_density.append(channel_signal_absorption_data)
    data_by_region[region] = data_by_density

    plt.xlabel('time [ms]')
    plt.ylabel('Neuron')
    ylabels = []
    yticks = []
    guids = np.unique(df2['guid'])
    # for i in range(len(data_by_density)):
    for i in range(len(density_names)):
        ylabels.append(density_names[i])
        yticks.append(i)

    phoneme_timestamps = json_data["phoneme_timestamps"]
    xticks = []
    xlabels = []
    for phoneme_timestamp in phoneme_timestamps:
        xticks.append(round((int(phoneme_timestamp["start_time"]) + int(phoneme_timestamp["end_time"]))))
        xlabels.append(phoneme_timestamp["phoneme"])
    plt.xticks(xticks, xlabels)
    plt.yticks(yticks, ylabels)

    plt.title(("Exploratory " if exploratory else "Activating ") + "Signal Activation Mapping (" + region + ")")

    plt.imshow(data_by_density, cmap='Blues', aspect="auto", interpolation="nearest")
    plt.savefig(region + '.png')
    plt.show()

