from janusbackup.worker.jobs import BaseJob


class JobManager:
    @classmethod
    def get_jobs(cls, only_active: bool = True):
        jobs = BaseJob.__subclasses__()

        if only_active:
            jobs = list(filter(lambda j: j.is_active, jobs))

        return jobs
