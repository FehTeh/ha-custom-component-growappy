"""API for GROWAPPY."""
import aiohttp
import logging

from .student import Student
from .token import Token
from .metric import Metric
from .consts import (
    API_LOGIN_URL,
    API_LOGIN_REFRESH_URL,
    API_LIST_STUDENTS_URL,
    API_DIARY_URL)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

class GROWAPPY:
    """Interfaces for https://api.growappy.com"""

    def __init__(self, websession):
        self.websession = websession
        self.json = None

    async def login(self, username, password) -> Token:
        """Issue LOGIN request."""
        try:
            _LOGGER.debug("Logging in...")
            async with self.websession.post(
                API_LOGIN_URL,
                headers = { "Content-Type": "application/json" },
                json={"username":username,"password":password}
            ) as res:
                if res.status == 200 and res.content_type == "application/json":
                    json = await res.json()
                    _LOGGER.debug("Done logging in.")
                    return Token(json)
                raise Exception("Could not retrieve token for user, login failed")
        except aiohttp.ClientError as err:
            _LOGGER.error(err)

    async def refreshToken(self, refresh_token) -> Token:
        """Issue REFRESH TOKEN request."""
        try:
            _LOGGER.debug("Refreshing token...")
            async with self.websession.post(
                API_LOGIN_REFRESH_URL,
                headers = { "Content-Type": "application/json" },
                json={"refresh":refresh_token}
            ) as res:
                if res.status == 200 and res.content_type == "application/json":
                    json = await res.json()
                    _LOGGER.debug("Done refreshing token.")
                    return Token(json)
                raise Exception("Could not retrieve token for user, refresh failed")
        except aiohttp.ClientError as err:
            _LOGGER.error(err)

    async def getStudents(self, access_token) -> list[Student]:
        """Issue STUDENTS requests."""
        try:
            _LOGGER.debug("Getting list of active students...")
            async with self.websession.get(
                API_LIST_STUDENTS_URL, 
                headers = { 
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}" }
            ) as res:
                if res.status == 200 and res.content_type == "application/json":
                    json = await res.json()
                    _LOGGER.debug("Done getting list of active students.")
                    return [ Student(student) for student in json['results'] ]
                raise Exception("Could not retrieve students list from API")
        except aiohttp.ClientError as err:
            _LOGGER.error(err)

    async def getDiary(self, access_token, studentId, startDate, endDate) -> list[Metric]:
        """Issue DIARY request."""
        try:
            _LOGGER.debug("Getting diary for student {}...".format(studentId))
            async with self.websession.get(
                API_DIARY_URL.format(startDate, endDate, studentId), 
                headers = { 
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}" }
            ) as res:
                if res.status == 200 and res.content_type == "application/json":
                    json = await res.json()
                    _LOGGER.debug("Done getting diary for student {}.".format(studentId))
                    return [ Metric(metric) for metric in json['results'] ]
                raise Exception("Could not retrieve diary for student {} from API".format(studentId))
        except aiohttp.ClientError as err:
            _LOGGER.error(err)