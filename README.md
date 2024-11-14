# Procesor artykułów HTML z AI 🤖

Aplikacja przetwarza pliki tekstowe na semantyczny kod HTML przy użyciu API OpenAI, automatycznie sugerując miejsca na obrazy wraz z promptami do ich wygenerowania.

<img src="https://th.bing.com/th/id/OIG3.VTOSIcm3WxV7xlQXLU_P?w=1024&h=1024&rs=1&pid=ImgDetMain" alt="AI robot converting the text" width="200"/>

## Wymagania

- Python 3.8 lub nowszy
- Zainstalowane wymagane biblioteki (patrz: `requirements.txt`)
- Klucz API OpenAI

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/Ravdar/oxido-zadanie-rekrutacyjne
cd article-processor
```

2. Zainstaluj wymagane zależności:
```bash
pip install -r requirements.txt
```

## Konfiguracja klucza API

Aplikacja umożliwia konfigurację klucza API OpenAI na kilka sposobów:

1. **Zmienna środowiskowa**:
```bash
export OPENAI_API_KEY='twój-klucz-api'
```

2. **Plik .env**:
Utwórz plik `.env` w głównym katalogu projektu:
```
OPENAI_API_KEY=twój-klucz-api
```

3. **Wprowadzenie ręczne**:
Jeśli żaden z powyższych sposobów nie jest skonfigurowany, aplikacja poprosi o wprowadzenie klucza API manualnie.

## Użycie

1. Umieść tekst artykułu w pliku `artykul.txt` w głównym katalogu projektu.

2. Uruchom aplikację:
```bash
python main.py
```

3. Wygenerowany kod HTML zostanie zapisany w pliku `artykul.html`.


## Uwagi

- Aplikacja używa modelu GPT-4 OpenAI. Możesz zmienić model w kodzie, modyfikując parametr `model` w funkcji `process_article_with_ai`.
- Upewnij się, że masz wystarczające środki na koncie OpenAI do korzystania z API.
- Wygenerowany kod HTML nie zawiera tagów `<html>`, `<head>` ani `<body>` - zawiera tylko zawartość do umieszczenia wewnątrz `<body>`.
