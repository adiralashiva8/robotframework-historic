from types import SimpleNamespace

# Store settings
settings = SimpleNamespace()

def store(key, value):
    global settings
    setattr(settings, key, value)

def get(key):
    global settings
    getattr(settings, key, None)
