from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

import pandas as pd
from twitchAPI.twitch import Twitch
import asyncio


class TwitchConnection(ExperimentalBaseConnection[Twitch]):
    """Basic st.experimental_connection implementation for the Twitch.tv API"""

    def _connect(self, **kwargs) -> Twitch:
        if 'secret' in kwargs:
            secret = kwargs.pop('secret')
        else:
            secret = self._secrets['secret']
        
        if 'client_id' in kwargs:
            client_id = kwargs.pop('client_id')
        else:
            client_id = self._secrets['client_id']

        async def init_twitch(client_id, secret):
            return await Twitch(client_id, secret)
        
        return asyncio.run(init_twitch(client_id, secret))
    
    def connection(self) -> Twitch:
        return self._instance


    def get_token(self) -> str:
        conn = self.connection()
        token = conn.get_app_token()
        return token 


    def get_top_games(self, num_games: int = 100, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        """Queries the current top games (or categories) with regards to number of viewers"""

        async def _get_top_games(num_games: int = 100, **kwargs):
            conn = self.connection()
            top_games_gen = conn.get_top_games(first=num_games)
            top_games = [game.to_dict() async for game in top_games_gen]
            return pd.DataFrame(top_games)
        
        @cache_data(ttl=ttl, show_spinner="Running `conn.get_top_games(...)`.")
        def run_get_games_func(num_games: int = 100, **kwargs):
            top_games_df = asyncio.run(_get_top_games(num_games, **kwargs))
            return top_games_df

        return run_get_games_func(num_games, **kwargs)

    def get_streams_by_game(self, game_id: str, type: str = "live", language: str = "en", num_channels: int = 100, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        """Queries streams streaming a certain game (given by game_id). Optionally, offline streams are returned as well and the language can be specified"""

        async def _get_streams_by_game(game_id: str, type: str, language: str, num_channels: int, **kwargs):
            conn = self.connection()
            top_streams_gen = conn.get_streams(game_id=game_id, stream_type=type, language=language, first=num_channels)
            top_streams = [stream.to_dict() async for stream in top_streams_gen]
            return pd.DataFrame(top_streams)
        
        @cache_data(ttl=ttl, show_spinner="Running `conn.get_streams_by_game(...)`.")
        def run_get_streams_func(game_id: str, type: str, language: str, num_channels: int, **kwargs):
            top_streams_df = asyncio.run(_get_streams_by_game(game_id, type, language, num_channels, **kwargs))
            return top_streams_df

        return run_get_streams_func(game_id, type, language, num_channels, **kwargs)

    def search_streams_by_name(self, query: str, live_only: bool = False, num_channels: int = 100, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        """Queries streams for a specified searach query. Optionally only live streams can be queried."""

        async def _search_streams_by_name(query: str, live_only: bool, num_channels: int, **kwargs):
            conn = self.connection()
            results_gen = conn.search_channels(query=query, live_only=live_only, first=num_channels)
            results = [stream.to_dict() async for stream in results_gen]
            return pd.DataFrame(results)
        
        @cache_data(ttl=ttl, show_spinner="Running `conn.search_streams_by_name(...)`.")
        def run_search_streams_func(query: str, live_only: bool, num_channels: int, **kwargs):
            results_df = asyncio.run(_search_streams_by_name(query, live_only, num_channels, **kwargs))
            return results_df

        return run_search_streams_func(query, live_only, num_channels, **kwargs)

