import scrapy
import json
import os


class StubHubSpider(scrapy.Spider):
    name = "stubhub"
    allowed_domains = ["stubhub.com"]
    base_url = "https://www.stubhub.com/explore?method=getExploreEvents&lat=MjUuNDQ3ODkwMw%3D%3D&lon=LTgwLjQ3OTIxOTY%3D&to=253402300799999&page={}&tlcId=2"

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'referer': 'https://www.stubhub.com/explore?lat=MjUuNDQ3ODkwMw%3D%3D&lon=LTgwLjQ3OTIxOTY%3D&to=253402300799999&page=1&tlcId=2',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }

    #Output file
    output_file = "stubhub_data.json"

    # def __init__(self):
    #     """Initialize and clear the JSON file before writing new data"""
    #     if os.path.exists(self.output_file):
    #         os.remove(self.output_file)

    def start_requests(self):
        yield scrapy.Request(
            url=self.base_url.format(0),
            headers=self.headers,
            callback=self.parse,
            meta={"page_number": 0, "data_list": []}
        )

    def parse(self, response):
        page_number = response.meta["page_number"]
        data_list = response.meta["data_list"]

        try:
            json_data = json.loads(response.text)
            events = json_data.get("events", [])

            for event in events:
                dict_data = {}

                dict_data["name"] = self.get_title(event)
                dict_data["datetime"] = self.get_datetime(event)
                dict_data["location"] = self.get_location(event)
                dict_data["link"] = self.get_link(event)
                data_list.append(dict_data)


                # data_list.append({
                #     "name": self.get_title(event),
                #     "datetime": self.get_datetime(event),
                #     "location": self.get_location(event),
                #     "link": self.get_link(event),
                # })

            # Save data to JSON file 
            self.save_to_json(data_list)

            #pagination
            if len(events) >= 48:  
                next_page = page_number + 1
                yield scrapy.Request(
                    url=self.base_url.format(next_page),
                    headers=self.headers,
                    callback=self.parse,
                    meta={"page_number": next_page, "data_list": data_list}
                )

        except json.JSONDecodeError as e:
            self.logger.error(f"json_data error: {e}")

    def get_title(self, item):
        try:
            return item.get("name", "-")
        except KeyError:
            return "-"

    def get_datetime(self, item):
        try:
            return f"{item['dayOfWeek']}, {item['formattedDateWithoutYear']}, {item['formattedTime']}"
        except KeyError:
            return "-"

    def get_location(self, item):
        try:
            return f"{item['formattedVenueLocation']}, {item['venueName']}"
        except KeyError:
            return "-"

    def get_link(self, item):
        try:
            return item['url']
        except KeyError:
            return "-"

    def save_to_json(self, data):
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

