from seleniumbase import SB

url = "https://www.worldometers.info/world-population/"

with SB(uc=True, test=True) as sb:
    sb.open(url)
    container = sb.wait_for_element("div.col-span-2>div.mt-2")
    # print(container.get_attribute("innerHTML"))

    # -------------------------------------------------------------------------------
    countries = container.find_elements("css selector", "div>div.flex.items-center")
    # -------------------------------------------------------------------------------

    world_population = []
    for country in countries:
        data = country.text.split("\n")
        world_population.append({"rank": data[0],
                                 "country": data[1],
                                 "population": data[2]
                                 })
    print(world_population)
