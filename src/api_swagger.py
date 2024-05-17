from flask_restx import Api

from app import app as __BOOSTED_APP__

api = Api(
    __BOOSTED_APP__,
    version="2.0",
    title="Boosted API",
    contact_url="https://iamjeremie.me/page/contact-me/",
    description='Provides a RESTFul API to record your time like the Android App "Boosted" does. The code isn´t however crafted by the Boosted Android team',
    license="GPL3",
)
