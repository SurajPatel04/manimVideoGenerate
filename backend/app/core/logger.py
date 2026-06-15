import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),            # logs to console
        logging.FileHandler("app.log"),     # logs also go to app.log
    ]
)

logger = logging.getLogger("manim_video")
