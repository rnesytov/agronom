from datetime import timedelta
import os


EMAIL_SENDING_TIMEOUT = timedelta(seconds=30)

MAGIC_LINK_URI = "http://api.master.agronom.takewing.ru/api/v0_1/auth/activate/"
MAGIC_LINK_EXPIRES_IN = timedelta(hours=12)

VK_REDIRECT_URI = "http://takewing.ru"
FB_REDIRECT_URI = "https://takewing.ru/"  # Trailing slash is important
GA_REDIRECT_URI = "https://takewing.ru"

FB_CLIENT_ID = os.environ.get(
    "FB_CLIENT_ID",
    "385739375589666"
)  # TODO: drop when secrets enabled
FB_CLIENT_SECRET = os.environ.get(
    "FB_CLIENT_SECRET",
    "d42259b5cd592627e53fc87162605fce"
)
GA_CLIENT_ID = os.environ.get(
    "GA_CLIENT_ID",
    "211000367150-89rkp2p1ln0b3jskv0jeb42cae4b4i7b.apps.googleusercontent.com"
)
GA_CLIENT_SECRET = os.environ.get(
    "GA_CLIENT_SECRET",
    "LXkJGquARrZhmRwkO4tSCbzh"
)

CADASTRAL_INFO_TIMEOUT_DELAY = 60
CADASTRAL_API_TIMEOUT = 10

WEATHER_API_KEY = '570cabc13dca49dab1295355190104'
WEATHER_API_TIMEOUT = 10
WEATHER_HISTORY_DAYS_IN_BULK = 30
WEATHER_HISTORY_COUNT_BULKS = 3
