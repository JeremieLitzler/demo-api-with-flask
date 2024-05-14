from flask_restx import Api

from app import app as __BOOSTED_APP__

api = Api(
    __BOOSTED_APP__,
    version="1.0",
    title="Boosted API",
    description="Provides a RESTFul API to record your time like the Android App does. The code isn´t however crafted by the Boosted Android team",
)
