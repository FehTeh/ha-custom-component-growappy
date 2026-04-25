import asyncio
import aiohttp
import sys

from tests import test_config
from unittest.mock import MagicMock

mock_ha = MagicMock()
sys.modules["homeassistant"] = mock_ha
sys.modules["homeassistant.core"] = mock_ha
sys.modules["homeassistant.config_entries"] = mock_ha
sys.modules["homeassistant.helpers"] = mock_ha
sys.modules["homeassistant.helpers.typing"] = mock_ha

from custom_components.growappy.api.growappy import GROWAPPY
from custom_components.growappy.api.token import Token

async def main():
    async with aiohttp.ClientSession() as session:
        api = GROWAPPY(session)

        if (test_config.API_ACCESS_TOKEN and test_config.API_REFRESH_TOKEN):
            print ("Using existing tokens from config...")
            token = Token({
                "access": test_config.API_ACCESS_TOKEN,
                "refresh": test_config.API_REFRESH_TOKEN
            })
        else:
            username = test_config.API_USERNAME
            password = test_config.API_PASSWORD
            token = await api.login(username, password)
        
        print ("Access Token:", token.access)
        print ("Refresh Token:", token.refresh)
        
        if (token):
            students = await api.getStudents(token.access)
            for student in students:
                print ("  Student Id........:", student.id)
                print ("  Student Name....:", student.name)
                print ("  Student Full Name....:", student.full_name)
                print ("  Student Status....:", student.status)

                metrics = await api.getDiary(token.access, student.id, "2026-04-24", "2026-04-24")
                for metric in metrics:
                    print ("    Metric Type......:", metric.type)
                    print ("    Metric State.....:", metric.state)
                    print ("    Metric Start.....:", metric.start)            

asyncio.get_event_loop().run_until_complete(main())