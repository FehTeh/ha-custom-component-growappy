import asyncio
import aiohttp

from custom_components.growappy.api.growappy import GROWAPPY

async def main():
    async with aiohttp.ClientSession() as session:
        api = GROWAPPY(session)

        username = input("Enter your username/email..: ")
        password = input("Enter your password........: ")

        token = await api.login(username, password)
        if (token):
            students = await api.getStudents(token)
            print ("Students............:", students)
            for student in students:
                print ("  Student Id........:", student.id)
                print ("  Student Name....:", student.name)
                print ("  Student Full Name....:", student.full_name)
                print ("  Student Status....:", student.status)

asyncio.get_event_loop().run_until_complete(main())