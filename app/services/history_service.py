from collections import deque
from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4


class PredictionHistory:
    def __init__(self, max_items=30):
        self._items = deque(maxlen=max_items)
        self._lock = Lock()

    def add(self, label, confidence, demo, source_filename):
        item = {
            "id": uuid4().hex[:12],
            "label": label,
            "confidence": round(float(confidence), 4),
            "demo": bool(demo),
            "source": source_filename or "recording.wav",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        with self._lock:
            self._items.appendleft(item)
        return item

    def list_recent(self):
        with self._lock:
            return list(self._items)


prediction_history = PredictionHistory()
