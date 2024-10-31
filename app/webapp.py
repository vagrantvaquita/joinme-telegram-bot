from urllib.parse import urljoin

from app.configs import WEBAPP_URL

CREATE_EVENT_URL = urljoin(WEBAPP_URL, "create")
LIST_EVENTS_URL = urljoin(WEBAPP_URL, "find")
LIST_MYEVENTS_URL = urljoin(WEBAPP_URL, "list")
