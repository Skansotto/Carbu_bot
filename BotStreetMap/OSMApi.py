import urllib.parse, requests

class OSMApi:
    
    @staticmethod
    def serachAddress(query):
        encoded_query = urllib.parse.quote(query)
        query_url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&addressdetails=1"
        print("Query url:"+query_url)
        result = requests.post(query_url)
        json_map_response = result.json()
        return json_map_response