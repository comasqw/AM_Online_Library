import httpx
from bs4 import BeautifulSoup
import asyncio

url = "https://bararanonline.com"
element_not_found_text = "Այս բաժինը լրացրած չէ կամ չի գտնվել"


async def parse_word(word):
    word = word.lower()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}/{word}")
    except Exception as e:
        return {"error": e}

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        word_info_list = []
        for element in soup.find_all(class_="content-core-arm w-100"):
            if not element.find("img"):
                word_info_list.append(element.text)
            else:
                word_info_list.append(element_not_found_text)

        english_translation_element = soup.find(class_="content-core-arm w-100 content-core-eng")
        if not english_translation_element.find("img"):
            word_info_list.append(english_translation_element.text)
        else:
            word_info_list.append(element_not_found_text)

        word_info = {
            "բացատրություն": word_info_list[0],
            "հոմանիշներ": word_info_list[1],
            "հականիշներ": word_info_list[2],
            "ռուսերեն թարգմանություն": word_info_list[3],
            "անգլերեն թարգմանություն": word_info_list[4]
        }

        return word_info
    else:
        return "Բառը չի գտնվել"

if __name__ == '__main__':
    info_word = asyncio.run(parse_word("բառ"))
    print(info_word)
