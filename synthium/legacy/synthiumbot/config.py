"""SynthiumBot settings (RECONSTRUCTION, 2026-11-24).

The original ``Configuration File.txt`` held a live Telegram bot token, so it is not
copied into this public repository. The bot reads the token from the environment
instead. Set ``TELEGRAM_TOKEN`` before running ``python -m synthium.legacy.synthiumbot.main``.
"""
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
