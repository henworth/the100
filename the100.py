import aiohttp
import asyncio
import urllib

title = 'the100'
__version__ = '0.0.1'

BASE_URL = 'https://www.the100.io'


class The100(object):

    def __init__(self, api_key, loop=None):
        """Base class for the100

        Args:
            api_key (str):
                the100.io API key
            loop [optional]:
                AsyncIO event loop, if not passed one will be created
        """
        headers = {
            'Authorization': f"Bearer {api_key}",
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        self._loop = asyncio.get_event_loop() if loop is None else loop
        self._session = aiohttp.ClientSession(loop=self._loop, headers=headers)

    def close(self):
        asyncio.ensure_future(self._session.close())

    async def _request(self, req_type, url, params=None, data=None):
        """Make an async HTTP request and attempt to return json (dict)"""
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        try:
            async with self._session.request(req_type, encoded_url, params=params) as r:
                json_res = await r.json()
        except aiohttp.ClientResponseError:
            raise The100Exception("Could not connect to the100.io")
        return json_res

    async def _get_request(self, url, params=None):
        """Make an async GET request and attempt to return json (dict)"""
        return await self._request('GET', url, params=params)

    async def _post_request(self, url, data=None):
        """Make an async POST request and attempt to return json (dict)"""
        return await self._request('POST', url, data=data)

    async def get_games(self):
        """Retrieves all `games` and their associated `game_activities`

        Returns:
            json (dict)
        """
        return await self._get_request(f'{BASE_URL}/api/v2/games')

    async def get_gaming_session(self, game_session_id):
        """Return a gaming session by specified id

        Args:
            game_session_id (str): The game session id

        Returns:
            json (dict)
        """
        return await self._get_request(f'{BASE_URL}/api/v2/game_sessions/{game_session_id}')

    async def get_gaming_sessions(self):
        """Return all gaming sessions

        Returns:
            json (dict)
        """
        return await self._get_request(f'{BASE_URL}/api/v2/gaming_sessions')

    async def get_group(self, group_id):
        """Return group by specified id

        Args:
            group_id (int): The group id

        Returns:
            json (dict)
        """
        return await self._get_request(f'{BASE_URL}/api/v2/groups/{group_id}')

    async def get_group_gaming_sessions(self, group_id):
        """Return group by specified id

        Args:
            group_id (int): The group id

        Returns:
            json (dict)
        """
        return await self._get_request(f'{BASE_URL}/api/v2/groups/{group_id}/gaming_sessions')

    async def get_group_users(self, group_id):
        """Return group members by specified group id

        Args:
            group_id (int): The group id

        Returns:
            json (dict)
        """
        return await self._get_request(f'{BASE_URL}/api/v2/groups/{group_id}/users')

    async def get_group_statuses(self, group_id):
        """Return group member statuses by specified group id

        Args:
            group_id (int): The group id

        Returns:
            json (dict)
        """
        return await self._get_request(f'{BASE_URL}/api/v2/groups/{group_id}/statuses')

    async def get_user(self, user_id):
        """Return user by specified id

        Args:
            user_id (int): The user id

        Returns:
            json (dict)
        """
        return await self._get_request(f'{BASE_URL}/api/v2/users/{user_id}')


class The100Exception(Exception):
    pass
