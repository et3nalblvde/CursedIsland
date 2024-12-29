import json


SAVE_FILE = "config/save_game.json"

def save_game(character, inventory, current_dialogue, location):

    game_data = {
        "location": location,
        "character": {
            "x": character.rect.x,
            "y": character.rect.y,
            "health": character.health
        },
        "progress": {
            "current_dialogue": current_dialogue
        },
        "inventory": inventory
    }


    with open(SAVE_FILE, 'w') as file:
        json.dump(game_data, file, indent=4)

    print("Игра сохранена!")

def load_game(character):

    try:
        with open(SAVE_FILE, 'r') as file:
            game_data = json.load(file)


        location = game_data["location"]
        character.rect.x = game_data["character"]["x"]
        character.rect.y = game_data["character"]["y"]
        character.health = game_data["character"]["health"]

        current_dialogue = game_data["progress"]["current_dialogue"]
        inventory = game_data["inventory"]

        print("Игра загружена!")
        return current_dialogue, inventory, location
    except FileNotFoundError:
        print("Не удалось найти файл сохранения. Начинаем новую игру.")
        return 1, [], 1
    except json.JSONDecodeError:
        print("Ошибка при чтении файла сохранения. Начинаем новую игру.")
        return 1, [], 1
