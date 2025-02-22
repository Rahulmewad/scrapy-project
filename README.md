# StubHub Scraper Documentation

## Overview
This Scrapy spider, `StubHubSpider`, scrapes event information from StubHub. It extracts event names, dates, locations, and links, then saves them into a JSON file.

## Installation and Requirements
Ensure you have Scrapy installed:
```bash
pip install scrapy
```

## Spider Details
- **Name**: `stubhub`
- **Allowed Domains**: `stubhub.com`
- **Base URL**: `https://www.stubhub.com/explore?method=getExploreEvents&lat=MjUuNDQ3ODkwMw%3D%3D&lon=LTgwLjQ3OTIxOTY%3D&to=253402300799999&page={}&tlcId=2`
- **Output File**: `stubhub_data.json`

## Headers
The spider includes headers to mimic a real browser request, including `user-agent`, `referer`, and `accept-language`.

## Workflow
1. **`start_requests()`**
   - Initiates the scraping process with page `0`.
   - Passes meta-data (`page_number` and `data_list`) to the `parse` method.

2. **`parse(response)`**
   - Parses JSON response to extract event data.
   - Calls helper methods to retrieve event details.
   - Saves extracted data to `stubhub_data.json`.
   - Implements pagination to request the next page if at least 48 events are found.

3. **Helper Methods**
   - `get_title(item)`: Extracts the event name.
   - `get_datetime(item)`: Extracts and formats the event date and time.
   - `get_location(item)`: Extracts the event location and venue.
   - `get_link(item)`: Extracts the event URL.

4. **`save_to_json(data)`**
   - Writes scraped data to `stubhub_data.json`.

## Running the Spider
To run the spider, use the following command:
```bash
scrapy crawl stubhub
```

## Error Handling
- Catches `json.JSONDecodeError` if the response is not valid JSON.
- Uses `try-except` blocks to handle missing keys in event data.

## Notes
- The pagination stops when fewer than 48 events are found.
- The JSON file is overwritten with each execution.

