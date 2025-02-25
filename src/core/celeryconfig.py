from core.config import DEBUG


if DEBUG:
    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/1"
else:
    broker_url = "redis://redis:6379/0"
    result_backend = "redis://redis:6379/1"


task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "Europe/Moscow"
enable_utc = True
