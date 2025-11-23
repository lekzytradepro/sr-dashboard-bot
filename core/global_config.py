# core/global_config.py

class GlobalConfig:
    """
    Global configuration manager for your bot.
    Handles read/write of settings used across signals, AI engines,
    API keys, time filters, risk filters, etc.
    """

    # Default global settings
    settings = {
        "bot_name": "QuantumSignalEngine",
        "version": "1.0.0",
        "auto_send_signals": True,
        "pre_entry_enabled": True,
        "wait_time_between_signals": 60,  # seconds
        "use_dynamic_filters": True,
        "trend_filter_strength": "medium",
        "risk_filter": True,
        "allowed_sessions": ["London", "NewYork"],
        "enable_daily_stats": True
    }

    @classmethod
    def update(cls, key, value):
        cls.settings[key] = value

    @classmethod
    def get(cls, key):
        return cls.settings.get(key, None)

    @classmethod
    def all(cls):
        return cls.settings
