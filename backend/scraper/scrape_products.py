"""
Galaxy Plastics product scraper.
Crawls categories, subcategories, and products into JSON.
"""

import json
import time
import urllib.robotparser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.galaxyplastics.com"
USER_AGENT = "GalaxyPlasticsChatbotScraper/1.0"

START_URLS = [
    "/product-category/municipal/",
    "/product-category/plumbing-industrial/",
    "/product-category/irrigation-agriculture/",
    "/product-category/corrosion-control/",
    "/product-category/electrical-duct-fittings/",
]


OUTPUT_PATH = (
    Path(__file__).parent.parent
    / "app"
    / "data"
    / "products.json"
)


visited = set()


def get_robot_parser():
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urljoin(BASE_URL, "/robots.txt"))

    try:
        rp.read()
    except Exception:
        print("Could not read robots.txt")

    return rp


def fetch(url):
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=10
        )

        response.raise_for_status()
        return response.text

    except requests.RequestException as e:
        print("Failed:", url, e)
        return None


def extract_links(html, current_url):

    soup = BeautifulSoup(html, "html.parser")

    products = set()
    categories = set()

    for a in soup.find_all("a", href=True):

        link = urljoin(current_url, a["href"])

        parsed = urlparse(link)

        if parsed.netloc and parsed.netloc != "www.galaxyplastics.com":
            continue

        link = link.split("#")[0]

        if "/product/" in link:
            products.add(link)

        elif "/product-category/" in link:
            categories.add(link)

    return products, categories


def scrape_product(url):
    html = fetch(url)

    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # Product name
    title = soup.find("h1", class_="product_title")

    name = (
        title.get_text(" ", strip=True)
        if title
        else urlparse(url).path.split("/")[-1]
    )

    # Product description
    description = ""

    # Galaxy Plastics Elementor product content
    content = soup.find(
        "div",
        attrs={
            "data-widget_type": "woocommerce-product-content.default"
        }
    )

    if content:
        container = content.find(
            "div",
            class_="elementor-widget-container"
        )

        if container:
            paragraphs = container.find_all("p")

            description = " ".join(
                p.get_text(" ", strip=True)
                for p in paragraphs
                if p.get_text(strip=True)
            )


    # Fallback selectors
    if not description:

        selectors = [
            "div.woocommerce-product-details__short-description",
            "div.entry-content",
            "main"
        ]

        for selector in selectors:

            content = soup.select_one(selector)

            if content:

                paragraphs = content.find_all("p")

                description = " ".join(
                    p.get_text(" ", strip=True)
                    for p in paragraphs
                    if p.get_text(strip=True)
                )

                if description:
                    break


    if not description:
        description = "No description available."


    # Get category from breadcrumb
    category = "Product"

    breadcrumb = soup.find(
        "nav",
        class_="woocommerce-breadcrumb"
    )

    if breadcrumb:
        links = breadcrumb.find_all("a")

        if len(links) > 1:
            category = links[1].get_text(
                " ",
                strip=True
            )


    return {
        "name": name,
        "category": category,
        "description": description,
        "url": url
    }



def crawl():

    rp = get_robot_parser()

    products = []
    product_urls = set()
    category_queue = set()


    for start in START_URLS:
        category_queue.add(
            urljoin(BASE_URL, start)
        )


    while category_queue:

        category_url = category_queue.pop()

        if category_url in visited:
            continue

        visited.add(category_url)

        if not rp.can_fetch(USER_AGENT, category_url):
            print("Blocked:", category_url)
            continue


        print("Scanning category:", category_url)

        html = fetch(category_url)

        if not html:
            continue


        found_products, found_categories = extract_links(
            html,
            category_url
        )


        product_urls.update(found_products)


        for category in found_categories:
            if category not in visited:
                category_queue.add(category)


        time.sleep(1)


    print(
        f"Found {len(product_urls)} products"
    )


    for index, url in enumerate(product_urls, 1):

        print(
            f"Scraping product {index}/{len(product_urls)}"
        )

        product = scrape_product(url)

        if product:

            product["id"] = str(index)

            products.append(product)


        time.sleep(1.5)


    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            products,
            f,
            indent=2,
            ensure_ascii=False
        )


    print(
        f"Saved {len(products)} products"
    )



if __name__ == "__main__":
    crawl()