# https://adventofcode.com/2023/day/20
from collections import deque, defaultdict
import re
from math import lcm

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def solve(is_part_2):
    broadcaster = None
    flipflop_destinations = {}
    flipflop_values = {}
    conjunction_destinations = {}
    conjunction_values = {}

    # Find broadcaster and all conjunctions
    for line in lines:
        sep = line.split(" -> ")
        if line.startswith("broadcaster"):
            broadcaster = sep[1].split(", ")
        elif line.startswith("&"):
            _id = sep[0][1:]
            conjunction_destinations[_id] = sep[1].split(", ")
            conjunction_values[_id] = {}
    
    # Find all flipflops and link conjunctions
    for line in lines:
        sep = line.split(" -> ")
        if line.startswith("%"):
            _id = sep[0][1:]
            flipflop_destinations[_id] = sep[1].split(", ")
            flipflop_values[_id] = False
            for dest_modules in flipflop_destinations[_id]:
                if dest_modules in conjunction_destinations:
                    conjunction_values[dest_modules][_id] = False
        # Connect conjunctions with conjunctions
        elif line.startswith("&"):
            _id = sep[0][1:]
            for dest_modules in conjunction_destinations[_id]:
                if dest_modules in conjunction_destinations:
                    conjunction_values[dest_modules][_id] = False
    

    # Unreadable list comprehension for fun :)
    # Takes the root "rx", and find the conjunctions 2 nodes down - the nodes for which all flip flops feed into.
    targets = [conj for t in [conj for conj, links in conjunction_destinations.items() if "jq" in links] for conj, links in conjunction_destinations.items() if t in links]

    q = deque()
    
    num_low = 0
    num_high = 0
    button_press = 0
    all_cycles_found = False
    target_cycles = {}
    while not all_cycles_found:
        # Early termination for part 1
        if not is_part_2 and button_press == 1000:
            return num_low * num_high

        # We are pressing the button at this point, which of course increases the button count
        # and the low signal count
        button_press += 1
        num_low += 1

        # Send high signals to each of the destinations in the broadcaster
        for signal_dest in broadcaster:
            num_low += 1
            q.append(("broadcaster", signal_dest, False))
        
        while q:
            received_from, module, received_signal = q.popleft()
            new_signal = received_signal

            # If we encounter a "debug" module with no output, we can safely ignore
            if module not in flipflop_destinations and module not in conjunction_destinations:
                continue

            # We have a flipflop (or broadcaster) module
            if module in flipflop_values or module == "broadcaster":
                # Since we have a flipflop we must look at this map to find out where to send the signal
                next_dests = flipflop_destinations[module]

                # If we receive a high pulse, then we ignore it and continue
                if received_signal == True: continue
                # A low signal will invert the current signal
                else: new_signal = not flipflop_values[module]

                # Update the relevant module with its new signal
                flipflop_values[module] = new_signal
            # We have a conjunction
            elif module in conjunction_values:
                # Since we have a conjunction we must look at this map to find out where to send the signal
                next_dests = conjunction_destinations[module]

                # Put the received signal into "memory" for this conjunction
                remembered_pulses = conjunction_values[module]
                remembered_pulses[received_from] = received_signal

                # High pulses are remembered for all inputs - send a low pulse
                if all(high_signal == True for high_signal in remembered_pulses.values()):
                    new_signal = False
                # Not all of them are high pulses - send a high pulse
                else:
                    new_signal = True
            
            # We will now send the new signal to this module's destinations
            for next_dest in next_dests:
                # If a flip-flop module receives a high pulse, it is ignored and nothing happens
                # However, if a flip-flop module receives a low pulse, it flips between on and off.
                if new_signal == True:
                    num_high += 1
                else:
                    num_low += 1

                # If we are handling a module in our targets (and are on part 2), we have to do some additional checks
                if is_part_2 and next_dest in targets:
                    for targ in targets:
                        # If every module feeding into this conjunction is sending a high pulse, then the conjunction
                        # will send a low (which is what we want). In this case, we check if this is the first time
                        # we've seen this conjunction send a low signal, and if so, add it to our cycle tracker
                        if all(c == True for c in conjunction_values[targ].values()) and targ not in target_cycles:
                            target_cycles[targ] = button_press
                    
                    # If we have found a cycle for every conjunction node we are tracking, we can break out of the loop
                    if all(targ in target_cycles for targ in targets):
                        all_cycles_found = True
                        break

                q.append((module, next_dest, new_signal))

    return lcm(*target_cycles.values())


def solve_part_1():
    return solve(is_part_2=False)


def solve_part_2():
    return solve(is_part_2=True)

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
