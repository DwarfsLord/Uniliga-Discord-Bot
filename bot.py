import discord
from PIL import Image, ImageFont, ImageDraw
import os

from dotenv import load_dotenv
# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()


intents = discord.Intents.none()
intents.messages = True

client = discord.Client(intents)

ergebnis_chanel_id = 902880440547946536

ergebnis_input_channel_name = 'ergebnisse-input'

font_bold = "/assets/Play-Bold.ttf"
font_regular = "/assets/Play-Regular.ttf"

win_colour = (255, 255, 255)
win_font = font_regular
lose_colour = (200, 200, 200)
lose_font = font_regular

game = ""
team_home = ""
team_oppo = ""
score_home = -1
score_oppo = -1


def find_font(image, string, font_name, max_x, font_size=40):
    font = ImageFont.truetype(font_name, size=font_size)
    while (image.multiline_textsize(string, font) > (max_x, 0)):
        font_size = font_size - 1
        font = ImageFont.truetype(font_name, size=font_size)
    return font


def draw_team_name(image, string, font_name, area_center_x, area_center_y, max_x, colour):
    font = find_font(image, string, font_name, max_x)
    x, y = image.multiline_textsize(string, font)
    image.multiline_text((area_center_x-x/2, area_center_y-y/2),
                         string, colour, font=font, align="center")


def draw_score(image, score_left, score_right, font_size=45):

    score_font = ImageFont.truetype(font_bold, size=font_size)

    x, y = image.multiline_textsize(str(score_left), score_font)

    image.multiline_text((235-x, 140), str(score_left),
                         (255, 255, 255), font=score_font, align="right")
    image.multiline_text((265, 140), str(score_right),
                         (255, 255, 255), font=score_font, align="left")

    x, y = image.multiline_textsize(":", score_font)
    image.multiline_text((250-x/2, 140), ":", (255, 255, 255),
                         font=score_font, align="center")


def draw_game(image, game):
    font = find_font(image, game, font_bold, 68, 30)
    x, y = image.multiline_textsize(game, font)
    image.multiline_text((5, 195-y), game, (255, 255, 255),
                         font=font, align="left")
    # image.multiline_text((5,195-y), game, (100,182,99), font = font, align = "left")


def draw_win(image):
    title = "WIN"
    font = ImageFont.truetype(font_bold, size=65)
    # font = ImageFont.truetype("Merriweather-Bold.ttf", size=65)
    x, y = image.multiline_textsize(title, font)
    image.multiline_text((250-x/2, -10), title,
                         (56, 139, 60), font=font, align="left")


def draw_loss(image):
    title = "LOSS"
    font = ImageFont.truetype(font_bold, size=65)
    x, y = image.multiline_textsize(title, font)
    image.multiline_text((250-x/2, -10), title,
                         (115, 40, 40), font=font, align="left")


def draw_draw(image):
    title = "TIE"
    font = ImageFont.truetype(font_bold, size=60)
    x, y = image.multiline_textsize(title, font)
    image.multiline_text((250-x/2, -10), title,
                         (99, 109, 196), font=font, align="left")


@client.event
async def on_message(message):
    print(message.channel)
    if (message.author.id != 902968959891021854 and str(message.channel) == ergebnis_input_channel_name):
        await questions(message)


async def questions(message):
    input = message.content

    print("test")

    global game
    global team_home
    global team_oppo
    global score_home
    global score_oppo

    if (input.find("!neu") != -1):
        game = team_home = team_oppo = ""
        score_home = score_oppo = -1
        await message.channel.send("Was wurde gespielt?")
    elif (game == ""):
        game = input
        print("Spiel: " + game)
        await message.channel.send("Wie heißt das Heimteam?")
    elif (team_home == ""):
        team_home = input
        print("Heim: " + team_home)
        await message.channel.send("Wie heißt das Gegnerteam?")
    elif (team_oppo == ""):
        team_oppo = input
        print("Gegner: " + team_oppo)
        await message.channel.send("Was war unser Score?")
    elif (score_home == -1):
        score_home = int(input)
        print("Punkte: " + str(score_home))
        await message.channel.send("Was war der gegnerische Score?")
    elif (score_oppo == -1):
        score_oppo = int(input)
        print("Punkte: " + str(score_oppo))
        await create_image(message.channel)
        await message.channel.send("""Passt das?
(Ja / !neu)""")
    elif (str(input) == "Ja"):
        await message.channel.send("""Ergebnis wurde gesendet!
Für weitere Ergebisse bitte _!neu_ verwenden.""")
        await create_image(message.guild.get_channel(ergebnis_chanel_id))


async def create_image(channel):
    global game
    global team_home
    global team_oppo
    global score_home
    global score_oppo

    background = Image.open("/assets/background2.png")
    image = ImageDraw.Draw(background)

    if (score_home > score_oppo):
        colour_home = win_colour
        colour_oppo = lose_colour
        font_home = win_font
        font_oppo = lose_font
        draw_win(image)
    elif (score_home < score_oppo):
        colour_home = lose_colour
        colour_oppo = win_colour
        font_home = lose_font
        font_oppo = win_font
        draw_loss(image)
    else:
        colour_home = win_colour
        colour_oppo = win_colour
        font_home = win_font
        font_oppo = win_font
        draw_draw(image)

    draw_team_name(image, team_home, font_home, 127, 100, 107, colour_home)
    draw_team_name(image, team_oppo, font_oppo, 373, 100, 107, colour_oppo)

    draw_score(image, score_home, score_oppo)

    draw_game(image, game)

    background.save("export.png")
    await channel.send("", file=discord.File('export.png'))
    os.remove('export.png')


client.run(os.environ.get("DISCORD_TOKEN"))
