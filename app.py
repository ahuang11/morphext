import time
import random
import string
import panel as pn

RAW_CSS = """

nav#header {
    margin-left: auto;
    margin-right: auto;
    max-width: 60%;
}

h1 {
    margin-left: 2%;
    margin-right: 2%;
    font-size: 4em;
    font-weight: bold;
}

h3 {
    margin-left: 2%;
    margin-right: 2%;
    font-size: 1.5em;
}

textarea.bk.bk-input {
    font-size: 2.5em;
    font-family: monospace
}

.bk bk-clearfix {
    font-size: 1.25em;
    font-family: monospace
}

.bk.bk-slider-title {
    font-size: 1.25em;
    font-family: monospace
}

.bk.bk-btn.bk-btn-default {
    font-size: 1.25em;
}
"""

pn.extension(sizing_mode="stretch_width", raw_css=[RAW_CSS])


def get_random_character():
    """
    If all options are selected, return a random character.
    If only numbers are selected, return a random number.
    If only letters are selected, return a random letter.
    """
    options = toggle_group.value
    choices = ""
    if "Numbers" in options:
        choices += string.digits
    if "Letters" in options:
        choices += string.ascii_letters
    if "Symbols" in options:
        choices += string.punctuation
    if not choices:
        choices = string.ascii_letters
    random_char = random.choice(choices)
    return random_char


def update_text(iteration):
    word = text_input.value_input
    chars = ""
    for index in range(len(word)):
        if index <= (iteration / morph_iterations.value):
            chars += word[index]
        else:
            chars += get_random_character()
    morphing_text.object = f"{chars}"


def trigger(event):
    word = event.new
    for iteration in range((len(word) + 1) * morph_iterations.value):
        time.sleep(morph_speed.value)
        update_text(iteration)


text_input_placeholder = "What would you like to morph?"
text_input = pn.widgets.TextAreaInput(
    placeholder=text_input_placeholder,
    max_length=18,
    sizing_mode="stretch_both",
    align="center",
    margin=(0, 0),
)
text_input.param.watch(trigger, "value_input")
morph_speed = pn.widgets.FloatInput(
    name="Morph Speed", value=0.03, start=0.001, end=1, step=0.01
)
morph_iterations = pn.widgets.IntInput(
    name="Morph Iterations", value=3, start=1, end=100
)
toggle_group = pn.widgets.ToggleGroup(
    value=["Numbers", "Letters"],
    options=["Numbers", "Letters", "Symbols"],
)
widget_box = pn.WidgetBox(text_input, pn.Row(morph_speed, morph_iterations), toggle_group)

morphing_text = pn.pane.Markdown(
    object="", sizing_mode="stretch_both", style={"font-size": "4.5em"}, margin=(0, 0, 0, 25)
)


grid_spec = pn.GridBox(
    widget_box,
    morphing_text,
    ncols=2,
    min_height=300,
)

template = pn.template.FastListTemplate(
    title="M O R P H E X T",
    main=[grid_spec],
    main_max_width="90%",
    accent="fast",
    font="monospace",
    shadow=False,
    theme=pn.template.theme.DarkTheme,
)
template.servable()
