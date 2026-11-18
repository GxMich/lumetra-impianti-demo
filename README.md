# Lumetra Impianti — sito dimostrativo

**Demo online → https://gxmich.github.io/lumetra-impianti-demo/**

> ### Attività di fantasia
>
> **Lumetra Impianti non esiste.** Nome, logo, indirizzo (Rocca Tessera è un paese inventato), telefono,
> email, storia, abilitazioni e lavori realizzati sono inventati e servono solo a mostrare come funziona il
> sito. Le foto dei lavori sono foto Unsplash che illustrano interventi immaginari.
>
> L'email usa il dominio `lumetra-impianti.example`: `.example` è riservato dallo IANA e non può recapitare
> posta. Il telefono è `+39 000 000 0000`. Il modulo di contatto mostra solo un riepilogo: non invia dati né
> allegati.
>
> Tutte le pagine hanno `<meta name="robots" content="noindex, nofollow">` e `robots.txt` blocca l'intero
> sito. Su un project site di GitHub Pages il `robots.txt` in sottocartella non viene letto: la protezione
> effettiva è il `noindex` nelle pagine.

Sito di una ditta di impianti elettrici e tecnologici che lavora per aziende, enti pubblici e privati.
Ventitré pagine statiche (404 compresa), senza framework e senza librerie esterne.

## Cosa mostra la demo

- **Home** con il lavoro più rappresentativo in apertura, numeri essenziali, lavori in evidenza, percorsi
  per tipo di committente (aziende, enti, progettisti, privati) e un elenco delle sette competenze che
  cambia foto al passaggio del mouse.
- **Sette pagine di competenza** (impianti elettrici, illuminazione, fotovoltaico, domotica, sicurezza,
  antincendio, diffusione sonora) con cosa si realizza, cosa preparare per il primo contatto e i lavori
  collegati.
- **Otto lavori** filtrabili per settore, ognuno con la sua scheda: dati del lavoro, interventi eseguiti,
  competenze coinvolte e lavori simili.
- **Azienda** con storia, abilitazioni e settori; **Assistenza** per manutenzione e guasti.
- **Contatti** con un modulo che si precompila dai link delle altre pagine (servizio e profilo), cambia
  titolo e indicazioni di conseguenza, controlla i campi e mostra il riepilogo della richiesta.
- Menu mobile in un `dialog`, barra di chiamata fissa su telefono, rispetto di «riduci movimento».

## Tecnologie

- HTML generato da `scripts/build_site.py` (solo libreria standard di Python). Competenze, lavori, settori e
  abilitazioni sono in `content/site.json`; le dimensioni delle foto in `content/media.json`.
- CSS in `assets/site.css`, minificato dal generatore in `assets/site.min.css` insieme ai font.
- JavaScript vanilla in `assets/core.js` e `assets/site.js`.
- Font IBM Plex Sans e IBM Plex Serif ospitati nel progetto (licenza SIL OFL, vedi `assets/fonts/`).
- Pubblicazione su GitHub Pages direttamente dal ramo `main`.

## Avviarla in locale

```bash
python scripts/build_site.py     # rigenera le pagine (facoltativo: sono già nel repository)
python -m http.server 8000
```

Poi apri http://127.0.0.1:8000/.

## Crediti

Foto da Unsplash, elencate in [CREDITI-FOTO.md](CREDITI-FOTO.md). Sito dimostrativo realizzato da
[Michele Modica](https://www.modicamichele.it).
