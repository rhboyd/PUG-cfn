import logging
import os
import time
import random

import boto3
from crhelper import CfnResource

logger = logging.getLogger(__name__)
helper = CfnResource(json_logging=False, log_level="DEBUG", boto_level="CRITICAL")

pokedex = {
    "1": ("Bulbasaur", 9),
    "2": ("Ivysaur", 10),
    "3": ("Venusaur", 10),
    "4": ("Charmander", 9),
    "5": ("Charmeleon", 10),
    "6": ("Charizard", 10),
    "7": ("Squirtle", 9),
    "8": ("Wartortle", 10),
    "9": ("Blastoise", 10),
    "10": ("Caterpie", 1),
    "11": ("Metapod", 2),
    "12": ("Butterfree", 4),
    "13": ("Weedle", 1),
    "14": ("Kakuna", 2),
    "15": ("Beedrill", 4),
    "16": ("Pidgey", 1),
    "17": ("Pidgeotto", 1),
    "18": ("Pidgeot", 10),
    "19": ("Rattata", 1),
    "20": ("Raticate", 1),
    "21": ("Spearow", 1),
    "22": ("Fearow", 1),
    "23": ("Ekans", 1),
    "24": ("Arbok", 2),
    "25": ("Pikachu", 5),
    "26": ("Raichu", 5),
    "27": ("Sandshrew", 1),
    "28": ("Sandslash", 1),
    "29": ("Nidoran Female", 1),
    "30": ("Nidorina", 1),
    "31": ("Nidoqueen", 10),
    "32": ("Nidoran Male", 1),
    "33": ("Nidorino", 1),
    "34": ("Nidoking", 10),
    "35": ("Clefairy", 3),
    "36": ("Clefable", 7),
    "37": ("Vulpix", 3),
    "38": ("Ninetales", 10),
    "39": ("Jigglypuff", 1),
    "40": ("Wigglytuff", 4),
    "41": ("Zubat", 1),
    "42": ("Golbat", 1),
    "43": ("Oddish", 1),
    "44": ("Gloom", 1),
    "45": ("Vileplume", 4),
    "46": ("Paras", 1),
    "47": ("Parasect", 1),
    "48": ("Venonat", 1),
    "49": ("Venomoth", 1),
    "50": ("Diglett", 1),
    "51": ("Dugtrio", 2),
    "52": ("Meowth", 1),
    "53": ("Persian", 2),
    "54": ("Psyduck", 1),
    "55": ("Golduck", 1),
    "56": ("Mankey", 1),
    "57": ("Primeape", 2),
    "58": ("Growlithe", 4),
    "59": ("Arcanine", 10),
    "60": ("Poliwag", 1),
    "61": ("Poliwhirl", 4),
    "62": ("Poliwrath", 5),
    "63": ("Abra", 5),
    "64": ("Kadabra", 4),
    "65": ("Alakazam", 10),
    "66": ("Machop", 1),
    "67": ("Machoke", 1),
    "68": ("Machamp", 4),
    "69": ("Bellsprout", 1),
    "70": ("Weepinbell", 1),
    "71": ("Victreebel", 3),
    "72": ("Tentacool", 1),
    "73": ("Tentacruel", 1),
    "74": ("Geodude", 1),
    "75": ("Graveler", 1),
    "76": ("Golem", 10),
    "77": ("Ponyta", 4),
    "78": ("Rapidash", 6),
    "79": ("Slowpoke", 1),
    "80": ("Slowbro", 1),
    "81": ("Magnemite", 1),
    "82": ("Magneton", 2),
    "83": ("Farfetch'd", 3),
    "84": ("Doduo", 1),
    "85": ("Dodrio", 1),
    "86": ("Seel", 1),
    "87": ("Dewgong", 2),
    "88": ("Grimer", 1),
    "89": ("Muk", 3),
    "90": ("Shellder", 7),
    "91": ("Cloyster", 7),
    "92": ("Gastly", 3),
    "93": ("Haunter", 4),
    "94": ("Gengar", 10),
    "95": ("Onix", 3),
    "96": ("Drowzee", 1),
    "97": ("Hypno", 2),
    "98": ("Krabby", 1),
    "99": ("Kingler", 2),
    "100": ("Voltorb", 1),
    "101": ("Electrode", 2),
    "102": ("Exeggcute", 4),
    "103": ("Exeggutor", 10),
    "104": ("Cubone", 5),
    "105": ("Marowak", 5),
    "106": ("Hitmonlee", 8),
    "107": ("Hitmonchan", 8),
    "108": ("Lickitung", 5),
    "109": ("Koffing", 2),
    "110": ("Weezing", 5),
    "111": ("Rhyhorn", 4),
    "112": ("Rhydon", 5),
    "113": ("Chansey", 8),
    "114": ("Tangela", 2),
    "115": ("Kangaskhan", 8),
    "116": ("Horsea", 1),
    "117": ("Seadra", 3),
    "118": ("Goldeen", 1),
    "119": ("Seaking", 2),
    "120": ("Staryu", 6),
    "121": ("Starmie", 10),
    "122": ("Mr. Mime", 8),
    "123": ("Scyther", 8),
    "124": ("Jynx", 6),
    "125": ("Electabuzz", 9),
    "126": ("Magmar", 8),
    "127": ("Pinsir", 8),
    "128": ("Tauros", 5),
    "129": ("Magikarp", 1),
    "130": ("Gyarados", 1),
    "131": ("Lapras", 9),
    "132": ("Ditto", 7),
    "133": ("Eevee", 9),
    "134": ("Vaporeon", 10),
    "135": ("Jolteon", 10),
    "136": ("Flareon", 10),
    "137": ("Porygon", 10),
    "138": ("Omanyte", 10),
    "139": ("Omastar", 10),
    "140": ("Kabuto", 10),
    "141": ("Kabutops", 10),
    "142": ("Aerodactyl", 10),
    "143": ("Snorlax", 9),
    "144": ("Articuno", 10),
    "145": ("Zapdos", 10),
    "146": ("Moltres", 10),
    "147": ("Dratini", 8),
    "148": ("Dragonair", 8),
    "149": ("Dragonite", 10),
    "150": ("Mewtwo", 10),
    "151": ("Mew", 10),
}

@helper.create
def create(event, context):
    dynamo_client = _client(event, "dynamodb")
    try:
        for entry in pokedex.keys():
            response = dynamo_client.put_item(
                TableName=event["ResourceProperties"]['TableName'],
                Item={
                    'PokemonNumber': {'S': entry},
                    'PokemonName': {'S': pokedex[entry][0]},
                    'Rarity': {'N': str(pokedex[entry][1])},
                    'Seen': {'BOOL': False}
                }
            )
            time.sleep(1.0/5.0)
    except Exception as e:
        print(e)

    helper.Data.update({"Starter": str(random.randint(0, 150))})
    return

# Need this stub function to prevent errors
@helper.update
def update(event, context):
    logger.info("Got Update")


# Need this stub function to prevent errors
@helper.delete
def delete(event, context):
    logger.info("Got Delete")
    #Scan Table and delete every entry


def handler(event, context):
    print(event)
    helper(event, context)


def _client(event, client_type):
    r = os.getenv("AWS_REGION")
    return boto3.client(client_type, region_name=r)
