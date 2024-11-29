from celery import shared_task

@shared_task(name="sum")
def post(a,b):
    print(a+b)
    return a + b


from pyfcm import FCMNotification

def fc():
    # Send to single device.

    fcm = FCMNotification(service_account_file="/home/rasif/Downloads/rent-test-24344-firebase-adminsdk-4ei5o-9adffd4797.json", project_id="rent-test-24344")

    # Google oauth2 credentials(such as ADC, impersonate credentials) can be used instead of service account file.

    # OR initialize with proxies

    proxy_dict = {
            "http"  : "http://127.0.0.1",
            "https" : "http://127.0.0.1",
            }

    fcm_body = {
            "message": {
                "title": "Hello",
                "body": "Julll",
                "url": "https://google.com"
            }
        }
    # fcm = FCMNotification(service_account_file="<service-account-json-path>", project_id="<project-id>", proxy_dict=proxy_dict)

    # Your service account file can be gotten from:  https://console.firebase.google.com/u/0/project/_/settings/serviceaccounts/adminsdk

    fcm_token = [
        "eV3cqxoBZsUWoeLCwxuxa8:APA91bE9FWf3OITYkC5ghggFEuwhiSPPNhnLwAypYiB1wy76xhta9-hTC7TUqqVLTPp7Zz1JgH4f8xV_q8T4lWLnoOmlNbqV92e_oFYtLpbTBhi6Nntor_zvgeirqs9PzoZsX8l7wbnl",
        "eAcW7RhqkpF-kAugO9X5ue:APA91bG7bagUURm0gmaqKqBtozwNy_2jQgl9yV_M-qSD8JoRIaatKgd6AOvb4TMUKNlCqWTUNSJZUMgUmSlMRkyh1Mn84-uXb4Dx7PMdJBNje0a1GVVF5ac_WKf3zCtO_6AJyx1ka0J9"
        ]
    notification_title = "Uber update"
    notification_body = "Hi John, your order is on the way!"
    notification_image = "https://example.com/image.png"
    result = fcm.async_notify_multiple_devices(registration_ids=fcm_token, notification_title=notification_title, notification_body=notification_body, notification_image=notification_image)
    print (result)