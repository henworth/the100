import aiohttp
import asyncio
import urllib

title = 'the100'
__version__ = '0.1.0'

BASE_URL = 'https://www.the100.io'


class The100(object):

    def __init__(self, api_key, base_url=None, loop=None):
        """Base class for the100

        Args:
            api_key (str):
                the100.io API key
            base_url (str) [optional]:
                the100.io base URL
            loop [optional]:
                AsyncIO event loop, if not passed one will be created
        """
        headers = {
            'Authorization': f"Bearer {api_key}",
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        self.base_url = base_url if base_url else BASE_URL
        self._loop = asyncio.get_event_loop() if loop is None else loop
        self._session = aiohttp.ClientSession(loop=self._loop, headers=headers)

    async def close(self):
        await self._session.close()

    async def _request(self, req_type, url, params=None, data=None):
        """Make an async HTTP request and attempt to return json (dict)"""
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        try:
            async with self._session.request(req_type, encoded_url, params=params, json=data) as r:
                json_res = await r.json()
        except aiohttp.ClientResponseError:
            raise The100Exception("Could not connect to the100.io")
        return json_res

    async def _get_request(self, url, params=None):
        """Make an async GET request and attempt to return json (dict)"""
        return await self._request('GET', url, params=params)

    async def _put_request(self, url, data=None):
        """Make an async PUT request and attempt to return json (dict)"""
        return await self._request('PUT', url, data=data)

    async def _post_request(self, url, data=None):
        """Make an async POST request and attempt to return json (dict)"""
        return await self._request('POST', url, data=data)

    async def _patch_request(self, url, data=None):
        """Make an async PATCH request and attempt to return json (dict)"""
        return await self._request('PATCH', url, data=data)

    async def _delete_request(self, url, data=None):
        """Make an async DELETE request and attempt to return json (dict)"""
        return await self._request('DELETE', url, data=data)

    async def get_games(self):
        """Retrieves all `games` and their associated `game_activities`

        Returns:
            json (dict)
        """
        return await self._get_request(f'{self.base_url}/api/v2/games')

    async def get_game(self, game_id):
        """Retrieves a `game` and its associated `game_activities`

        Returns:
            json (dict)
        """
        games = await self.get_games()
        for game in games:
            if game['id'] == game_id:
                return game
        return None

    async def get_game_by_name(self, game_name):
        """Retrieves a `game` and its associated `game_activities`

        Returns:
            json (dict)
        """
        games = await self.get_games()
        for game in games:
            if game['name'] == game_name:
                return game
        return None

    async def get_gaming_session(self, game_session_id):
        """Return a gaming session by specified id

        Args:
            game_session_id (int): The game session id

        Returns:
            json (dict)
        """
        return await self._get_request(f'{self.base_url}/api/v2/gaming_sessions/{game_session_id}')

    async def create_gaming_session(self, game_session_details):
        """Create gaming session by specified id

        Requires a whitelisted authentication token.

        Args:
            game_session_details (dict): The game session details

                {
                    "game_id": 13,
                    "platform": "xbox-one",
                    "description": "Testing things",
                    "activity": "Raid - Leviathan",
                    "start_time": "2019-06-09T21:00:00.000-07:00",
                    "group_name": "Alpha Company 760",
                    "make_auto_public": False,
                    "beginners_welcome": False,
                    "sherpa_requested": False,
                    "headset_required": True,
                    "party_size": 1,
                    "public_visible": True,
                    "group_visible": True,
                    "friends_visible": True,
                    "private_visible": False
                }

        Returns:
            json (dict)
        """
        return await self._post_request(
            f'{self.base_url}/api/v2/gaming_sessions', data=game_session_details)

    async def edit_gaming_session(self, game_session_id, game_session_details):
        """Edit game session by specified id

        Requires a whitelisted authentication token.

        Args:
            game_session_id (int):       The game session id
            game_session_details (dict): The game session details to modify

        Returns:
            json (dict)
        """
        return await self._patch_request(
            f'{self.base_url}/api/v2/gaming_sessions/{game_session_id}', data=game_session_details)

    async def delete_gaming_session(self, game_session_id):
        """Delete game session by specified id

        Requires a whitelisted authentication token.

        Args:
            game_session_id (int): The game session id

        Returns:
            json (dict)
        """
        return await self._delete_request(f'{self.base_url}/api/v2/gaming_sessions/{game_session_id}')

    async def get_gaming_sessions(self):
        """Return all gaming sessions

        Returns:
            json (dict)
        """
        return await self._get_request(f'{self.base_url}/api/v2/gaming_sessions')

    async def get_group(self, group_id):
        """Return group by specified id

        Args:
            group_id (int): The group id

        Returns:
            json (dict)
        """
        return await self._get_request(f'{self.base_url}/api/v2/groups/{group_id}')

    async def get_group_gaming_sessions(self, group_id):
        """Return group by specified id

        Args:
            group_id (int): The group id

        Returns:
            json (dict)
        """
        return await self._get_request(f'{self.base_url}/api/v2/groups/{group_id}/gaming_sessions')

    async def get_group_users(self, group_id, page=None):
        """Return group members by specified group id

        Args:
            group_id (int): The group id

        Returns:
            json (dict)
        """
        params = {'page': page}
        return await self._get_request(f'{self.base_url}/api/v2/groups/{group_id}/users', params=params)

    async def get_group_statuses(self, group_id):
        """Return group member statuses by specified group id

        Args:
            group_id (int): The group id

        Returns:
            json (dict)
        """
        return await self._get_request(f'{self.base_url}/api/v2/groups/{group_id}/statuses')

    async def get_user(self, user_id):
        """Return user by specified id

        Args:
            user_id (int): The user id

        Returns:
            json (dict)
        """
        return await self._get_request(f'{self.base_url}/api/v2/users/{user_id}')

    async def create_gaming_session_discord(self, game_session_details):
        """Create gaming session on behalf of a discord user

        Requires a whitelisted authentication token.

        Args:
            game_session_details (dict): The game session details

                {
                   "guild_id": (int) <discord guild id>,
                   "username": (str) <discord username>,
                   "discriminator": (int) <discord user discriminator>,
                   "message": (str) <game session create message>
                }
            
            Note: Message must follow this syntax, per https://www.the100.io/discord-bot-for-destiny-2
                `!create group platform activity date & time "description"`

        Returns:
            json (dict)
        """
        return await self._post_request(
            f'{self.base_url}/api/v2/discordbots/create_gaming_session',
            data=game_session_details
        )


class The100Exception(Exception):
    pass
