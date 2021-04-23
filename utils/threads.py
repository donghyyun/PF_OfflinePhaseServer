import threading


def get_active_threads():
    threads = []
    for thread in threading.enumerate():
        if thread.name.startswith('Main') or thread.name.startswith('pymongo'):
            continue
        threads.append(thread)

    return threads


def processes_join(process_name):
    for thread in threading.enumerate():
        name = thread.getName()

        if name.startswith(process_name):
            thread.join()


def set_thread_name(name):
    thread = threading.current_thread()
    thread.name = name + " " + thread.name
