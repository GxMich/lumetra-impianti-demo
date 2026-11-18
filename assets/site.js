/* Service previews, sector filters and a local-only contact preview. */
(() => {
  'use strict';
  const params = new URLSearchParams(location.search);
  document.querySelectorAll('[data-prefill]').forEach(select => {
    const wanted = params.get(select.dataset.prefill);
    if (!wanted) return;
    const option = [...select.options].find(option => option.value === wanted);
    if (option) select.value = option.value;
  });

  // A prefilled request gets a matching heading: the service first, then the profile.
  const contextOf = name => {
    const select = document.querySelector(`[data-prefill="${name}"]`);
    const option = select && params.get(name) ? select.selectedOptions[0] : null;
    return option && option.dataset.title ? option : null;
  };
  const context = contextOf('servizio') || contextOf('profilo');
  const contactTitle = document.querySelector('[data-contact-title]');
  if (context && contactTitle) {
    const heading = context.dataset.title.replace(/\.$/, '');
    contactTitle.textContent = context.dataset.title;
    document.querySelector('[data-contact-lead]').textContent = context.dataset.lead;
    document.querySelector('[data-form-title]').textContent = heading;
    document.title = `${heading} | Lumetra Impianti`;
    // The new text above may have moved the form the link points to.
    if (location.hash === '#richiesta') document.getElementById('richiesta')?.scrollIntoView();
  }

  const skills = document.querySelector('[data-skills]');
  if (skills) {
    const links = [...skills.querySelectorAll('[data-skill]')];
    const images = [...document.querySelectorAll('[data-skill-img]')];
    const show = id => {
      links.forEach(link => link.classList.toggle('is-on', link.dataset.skill === id));
      images.forEach(img => img.classList.toggle('is-on', img.dataset.skillImg === id));
    };
    links.forEach(link => {
      link.addEventListener('mouseenter', () => show(link.dataset.skill));
      link.addEventListener('focus', () => show(link.dataset.skill));
    });
  }

  const filters = document.querySelector('[data-filters]');
  if (filters) {
    const cards = [...document.querySelectorAll('[data-works] [data-cat]')];
    const count = document.querySelector('[data-filter-count]');
    const buttons = [...filters.querySelectorAll('[data-filter]')];
    function applyFilter(value, updateURL) {
      if (!buttons.some(button => button.dataset.filter === value)) value = 'Tutti';
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === value)));
      const visible = cards.filter(card => {
        card.hidden = value !== 'Tutti' && card.dataset.cat !== value;
        return !card.hidden;
      });
      count.textContent = `${visible.length} ${visible.length === 1 ? 'lavoro' : 'lavori'}${value === 'Tutti' ? '' : ` nel settore ${value.toLowerCase()}`}`;
      if (updateURL) {
        const url = new URL(location.href);
        if (value === 'Tutti') url.searchParams.delete('settore');
        else url.searchParams.set('settore', value);
        history.replaceState(null, '', url);
        window.siteMotion?.animate(document.querySelector('[data-works]'), [{ opacity: .65 }, { opacity: 1 }], { duration: 180 });
      }
    }
    applyFilter(params.get('settore') || 'Tutti', false);
    filters.addEventListener('click', event => {
      const button = event.target.closest('[data-filter]');
      if (button) applyFilter(button.dataset.filter, true);
    });
    window.addEventListener('popstate', () => applyFilter(new URLSearchParams(location.search).get('settore') || 'Tutti', false));
  }

  const form = document.querySelector('[data-form-demo]');
  if (!form) return;
  const submit = form.querySelector('[data-submit]');
  const fields = form.querySelector('[data-form-fields]');
  const review = form.querySelector('[data-form-ok]');
  const summary = form.querySelector('[data-form-errors]');
  const fileStatus = form.querySelector('[data-file-status]');
  const labels = { nome: 'Nome e cognome', azienda: 'Azienda, ente o studio', comune: 'Comune dell’intervento', email: 'Email', telefono: 'Telefono', messaggio: 'Descrizione', allegato: 'Allegato' };
  const get = name => form.elements.namedItem(name);
  const text = name => String(get(name).value).trim();
  let attempted = false;
  submit.disabled = false;

  function updateContext() {
    const documentation = text('servizio') === 'Documentazione aziendale';
    get('comune').required = !documentation;
    form.querySelector('label[for="comune"]').textContent = `Comune dell’intervento${documentation ? ' (facoltativo)' : ' *'}`;
    get('messaggio').placeholder = documentation ? 'Documenti o informazioni aziendali richiesti…' : 'Tipo di edificio, impianto da realizzare o problema da risolvere…';
  }
  updateContext();
  get('servizio').addEventListener('change', updateContext);

  function fileError() {
    const file = get('allegato').files[0];
    if (!file) return '';
    if (file.size > 10 * 1024 * 1024) return 'Scegli un file di dimensione inferiore o uguale a 10 MB.';
    if (!/\.(pdf|jpe?g|png|webp)$/i.test(file.name)) return 'Scegli un file PDF, JPG, PNG o WebP.';
    return '';
  }

  const contactMissing = 'Indica almeno un recapito: email oppure telefono.';
  // The missing contact is one error of the fieldset, reported once and reached through the email field.
  const target = name => name === 'recapito' ? 'email' : name;
  const invalidNames = list => new Set(list.flatMap(([name]) => name === 'recapito' ? ['email', 'telefono'] : [name]));

  function errors() {
    const result = [];
    if (!text('nome')) result.push(['nome', 'Inserisci nome e cognome.']);
    if (get('comune').required && !text('comune')) result.push(['comune', 'Indica il comune in cui si trova l’immobile.']);
    if (!text('email') && !text('telefono')) result.push(['recapito', contactMissing]);
    if (text('email') && !get('email').validity.valid) result.push(['email', 'Controlla il formato dell’indirizzo email.']);
    if (text('telefono') && (!/^[+()\d\s./-]+$/.test(text('telefono')) || text('telefono').replace(/\D/g, '').length < 6)) result.push(['telefono', 'Controlla il numero di telefono, incluso il prefisso.']);
    if (!text('messaggio')) result.push(['messaggio', 'Descrivi brevemente l’intervento da realizzare o il problema da risolvere.']);
    if (fileError()) result.push(['allegato', fileError()]);
    return result;
  }

  function showFieldErrors(list) {
    const invalid = invalidNames(list);
    Object.keys(labels).forEach(name => {
      const error = list.find(item => item[0] === name);
      const message = document.getElementById(`${name}-error`);
      get(name).setAttribute('aria-invalid', String(invalid.has(name)));
      if (message) { message.textContent = error?.[1] || ''; message.hidden = !error; }
    });
    const missing = list.some(([name]) => name === 'recapito');
    const channelError = document.getElementById('recapito-error');
    channelError.textContent = missing ? contactMissing : '';
    channelError.hidden = !missing;
  }

  // Bring the error summary into view below the sticky header, then focus the first field without a second jump.
  // When summary and field do not fit together, the field and its label take priority.
  function revealSummary(name) {
    const header = document.querySelector('[data-header]');
    const bar = document.querySelector('.mobile-contact');
    const stuck = header ? header.offsetHeight + Math.min(parseFloat(getComputedStyle(header).top) || 0, 0) : 0;
    const covered = bar && getComputedStyle(bar).position === 'fixed' ? bar.offsetHeight : 0;
    const input = get(target(name));
    const box = input.closest(name === 'recapito' ? 'fieldset' : '.field') || input;
    const from = summary.getBoundingClientRect().top;
    const fits = box.getBoundingClientRect().bottom - from <= innerHeight - stuck - 24 - covered - 16;
    const top = (fits ? from : box.getBoundingClientRect().top) + window.scrollY - stuck - 24;
    window.scrollTo({ top: Math.max(0, top), behavior: window.siteMotion?.reduced() ? 'auto' : 'smooth' });
    input.focus({ preventScroll: true });
  }

  function appendDetail(list, label, value) {
    if (!value) return;
    const row = document.createElement('div');
    const term = document.createElement('dt');
    const definition = document.createElement('dd');
    term.textContent = label;
    definition.textContent = value;
    row.append(term, definition);
    list.append(row);
  }

  form.addEventListener('submit', event => {
    event.preventDefault();
    attempted = true;
    const list = errors();
    showFieldErrors(list);
    summary.replaceChildren();
    summary.hidden = list.length === 0;
    if (list.length) {
      const intro = document.createElement('p');
      intro.textContent = `Per rivedere la richiesta, controlla ${list.length === 1 ? 'il campo indicato' : 'i campi indicati'}.`;
      const ul = document.createElement('ul');
      list.forEach(([name, message]) => {
        const li = document.createElement('li');
        const link = document.createElement('a');
        link.href = `#${target(name)}`;
        link.textContent = message;
        li.append(link);
        ul.append(li);
      });
      summary.append(intro, ul);
      revealSummary(list[0][0]);
      return;
    }
    const details = review.querySelector('[data-review-details]');
    details.replaceChildren();
    appendDetail(details, 'Profilo', text('profilo'));
    appendDetail(details, 'Servizio', text('servizio') || 'Da valutare insieme');
    ['nome', 'azienda', 'comune', 'email', 'telefono', 'messaggio'].forEach(name => appendDetail(details, labels[name], text(name)));
    const file = get('allegato').files[0];
    if (file) appendDetail(details, 'Allegato', file.name);
    // Intentionally local: no fetch, email, persistent storage or file reads.
    fields.hidden = true;
    review.hidden = false;
    review.focus({ preventScroll: true });
    review.scrollIntoView({ behavior: window.siteMotion?.reduced() ? 'auto' : 'smooth', block: 'center' });
  });

  form.addEventListener('input', () => {
    if (!attempted) return;
    summary.hidden = true;
    const remaining = invalidNames(errors());
    // Clear corrected messages without announcing new errors on every key press.
    form.querySelectorAll('[aria-invalid="true"]').forEach(input => {
      if (remaining.has(input.name)) return;
      input.setAttribute('aria-invalid', 'false');
      const message = document.getElementById(`${input.name}-error`);
      if (message) message.hidden = true;
    });
    if (text('email') || text('telefono')) document.getElementById('recapito-error').hidden = true;
  });

  get('allegato').addEventListener('change', () => {
    const file = get('allegato').files[0];
    fileStatus.textContent = file ? `${file.name} — ${(file.size / 1024 / 1024).toFixed(2).replace('.', ',')} MB` : 'Nessun file selezionato';
    const error = fileError();
    const message = document.getElementById('allegato-error');
    message.textContent = error;
    message.hidden = !error;
    get('allegato').setAttribute('aria-invalid', String(Boolean(error)));
  });

  form.querySelector('[data-form-again]').addEventListener('click', () => {
    review.hidden = true;
    fields.hidden = false;
    get('nome').focus();
  });
})();
