import os
import time
import requests

from datetime import timedelta

from timeloop import Timeloop

tl = Timeloop()

api = os.environ['API_TINDER']

@tl.job(interval=timedelta(minutes=1))
def sample_job_every_2s():
    response = requests.get("https://api.gotinder.com/profile",
                            headers={'x-auth-token': '1f7a383e-cb45-4ff0-93e4-469f84ec337f'})
    print(response.json())


if __name__ == "__main__":
    sample_job_every_2s()
    tl.start(block=True)
