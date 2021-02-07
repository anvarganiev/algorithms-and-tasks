import numpy as np

orders = []
with open('input_ex2.txt') as input_file:
    amount = int(input_file.readline())
    for line in input_file.readlines():
        orders += [list(line.split())]

available_at = np.full(shape=amount, fill_value='00:00:00')
orders = np.array(sorted(orders))
used_couriers = 0

for order_id in range(amount):
    available_courier = np.argwhere(available_at <= orders[order_id][0])[0]
    if available_at[available_courier] == '00:00:00':
        used_couriers += 1  # assign order to a new courier
    available_at[available_courier] = orders[order_id][1]  # update time of availability
print(used_couriers)
