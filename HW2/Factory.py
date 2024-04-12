class Job:
    def __init__(self, id):
        self.id = id
        self.processingTime = []
        self.minimalTime = -1
    def add(self, time):
        self.processingTime.append(time)
    def calculateMinimalTime(self):
        if self.minimalTime == -1:
            self.minimalTime = sum(self.processingTime)
        return self.minimalTime
    
class JobSequence:
    def __init__(self, jobs: list[Job]):
        self.sequence = jobs
        self.num_of_jobs = len(self.sequence)
        self.fitness = -1
    def print(self):
        for job in self.sequence:
            print('{:02}'.format(job.id), end=" ")
        print()

class Factory:
    def __init__(self, num_of_machines: int):
        self.num_of_machines = num_of_machines
    
    def calculateMakespan(self, jobSequence: JobSequence):
        machine_end_time = [0] * self.num_of_machines
        job_end_time = [0] * jobSequence.num_of_jobs
        for job in jobSequence.sequence:
            last_end_time = 0
            start_time = 0
            end_time = 0
            for machine in range(self.num_of_machines):
                last_end_time = end_time
                start_time = max(machine_end_time[machine], last_end_time)
                end_time = start_time + job.processingTime[machine]
                machine_end_time[machine] = end_time
            job_end_time[job.id] = end_time
        return job_end_time[jobSequence.sequence[-1].id]