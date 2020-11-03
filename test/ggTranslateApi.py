import pprint
from googleapiclient.discovery import build

api = "AIzaSyD79kNJykY2xrelsR8tE3QciUe83nOyYKw"
# api = "AIzaSyBNPasppAcUvEuuSB97iCTlxxzMew1y6Xc"


def main():

    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build('translate', 'v2',
                    developerKey=api)

    print(service.translations().list(
        target='vi',
        q=['flower']
    ).execute())


if __name__ == '__main__':
    main()
