import { useMemo, useState } from 'react';
import { Search, X } from 'lucide-react';
import type { ParkrunResult } from '../types';
import { formatDate } from '../lib/data';
import { Empty } from '../components/Status';

export default function Results({ results }: { results: ParkrunResult[] }) {
  const [query, setQuery] = useState('');
  const [event, setEvent] = useState('all');
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [pbOnly, setPbOnly] = useState(false);
  const [page, setPage] = useState(1);
  const pageSize = 30;
  const events = useMemo(() => [...new Set(results.map(r => r.event).filter(Boolean))].sort(), [results]);
  const filtered = useMemo(() => results.filter(r => {
    const q = query.trim().toLowerCase();
    const matchesQuery = !q || [r.athlete, r.event, r.time, r.position?.toString(), r.athleteId].some(v => String(v ?? '').toLowerCase().includes(q));
    return matchesQuery && (event === 'all' || r.event === event) && (!from || r.date >= from) && (!to || r.date <= to) && (!pbOnly || r.pb);
  }).sort((a,b) => b.date.localeCompare(a.date) || a.athlete.localeCompare(b.athlete)), [results, query, event, from, to, pbOnly]);
  const pages = Math.max(1, Math.ceil(filtered.length / pageSize));
  const visible = filtered.slice((page-1)*pageSize, page*pageSize);
  function reset() { setQuery(''); setEvent('all'); setFrom(''); setTo(''); setPbOnly(false); setPage(1); }
  return <>
    <div className="page-heading"><div><p className="eyebrow">THE FULL HISTORY</p><h1>Results explorer</h1><p>Search, filter and explore every athlete result in the dataset.</p></div><div className="heading-icon"><Search size={34}/></div></div>
    <section className="filter-panel"><label className="field search-field"><span>Search athlete, event or time</span><div className="input-with-icon"><Search size={17}/><input value={query} onChange={e => {setQuery(e.target.value);setPage(1)}} placeholder="e.g. Alex, Torrens, 24:30"/></div></label><label className="field"><span>Event</span><select value={event} onChange={e => {setEvent(e.target.value);setPage(1)}}><option value="all">All events</option>{events.map(e => <option key={e}>{e}</option>)}</select></label><label className="field"><span>From</span><input type="date" value={from} onChange={e => {setFrom(e.target.value);setPage(1)}}/></label><label className="field"><span>To</span><input type="date" value={to} onChange={e => {setTo(e.target.value);setPage(1)}}/></label><label className="check-field"><input type="checkbox" checked={pbOnly} onChange={e => {setPbOnly(e.target.checked);setPage(1)}}/> Personal bests only</label><button className="text-button" onClick={reset}><X size={15}/> Clear filters</button></section>
    <div className="table-toolbar"><strong>{filtered.length.toLocaleString('en-AU')} results</strong><span>Showing {filtered.length ? (page-1)*pageSize+1 : 0}–{Math.min(page*pageSize, filtered.length)}</span></div>
    <div className="table-wrap"><table><thead><tr><th>Date</th><th>Athlete</th><th>Event</th><th>Time</th><th>Position</th><th>Age grade</th><th>PB</th></tr></thead><tbody>{visible.map(r => <tr key={r.id}><td>{formatDate(r.date)}</td><td className="athlete-cell">{r.athlete}</td><td>{r.event || '—'}</td><td className="time-cell">{r.time || '—'}</td><td>{r.position ?? '—'}</td><td>{r.ageGrade != null ? `${r.ageGrade}${String(r.ageGrade).includes('%') ? '' : '%'}` : '—'}</td><td>{r.pb ? <span className="pb-badge">PB</span> : '—'}</td></tr>)}</tbody></table>{visible.length === 0 && <Empty/>}</div>
    {filtered.length > pageSize && <div className="pagination"><button disabled={page===1} onClick={() => setPage(page-1)}>Previous</button><span>Page {page} of {pages}</span><button disabled={page===pages} onClick={() => setPage(page+1)}>Next</button></div>}
  </>;
}
