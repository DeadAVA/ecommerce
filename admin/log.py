from flask import request
from datetime import datetime
from models.models import ActivityLog, db

def log_activity(user_id, action, extra_info=None):
    ip = request.remote_addr
    log = ActivityLog(user_id=user_id, action=action, ip_address=ip, extra_info=extra_info)
    db.session.add(log)
    db.session.commit()