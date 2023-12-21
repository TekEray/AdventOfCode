from collections import defaultdict, deque
import os
import math

def readInput():
    script_dir = os.path.dirname(__file__)
    rel_path = "inputs/input.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path,'r') as f:
        return f.read().splitlines()

modules = defaultdict(lambda: {'prefix':'', 'state': 0, 'memory': [], 'outputs': [], 'inputs': []})

lowHighDict = {'low': 0,
               'high':1}


def parseInput(input):
    # Parse module configuration
    for line in input:
        source, destinations = line.split(' -> ')
        source = source.strip()

        if source.startswith('%') or source.startswith('&'):
            module_name = source[1:]
            prefix = source[:1]
        else:
            prefix = ''
            module_name = source
        # Set the 'outputs' field for all modules
        modules[module_name]['outputs'] = destinations.split(', ')
        modules[module_name]['prefix'] = prefix
        for dest in destinations.split(', '):
            modules[dest]['inputs'].append(module_name)
            modules[dest]['memory'].append(0)

def process_pulse(module, pulse):
    if modules[module]['prefix'] == '%':  # Flip-flop module
        if pulse == 'low':
            modules[module]['state'] = 1 - modules[module]['state']
            return 'high' if modules[module]['state'] == 1 else 'low'
        else:
            return ''

    elif modules[module]['prefix'] == '&':  # Conjunction module
        if all(modules[module]['memory']):
            return 'low'
        else:
            return 'high'

    else:  # Broadcaster or other module
        return pulse


def push_button(times):
    low_pulse_count = 0
    high_pulse_count = 0
    for _ in range(times):
        q1 = deque([('broadcaster', 'low')])
        while q1:
            module, pulse = q1.popleft()
            if pulse == 'low':
                low_pulse_count += 1
            elif pulse == 'high':
                high_pulse_count += 1
            new_pulse = process_pulse(module, pulse)
            if not new_pulse:
                continue
            outputs = modules[module]['outputs']
            for new_module in outputs:
                new_module_dict = modules[new_module]
                if new_module_dict['prefix'] == '&':
                    input_idx = new_module_dict['inputs'].index(module)
                    new_module_dict['memory'][input_idx] = lowHighDict[new_pulse]
                q1.append((new_module, new_pulse))
    return low_pulse_count, high_pulse_count

def repeat_rx_low():
    i=0
    stop = False
    jm_memory_count = [0,0,0,0]
    while not stop:
        i += 1
        q1 = deque([('broadcaster', 'low')])
        while q1:
            module, pulse = q1.popleft()
            new_pulse = process_pulse(module, pulse)
            if module == 'jm' and any(modules[module]['memory']): #and lowHighDict[new_pulse]:
                for idx, mem in enumerate(modules[module]['memory']):
                    if mem and jm_memory_count[idx] == 0:
                        jm_memory_count[idx] = i
                    if 0 not in jm_memory_count:
                        stop = True
            if not new_pulse:
                continue
            outputs = modules[module]['outputs']
            for new_module in outputs:
                new_module_dict = modules[new_module]
                if new_module_dict['prefix'] == '&':
                    input_idx =new_module_dict['inputs'].index(module)
                    new_module_dict['memory'][input_idx] = lowHighDict[new_pulse]
                q1.append((new_module, new_pulse))
    return jm_memory_count

def main():
    global modules
    inputPuzzle = readInput()
    parseInput(inputPuzzle)
    low_pulse_count, high_pulse_count = push_button(1000)
    print('LOW: ',low_pulse_count, ' HIGH: ', high_pulse_count)
    print('PART A: ', low_pulse_count*high_pulse_count)

    modules = defaultdict(lambda: {'prefix':'', 'state': 0, 'memory': [], 'outputs': [], 'inputs': []})
    parseInput(inputPuzzle)
    print('PART B: ', math.lcm(*repeat_rx_low()))

if __name__ == '__main__':
    main()