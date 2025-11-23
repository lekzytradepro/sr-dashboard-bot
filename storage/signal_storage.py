# storage/signal_storage.py

# Temporary in-memory storage for generated signals.
# Later you can connect this to a database if you want.

latest_signals = {}

def save_signal(asset, signal_data):
    latest_signals[asset] = signal_data

def get_signal(asset):
    return latest_signals.get(asset)

def get_all_signals():
    return latest_signals
