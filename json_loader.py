import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

f = open('signal_absorption_time_series.json', 'r')
write_file = open('array_output.txt', 'a')
json_data = json.loads(f.read())

def parse_signal_absorption_data(signal_absorption_data):
    parsed_data = []
    for i in range(len(signal_absorption_data)):
        density_data = signal_absorption_data[i]
        channels = density_data["channels"]
        guid = density_data["guid"]
        j = 0
        while j < len(channels):
            channel_data = channels[j]
            channel = channel_data["channel"]
            timestamp_data = channel_data["timestamp_data"]
            signal_absorption = channel_data["signal_absorption"]
            k = 0
            while k < len(timestamp_data):
                parsed_data.append({"guid": guid, "channel": channel, "timestamp": timestamp_data[k], "signal_absorption": float(signal_absorption[k])})
                k += 1
            j += 1
    return parsed_data

signal_absorption_data = json_data["signal_absorption_time_series_data"]
parsed_data = parse_signal_absorption_data(signal_absorption_data)

df2 = pd.DataFrame(signal_absorption_data)

# guid_list = ["f4ef2bdd-68fd-450d-9a41-1a75881dd092"]
# channel_list = [0]
#df = df#.query('guid in @guid_list & channel in @channel_list')
print(df2)

# Arbitrarily using channel 0
array_tester = [o[0] for o in df2['channels'].values]
data_by_density = []

hide_zeroes = True

for i in range(len(array_tester)):
    density_channel_data = []
    for j in range(len(array_tester[i]['signal_absorption'])):
        density_channel_data.append(array_tester[i]['signal_absorption'][j])
    if not hide_zeroes or len([num for num in density_channel_data if num > 0]) > 0:
        data_by_density.append(density_channel_data)

#plt.pcolormesh(data_by_density, cmap='Blues')

plt.xlabel('time [ms]')
plt.ylabel('Neuron')
ylabels = []
yticks = []
guids = np.unique(df2['guid'])
for i in range(len(data_by_density)):
    ylabels.append("Density " + str(i + 1))
    yticks.append(i)
#yticks = np.arange(len(array_tester)) + 0.5

plt.yticks(yticks, ylabels)


# plt.tick_params(axis='x', which='both', top='off')
# plt.tick_params(axis='y', which='both', left='off', right='off')

plt.title("%s" %
          ("Density Network Signal Activation Mapping"))

#plt.colorbar()


write_file.write(str(data_by_density))

plt.imshow(data_by_density, cmap='Blues', aspect="auto", interpolation="nearest")
plt.show()