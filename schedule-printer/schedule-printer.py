import os
from datetime import datetime

import download
try: 
    import parse
except Exception: 
    download.main()
    import parse


NOW = datetime.now()
SCHEDULE_PATH = os.path.join(download.ASSETS_FOLDER, 'schedule.html')
UPDATE_THRESHOLD_MINUTES = 15


def ping():
    last_modified = datetime.fromtimestamp(os.stat(SCHEDULE_PATH).st_mtime)
    elapsed = NOW - last_modified

    if (elapsed.seconds / 60) > UPDATE_THRESHOLD_MINUTES: 
        download.main()


def long_table():
    return parse.main()
