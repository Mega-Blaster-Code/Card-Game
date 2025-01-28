import random
import time


def to_hex(nome):
    return nome.encode('utf-8').hex()

def to_string(dado):
    return bytes.fromhex(dado).decode('utf-8')

def get_cards():
    try:
        with open("cards_info", "r") as arq:
            cards = []
            for line in arq:
                line = line.strip()
                line = to_string(line)
                card_info = line
                cards.append(card_info.split("f")[0].split(","))
            return cards
    except:
        print("erro")
        return []

def write_card(id, level):
    card_data = f"{id},{level}f{random.randint(0,999999)}"
    card = to_hex(card_data)

    with open("cards_info", "a") as arq:
        arq.write(card+"\n")


def remove_card(name):
    cards = get_cards()
    new_cards = [card for card in cards if card[0] != name]

    with open("cards_info", "w") as arq:
        for card in new_cards:
            card_data = ",".join(card)
            card = to_hex(card_data)
            arq.write(card + "\n")
