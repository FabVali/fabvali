import requests

GITHUB_USERNAME = "FabVali"
API_ENDPOINT = f"https://api.github.com/users/fabvali/repos"

def fetch_language_stats():
    response = requests.get(API_ENDPOINT)
    response.raise_for_status() 
    repos = response.json()

    language_usage = {}
    total_size = 0

    for repo in repos:
        if not repo["fork"]:
            language_url = repo["languages_url"]
            language_response = requests.get(language_url)
            language_response.raise_for_status()
            languages = language_response.json()

            for language, size in languages.items():
                if language not in language_usage:
                    language_usage[language] = 0
                language_usage[language] += size
                total_size += size

    language_percentages = {
        language: round((size / total_size) * 100, 2)
        for language, size in language_usage.items()
    }
    return language_percentages

def update_readme_with_languages(language_stats):
    readme_path = "README.md"

    with open(readme_path, "r") as file:
        content = file.readlines()

    start_marker = "<!--START_SECTION:language_stats-->"
    end_marker = "<!--END_SECTION:language_stats-->"

    try:
        start_index = content.index(f"{start_marker}\n")
        end_index = content.index(f"{end_marker}\n")
    except ValueError:
        raise ValueError("Platzhalter für Programmiersprachen-Statistiken nicht in README.md gefunden.")

    updated_stats = "\n".join(
        [f"🔹 {language}: {percentage}%" for language, percentage in language_stats.items()]
    )

    content[start_index + 1:end_index] = [updated_stats + "\n"]

    with open(readme_path, "w") as file:
        file.writelines(content)

if __name__ == "__main__":
    try:
        stats = fetch_language_stats()
        update_readme_with_languages(stats)
        print("README.md erfolgreich aktualisiert!")
    except Exception as e:
        print(f"Fehler: {e}")
