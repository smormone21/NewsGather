
import json, pathlib, datetime as dt, yaml, re

BASE_DIR = pathlib.Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
SITE_CONTENT = BASE_DIR / 'site' / 'content'
TEMPLATE = (BASE_DIR/'templates'/'article_template.md').read_text()

cfg = yaml.safe_load((BASE_DIR/'config.yaml').read_text())
languages = cfg['languages']

def render(template, ctx):
    out = template
    # rudimentary replacements
    for k,v in ctx.items():
        if isinstance(v,list):
            continue
        out = out.replace('{{ '+k+' }}', str(v))
    # urls list
    urls_block = '\n'.join([f'  - "{u}"' for u in ctx['urls']])
    out = re.sub(r'{% for url.*?%}(.*?){% endfor %}', urls_block, out, flags=re.S)
    return out

def main():
    entries = json.loads((DATA_DIR/'articles_translated.json').read_text())
    for e in entries:
        lang_dir = SITE_CONTENT / e['lang'] / 'posts'
        lang_dir.mkdir(parents=True, exist_ok=True)
        ctx = {
            'title': e['title'],
            'date': dt.datetime.utcnow().isoformat(),
            'lang': e['lang'],
            'urls': [e['link']],
            'slug': e['slug'],
            'body': e['markdown']
        }
        md = render(TEMPLATE, ctx)
        (lang_dir / f"{e['slug']}.md").write_text(md, encoding='utf-8')

if __name__ == '__main__':
    main()
