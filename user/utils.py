from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail


def send():
    try:
        sent_mail_mail = send_mail(
                "hello",
                "txt_",
                "rasif@metrictreelabs.com",
                ['rasifazak123@gmail.com'],
                fail_silently=False,
            )
        print(sent_mail_mail)
        return "done"
    except Exception as e:
        print("[[[[[[]]]]]]",e)
        return str(e)
    
from asgiref.sync import async_to_sync
import asyncio


async def some_async_function():
        # Simulating an asynchronous operation with asyncio.sleep
        await asyncio.sleep(2)
        return "Async operation complete!"

async def get():
        # Your asynchronous code here
        result = await some_async_function()

        # If you need to use the result in a synchronous context, you can use async_to_sync
        sync_result = async_to_sync(some_async_function)()
        print("oooooooooooooooooooooo")

        return ({"result": result, "sync_result": sync_result})