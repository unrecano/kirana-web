"""
Crawler for site: Documentary Heaven
"""
from .utils import get_html_from_url

URL_BASE = "https://documentaryheaven.com"
SITE = "Documentary Heaven"

def get_document():
    """
    Obtener documento html de página principal.
    """
    return get_html_from_url(f'{URL_BASE}/all')

def get_documentaries_in_page(page):
    """
    Obtener listado de elementos con información de documentales de una
    página específica.

    url -- string.
    """
    url = f'{URL_BASE}/all/page/{page}/'
    document = get_html_from_url(url)
    return document.find_all('article', class_='post')

def get_url_documentary(documentary):
    """
    Extraer la url del detalle de un elemento documental (HTML).

    element -- string.
    """
    return documentary.find('h2').find("a").get('href')

def all_documentaries_documentaryheaven():
    """
    Retornar un array con todas las urls de los documentales del sitio.
    """
    document = get_document()
    _all = []
    paginator = document.find("div", class_="numeric-nav").find_all("li")
    pages = [e.find("a") for e in paginator if e.find("a") is not None]
    for i in range(1, int(pages[-2].text) + 1):
        documentaries = [get_url_documentary(d) \
            for d in get_documentaries_in_page(i)]
        _all = _all + documentaries
    return _all

def documentary_documentaryheaven(url):
    """
    Extraer información del detalle de un documental.

    url -- string.
    """
    html = get_html_from_url(url)
    main = html.find("section", {"id": "primary"}).find("article")
    title = main.find("h1").text
    year = main.find("meta", {"itemprop": "dateCreated"}).get("content") \
        if main.find("meta", {"itemprop": "dateCreated"}) else None
    duration = main.find("time").text.split(" ")[0] \
        if main.find("time") else None
    tags = main.find_all("a", {"rel": "category tag"})
    paragraphs = main.find("div", {"class": "entry-content"}).find_all("p")
    embedded = html.find("meta", {"itemprop": "embedUrl"}).get("content") \
        if html.find("meta", {"itemprop": "embedUrl"}) else None
    return {
        "url": url,
        "site": SITE,
        "title": title,
        "year": year,
        "embedded": embedded,
        "duration": duration,
        "tags": [t.text.strip() for t in tags],
        "description": " ".join([p.text.strip() for p in paragraphs])
    }
