import json, os, pathlib, yaml, time, datetime as dt
import openai

    BASE_DIR = pathlib.Path(__file__).parent
    DATA_DIR = BASE_DIR / 'data'
    TEMPLATE_PATH = BASE_DIR / 'templates' / 'article_template.md'

    cfg = yaml.safe_load((BASE_DIR/'config.yaml').read_text())
    languages = cfg['languages']
    default_lang = cfg.get('default_language','en')

    openai.api_key = os.getenv('OPENAI_API_KEY')

    SYSTEM_REWRITE = """    You are a journalist rewriting news articles in a clear, neutral, B1-level English style similar to Reuters.
    Output Markdown only, without headings other than those that appear in the text.
    """

    SYSTEM_TRANSLATE = """    Translate the following Markdown article into {lang_name}. Keep the formatting. Maintain a neutral tone and B1 readability.
    """


    def load_articles():
        return json.loads((DATA_DIR/'articles_raw.json').read_text())

    def chat(prompt, system):
        res = openai.ChatCompletion.create(
            model='gpt-4o',
            messages=[
                {'role':'system','content':system},
                {'role':'user','content':prompt}
            ],
            temperature=0.2
        )
        return res.choices[0].message.content.strip()

    LANG_NAMES = {
        'en':'English',
        'it':'Italian',
        'es':'Spanish',
        'fr':'French',
        'de':'German'
    }

    def rewrite(art):
        prompt = f"""Rewrite the following article in under 400 words.

Title: {art['title']}

Original text (may be truncated):
{art.get('summary','')}

URL: {art['link']}
"""
        return chat(prompt, SYSTEM_REWRITE)

    def translate(md, lang_code):
        system = SYSTEM_TRANSLATE.format(lang_name=LANG_NAMES[lang_code])
        return chat(md, system)

    def main():
        DATA_DIR.mkdir(exist_ok=True)
        simplified = []
        for art in load_articles():
            # rewrite in default language first
            body_en = rewrite(art)
            translations = {default_lang: body_en}
            titles = {default_lang: art['title']}  # we keep original title for EN; could translate too

            for lang in languages:
                if lang == default_lang:
                    continue
                md = translate(body_en, lang)
                translations[lang] = md
                # naive title extraction: first line up to newline
                title_line = md.split('\n',1)[0]
                titles[lang] = title_line if len(title_line.split())<20 else art['title']

            for lang in languages:
                simplified.append({
                    'id': art['id'],
                    'slug': art['id'][:10],
                    'title': titles.get(lang, art['title']),
                    'markdown': translations[lang],
                    'lang': lang,
                    'link': art['link'],
                    'published': art['published']
                })
            time.sleep(1)  # avoid hitting rate limits

        (DATA_DIR/'articles_translated.json').write_text(json.dumps(simplified, ensure_ascii=False, indent=2), encoding='utf-8')

    if __name__ == '__main__':
        main()
