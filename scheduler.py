# scheduler.py
import time
from collections import deque

class ProcessScheduler:
    def __init__(self):
        self.process_queue = []
        self.schedule_history = []
        self.current_pid = 1
        self.current_time = 0
        self.quantum = 2  # Default time quantum for Round Robin

    def add_process(self, name, burst_time):
        """Add a new process with auto-generated PID and status"""
        try:
            burst_time = int(burst_time)
            if burst_time <= 0:
                raise ValueError
        except ValueError:
            return "Burst time must be a positive integer."

        pid = self.current_pid
        self.current_pid += 1

        self.process_queue.append({
            'pid': pid,
            'name': name,
            'burst_time': burst_time,
            'remaining_time': burst_time,
            'arrival_time': self.current_time,
            'status': 'Ready',
            'start_time': None,
            'end_time': None
        })
        return f"Process '{name}' (PID: {pid}) added with burst time {burst_time}ms."

    def reset_processes(self):
        """Clear all processes and reset scheduler state"""
        self.process_queue = []
        self.schedule_history = []
        self.current_time = 0
        return "Scheduler has been reset."

    def fcfs_schedule(self):
        """First-Come-First-Served scheduling algorithm"""
        if not self.process_queue:
            return "No processes to schedule."

        timeline = []
        current_time = self.current_time

        for process in sorted(self.process_queue, key=lambda p: p['arrival_time']):
            if process['status'] != 'Completed':
                process['status'] = 'Running'
                process['start_time'] = current_time

                start = current_time
                end = current_time + process['burst_time']
                timeline.append({
                    'pid': process['pid'],
                    'name': process['name'],
                    'start': start,
                    'end': end,
                    'duration': process['burst_time']
                })

                current_time = end
                process['end_time'] = end
                process['status'] = 'Completed'

        self.current_time = current_time
        self.schedule_history.extend(timeline)
        return timeline

    def round_robin_step(self):
        """Execute one step of Round Robin scheduling"""
        if not any(p['remaining_time'] > 0 for p in self.process_queue):
            return "All processes completed."

        for process in self.process_queue:
            if process['remaining_time'] > 0:
                if process['status'] != 'Running':
                    process['status'] = 'Running'
                    if process['start_time'] is None:
                        process['start_time'] = self.current_time

                exec_time = min(self.quantum, process['remaining_time'])
                start = self.current_time
                end = start + exec_time

                timeline_entry = {
                    'pid': process['pid'],
                    'name': process['name'],
                    'start': start,
                    'end': end,
                    'duration': exec_time
                }

                process['remaining_time'] -= exec_time
                self.current_time = end

                if process['remaining_time'] <= 0:
                    process['status'] = 'Completed'
                    process['end_time'] = end
                else:
                    process['status'] = 'Ready'

                self.schedule_history.append(timeline_entry)
                return timeline_entry

        return "No processes ready to execute."

    def get_process_queue(self):
        """Return the current process queue with details"""
        return sorted(self.process_queue, key=lambda p: p['arrival_time'])

    def get_process_details(self, pid):
        """Get detailed information for a specific process"""
        for process in self.process_queue:
            if process['pid'] == pid:
                return process
        return None

    def visualize_schedule(self):
        """Generate Gantt chart visualization data"""
        if not self.schedule_history:
            return []

        # Create timeline visualization
        visualization = []
        for entry in self.schedule_history:
            visualization.append({
                'pid': entry['pid'],
                'name': entry['name'],
                'start': entry['start'],
                'end': entry['end'],
                'duration': entry['duration']
            })
        return visualization