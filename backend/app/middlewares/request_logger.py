import time

from flask import g, request


def register_request_logger(app):
    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def log_request(response):
        duration_ms = round((time.time() - g.get("start_time", time.time())) * 1000, 2)
        app.logger.info(
            f"{request.method} {request.path} -> {response.status_code} ({duration_ms}ms)"
        )
        return response
