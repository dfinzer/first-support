from rq import Worker, Queue, Connection
from work import conn


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, ['default'])))
        worker.work()