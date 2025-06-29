# memory_manager.py
from datetime import datetime
import random

# Constants
BLOCK_SIZE = 1
TOTAL_BLOCKS = 100
TOTAL_MEMORY = BLOCK_SIZE * TOTAL_BLOCKS

# State
memory = [None] * TOTAL_BLOCKS  # Each block = None or (PID, color)
processes = {}  # PID: {name, start, size, color, status, alloc_time}
next_pid = 1

def generate_color():
    # Generate a distinct color
    return "#{:06x}".format(random.randint(0x111111, 0xEEEEEE))

def first_fit(process_name, size_kb):
    global next_pid
    blocks_needed = size_kb
    free_count = 0
    start_index = 0

    for i in range(TOTAL_BLOCKS):
        if memory[i] is None:
            if free_count == 0:
                start_index = i
            free_count += 1
            if free_count == blocks_needed:
                color = generate_color()
                for j in range(start_index, start_index + blocks_needed):
                    memory[j] = (next_pid, color)
                processes[next_pid] = {
                    'name': process_name,
                    'start': start_index,
                    'size': blocks_needed,
                    'color': color,
                    'status': 'Ready',
                    'alloc_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                result = f"Allocated {blocks_needed}KB to '{process_name}' (PID: {next_pid}) using First-Fit."
                next_pid += 1
                return result
        else:
            free_count = 0

    return f"Not enough contiguous memory for process '{process_name}' (needed: {blocks_needed} blocks)."

def best_fit(process_name, size_kb):
    global next_pid
    blocks_needed = size_kb
    best_start = -1
    best_size = float('inf')
    current_start = -1
    current_size = 0

    for i in range(TOTAL_BLOCKS + 1):
        if i < TOTAL_BLOCKS and memory[i] is None:
            if current_start == -1:
                current_start = i
            current_size += 1
        else:
            if current_size >= blocks_needed and current_size < best_size:
                best_start = current_start
                best_size = current_size
            current_start = -1
            current_size = 0

    if best_start != -1:
        color = generate_color()
        for j in range(best_start, best_start + blocks_needed):
            memory[j] = (next_pid, color)
        processes[next_pid] = {
            'name': process_name,
            'start': best_start,
            'size': blocks_needed,
            'color': color,
            'status': 'Ready',
            'alloc_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        result = f"Allocated {blocks_needed}KB to '{process_name}' (PID: {next_pid}) using Best-Fit."
        next_pid += 1
        return result

    return f"Not enough contiguous memory for process '{process_name}' (needed: {blocks_needed} blocks)."

def free(process_id):
    try:
        pid = int(process_id)
        if pid not in processes:
            return f"No process with PID {pid} found."

        start = processes[pid]['start']
        size = processes[pid]['size']
        for i in range(start, start + size):
            if memory[i] and memory[i][0] == pid:
                memory[i] = None

        name = processes[pid]['name']
        del processes[pid]
        return f"Freed {size}KB from process '{name}' (PID: {pid})."
    except ValueError:
        return "Invalid Process ID."

def compact_memory():
    global memory
    new_memory = [None] * TOTAL_BLOCKS
    new_index = 0
    for pid in sorted(processes):
        proc = processes[pid]
        size = proc['size']
        for i in range(size):
            new_memory[new_index + i] = (pid, proc['color'])
        proc['start'] = new_index
        new_index += size
    memory = new_memory
    return "Memory compaction completed."

def get_memory_blocks():
    """Returns a list of (PID, color) or None for each block"""
    return memory.copy()

def get_memory_state():
    block_display = [None if m is None else processes[m[0]]['name'] for m in memory]
    process_table = [{
        'PID': pid,
        'Name': info['name'],
        'Start': info['start'],
        'Size': info['size'],
        'Status': info['status'],
        'Allocated': info['alloc_time']
    } for pid, info in processes.items()]
    return {
        'blocks': block_display,
        'process_table': sorted(process_table, key=lambda x: x['Start'])
    }

def reset_memory():
    global memory, processes, next_pid
    memory = [None] * TOTAL_BLOCKS
    processes = {}
    next_pid = 1
    return "Memory has been completely reset."

def get_memory_blocks():
    """Returns list of (pid, color) tuples or None"""
    return memory.copy()
