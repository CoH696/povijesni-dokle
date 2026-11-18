/*
 Povijesni Dokle? – prepoznavanje odgovora (ES module, bez vanjskih ovisnosti).
 Učitati JSON iz odgovori_vukovar_dokle.json i pozvati:
 const result = checkAnswer(data, 9, 'Skabranja');
 // { status:'accepted', canonical:'Škabrnja', kind:'alias' }
 
 Statusi:
 - accepted: točno podudaranje, unaprijed zadan alias ili vrlo siguran jednoslovni tipfeler;
 - review: sličan odgovor, više kandidata ili odgovor izvan baze – nastavnik odlučuje;
 - blank: prazno polje;
 - invalid_question: pogrešan ID.

 Kanonski odgovori služe kao jedinstveni ključevi za izračun rijetkosti.
 Nikada NE dodjeljujte 0 bodova odgovoru s oznakom 'review' bez nastavničke odluke.
*/
export function normalizeAnswer(value) {
  return String(value ?? '')
    .trim()
    .toLocaleLowerCase('hr')
    .replace(/đ/g, 'd')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9 ]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function editDistance(a, b, maxDistance = 2) {
  if (Math.abs(a.length - b.length) > maxDistance) return maxDistance + 1;
  let prev = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    const next = [i];
    let rowMinimum = i;
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      const d = Math.min(prev[j] + 1, next[j - 1] + 1, prev[j - 1] + cost);
      next.push(d);
      rowMinimum = Math.min(rowMinimum, d);
    }
    if (rowMinimum > maxDistance) return maxDistance + 1;
    prev = next;
  }
  return prev[b.length];
}

export function checkAnswer(data, questionId, rawInput) {
  const id = String(questionId);
  const question = [...(data.questions ?? []), ...(data.single_answer_bonus ?? [])]
    .find(q => String(q.id) === id);
  if (!question) return { status: 'invalid_question', questionId: id };
  const input = normalizeAnswer(rawInput);
  if (!input) return { status: 'blank', questionId: id };

  const variants = [];
  for (const answer of question.answers) {
    for (const form of [answer.canonical, ...(answer.aliases ?? [])]) {
      const value = normalizeAnswer(form);
      if (value) variants.push({ canonical: answer.canonical, value, form });
    }
  }
  // Najprije točno podudaranje nakon uklanjanja dijakritike, interpunkcije i razlika velikih slova.
  const direct = [...new Set(variants.filter(v => v.value === input).map(v => v.canonical))];
  if (direct.length === 1) {
    const canonical = direct[0];
    return { status: 'accepted', questionId: id, canonical, kind: normalizeAnswer(canonical) === input ? 'exact' : 'alias' };
  }
  if (direct.length > 1) return { status: 'review', questionId: id, reason: 'ambiguous_alias', suggestions: direct };

  // Približno podudaranje samo za tipfelere, bez prihvaćanja podnizova.
  // Dugi izrazi: do 2 uređivanja -> sugerirati, ali ne uvijek automatski prihvatiti.
  const allowance = input.length >= 8 ? 2 : input.length >= 5 ? 1 : 0;
  const ranked = new Map();
  if (allowance > 0) {
    for (const v of variants) {
      if (Math.abs(v.value.length - input.length) > allowance) continue;
      const d = editDistance(input, v.value, allowance);
      if (d > allowance) continue;
      const prev = ranked.get(v.canonical);
      if (prev === undefined || d < prev) ranked.set(v.canonical, d);
    }
  }
  const candidates = [...ranked.entries()]
    .map(([canonical, distance]) => ({ canonical, distance }))
    .sort((a, b) => a.distance - b.distance || a.canonical.localeCompare(b.canonical, 'hr'));
  if (!candidates.length) {
    return { status: 'review', questionId: id, reason: 'not_in_database', suggestions: [] };
  }
  const tied = candidates.filter(x => x.distance === candidates[0].distance);
  // Automatski prolazi jedino nedvosmislen tipfeler s jednim pomakom na 7+ znakova.
  if (tied.length === 1 && candidates[0].distance === 1 && input.length >= 7) {
    return { status: 'accepted', questionId: id, canonical: candidates[0].canonical, kind: 'one_character_typo' };
  }
  return {
    status: 'review', questionId: id,
    reason: tied.length > 1 ? 'ambiguous_typo' : 'possible_typo',
    suggestions: candidates.slice(0, 3)
  };
}

// Točan kanonski odgovor iz review-statusa može naknadno potvrditi nastavnik.
// Tek tada podatke koristite za zbrajanje učestalosti i dodjelu bodova.
export function rarityPoints(frequency) {
  if (frequency === 1) return 10;
  if (frequency >= 2 && frequency <= 3) return 7;
  if (frequency >= 4 && frequency <= 5) return 5;
  if (frequency >= 6) return 3;
  return 0;
}
