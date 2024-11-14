import os
from openai import OpenAI
import sys
from pathlib import Path


DEFAULT_ARTICLE_FILENAME = "Zadanie dla JJunior AI Developera - tresc artykulu.txt"


def load_api_key():
    """Ładuje klucz API OpenAI z różnych źródeł w kolejności priorytetowej."""
    # 1. Sprawdź zmienną środowiskową
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return api_key

    # 2. Sprawdź plik .env
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    api_key = line.split('=')[1].strip().strip("'").strip('"')
                    return api_key

    # 3. Poproś użytkownika o wprowadzenie klucza
    api_key = input("Podaj swój klucz API OpenAI: ").strip()
    if api_key:
        return api_key

    print("Błąd: Nie znaleziono klucza API OpenAI.")
    sys.exit(1)

def get_input_filename():
    """Wybór pliku zawierającego artykuł."""
    if os.path.exists(DEFAULT_ARTICLE_FILENAME):
        return DEFAULT_ARTICLE_FILENAME
    
    print(f"\nDomyślny plik '{DEFAULT_ARTICLE_FILENAME}' nieznaleziony.")
    while True:
        user_filename = input("\nWprowadź ściezkę do pliku z artykułen (lub naciśnij Ctrl+C aby zrezygnować): ").strip()
        
        if not user_filename:
            print("Nazwa pliku nie moze być pusta. Spróbuj jeszcze raz.")
            continue
            
        if os.path.exists(user_filename):
            return user_filename
        else:
            print(f"Plik '{user_filename}' nieznaleziony. Spróbuj jeszcze raz.")    

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
    Transform the following article into HTML code according to these guidelines:

    1. Use semantic HTML5 tags to properly structure the content, including but not limited to:
       - article
       - section
       - header
       - h1, h2, h3 (for proper heading hierarchy)
       - p
       - blockquote (for quotes if present)
       - ul/ol for lists
       - figure/figcaption for images

    2. Identify strategic locations where images would enhance the content and add img tags with:
       - src="image_placeholder.jpg"
       - detailed alt attributes containing specific AI image generation prompts
       - appropriate figcaption elements for image descriptions in the language of the article
       - ensure each image placement serves a clear purpose in supporting the content

    3. Important requirements:
       - Do NOT include html, head, or body tags
       - Do NOT add any CSS or JavaScript
       - Do NOT include any external resources
       - Focus on semantic structure and content organization

    4. Additional considerations:
       - Preserve the original content hierarchy
       - Use appropriate HTML5 elements for content meaning
       - Ensure logical flow of information
       - Add descriptive alt texts that could serve as image AI generation prompts

    Here's the article to process:

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
    # Załaduj klucz API
    api_key = load_api_key()

    # Inicjalizacja klienta OpenAI
    client = OpenAI(api_key=api_key)

    # Uzyskanie nazwy nazwy pliku wejściowego
    input_filename = get_input_filename()
    print(f"\nPrzetwarzany plik: {input_filename}")

    # Wczytanie artykułu
    article_content = read_article(input_filename)

    # Przetwórz artykuł z użyciem AI
    html_content = process_article_with_ai(client, article_content)

    # Zapisz wynik
    save_html(html_content, 'artykul.html')
    print("Artykuł został pomyślnie przetworzony i zapisany jako artykul.html")

if __name__ == "__main__":
    main()