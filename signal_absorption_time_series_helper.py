import numpy as np
import matplotlib.pyplot as plt


def get_timestamp_start_and_end_index(start_time, end_time, example_timestamp_data):
    timestamp_selection_start_index = 0
    timestamp_selection_end_index = 0
    # multiply by 2 because currently the timestamps are recorded at half-millisecond intervals (should somehow change that maybe?...)
    while timestamp_selection_start_index < len(example_timestamp_data) and example_timestamp_data[timestamp_selection_start_index] < start_time and timestamp_selection_start_index < end_time * 2:
        timestamp_selection_start_index += 1
    while timestamp_selection_end_index < len(example_timestamp_data) and example_timestamp_data[timestamp_selection_end_index] < end_time and timestamp_selection_end_index < end_time * 2:
        timestamp_selection_end_index += 1
    return timestamp_selection_start_index, timestamp_selection_end_index

def consolidate_combined_channel_signal_activation_data(num_channels, region_data):
    consolidated_signal_activation_data = []
    for density_data in region_data['channels'].values:
        highest_exploratory_signal_absorption = []
        highest_activating_signal_absorption = []
        highest_exploratory_signal_channel = []
        highest_activating_signal_channel = []
        for i in range(len(density_data[0]['timestamp_data'])):
            timestamp_highest_exploratory_signal_absorption = 0
            timestamp_highest_activating_signal_absorption = 0
            highest_exploratory_signal_channel.append(0)
            highest_activating_signal_channel.append(0)
            highest_exploratory_signal_absorption.append(0)
            highest_activating_signal_absorption.append(0)
            j = 0
            while j < num_channels:
                current_exploratory_signal_absorption = density_data[j]['exploratory_signal_absorption'][i]
                current_activating_signal_absorption = density_data[j]['activating_signal_absorption'][i]
                if j == 1 and current_exploratory_signal_absorption != 0:
                    print("")
                if current_exploratory_signal_absorption > timestamp_highest_exploratory_signal_absorption:
                    highest_exploratory_signal_channel[i] = j
                    highest_exploratory_signal_absorption[i] = current_exploratory_signal_absorption
                    timestamp_highest_exploratory_signal_absorption = current_exploratory_signal_absorption
                if current_activating_signal_absorption > timestamp_highest_activating_signal_absorption:
                    highest_activating_signal_channel[i] = j
                    highest_activating_signal_absorption[i] = current_activating_signal_absorption
                    timestamp_highest_activating_signal_absorption = current_activating_signal_absorption
                j += 1

        consolidated_signal_activation_data.append({"timestamp_data": density_data[0]["timestamp_data"],
                                                    "highest_exploratory_signal_channel": highest_exploratory_signal_channel,
                                                    "highest_activating_signal_channel": highest_activating_signal_channel,
                                                    "exploratory_signal_absorption": highest_exploratory_signal_absorption,
                                                    "activating_signal_absorption": highest_activating_signal_absorption})
    return consolidated_signal_activation_data

def parse_consolidated_signal_activation_data_into_densities(consolidated_signal_activation_data, timestamp_selection_start_index, timestamp_selection_end_index, exploratory, hide_zeroes, density_names):
    preserved_density_names = []
    data_by_density = []

    for i in range(len(consolidated_signal_activation_data)):
        channel_signal_absorption_data = []
        signal_absorption_index = timestamp_selection_start_index
        try:
            if exploratory:
                while signal_absorption_index < timestamp_selection_end_index:
                    channel_signal_absorption_data.append(consolidated_signal_activation_data[i]['exploratory_signal_absorption'][signal_absorption_index])
                    signal_absorption_index += 1
            else:
                while signal_absorption_index < timestamp_selection_end_index:
                    channel_signal_absorption_data.append(consolidated_signal_activation_data[i]['activating_signal_absorption'][signal_absorption_index])
                    signal_absorption_index += 1
        except Exception as e:
            print(e)
        nonzero_value_count = len([num for num in channel_signal_absorption_data if num > 0])
        if not hide_zeroes or nonzero_value_count > 0:
            preserved_density_names.append(density_names[i])
            data_by_density.append(channel_signal_absorption_data)

    return data_by_density, preserved_density_names

def create_x_axis_phoneme_labels(phoneme_timestamps, selected_start_time, selected_end_time):
    xlabels = []
    xticks = []
    h_starred = False
    for phoneme_timestamp in phoneme_timestamps:
        average_timestamp = round((int(phoneme_timestamp["start_time"]) + int(phoneme_timestamp["end_time"])) / 2)
        if average_timestamp > selected_start_time and average_timestamp < selected_end_time:
            # doubled because each index is only a half ms, so if we want to convert from ms to index we x2
            if not h_starred or phoneme_timestamp["phoneme"] == "h#":
                xticks.append((average_timestamp - selected_start_time) * 2)
                xlabels.append(phoneme_timestamp["phoneme"])

    return xticks, xlabels

def plot_x_and_y_axis_labels(x_title, y_title, preserved_density_names, phoneme_timestamps, selected_start_time, selected_end_time, exploratory, region):
    plt.xlabel(x_title)
    plt.ylabel( y_title)

    ylabels = []
    yticks = []

    for i in range(len(preserved_density_names)):
        ylabels.append(preserved_density_names[i])
        yticks.append(i)

    xticks, xlabels = create_x_axis_phoneme_labels(phoneme_timestamps, selected_start_time, selected_end_time)

    plt.xticks(xticks, xlabels)
    plt.yticks(yticks, ylabels)

    plt.title(("Exploratory " if exploratory else "Activating ") + "Signal Activation Mapping ("
              + str(region) + ": " + str(selected_start_time) + "ms to " + str(selected_end_time) + "ms)")

def get_mask_from_signal_activation_data(consolidated_signal_activation_data, exploratory, hide_zeroes, data_by_density, masking_channel):
    num_cols = len(consolidated_signal_activation_data[0]['highest_exploratory_signal_channel'])
    num_rows = len(consolidated_signal_activation_data)
    mask_values = []
    for i in range(num_rows):
        current_density_data = consolidated_signal_activation_data[i]
        nonzero_value_count = len(
            [num for num in current_density_data['exploratory_signal_absorption'] if num > 0]) if exploratory else len(
            [num for num in current_density_data['activating_signal_absorption'] if num > 0])
        if not hide_zeroes or nonzero_value_count > 0:
            mask_values.append([1] * num_cols)
            for j in range(num_cols):
                if (exploratory and current_density_data['highest_exploratory_signal_channel'][j] == masking_channel) or (
                        not exploratory and current_density_data['highest_activating_signal_channel'][j] == masking_channel):
                    mask_values[len(mask_values) - 1][j] = 0
    mask_arr = np.ma.masked_array(data_by_density, mask=mask_values)
    return mask_arr
