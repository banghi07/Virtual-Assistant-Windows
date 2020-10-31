import pprint
from googleapiclient.discovery import build

api = "AIzaSyD79kNJykY2xrelsR8tE3QciUe83nOyYKw"

def main():
    service = build("customsearch", "v1",  developerKey="AIzaSyD79kNJykY2xrelsR8tE3QciUe83nOyYKw")
    response = service.cse().list(q="khoa học máy tính", cx="efcdf7a6d77b621bc", num="3").execute()
    pprint.pprint(response)
    # fields="items/displayLink, items/formattedUrl, items/link, items/snippet, items/title"
    # print(response["items"][1]["formattedUrl"])

if __name__ == "__main__":
    main()
    
