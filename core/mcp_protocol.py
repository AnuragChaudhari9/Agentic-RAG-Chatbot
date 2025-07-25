import uuid
import datetime

class MCPMessage:
    def __init__(self, sender, receiver, msg_type, payload, trace_id=None, timestamp=None):
        self.sender = sender
        self.receiver = receiver
        self.msg_type = msg_type
        self.payload = payload
        self.trace_id = trace_id or str(uuid.uuid4())
        self.timestamp = timestamp or datetime.datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.msg_type,  # export as 'type'
            "trace_id": self.trace_id,
            "timestamp": self.timestamp,
            "payload": self.payload
        }

    def __repr__(self):
        return f"[{self.msg_type}] {self.sender} → {self.receiver} | {self.trace_id}"
