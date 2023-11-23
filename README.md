<div>
    <img align="left" src="https://github.com/Kourva/CtrlBot/assets/118578799/406e0dba-c5f4-486d-b7a4-9b586e009a38" width=140 />
    <h3 align="center">CtrlBot</h3> 
    <p align="center">Rich feature group guard bot for Telegram groups &amp; supergroups</p>
</div>

```plaintext
I will help you to manage your group. I have many commands and features...
```

# Installation
First of all, you need to install few thing on your machine
+ `Python`: This bot is coded in pyhon language, so you need to install it before using the bot.
+ `Pip`: You need to install some libraries for this poject, so you need pip also.
+ `Git`: You need git to clone this repository. (this is **optional**: you can download ziped source file)
1. **Clone the repository**
```bash
git clone https://github.com/Kourva/CtrlBot
```
2. **Navigate to source directory**
```bash
cd CtrlBot
```
3. **Install requirements**
```bash
pip install -r requirements.txt
```
OK now you have one step to go. you need to config some variables before running bot...

# Configuration
Open `setting.py` with any editor you like and edit these sections:
+ **Token**: Set your bot token. Get one from [BotFather](https://t.me/BotFather)
```python
31 # Token for bot token. somthing like this: 1234567890:AABBCCDDEEFFGGHHIIIJJMMLLSS
32 TOKEN: str = "Bot Token"
```
+ **Sponsor Group**: Set the sponser group for admins, they are required to join before using bot:
```python
34 # Support or sponsor group ID
35 GROUP: str = "@Sponsor group username"
```
> This option is disabled by default. you need to enable it (See [**WIKI**](https://github.com/Kourva/CtrlBot/wiki) section below)
+ **Support**: All errors will be sent to the admin of bot, set the ID of admin or yourself:
```python
37 # Chat-ID of support admin to send errors 
38 SUPPORT: int = 1234567890
```
+ **Share Text**: This is needed when you want to share your bot to friend using forward.
```python
46 # Share LINK & TEXT used to share bot
47 SHARE_TEXT: str = "t.me/BotUsername"
48 SHARE_LINK: str = (
49     f"\n💥 Powerful & Free group guard bot for groups and super-groups!"
50     f"\n\n👾 Start now and enjoy"
51 )
```
Now we are ready to launch our bot:
```python
python main.py
```

# Want to learn more?
Visit **[Wiki](https://github.com/Kourva/CtrlBot/wiki)** page for more details.
