import numpy as np
import matplotlib.pyplot as plot
import scipy.stats as sp
plot.style.use('ggplot')


def init(starting_traffic_light, mean, deviation):
    global now, queue_length, end, traffic_light_is_green, \
        server_is_idle, event_list, gaussian_parameters, queue_length_at_current_time, \
        total_inter_arrival_time, total_arrivals

    now = 0                 # Simulation time
    queue_length = 0        # Queue length
    end = 14400             # Simulation duration for 4 hours (14400 seconds)
    traffic_light_is_green = starting_traffic_light  # Traffic lights status
    server_is_idle = True   # Check if there are cars crossing
    # 0 - arrival, 1 - begin service, 2 - end service, 3 - change traffic lights
    # Initially the traffic lights are green/red, schedule an event at 30 seconds to change it
    event_list = [[0, now], [3, now + 30]]
    # Gaussian parameters, mean and deviation
    gaussian_parameters = [mean, deviation]
    # Queue data against time for plotting
    queue_length_at_current_time = []
    # All arrival rates for traffic intensity
    total_inter_arrival_time = 0
    # Total arrivals for traffic intensity
    total_arrivals = 0


def generate_inter_arrival_time():
    global gaussian_parameters
    inter_arrival_time = 0
    while inter_arrival_time < 1 or inter_arrival_time > 10:
        inter_arrival_time = np.random.exponential(2)
    # Switch NOW to hours since parameters are in hours
    inter_arrival_time /= sp.norm.pdf(now / 3600, loc=gaussian_parameters[0], scale=gaussian_parameters[1])
    return inter_arrival_time


def arrival():
    global now, event_list, queue_length, traffic_light_is_green, queue_length_at_current_time, \
        total_inter_arrival_time, total_arrivals
    text_file.write("Arrival at time %lf\n" % now)
    # Generate inter-arrival time
    inter_arrival_time = generate_inter_arrival_time()
    # Schedule next arrival event
    event_list.append([0, now + inter_arrival_time])
    queue_length += 1
    # If lights are green and server is idle, start event immediately
    if traffic_light_is_green and server_is_idle:
        event_list.append([1, now])
    # Used for plotting
    queue_length_at_current_time.append([queue_length, now])
    # Traffic intensity
    total_arrivals += 1
    total_inter_arrival_time += inter_arrival_time


def begin_service():
    global queue_length, traffic_light_is_green, now, event_list, server_is_idle, queue_length_at_current_time
    text_file.write("Begin service at time %lf\n" % now)
    # Service time is fixed constant
    service_time = 2
    queue_length -= 1
    server_is_idle = False
    # Schedule next ending of service event
    event_list.append([2, service_time + now])
    # Used for plotting
    queue_length_at_current_time.append([queue_length, now])


def end_service():
    global server_is_idle, event_list, queue_length, now, queue_length_at_current_time
    text_file.write("End service at time %lf\n" % now)
    server_is_idle = True
    # Lights can change colour when a car is passing but the car still pass
    if queue_length > 0 and traffic_light_is_green:
        # Schedule beginning of service event
        event_list.append([1, now])


def change_of_traffic_lights():
    global traffic_light_is_green, event_list, queue_length
    text_file.write("Change Lights to %r at time %lf\n" % (not traffic_light_is_green, now))

    # If traffic light were green change them to red
    if traffic_light_is_green:
        traffic_light_is_green = False
    # Else turn them green and schedule service event if there are
    # cars that need to pass
    else:
        traffic_light_is_green = True
        # If there are cars in the queue
        if queue_length > 0:
            event_list.append([1, now])
    # Schedule next change of traffic lights
    event_list.append([3, now + 30])


def run_simulation(is_starting_traffic_light, mean, deviation):
    global now, event_list, queue_length_at_current_time, end
    # Assign values to the variables that will be used in the simulation
    init(is_starting_traffic_light, mean, deviation)
    # Will simulate for 4 hours
    while now < end:
        # Sorting event according to time
        event_list = sorted(event_list, key=lambda x: x[1])
        first_event = event_list[0]
        now = first_event[1]
        # 4 event type: arrival event, begin service,
        # end service, change traffic lights (0, 1, 2, 3)
        if first_event[0] == 0:
            arrival()
        elif first_event[0] == 1:
            begin_service()
        elif first_event[0] == 2:
            end_service()
        elif first_event[0] == 3:
            change_of_traffic_lights()
        # Delete the event that was completed
        del event_list[0]

    return np.array(queue_length_at_current_time)


def calculate_traffic_intensity():
    global total_inter_arrival_time, total_arrivals
    arrival_rate = 1 / (total_inter_arrival_time / total_arrivals)
    # Service time is a constant 2 for every car
    service_rate = 1 / 2
    return arrival_rate / service_rate

# Output to a text file
text_file = open("Output.txt", "w")

# Road A morning simulation, mean = 2, dev = 1
np_queue_roadA_Morning = run_simulation(True, 2, 1)
print("The traffic intensity of Road A in the morning: %lf" % calculate_traffic_intensity())

# Road B morning simulation, mean = 2.5, dev = 0.95
np_queue_roadB_Morning = run_simulation(False, 2.5, 0.95)
print("The traffic intensity of Road B in the morning: %lf" % calculate_traffic_intensity())

plot.figure()
plot.plot(np_queue_roadA_Morning[:, 1] / 3600, np_queue_roadA_Morning[:, 0], '-or', label='Road A')
plot.plot(np_queue_roadB_Morning[:, 1] / 3600, np_queue_roadB_Morning[:, 0], '-ob', label='Road B')
plot.xlabel("Now")
plot.ylabel("Queue Length")
plot.title("Morning")
plot.legend()

# Road A Evening simulation, mean = 2, dev = 0.95
np_queue_roadA_Evening = run_simulation(True, 2, 0.95)
print("The traffic intensity of Road A in the Evening: %lf" % calculate_traffic_intensity())

# Road B Evening simulation, mean = 1.5, dev - 1
np_queue_roadB_Evening = run_simulation(False, 1.5, 1)
print("The traffic intensity of Road B in the Evening: %lf" % calculate_traffic_intensity())

plot.figure()
plot.plot(np_queue_roadA_Evening[:, 1] / 3600, np_queue_roadA_Evening[:, 0], '-or', label='Road A')
plot.plot(np_queue_roadB_Evening[:, 1] / 3600, np_queue_roadB_Evening[:, 0], '-ob', label='Road B')
plot.xlabel("Now")
plot.ylabel("Queue Length")
plot.title("Evening")
plot.legend()
plot.show()

text_file.close()
