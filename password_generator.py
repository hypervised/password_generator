import random
import json
from flask import Flask, render_template, flash, request
from werkzeug.exceptions import InternalServerError
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.fields.core import BooleanField, DecimalField, IntegerField
from wtforms.widgets.core import CheckboxInput

# Flask config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "7d441f27d441f27567d441f2b6176a"


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
        self.ambiguos = ["{", "}", "[", "]", "|", "<", ">", "/", ".", ",", "\\", '"']
        self.numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        self.character_set = {
            "lowercase": self.lower,
            "uppercase": self.upper,
            "special": self.special,
            "ambiguos": self.ambiguos,
            "numbers": self.numbers,
        }

        self.character_types = ["lower", "upper", "special", "numbers", "ambiguos"]

    def show_character_set(self):
        return self.character_set

    def show_character_types(self):
        return self.character_types

    def generate(self):
        lower = self.lower
        upper = self.upper
        special = self.special
        numbers = self.numbers
        ambiguos = self.ambiguos
        included_characters = self.complexity["include"]
        if included_characters == []:
            raise ValueError(
                "The requested complexity does not meet the minimum complexity requirement"
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


@app.route("/complex")
def generate_strong_password():
    data = {
        "length": 16,
        "include": ["lower", "upper", "numbers", "special", "ambiguos"],
    }
    pw = password(complexity=data)
    returned_password = pw.generate()
    return returned_password


@app.route("/simple")
def generate_weak_password():
    data = {
        "length": 6,
        "include": ["lower", "numbers"],
    }
    pw = password(complexity=data)
    returned_password = pw.generate()
    return returned_password


class password_form(Form):
    length = IntegerField("length:", validators=[validators.required()])
    lower = BooleanField("lower:")
    upper = CheckboxInput("upper:")
    special = CheckboxInput("special:")
    number = CheckboxInput("number:")
    ambiguos = CheckboxInput("ambiguos:")


@app.route("/", methods=["GET", "POST"])
def custom():
    form = password_form(request.form)

    if form.validate():
        include = []
        length = request.form["length"]

        character_types = ["lower", "upper", "special", "numbers", "ambiguos"]
        for character_type in character_types:
            try:
                status = request.form[character_type]
                if status == "on":
                    include.append(character_type)

            except KeyError:
                pass

        data = {
            "length": length,
            "include": include,
        }

        pw = password(complexity=data)
        try:
            returned_password = pw.generate()
            return returned_password

        except ValueError as ComplexityError:
            print(ComplexityError.args)
            return render_template("custom.html", form=form)

    return render_template("custom.html", form=form)


if __name__ == "__main__":
    app.run(port=8080)
