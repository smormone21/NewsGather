
import feedparser, json, yaml, hashlib, datetime as dt, pathlib

BASE_DIR = pathlib.Path(__file__).parent
CFG_PATH = BASE_DIR / 'config.yaml'
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

def load_config():
    with open(CFG_PATH,'r') as f:
        return yaml.safe_load(f)

def fetch(url):
    return feedparser.parse(url)

def main():
    cfg = load_config()
    out = []
    for src in cfg['sources']:
        parsed = fetch(src)
        for e in parsed.entries:
            uid = hashlib.sha256(e.link.encode()).hexdigest()
            out.append({
                'id': uid,
                'title': e.title,
                'summary': getattr(e,'summary',''),
                'link': e.link,
                'published': getattr(e,'published',dt.datetime.utcnow().isoformat())
            })
    (DATA_DIR/'articles_raw.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
