from collections import defaultdict, deque

auto_reply_enabled = True
AUTO_REPLY_DELAY = 15

chat_histories = defaultdict(lambda: deque(maxlen=25))
messages_log = {}
auto_reply_timers = {}
last_client_message = {}
booking_data = defaultdict(lambda: {
    "service": None,
    "master": None,
    "time": None
})
