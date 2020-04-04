# telegram-taunt

Telegram bot in inline mode which sends short audio files. Inpired by "taunts" in Age of Empires II (sent as a reaction to something that has happened in the game).

# Bot usage

Taunts are described in the database by fields "name", "content", "voice", "category" and "source", and they have an immutable ID.

Find taunts which contains exactly "foo bar" in any field of their description:

    @TauntBot foo bar

Find taunts which contains both "abc" and "xyz":

    @TauntBot abc & xyz 

Find taunts which contain "qwerty" in their "source" field:

    @TauntBot source: qwerty

Find taunts which have the voices "X" and "Y" and have the word "abc" in their content:

    @TauntBot voice: X & voice: Y & content: abc

Show 50 taunts sorted by ID starting from ID "234"

    @TauntBot 234

# config.py

    # Telegram bot's token
    botToken = 'your token here'
    # taunt http URL
    httpURL = 'url of dir with taunts'
    # easter eggs
    easterEggs = [
        ['some words', 'ID of taunt which will be shown by the bot when these words are typed'],
        ['example', '100']
    ]

# Requirements

* python3.6 or higher
* [requests](http://docs.python-requests.org/en/master/)

# Additional info

* [ogg encoding](https://stackoverflow.com/questions/40245871/telegram-api-sendvoice-method-sends-voice-as-file)