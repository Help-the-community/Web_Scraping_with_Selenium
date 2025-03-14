import scrapy
import json


class PlayersSpider(scrapy.Spider):
    name = "players"
    allowed_domains = ["baseball-reference.com"]
    start_urls = [f"https://www.baseball-reference.com/players/{letter}/" for letter in "ab"]


    def parse(self, response):
        # Extract player profile links
        player_links = response.css("div#div_players_ > p a::attr(href)").getall()
        for link in player_links:
            full_link = response.urljoin(link)
            yield scrapy.Request(url=full_link, callback=self.parse_player)

    @staticmethod
    def parse_player(response):
        # Extract player information
        player_name = response.css("h1 span::text").get()
        position = response.css("p:contains('Position') strong::text").re_first(r"Position: (.+)")
        bats = response.css("p:contains('Bats')::text").re_first(r"Bats: (.+?) •")
        throws = response.css("p:contains('Throws')::text").re_first(r"Throws: (.+)")
        height = response.css("p:contains('lb') span:nth-child(1)::text").get()
        weight = response.css("p:contains('lb') span:nth-child(2)::text").get()
        birth_date = response.css("span#necro-birth a::text").getall()
        birth_location = response.css("p:contains('Born:') span:last-child::text").get()
        draft_info = response.css("p:contains('Drafted by')::text").get()
        high_school = response.css("p:contains('High School:') a::text").get()
        college = response.css("p:contains('Schools:') a::text").getall()
        debut = response.css("p:contains('Debut:') a::text").get()
        last_game = response.css("p:contains('Last Game:') a::text").get()
        rookie_status = response.css("p:contains('Rookie Status:')::text").re_first(r"Rookie Status:\s+(.+)")
        agent = response.css("p:contains('Agents')::text").get()
        nickname = response.css("p:contains('Nicknames:') a::text").get()
        twitter = response.css("p:contains('Twitter:') a::attr(href)").get()

        # Extract player's image URL
        image_url = response.css("div.media-item img::attr(src)").get()

        # Store the extracted data in a dictionary
        player_data = {
            "name": player_name,
            "position": position,
            "bats": bats,
            "throws": throws,
            "height": height,
            "weight": weight,
            "birth_date": " ".join(birth_date),
            "birth_location": birth_location,
            "draft_info": draft_info,
            "high_school": high_school,
            "college": college,
            "debut": debut,
            "last_game": last_game,
            "rookie_status": rookie_status,
            "agent": agent,
            "nickname": nickname,
            "twitter": twitter,
            "image_url": response.urljoin(image_url),  # Ensure the URL is absolute
        }

        # Write the data to a JSON file
        with open("players.json", "a") as f:
            f.write(json.dumps(player_data) + "\n")

        yield player_data

