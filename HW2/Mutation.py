from Factory import Factory, JobSequence, Job
import random
class Mutation:
    def __init__(self, method):
        self.method = method
    
    def mutate(self, jobSequence: JobSequence):
        if self.method == "cut_insert":
            return self.cut_insert(jobSequence)
        elif self.method == "reverse":
            return self.reverse(jobSequence)
        elif self.method == "mixed":
            return self.mixed(jobSequence)
    
    def cut_insert(self, jobSequence: JobSequence):
        # cut and insert
        k = random.randint(0, jobSequence.num_of_jobs)
        return JobSequence(jobSequence.sequence[k:] + jobSequence.sequence[:k])
    
    def reverse(self, jobSequence: JobSequence):
        # reverse the sequence
        jobSequence.sequence.reverse()
        return jobSequence

    def mixed(self, jobSequence: JobSequence):
        #If random_value is less than 0.5, execute plan one; otherwise, execute plan two
        random_value = random.random()
        if random_value < 0.5:
            # cut and insert
            k = random.randint(0, jobSequence.num_of_jobs)
            jobSequence = JobSequence(jobSequence.sequence[k:] + jobSequence.sequence[:k])
        else:
            # reverse the sequence
            jobSequence.sequence.reverse()
        return jobSequence