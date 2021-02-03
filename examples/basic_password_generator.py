import random


class password:
    def __init__(self, complexity):
        self.complexity = complexity
        self.lower = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]
        self.upper = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        self.special = [
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "_",
            "=",
            "+",
            "?",
        ]
        self.ambiguous = ["{", "}", "[", "]", "|", "<", ">", "/", ".", ",", "\\", '"']
        self.numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        self.character_set = {
            "lowercase": self.lower,
            "uppercase": self.upper,
            "special": self.special,
            "ambiguous": self.ambiguous,
            "numbers": self.numbers,
        }

        self.character_types = ["lower", "upper", "special", "numbers", "ambiguous"]

    def show_character_set(self):
        return self.character_set

    def show_character_types(self):
        return self.character_types

    def generate(self):
        included_characters = self.complexity["include"]
        if included_characters == []:
            raise ValueError(
                "Error: Please select at least one of: Lower Case, \
                Upper Case, Special Characters, Numbers or ambiguous"
            )
        password_length = int(self.complexity["length"])
        generated_password = ""
        password_complexity_sequence = []
        for character_count in range(password_length):
            selected_character_set = random.choice(included_characters)
            password_complexity_sequence.append(selected_character_set)
        for selected_character_set in password_complexity_sequence:
            new_character = random.choice(getattr(self, selected_character_set))
            generated_password += new_character

        return generated_password


complexity = {
    "length": 16,
    "include": ["lower", "upper", "special", "numbers", "ambiguous"],
}
pw = password(complexity).generate()

print(pw)
