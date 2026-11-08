// Remove only explicitly marked ads from the top-level aweme_list. Preserve the
// original JSON bytes elsewhere, including integer IDs beyond JS safe range.
export default async function (ctx) {
  if (!ctx.response || ctx.response.status !== 200 || !ctx.response.body) return;
  try {
    const text = await ctx.response.text();
    const data = JSON.parse(text);
    if (!data || Array.isArray(data) || typeof data !== 'object' || !Array.isArray(data.aweme_list)) return;

    // Locate the top-level array without serializing the surrounding response.
    let i = 0;
    const ws = () => { while (/\s/.test(text[i] || '')) i++; };
    function stringEnd() {
      i++;
      while (i < text.length) {
        if (text[i] === '\\') { i += 2; continue; }
        if (text[i++] === '"') return;
      }
    }
    function valueEnd() {
      ws();
      if (text[i] === '"') { stringEnd(); return; }
      if (text[i] === '{' || text[i] === '[') {
        const stack = [text[i++] === '{' ? '}' : ']'];
        while (stack.length && i < text.length) {
          const c = text[i];
          if (c === '"') stringEnd();
          else if (c === '{' || c === '[') { stack.push(c === '{' ? '}' : ']'); i++; }
          else if (c === stack[stack.length - 1]) { stack.pop(); i++; }
          else i++;
        }
        return;
      }
      while (i < text.length && !/[\s,}\]]/.test(text[i])) i++;
    }
    ws(); i++; // opening object
    while (i < text.length) {
      ws(); if (text[i] === '}') return;
      const start = i; stringEnd();
      const key = JSON.parse(text.slice(start, i));
      ws(); i++; ws(); // colon
      if (key === 'aweme_list' && text[i] === '[') {
        const arrayStart = i++;
        const kept = [];
        let removed = 0;
        ws();
        while (text[i] !== ']') {
          const itemStart = i;
          valueEnd();
          const raw = text.slice(itemStart, i);
          const item = JSON.parse(raw);
          const ad = item && typeof item === 'object' && !Array.isArray(item) &&
            (item.is_ads === true || item.is_ads === 1 || item.is_ads === '1' ||
             item.is_ad === true || item.is_ad === 1 || item.is_ad === '1');
          if (ad) removed++; else kept.push(raw);
          ws(); if (text[i] === ',') { i++; ws(); } else break;
        }
        if (!removed) return;
        return { body: text.slice(0, arrayStart) + '[' + kept.join(',') + ']' + text.slice(i + 1) };
      }
      valueEnd(); ws();
      if (text[i] === ',') i++; else return;
    }
  } catch (_) {
    // Unknown, non-JSON, or unreadable responses pass through unchanged.
  }
}
