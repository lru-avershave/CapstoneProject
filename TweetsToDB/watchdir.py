import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from ImportText import TextToTweet

def on_created(event):
    print(f"{event.src_path} has been created!")
    TextToTweet(event.src_path)

def watch():
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    path = "../example_data"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    my_observer.start()
    try:
        print("Starting program watching dir.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping program...")
        my_observer.stop()
        my_observer.join()