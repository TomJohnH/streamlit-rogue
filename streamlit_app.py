import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import time
import pandas as pd
from random import randrange

st.set_page_config(page_title="The Shadows’s Den", page_icon="🗡️")

# ---------------- callbacks ----------------


def left_callback():
    st.session_state.left_clicked = True


def right_callback():
    st.session_state.right_clicked = True


def up_callback():
    st.session_state.up_clicked = True


def down_callback():
    st.session_state.down_clicked = True


# ---------------- function - load data with level ----------------

# level is an array - please check level renderer for more details


@st.cache_data
def fetch_data(level_name):
    df = pd.read_csv(level_name, sep=",", header=None)
    return df


# ---------------- function - external css definition ----------------


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------------- function & data definition - level renderer ----------------

# level is an array with values specified below
# each value of matrix is rendered into html value

tileset = {
    "E": "&#xB7;",  # "&#xA0;",
    "W": '<span style="color:White">&#x2593;</span>',
    "C": "&#x2591;",
    "D": '<span style="color:Grey">D</span>',
    "@": '<span style="color:GreenYellow">@</span>',
    "G": '<span style="color:gold">G</span>',
    "M": '<span style="color:white">M</span>',
    "B": '<span style="color:red">B</span>',
    "N": "&#xA0;",
    "X": '<span style="color:violet">X</span>',
}


def level_renderer(df):
    l1 = '<span style="color:Grey">'
    for x in df:  # array from data frame: df.values
        for y in x:
            l1 = l1 + tileset[y]
        l1 = l1 + "<br>"
        # print("this is value", tileset[y], " yes |")
    l1 = l1 + "</span>"
    return l1


# ---------------- function & data - character mover ----------------

# tileset_movable - dictionary of bools for collision detection
# inital_level - state of inital level array
# level_temp - state of output level array

tileset_movable = {
    "E": True,
    "W": False,
    "C": True,
    "D": True,
    "@": False,
    "G": True,
    "M": True,
    "B": True,
    "N": False,
    "X": True,
}

move_directions = ["l", "r", "u", "d"]


def move(inital_level, direction, who, i):

    # where is the player?
    k = np.where(inital_level == who)

    # check if we have anything to return (important for non-player)
    # added k[0] lenght checking to take into account that monsters can attack each other
    if any(k[0]) and i < len(k[0]):
        from_top = k[0][i]
        from_left = k[1][i]
        # st.write(k)

        # let's copy input array and remove player
        level_temp = inital_level.copy()
        level_temp[from_top, from_left] = "E"

        # let's check where player can move
        movement = {}
        movement["lt"] = inital_level[from_top, from_left - 1]  # left
        movement["rt"] = inital_level[from_top, from_left + 1]  # right
        movement["ut"] = inital_level[from_top - 1, from_left]  # up
        movement["dt"] = inital_level[from_top + 1, from_left]  # down
        # st.session_state["previous_movement_state"] = movement

        # st.write(movement)

        if direction == "l":
            if from_left > 0:
                if tileset_movable[movement["lt"]] == True:
                    level_temp[from_top, from_left - 1] = who
                    # st.session_state["previous_move"] = "l"
                    return level_temp
                else:
                    return inital_level
            else:
                return inital_level

        if direction == "r":
            if from_left < 48:
                # st.write(from_left)
                if tileset_movable[movement["rt"]] == True:
                    level_temp[from_top, from_left + 1] = who
                    # st.session_state["previous_move"] = "r"
                    return level_temp
                else:
                    return inital_level
            else:
                return inital_level
        if direction == "u":
            if from_top > 0:
                if tileset_movable[movement["ut"]] == True:
                    level_temp[from_top - 1, from_left] = who
                    # st.session_state["previous_move"] = "u"
                    return level_temp
                else:
                    return inital_level
            else:
                return inital_level

        if direction == "d":
            if from_top < 48:
                if tileset_movable[movement["dt"]] == True:
                    level_temp[from_top + 1, from_left] = who
                    # st.session_state["previous_move"] = "d"
                    return level_temp
                else:
                    return inital_level
            else:
                return inital_level
    else:
        return inital_level


# ---------------- initiat session states ----------------

if "left_clicked" not in st.session_state:
    st.session_state["left_clicked"] = False

if "right_clicked" not in st.session_state:
    st.session_state["right_clicked"] = False

if "up_clicked" not in st.session_state:
    st.session_state["up_clicked"] = False

if "down_clicked" not in st.session_state:
    st.session_state["down_clicked"] = False

if "backpack" not in st.session_state:
    st.session_state["backpack"] = {"gold": 0}

if "hero_stats" not in st.session_state:
    st.session_state["hero_stats"] = {
        "hp": 20,
        "max_hp": [20, 30, 50, 100],
        "exp": 0,
        "lvl_exp": [15, 30, 50, 80],
        "kills": 0,
        "player_level": 0,
    }

if "ending_condition" not in st.session_state:
    st.session_state["ending_condition"] = False

if "level_no" not in st.session_state:
    st.session_state["level_no"] = 1

if "level_change" not in st.session_state:
    st.session_state["level_change"] = False

#######################################################
#
#                   MAIN GAME CODE
#
#######################################################

# ---------------- CSS ----------------

local_css("style.css")

# ---------------- data ----------------

# fetch level with certain number
df = fetch_data("level" + str(st.session_state["level_no"]) + ".csv")

if ("level" not in st.session_state) or st.session_state["level_change"]:
    st.session_state["level"] = df.values
    st.session_state["level_change"] = False

if ("level_before_move" not in st.session_state) or st.session_state["level_change"]:
    st.session_state["level_before_move"] = df.values
    st.session_state["level_change"] = False

# ---------------- graphic engine pt 1 :-) ----------------

display_html = st.empty()
html = level_renderer(st.session_state["level"])  # chamber_renderer(size)

if not st.session_state["ending_condition"] and not (
    st.session_state.left_clicked
    or st.session_state.right_clicked
    or st.session_state.up_clicked
    or st.session_state.down_clicked
):
    display_html.markdown(html, unsafe_allow_html=True)

#######################################################
#
#                   REACTIONS TO BUTTONS
#
#######################################################

# ---------------- function - check if player is interacting with something ----------------


def interaction(game_object):
    # actual position of the player
    k = np.where(st.session_state["level"] == "@")
    # st.write(k)
    from_top = k[0][0]
    from_left = k[1][0]

    # initiate response
    result = False

    # check if actual position of player is equal to position of Door
    for i in range(
        len(np.where(st.session_state["level_before_move"] == game_object)[0])
    ):

        if (
            from_top
            == np.where(st.session_state["level_before_move"] == game_object)[0][i]
            and from_left
            == np.where(st.session_state["level_before_move"] == game_object)[1][i]
        ):
            result = True

    return result


def object_position(game_object, i):
    # actual position of the player
    k = np.where(st.session_state["level"] == game_object)

    if any(k[0]):
        # added k[0] lenght checking to take into account that monsters can attack each other
        if i < len(k[0]):
            postion = [k[0][i], k[1][i]]
            return postion
        else:
            return [0, 0]
    else:
        return [0, 0]


def distance_from_player(a, b):
    distance = (object_position("@", 0)[0] - a) ** 2 + (
        object_position("@", 0)[1] - b
    ) ** 2
    return distance


# ---------------- if button or key pressed move player ----------------

if st.session_state.left_clicked and not st.session_state["ending_condition"]:
    # status = st.write(move(df.values, "left"))  # st.write("left")

    st.session_state["level"] = move(st.session_state["level"], "l", "@", 0).copy()

if st.session_state.right_clicked and not st.session_state["ending_condition"]:
    # status = st.write(move(df.values, "left"))  # st.write("left")

    st.session_state["level"] = move(st.session_state["level"], "r", "@", 0).copy()

if st.session_state.up_clicked and not st.session_state["ending_condition"]:
    # status = st.write(move(df.values, "left"))  # st.write("left")

    st.session_state["level"] = move(st.session_state["level"], "u", "@", 0).copy()

if st.session_state.down_clicked and not st.session_state["ending_condition"]:
    # status = st.write(move(df.values, "left"))  # st.write("left")

    st.session_state["level"] = move(st.session_state["level"], "d", "@", 0).copy()

# ---------------- if button or key pressed interact and render graphics ----------------

if (
    st.session_state.left_clicked
    or st.session_state.right_clicked
    or st.session_state.up_clicked
    or st.session_state.down_clicked
) and not st.session_state["ending_condition"]:

    # ---------------- helper function ----------------
    # refactor later - to proper x and y
    # refactor later - move somewhere else

    # ---------------- move boss ----------------

    calc_dist_aft_move = {
        "l": distance_from_player(
            object_position("B", 0)[0], object_position("B", 0)[1] - 1
        ),
        "r": distance_from_player(
            object_position("B", 0)[0], object_position("B", 0)[1] + 1
        ),
        "u": distance_from_player(
            object_position("B", 0)[0] - 1, object_position("B", 0)[1]
        ),
        "d": distance_from_player(
            object_position("B", 0)[0] + 1, object_position("B", 0)[1]
        ),
    }

    # st.session_state["level"] = move(
    #     st.session_state["level"], move_directions[randrange(4)], "B"
    # ).copy()

    if randrange(10) < 6:
        st.session_state["level"] = move(
            st.session_state["level"],
            min(calc_dist_aft_move, key=calc_dist_aft_move.get),
            "B",
            0,
        ).copy()
    else:
        st.session_state["level"] = move(
            st.session_state["level"], move_directions[randrange(4)], "B", 0
        ).copy()

    # ---------------- move monster ----------------

    # check if any monsters left on the level
    if any(np.where(st.session_state["level"] == "M")[0]):

        # calculate action for each monster
        for i in range(len(np.where(st.session_state["level"] == "M")[0])):

            # calculated distances after move
            # left, right, up, down
            calc_dist_aft_move = {
                "l": distance_from_player(
                    object_position("M", i)[0], object_position("M", i)[1] - 1
                ),
                "r": distance_from_player(
                    object_position("M", i)[0], object_position("M", i)[1] + 1
                ),
                "u": distance_from_player(
                    object_position("M", i)[0] - 1, object_position("M", i)[1]
                ),
                "d": distance_from_player(
                    object_position("M", i)[0] + 1, object_position("M", i)[1]
                ),
            }

            # st.write(calc_dist_aft_move)
            # st.write(min(calc_dist_aft_move, key=calc_dist_aft_move.get))

            if randrange(10) < 6:
                st.session_state["level"] = move(
                    st.session_state["level"],
                    min(calc_dist_aft_move, key=calc_dist_aft_move.get),
                    "M",
                    i,
                ).copy()
            else:
                st.session_state["level"] = move(
                    st.session_state["level"], move_directions[randrange(4)], "M", i
                ).copy()

    # ---------------- graphic engine pt  2:-) ----------------

    html = level_renderer(st.session_state["level"])

    display_html.empty()
    display_html = st.markdown(html, unsafe_allow_html=True)

    if interaction("D") == True:
        # st.write(Door())
        st.write("door opened")

    if interaction("G") == True:
        # st.write(Door())
        st.write("gold acquired")
        st.session_state["backpack"]["gold"] = st.session_state["backpack"]["gold"] + 10

    if interaction("M") == True:
        damage = randrange(
            st.session_state["hero_stats"]["max_hp"][
                st.session_state["hero_stats"]["player_level"]
            ]
        )
        st.write("fight with monster")
        st.session_state["hero_stats"]["hp"] = (
            st.session_state["hero_stats"]["hp"] - damage
        )
        st.write("-" + str(damage) + " hp")
        st.session_state["hero_stats"]["kills"] = (
            st.session_state["hero_stats"]["kills"] + 1
        )
        st.session_state["hero_stats"]["exp"] = (
            st.session_state["hero_stats"]["exp"] + 20
        )

    if interaction("B") == True:
        damage = randrange(
            st.session_state["hero_stats"]["max_hp"][
                st.session_state["hero_stats"]["player_level"]
            ]
        )
        st.write("fight with boss")
        st.session_state["hero_stats"]["hp"] = (
            st.session_state["hero_stats"]["hp"] - damage
        )
        st.write("-" + str(damage) + " hp")
        st.session_state["hero_stats"]["kills"] = (
            st.session_state["hero_stats"]["kills"] + 1
        )

    if st.session_state["hero_stats"]["hp"] <= 0:
        st.session_state["ending_condition"] = True

    if interaction("X") == True:
        if st.session_state["level_no"] == 3:
            st.session_state["ending_condition"] = True
        else:
            st.session_state["level_no"] += 1
            st.session_state["level_change"] = True
            st.experimental_rerun()

    # ---------------- level up ----------------

    if (
        st.session_state["hero_stats"]["exp"] > 20
        and st.session_state["hero_stats"]["player_level"] == 0
    ):
        st.session_state["hero_stats"]["hp"] = min(
            st.session_state["hero_stats"]["hp"] + 10,
            st.session_state["hero_stats"]["hp"],
        )
        st.session_state["hero_stats"]["player_level"] = (
            st.session_state["hero_stats"]["player_level"] + 1
        )

    # ---------------- update new inital state of level ----------------

    st.session_state["level_before_move"] = st.session_state["level"]

    # ---------------- reset buttons state ----------------

    st.session_state.left_clicked = False
    st.session_state.up_clicked = False
    st.session_state.right_clicked = False
    st.session_state.down_clicked = False


if st.session_state["ending_condition"] == True:
    display_html.empty()
    if st.session_state["hero_stats"]["hp"] > 0:
        display_html = st.markdown(
            "You have reached to the end of the dungeon. Thank you for playing The Shadow's Den",
            unsafe_allow_html=True,
        )
    if st.session_state["hero_stats"]["hp"] <= 0:
        display_html = st.markdown(
            "Unfortunately, you died. Please restart the game.", unsafe_allow_html=True
        )

# ---------------- user console :-) ----------------

# if st.session_state["hero_stats"]["kills"] > 0:
kills = "".join("💀" for i in range(st.session_state["hero_stats"]["kills"]))
# else:
#     kills = "0"

st.caption(
    "Gold: "
    + str(st.session_state["backpack"]["gold"])
    + " Hp: "
    + str(st.session_state["hero_stats"]["hp"])
    + "("
    + str(
        st.session_state["hero_stats"]["max_hp"][
            st.session_state["hero_stats"]["player_level"]
        ]
    )
    + ")"
    + " Exp: "
    + str(st.session_state["hero_stats"]["exp"])
    + " Player level: "
    + str(st.session_state["hero_stats"]["player_level"])
    + " Monsters slayed: "
    + kills
)


# https://www.ee.ucl.ac.uk/~mflanaga/java/HTMLandASCIItableC1.html
# https://htmlcolorcodes.com/color-names/

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
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<br> <span style="color:GreenYellow">@</span> - player',
        unsafe_allow_html=True,
    )
    st.markdown('<br> <span style="color:red">B</span> - boss', unsafe_allow_html=True)
    st.markdown(
        '<br> <span style="color:white">M</span> - monster', unsafe_allow_html=True
    )
    st.markdown('<br> <span style="color:gold">G</span> - gold', unsafe_allow_html=True)
    st.markdown(
        '<br> <span style="color:grey">D</span> - door',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<br> <span style="color:violet">X</span> - exit',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(
        "The Shadow's Den v0.2 - inspired by Rogue (also known as Rogue: Exploring the Dungeons of Doom) a dungeon crawling video game by Michael Toy and Glenn Wichman with later contributions by Ken Arnold. Rogue was originally developed around 1980 for Unix-based mainframe systems as a freely distributed executable. It was later included in the official Berkeley Software Distribution 4.2 operating system (4.2BSD)."
    )

    # "C": "&#x2591;",
    # "D": "D",
    # "@": '<span style="color:green">@</span>',
    # "G": '<span style="color:gold">G</span>',
    # "M": "M",
    # "B": '<span style="color:red">B</span>',

    components.html(
        """
<script>
const doc = window.parent.document;
buttons = Array.from(doc.querySelectorAll('button[kind=secondary]'));
const left_button = buttons.find(el => el.innerText === 'LEFT');
const right_button = buttons.find(el => el.innerText === 'RIGHT');
const up_button = buttons.find(el => el.innerText === String.fromCharCode(160)+'UP'+String.fromCharCode(160));
const down_button = buttons.find(el => el.innerText === 'DOWN');
doc.addEventListener('keydown', function(e) {
    switch (e.keyCode) {
        case 37: // (37 = left arrow)
            left_button.click();
            break;
        case 39: // (39 = right arrow)
            right_button.click();
            break;
        case 38: // (39 = right arrow)
            up_button.click();
            break;
        case 40: // (39 = right arrow)
            down_button.click();
            break;
    }
});
</script>
""",
        height=0,
        width=0,
    )

# ------------ footer  ---------------------------

st.markdown(
    f"""
    <div class="coffee" id="coffee">
    <a href="https://www.buymeacoffee.com/tomjohn" style="color: grey; text-decoration:none;">
    <div style="justify-content: center;margin:0px; border:solid 2px;background-color: #0e1117; ;border-radius:10px 10px 0 0; border-color:#21212f; width: fit-content;padding:0.425rem">
    <img src="https://raw.githubusercontent.com/TomJohnH/streamlit-game/main/images/coffe.png" style="max-width:20px;margin-right:10px;">
    Buy me a coffee</a></div></div>""",
    unsafe_allow_html=True,
)

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
