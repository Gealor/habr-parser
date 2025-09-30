import asyncio
from pprint import pprint
import aiohttp
from config import settings
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from decorator import write_into_file
from models import Article


async def get_url_html(url: str, aiohttp_session: aiohttp.ClientSession) -> str:
    async with aiohttp_session.get(
        url, 
        headers={"User-Agent": str(UserAgent.chrome)},
    ) as response:
        response.raise_for_status()
        html = await response.text() # text() для получения кода html страницы сайта
    return html


def get_soup(html_text: str) -> BeautifulSoup:
    return BeautifulSoup(html_text, features="lxml")

def get_all_datas_for_article(article_soup: BeautifulSoup):
    head = article_soup.find("a", class_="tm-title__link")
    return {
        "title": head.find("span").text, # получаем текст по тегу span
        "url": head.get("href"),
        "count_views": article_soup.find("span", class_="tm-icon-counter__value").get("title"),
        "rating": article_soup.find(
                "span", 
                class_="tm-votes-meter__value tm-votes-meter__value_positive tm-votes-meter__value_appearance-article tm-votes-meter__value_rating tm-votes-meter__value"
            ).get("title"),
    }

def get_all_habr_articles(soup: BeautifulSoup):
    result = []
    all_articles_soup = soup.find_all("article", class_="tm-articles-list__item")
    for article_soup in all_articles_soup:
        data = get_all_datas_for_article(article_soup)
        article_model = Article(**data)
        result.append(article_model)
    return result

def parse_items(articles_model: list[Article]) -> list[dict]:
    return [article.model_dump() for article in articles_model]

@write_into_file(settings.FILEPATH)
async def main():
    async with aiohttp.ClientSession() as session:
        html_text = await get_url_html(settings.URL_HABR, session)
    
    soup = get_soup(html_text)
    result = get_all_habr_articles(soup)
    parse_result = parse_items(result)
    pprint(parse_result)
    return parse_result

if __name__=="__main__":
    asyncio.run(main())


    