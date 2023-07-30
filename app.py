import streamlit as st
import streamlit.components.v1 as components
from twitch_connection.connection import TwitchConnection

st.set_page_config(
    page_title='Streamlit connections - Twitch API',
    page_icon='🔌',
   #  layout="wide"
)
#twitch_logo.png
conn = st.experimental_connection('twitch_api', type=TwitchConnection)

st.title("🔌 Streamlit connections hackathon ")
st.header("Twitch.tv API connection demo app")
st.write("This is the demo app showcasing the Twitch API implemented as a streamlit connection. [Twitch.tv](https://twitch.tv) \
        is a popular live streaming website and provides an API to let developers build creative integrations for the broader \
        Twitch community. We'll be using a python implementation of the API [pyTwitchAPI](https://github.com/Teekeks/pyTwitchAPI).")
st.write("The Twitch API knows 2 different authentications. App and User Authentication. Which one you need (or if one at all) \
            depends on what calls you want to use. For this demo we'll only use the app authentication as it does not require you to \
            have a twitch account.")


st.subheader("Choose a Twitch.tv channel to watch")

tab1, tab2= st.tabs(["By Game", "By Streamer"])

with tab1:
   st.write("To choose a twitch.tv channel to watch, we can query the top games currently watched and then choose a popular channel. \
      Some information about the chosen stream is displayed and the stream is embedded as an iframe.")
   top_games_data = conn.get_top_games(50)

   game_option = st.selectbox(
    'Choose one of the top games',
    top_games_data["name"].to_list())


   selected_game_id = top_games_data[top_games_data["name"] == game_option]["id"].iloc[0]
   top_streams_data = conn.get_streams_by_game(selected_game_id)
   stream_option = st.selectbox(
    'Choose one of the top streams',
    top_streams_data["user_name"].to_list())

   streamer_data = top_streams_data[top_streams_data["user_name"] == stream_option].iloc[0]
   streamer_info_cols = ["user_name", "game_name", "title", "viewer_count", "started_at", "language" ]
   st.dataframe(streamer_data[streamer_info_cols], use_container_width=True)

   if stream_option:
      components.iframe(f"https://player.twitch.tv/?channel={stream_option}&parent=twitch-tv-api-connection.streamlit.app", width=800, height=600, scrolling=False)

with tab2:
   st.write("As a second option, we can directly search for a stream.")

   text_search = st.text_input("Search for a stream to watch", value="")

   if st.button('Search') and text_search != "":
      st.session_state["search_results"] = conn.search_streams_by_name(text_search, live_only=True)

   if "search_results" in st.session_state:
      search_results = st.session_state["search_results"]
      stream_select = st.selectbox(
         'Choose one of the streams',
         search_results["broadcaster_login"].to_list())

      streamer_info_cols = ["broadcaster_login", "game_name", "title", "started_at", "broadcaster_language" ]
      st.dataframe(search_results[search_results["broadcaster_login"] == stream_select][streamer_info_cols].T, use_container_width=True)

      if stream_select:
         components.iframe(f"https://player.twitch.tv/?channel={stream_select}&parent=twitch-tv-api-connection.streamlit.app", width=800, height=600, scrolling=False)


