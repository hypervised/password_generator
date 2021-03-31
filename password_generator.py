import random
import json
from multidict import MultiDict
from flask import Flask, render_template, flash, request, session
from werkzeug.exceptions import InternalServerError
from werkzeug.utils import html
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.fields.core import BooleanField, DecimalField, IntegerField
from wtforms.widgets.core import CheckboxInput

# Flask config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "somesecret1234"


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


@app.route("/complex")
def generate_strong_password():
    data = {
        "length": 16,
        "include": ["lower", "upper", "numbers", "special", "ambiguous"],
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
    ambiguous = CheckboxInput("ambiguous:")
    returned_password = TextField("password")


@app.route("/", methods=["GET", "POST"])
def custom():
    form = password_form(request.form)

    if form.validate():
        include = []
        length = request.form["length"]

        character_types = ["lower", "upper", "special", "numbers", "ambiguous"]
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
            return render_template(
                "custom.html", form=form, returned_password=returned_password
            )

        except ValueError as ComplexityError:
            complexity_error = str(ComplexityError.args)
            flash(complexity_error)

    return render_template("custom.html", form=form)


if __name__ == "__main__":
    app.run(port=8080)
