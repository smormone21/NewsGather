# newsgather 🌍📰

**newsgather** è un giornale automatico multilingue che:
1. Raccoglie notizie da fonti certificate
2. Le riscrive in stile chiaro, neutrale (livello B1)
3. Traduce ogni articolo in ⚑ EN, IT, ES, FR, DE
4. Pubblica un sito statico multilingue con Hugo

## Setup rapido

1. Crea un repository GitHub da questo template (Use this template → Create).
2. In *Settings → Secrets* aggiungi:
   * `OPENAI_API_KEY`
   * (opzionale) `NETLIFY_AUTH_TOKEN`, `NETLIFY_SITE_ID` per il deploy automatico su Netlify
3. Al primo push GitHub Actions lancerà la pipeline e pubblicherà il sito.

### Config

Tutte le impostazioni sono in `config.yaml`, incluse le fonti RSS.

### Deploy

* **GitHub Pages**: gratis; si attiva da Settings → Pages.
* **Netlify**: più veloce, dominio personalizzabile; aggiungi i due secret sopra.

Made with ♥ by you, 100 % sotto il tuo controllo.