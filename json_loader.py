import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

f = open('4_27_8.json', 'r')
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

# guid_list = ["f4ef2bdd-68fd-450d-9a41-1a75881dd092"]
# channel_list = [0]
#df = df#.query('guid in @guid_list & channel in @channel_list')
#print(df2)

# Arbitrarily using channel 0
data_by_channel = []#[o[0] for o in df2['channels'].values]
density_names = []

i = 0
num_channels = len(df2['channels'].values[0])
while i < num_channels:
    data_by_channel.extend(o[i] for o in df2['channels'].values)
    density_names.extend(o + str(':') + str(i) for o in df2['name'])
    i += 1
data_by_channel.reverse()
density_names.reverse()
data_by_density = []
density_regions = {}
hide_zeroes = False
exploratory = True

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

#plt.pcolormesh(data_by_density, cmap='Blues')

plt.xlabel('time [ms]')
plt.ylabel('Neuron')
ylabels = []
yticks = []
guids = np.unique(df2['guid'])
#for i in range(len(data_by_density)):
for i in range(len(density_names)):
    ylabels.append(density_names[i])
    yticks.append(i)
#yticks = np.arange(len(array_tester)) + 0.5

phoneme_timestamps = json_data["phoneme_timestamps"]
phoneme_averaged_timestamps = []
xticks = []
xlabels = []
for phoneme_timestamp in phoneme_timestamps:
    #phoneme_averaged_timestamps.append({ "phoneme": phoneme_timestamp["phoneme"], "average_timestamp": str((int(phoneme_timestamp["start_time"]) + int(phoneme_timestamp["end_time"])) / 2)})
    xticks.append(round((int(phoneme_timestamp["start_time"]) + int(phoneme_timestamp["end_time"]))))
    xlabels.append(phoneme_timestamp["phoneme"])
plt.xticks(xticks, xlabels)
plt.yticks(yticks, ylabels)


# plt.tick_params(axis='x', which='both', top='off')
# plt.tick_params(axis='y', which='both', left='off', right='off')

plt.title(("Exploratory " if exploratory else "Activating ") + "Density Network Signal Activation Mapping")

#plt.colorbar()
plt.imshow(data_by_density, cmap='Blues', aspect="auto", interpolation="nearest")
plt.show()