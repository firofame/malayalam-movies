import requests
from bs4 import BeautifulSoup

# Set the base URL
base_url = 'https://einthusan.tv/movie/results/?find=Popularity&lang=malayalam&page='

# Open the README.md file in write mode
with open('README.md', 'w', encoding='utf-8') as readme_file:
    try:
        # Write header and introduction
        readme_file.write("# Malayalam Movies on Einthusan\n\n")
        readme_file.write("This repository contains a list of popular Malayalam movies available on Einthusan.\n\n")
        readme_file.write("## Movie List\n\n")

        # Assuming you want to scrape titles from pages 1 to 5 (you can adjust the range as needed)
        for page_num in range(1, 6):
            # Construct the URL for the current page
            url = f'{base_url}{page_num}&ptype=View&tp=l30d'

            # Send a request to the URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Assuming movie titles are contained within HTML elements with a specific class, adjust this based on the actual structure of the webpage
            movie_elements = soup.find_all('a', class_='title')

            # Write the list of movie titles for the current page with corrected serial numbers and popularity status to the README.md file
            for index, movie_element in enumerate(movie_elements, start=(page_num - 1) * len(movie_elements) + 1):
                title = movie_element.find('h3').text.strip()
                status = movie_element.find('span')

                # Write the movie information in a formatted way
                readme_file.write(f"{index}. **{title}**")
                if status and status.text.strip():
                    popularity = status.text.strip()
                    readme_file.write(f" ({popularity})")
                readme_file.write("\n")

    except Exception as e:
        readme_file.write(f"\n\n## Error\n\nAn error occurred while updating the movie list:\n\n```\n{str(e)}\n```")
