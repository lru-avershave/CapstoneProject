import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from ImportText import TextToTweet

def on_created(event):
    '''
    If a .txt file is created, this event will fire off and add the new Tweets into the database.
    '''
    print(f"{event.src_path} has been created!")
    TextToTweet(event.src_path)

def watch():
    '''
    This watches the folder for any changes. In this case, it watches for any creation of .txt files.
    Once a file is created, it will go through and add the new tweets into the database.
    The Tweet model catches any identical Tweet using the Tweet ID.
    '''
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