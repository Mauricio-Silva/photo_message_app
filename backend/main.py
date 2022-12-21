# cSpell:disable
try:
    import flask
    import json
    import uuid
    import PIL
    import os
    import io
except ImportError:
    raise ImportError("\033[31mIt was not possible to perform imports\033[m")


from app import app


app.run(host="0.0.0.0", debug=True, port=9700)




