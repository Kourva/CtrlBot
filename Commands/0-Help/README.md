# Help command handler
If you want to use this bot with your own website and channel, change this section:
```python
# Making reply markup for help
Markups: ClassVar[Any] = telebot.util.quick_markup({
    "Website": {
        "url": "https://kourva.github.io/GroupCtrl"
    },
    "Channel": {
        "url": "https://t.me/GroupCtrl"
    },
    "Get on Private chat": {
        "callback_data": f"Send_Help_Private@{user.id}"
    }
}, row_width=2)
```
