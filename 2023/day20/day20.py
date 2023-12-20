# https://adventofcode.com/2023/day/20
from collections import deque, defaultdict
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def solve_part_1():
    # & inverter/conjunction
    # % flipflop
    # broadcaster -> low pulse


    broadcaster = None
    flipflop_destinations = {}
    flipflop_values = {}
    conjunction_destinations = {}
    conjunction_values = {}
    ans = 0

    # Find broadcaster and all conjunctions
    for line in lines:
        sep = line.split(" -> ")
        if line.startswith("broadcaster"):
            broadcaster = sep[1].split(", ")
            print("Broadcaster found:", broadcaster)
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
    q = deque()
    print("broadcaster", broadcaster)
    print("flipflop dests", flipflop_destinations)
    print("flipflop vals", flipflop_values)
    print("conjunction dests", conjunction_destinations)
    print("conunction vals", conjunction_values)
    
    m = {
        True: "high",
        False: "low"
    }
    num_low = 0
    num_high = 0
    button_press = 0
    while True:
        if button_press == 1000:
            return num_low * num_high
        button_press += 1
        if button_press % 1_000_000 == 0:
            print("Press:", button_press)
        # print("-----")
        # print("flipflop vals", flipflop_values)
        # print("conunction vals", conjunction_values)
        # print("-----")
        # input()
        # print("button -low-> broadcaster")
        num_low += 1
        # Send high signals to each of the destinations in the broadcaster
        for signal_dest in broadcaster:
            # flipflop_values[signal_dest] = False
            num_low += 1
            q.append(("broadcaster", signal_dest, False))
        
        while q:
            received_from, module, received_signal = q.popleft()
            new_signal = received_signal
            # print()
            # print(f"{received_from} -{m[received_signal]}-> {module}")
            # if module in flipflop_values:
            #     print(f"module {module} has {m[flipflop_values[module]]} signal")
            # print(conjunction_values)
            # print(f"Module {module} {flipflop_values}")
            # print("Module", module, conjunction_values)

            if module == "rx":
                if received_signal == False:
                    return button_press
                # print("IN RX")
                # print(received_signal)
                # input()
                # print(conjunction_values)
                continue
            elif module == "output":
                continue


            if module in flipflop_values or module == "broadcaster":
                # If we receive a high pulse, then we ignore it and continue
                if received_signal == True:
                    continue
                # A low signal will invert the current signal
                else:
                    new_signal = not flipflop_values[module]

                flipflop_values[module] = new_signal
                next_dests = flipflop_destinations[module]
                # print("module", module, received_signal, new_signal)

            elif module in conjunction_values:
                next_dests = conjunction_destinations[module]

                # print(1, conjunction_values[module])
                remembered_pulses = conjunction_values[module]
                remembered_pulses[received_from] = received_signal
                # print(2, conjunction_values[module])
                # High pulses are remembered for all inputs - send a low pulse
                # print("------------")
                # print(conjunction_values)
                # print(remembered_pulses)
                # print(remembered_pulses[received_from])
                # print("------------")
                if all(high_signal == True for high_signal in remembered_pulses.values()):
                    new_signal = False
                # Not all of them are high pulses - send a high pulse
                else:
                    new_signal = True
                
                # 
                # remembered_pulses[received_from] = received_signal
                # remembered_pulses[received_from] = new_signal # WAS WORKIGN
                # conjunction_values[module] = new_signal

            else:
                print('module', module)
                # continue
                assert False
            
            # print("Next", next_dests)
            for next_dest in next_dests:
                # If a flip-flop module receives a high pulse, it is ignored and nothing happens
                # However, if a flip-flop module receives a low pulse, it flips between on and off.
                # print(module, f"-{m[new_signal]}->", next_dest)
                if new_signal == True:
                    num_high += 1
                else:
                    num_low += 1
                q.append((module, next_dest, new_signal))

        
    print("low", num_low, "high", num_high)
            # q.append(next_dest)

        # print("Curr", module, pulse)
        # input()
    return num_low * num_high


def solve_part_2():
    ans = 0
    for line in lines:
        pass
    return ans


# > 310644688
# > 332991527
print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

