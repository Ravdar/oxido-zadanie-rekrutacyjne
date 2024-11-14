import os
from openai import OpenAI
import sys

def read_article(filename):
    """Odczytuje zawartość pliku tekstowego."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Błąd: Plik {filename} nie został znaleziony.")
        sys.exit(1)
    except Exception as e:
        print(f"Wystąpił błąd podczas odczytu pliku: {e}")
        sys.exit(1)

def save_html(content, filename):
    """Zapisuje wygenerowany HTML do pliku."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Wystąpił błąd podczas zapisywania pliku: {e}")
        sys.exit(1)

def process_article_with_ai(client, article_content):
    """Przetwarza artykuł używając OpenAI API."""
    prompt = """
    Przekształć poniższy artykuł na kod HTML zgodnie z następującymi wytycznymi:
    1. Użyj odpowiednich tagów HTML do strukturyzacji treści (np. article, section, h1, h2, p).
    2. Zidentyfikuj miejsca, gdzie warto wstawić obrazy i dodaj tagi img z:
       - src="image_placeholder.jpg"
       - atrybutem alt zawierającym dokładny prompt do wygenerowania obrazu
       - figcaption dla podpisu pod obrazem
    3. Nie dodawaj tagów html, head, body ani żadnego CSS czy JavaScript.
    4. Zachowaj oryginalną strukturę i hierarchię treści.

    Oto artykuł do przetworzenia:

    {article_content}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # lub inny odpowiedni model
            messages=[
                {"role": "system", "content": "Jesteś ekspertem w tworzeniu semantycznego HTML5."},
                {"role": "user", "content": prompt.format(article_content=article_content)}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Wystąpił błąd podczas komunikacji z OpenAI API: {e}")
        sys.exit(1)

def main():
    # Sprawdź czy klucz API jest ustawiony
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Błąd: Nie znaleziono klucza API OpenAI. Ustaw zmienną środowiskową OPENAI_API_KEY.")
        sys.exit(1)

    # Inicjalizacja klienta OpenAI
    client = OpenAI(api_key=api_key)

    # Odczytaj artykuł
    article_content = read_article('artykul.txt')

    # Przetwórz artykuł z użyciem AI
    html_content = process_article_with_ai(client, article_content)

    # Zapisz wynik
    save_html(html_content, 'artykul.html')
    print("Artykuł został pomyślnie przetworzony i zapisany jako artykul.html")

if __name__ == "__main__":
    main()