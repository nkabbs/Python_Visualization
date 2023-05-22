


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