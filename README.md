# OzBargain-Deals-Bot

As I was in need of some wireless headphones, I built a deal notification bot to let me know via email when a deal popped up on OzBargain.

The bot uses the feedparser Python package to read in data from OzBargain’s RSS feed and the smtplib package to send out emails upon finding relevant deals. I also pushed the bot onto Heroku’s cloud computing platform to keep it scanning for deals 24/7. The Procfile and requirements.txt files were needed alongside the ozbargain_bot_latest.py file to get the bot running on Heroku. It suffices to say that I did end up purchasing my headphones through a deal from this bot.
