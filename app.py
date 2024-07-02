import re
import requests
from bs4 import BeautifulSoup

def fetch_html_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None

def extract_movie_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    movies = []

    for movie_item in soup.find_all('li', class_=lambda x: x != 'adspace-lb'):
        movie = {}

        # Extract title
        title_elem = movie_item.find('a', class_='title')
        if title_elem and title_elem.h3:
            movie['title'] = title_elem.h3.text.strip()
        else:
            continue  # Skip this movie if no title is found

        # Extract year and language
        info_elem = movie_item.find('div', class_='info')
        if info_elem and info_elem.p:
            info_text = info_elem.p.text.strip()
            year_match = re.search(r'\d{4}', info_text)
            if year_match:
                movie['year'] = year_match.group()
            lang_span = info_elem.p.find('span')
            if lang_span:
                movie['language'] = lang_span.text.strip()

        # Extract synopsis
        synopsis_elem = movie_item.find('p', class_='synopsis')
        if synopsis_elem:
            movie['synopsis'] = synopsis_elem.text.strip()

        # Extract professionals
        professionals = []
        for prof_elem in movie_item.find_all('div', class_='prof'):
            name_elem = prof_elem.find('p')
            role_elem = prof_elem.find('label')
            if name_elem and role_elem:
                professionals.append({
                    'name': name_elem.text.strip(),
                    'role': role_elem.text.strip()
                })
        movie['professionals'] = professionals

        # Extract ratings
        ratings = {}
        ratings_ul = movie_item.find('ul', class_='average-rating')
        if ratings_ul:
            for rating_elem in ratings_ul.find_all('li'):
                label_elem = rating_elem.find('label')
                value_elem = rating_elem.find('p')
                if label_elem and value_elem:
                    ratings[label_elem.text.strip()] = value_elem.text.strip()
        movie['ratings'] = ratings

        # Extract extras (IMDb and Trailer links)
        extras = {}
        extras_elem = movie_item.find('div', class_='extras')
        if extras_elem:
            for link in extras_elem.find_all('a'):
                if 'Wiki' in link.text:
                    extras['imdb'] = link['href']
                elif 'Trailer' in link.text:
                    extras['trailer'] = link['href']
        movie['extras'] = extras

        movies.append(movie)

    return movies

def write_to_readme(movies):
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write("# Einthusan Movie Details\n\n")
        for movie in movies:
            if movie:  # Only write non-empty movie dictionaries
                f.write(f"## {movie.get('title', 'Unknown Title')}\n\n")
                f.write(f"- **Year**: {movie.get('year', 'N/A')}\n")
                f.write(f"- **Language**: {movie.get('language', 'N/A')}\n")
                f.write(f"- **Synopsis**: {movie.get('synopsis', 'N/A')}\n\n")
                
                f.write("### Professionals\n")
                for prof in movie.get('professionals', []):
                    f.write(f"- {prof['role']}: {prof['name']}\n")
                f.write("\n")
                
                f.write("### Ratings\n")
                for rating_type, rating_value in movie.get('ratings', {}).items():
                    f.write(f"- {rating_type}: {rating_value}\n")
                f.write("\n")
                
                f.write("### Links\n")
                extras = movie.get('extras', {})
                if 'imdb' in extras:
                    f.write(f"- [IMDb]({extras['imdb']})\n")
                if 'trailer' in extras:
                    f.write(f"- [Trailer]({extras['trailer']})\n")
                f.write("\n---\n\n")

# Example usage
url = "https://einthusan.tv/movie/results/?find=Popularity&lang=malayalam&ptype=view&tp=l30d"
html_content = fetch_html_content(url)

if html_content:
    movie_details = extract_movie_details(html_content)
    write_to_readme(movie_details)
    print("Movie details have been written to README.md")
else:
    print("Failed to fetch HTML content. Please check the URL and your internet connection.")
