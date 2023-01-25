import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import numpy as np

# -------------- refrence docs: --------------

# https://developer.mozilla.org/en-US/docs/Games/Techniques/Tilemaps

# ------------------------------------------------------------------------


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(
    page_title="The Shadows’s Den 2", page_icon="🗡️", initial_sidebar_state="collapsed"
)

# @st.cache
def fetch_data(level_name):
    df = pd.read_csv(level_name, sep=",", header=None)
    return df


# ---------------- initiat session states ----------------

if "left_clicked" not in st.session_state:
    st.session_state["left_clicked"] = False

if "right_clicked" not in st.session_state:
    st.session_state["right_clicked"] = False

if "up_clicked" not in st.session_state:
    st.session_state["up_clicked"] = False

if "down_clicked" not in st.session_state:
    st.session_state["down_clicked"] = False

if "steps" not in st.session_state:
    st.session_state["steps"] = 0

# ---------------- links ----------------

cat = "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/other/cat.gif"
player = "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/other/player.gif"
chort = "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/other/monster.gif"

# ---------------- callbacks ----------------


def player_can_move(logic_layer, x, y):
    if tileset_movable[logic_layer[x - 1, y - 1]] == True:
        return True
    else:
        pass


def left_callback():

    if player_can_move(
        st.session_state[
            "level"
        ],  # note the different order of x and y. Done to confuse myself in the future.
        # good luck future me
        st.session_state["player_y"],
        st.session_state["player_x"] - 1,
    ):
        st.session_state["player_x"] -= 1
        st.session_state.left_clicked = True
        st.session_state["steps"] += 1


def right_callback():
    if player_can_move(
        st.session_state["level"],
        st.session_state["player_y"],
        st.session_state["player_x"] + 1,
    ):
        st.session_state["player_x"] += 1
        st.session_state.right_clicked = True
        st.session_state["steps"] += 1


def up_callback():
    if player_can_move(
        st.session_state["level"],
        st.session_state["player_y"] - 1,
        st.session_state["player_x"],
    ):
        st.session_state["player_y"] -= 1
        st.session_state.up_clicked = True
        st.session_state["steps"] += 1


def down_callback():
    if player_can_move(
        st.session_state["level"],
        st.session_state["player_y"] + 1,
        st.session_state["player_x"],
    ):
        st.session_state["player_y"] += 1
        st.session_state.down_clicked = True
        st.session_state["steps"] += 1


# ---------------- CSS ----------------

local_css("style.css")

if "player_x" not in st.session_state:
    st.session_state["player_x"] = 4

if "player_y" not in st.session_state:
    st.session_state["player_y"] = 5

# ---------------- tilset dictionary ----------------

tileset = {
    "@": "https://oshi.at/ZMUu/avRY.gif",
    "W": "https://thumbs2.imgbox.com/10/db/7zaxbIP8_t.png",  # wall
    "FP": "https://thumbs2.imgbox.com/29/22/5rTLr6WH_t.png",  # floor_plain
    # "FP": "https://oshi.at/PQkn/ExtR.png",  # floor 1 tilset 2
    "CAT": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/other/cat.gif",  # cat
    "M": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/other/monster.gif",  # monster, skeleton
    "FS": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/floor_stain_1.png",
    "E": "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==",
    "FE3": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/floor_edge_3.png",  # floor_edge_3
    "WON": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/Wall_outer_n.png",  # Wall_outer_n
    "WOE": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/Wall_outer_e.png",  # Wall_outer_e
    "WONE": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/Wall_outer_ne.png",  # Wall_outer_ne
    "WOW": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/Wall_outer_w.png",  # Wall_outer_w
    "WONW": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/Wall_outer_nw.png",  # wall_outer_nw
    "WFR": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/Wall_front_right.png",  # wall front right
    "WTR": "https://oshi.at/QpWg/Mfxv.png",  # wall top right
    # "DK": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/wall_missing_brick_2.png",  # darkness
    "WMB": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/wall_missing_brick_2.png",  # wall missing brick 1
    "BOX": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/box.png",  # box
    "DR": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/darkness_right.png",  # darkenss right
    "DB": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/darkness_bottom.png",  # darkness bottom
    "T": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/torch_1.png",  # torch
    "FMN1": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/floor_mud_n_1.png",  # floor_mud_n_1
    "FMN2": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/floor_mud_n_2.png",  # floor_mud_n_2
    "FMNE": "https://raw.githubusercontent.com/TomJohnH/streamlit-rogue/main/graphics/tileset/floor_mud_ne.png",  # floor_mud_ne
}

tileset_movable = {
    "@": True,
    "W": False,
    "FP": True,  # floor_plain
    # "FP": "https://oshi.at/PQkn/ExtR.png",  # floor 1 tilset 2
    "CAT": True,
    "M": True,  # monster, skeleton
    "FS": True,
    "E": False,
    "FE3": False,  # floor_edge_3
    "WON": False,  # wall outer n
    "WOE": False,  # wall outer e
    "WONE": False,  # wall outer ne
    "WOW": False,  # wall outer w
    "WONW": False,  # wall_outer_nw
    "WFR": False,  # wall front right
    "WTR": False,  # wall top right
    "DK": False,  # darkness
    "WMB": False,  # wall missing brick
    "BOX": False,  # box
    "DR": False,  # darkenss right
    "DB": False,  # darkness bottom
    "T": False,  # torch
    "FMN1": True,  # floor mud n1
    "FMN2": True,
    "FMNE": True,  # floor mud ne
}


def level_renderer(df, game_objects):
    i = 0
    j = 0
    level_html = '<div class="container"><div class="gamegrid">'
    for x in df:  # array from data frame: df.values
        # st.write(x)
        j = 0
        for y in x:

            # if y == "FP" and random.uniform(0, 1) > 0.7:
            #     tilset_tile = tileset["DK"]
            # else:
            #     tilset_tile = tileset[y]

            level_html = (
                level_html
                + '<img src="'
                + tileset[y]  # tilset_tile
                + '" style="grid-column-start: '
                + str(j + 1)
                + "; grid-row-start: "
                + str(i + 1)
                + ';">'
            )
            j = j + 1
        i = i + 1
    level_html = level_html + game_objects + "</div></div>"
    return level_html


# fetch level with certain number
df = fetch_data("test.csv")
if "level" not in st.session_state:  # or st.session_state["level_change"]:
    st.session_state["level"] = df.values


# this is very subotimal change to classes

player = f"""
<img src="{player}" id="player" class="player" style="grid-column-start: {st.session_state["player_x"]}; grid-row-start: {st.session_state["player_y"]};">"""

game_objects = f"""
<img src="{chort}" style="grid-column-start: 42; grid-row-start: 30;">
<img src="{chort}" style="grid-column-start: 20; grid-row-start: 22;">
<img src="{cat}" style="grid-column-start: 33; grid-row-start: 3;">"""

boxes = f"""
<img src="{tileset["BOX"]}" style="grid-column-start: 4; grid-row-start: 17;">
<img src="{tileset["BOX"]}" style="grid-column-start: 6; grid-row-start: 3;">
<img src="{tileset["BOX"]}" style="grid-column-start: 37; grid-row-start: 29;">
"""

voids = f"""
<img src="{tileset["DR"]}" style="grid-column-start: 47; grid-row-start: 13; grid-column-end:49">

"""
torches = f"""
<img src="{tileset["T"]}" style="grid-column-start: 21; grid-row-start: 5">
<img src="{tileset["T"]}" style="grid-column-start: 19; grid-row-start: 25">
<img src="{tileset["T"]}" style="grid-column-start: 22; grid-row-start: 25">
<img src="{tileset["T"]}" style="grid-column-start: 46; grid-row-start: 30">
<img src="{tileset["T"]}" style="grid-column-start: 33; grid-row-start: 13">
"""

html = level_renderer(
    st.session_state["level"], player + game_objects + boxes + voids + torches
)
display_html = st.empty()
display_html = st.markdown(html, unsafe_allow_html=True)

st.button("L", on_click=left_callback)
st.button("R", on_click=right_callback)
st.button("U", on_click=up_callback)
st.button("D", on_click=down_callback)

# st.markdown(
#     '<div class="console-container">Hp: 20/20<br> Exp: 0/30<br> Gold: 0 </div>',
#     unsafe_allow_html=True,
# )


# ------------ sidebar for backup input ---------------------------

with st.sidebar:
    st.write("Use keyboard arrows or buttons below")
    st.markdown("<br>", unsafe_allow_html=True)
    left_col, middle_col, right_col = st.columns([1, 1, 1])
    with middle_col:
        st.button("&nbsp;UP&nbsp;", on_click=up_callback, key="UP")
    st.markdown("<br>", unsafe_allow_html=True)

    left_col, middle_col, right_col = st.columns([1, 1, 1])
    with left_col:
        st.button("LEFT", on_click=left_callback, key="LEFT")

    with right_col:
        st.button("RIGHT", on_click=right_callback, key="RIGHT")
    st.markdown("<br>", unsafe_allow_html=True)
    left_col, middle_col, right_col = st.columns([1, 1, 1])
    with middle_col:
        st.button("DOWN", on_click=down_callback, key="DOWN")


# ------------ Console div  ---------------------------

st.markdown(
    f"""
    <div class="bpad" id="bpad">HP: 20/20<div>Exp: 0/30</div><div>Steps: {st.session_state["steps"]}</div></div>""",
    unsafe_allow_html=True,
)

# ------------ JS for catching input ---------------------------

#

components.html(
    """
<script>
const doc = window.parent.document;
buttons = Array.from(doc.querySelectorAll('button[kind=secondary]'));
const left_button = buttons.find(el => el.innerText === 'LEFT');
const right_button = buttons.find(el => el.innerText === 'RIGHT');
const up_button = buttons.find(el => el.innerText === String.fromCharCode(160)+'UP'+String.fromCharCode(160));
const down_button = buttons.find(el => el.innerText === 'DOWN');

const left_button2 = buttons.find(el => el.innerText === 'L');
const right_button2 = buttons.find(el => el.innerText === 'R');
const up_button2 = buttons.find(el => el.innerText === 'U');
const down_button2 = buttons.find(el => el.innerText === 'D');

Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'L').classList.add('bbutton-left');
Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'R').classList.add('bbutton-right');
Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'U').classList.add('bbutton-up');
Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'D').classList.add('bbutton-down');


doc.addEventListener('keydown', function(e) {
switch (e.keyCode) {
    case 37: // (37 = left arrow)
        left_button.click();
        window.parent.document.getElementById('player').scrollIntoView();
        break;
    case 39: // (39 = right arrow)
        right_button.click();
        window.parent.document.getElementById('player').scrollIntoView(); 
        break;
    case 38: // (39 = right arrow)
        up_button.click();
        window.parent.document.getElementById('player').scrollIntoView();
        break;
    case 40: // (39 = right arrow)
        down_button.click();
        window.parent.document.getElementById('player').scrollIntoView();   
        break;
}
});



left_button.addEventListener("click",function() {
  window.parent.document.getElementById('player').scrollIntoView();
  console.log("left")
});

right_button.addEventListener("click",function() {
  window.parent.document.getElementById('player').scrollIntoView();
  console.log("right")
});

left_button2.addEventListener("click",function() {
  window.parent.document.getElementById('player').scrollIntoView();
  console.log("left")
});

right_button2.addEventListener("click",function() {
  window.parent.document.getElementById('player').scrollIntoView();
  console.log("right")
});

up_button.addEventListener("click",function() {
  window.parent.document.getElementById('player').scrollIntoView();
  console.log("up")
});

down_button.addEventListener("click",function() {
  window.parent.document.getElementById('player').scrollIntoView();
  console.log("down")
});

up_button2.addEventListener("click",function() {
  window.parent.document.getElementById('player').scrollIntoView();
  console.log("up")
});

down_button2.addEventListener("click",function() {
  window.parent.document.getElementById('player').scrollIntoView();
  console.log("down")
});





</script>
""",
    height=0,
    width=0,
)
