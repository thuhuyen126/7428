import streamlit as st
import random, os

st.set_page_config(page_title="Pikachu Nối Thú", layout="wide")
st.title("🎮 Pikachu Nối Thú – Streamlit")

ROWS, COLS = 4, 6
IMAGES = ["cat.png","dog.png","rabbit.png","pig.png","lion.png","panda.png"]

def init_board():
    total = ROWS*COLS//2
    imgs = (IMAGES * ((total//len(IMAGES))+1))[:total] * 2
    random.shuffle(imgs)
    return [imgs[i*COLS:(i+1)*COLS] for i in range(ROWS)]

if "board" not in st.session_state:
    st.session_state.board = init_board()
    st.session_state.visible = [[True]*COLS for _ in range(ROWS)]
    st.session_state.first = None

def reset():
    st.session_state.board = init_board()
    st.session_state.visible = [[True]*COLS for _ in range(ROWS)]
    st.session_state.first = None

st.button("🔁 Chơi lại", on_click=reset)

for i in range(ROWS):
    cols = st.columns(COLS)
    for j in range(COLS):
        if not st.session_state.visible[i][j]:
            cols[j].empty()
            continue
        img = st.session_state.board[i][j]
        path = os.path.join("images", img)
        if not os.path.exists(path):
            cols[j].write("❌ ảnh mất!")
            continue

        if cols[j].button("", key=f"{i}-{j}"):
            if st.session_state.first is None:
                st.session_state.first = (i,j)
            else:
                i1,j1 = st.session_state.first
                if (i1,j1)!=(i,j) and st.session_state.board[i1][j1]==img:
                    st.session_state.visible[i1][j1] = False
                    st.session_state.visible[i][j] = False
                st.session_state.first = None
        cols[j].image(path, use_container_width=True)
