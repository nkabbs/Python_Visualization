import random

output_data = []

def generate_activation_timeline(fake_data, curr_time, uninitialized_phase_length, increasing_activation_phase_length, maintained_activation_phase_length, decreasing_activation_phase_length, post_activation_phase_length):

    for i in range(uninitialized_phase_length):
        fake_data.append(random.random() / uninitialized_reduction_factor)
        curr_time += 1

    frame = 0
    for i in range(curr_time, curr_time + increasing_activation_phase_length):
        completion_ratio = frame / increasing_activation_phase_length
        value = completion_ratio * activation_phase_baseline + random.random() * activation_phase_variance
        fake_data.append(value)
        curr_time += 1
        frame += 1

    for i in range(curr_time, curr_time + maintained_activation_phase_length):
        value = .8 + random.random() * .2
        fake_data.append(value)
        curr_time += 1

    frame = 0
    for i in range(curr_time, curr_time + decreasing_activation_phase_length):
        completion_ratio = frame / decreasing_activation_phase_length
        print(completion_ratio)
        if (completion_ratio > 1):
            print("i: " + str(i))
            print("numerator: " + str(i - (uninitialized_phase_length + increasing_activation_phase_length + maintained_activation_phase_length)))
        value = (1 - completion_ratio) * activation_phase_baseline + random.random() * activation_phase_variance
        fake_data.append(value)
        curr_time += 1
        frame += 1

    for i in range(post_activation_phase_length):
        fake_data.append(random.random() * post_activation_phase_variance)
        curr_time += 1
    return curr_time


uninitialized_phase_length = 35
increasing_activation_phase_length = 15
maintained_activation_phase_length = 40
decreasing_activation_phase_length = 15
post_activation_phase_length = 95

# uninitialized_phase_length = 65
# increasing_activation_phase_length = 35
# maintained_activation_phase_length = 10
# decreasing_activation_phase_length = 35
# post_activation_phase_length = 55


uninitialized_reduction_factor = 10
activation_phase_baseline = .9
activation_phase_variance = .1
post_activation_phase_variance = .2

# uninitialized_reduction_factor = 5
# activation_phase_baseline = .4
# activation_phase_variance = .3
# post_activation_phase_variance = .05
curr_time = 0
time_tracked_per_density = uninitialized_phase_length + increasing_activation_phase_length + maintained_activation_phase_length + decreasing_activation_phase_length + post_activation_phase_length
for i in range (10):
    timestamp_values = []
    for j in range(4):
        timestamp_values.append(random.randint(0,200))
    timestamp_values.sort()

    uninitialized_phase_length = timestamp_values[0]
    increasing_activation_phase_length = timestamp_values[1] - timestamp_values[0]
    maintained_activation_phase_length = timestamp_values[2] - timestamp_values[1]
    decreasing_activation_phase_length = timestamp_values[3] - timestamp_values[2]
    post_activation_phase_length = 200 - timestamp_values[3]
    time_tracked_per_density = uninitialized_phase_length + increasing_activation_phase_length + maintained_activation_phase_length + decreasing_activation_phase_length + post_activation_phase_length
    print("time_tracked per density: " + str(time_tracked_per_density))
    fake_data = []
    curr_time = generate_activation_timeline(fake_data, curr_time, uninitialized_phase_length, increasing_activation_phase_length, maintained_activation_phase_length, decreasing_activation_phase_length, post_activation_phase_length)
    #generate_activation_timeline(fake_data, curr_time, 75, 25, 5, 5, 35)
    output_data.append(fake_data)
print(output_data)
# uninitialized_phase_length = 35
# increasing_activation_phase_length = 15
# maintained_activation_phase_length = 40
# decreasing_activation_phase_length = 15
# post_activation_phase_length = 95