import { useMemo, useState } from 'react';
import { Award, CalendarDays } from 'lucide-react';
import type { Milestone, ParkrunResult } from '../types';
import { extractMilestones, formatDate, monthKey } from '../lib/data';
import { Empty } from '../components/Status';

export default function Milestones({ results }: { results: ParkrunResult[] }) {
  const milestones = useMemo(() => extractMilestones(results), [results]);
  const availableMonths = [...new Set(milestones.map(m => monthKey(m.date)))].sort().reverse();
  const [month, setMonth] = useState(availableMonths[0] || new Date().toISOString().slice(0,7));
  const [category, setCategory] = useState('all');
  const shown = milestones.filter(m => monthKey(m.date) === month && (category === 'all' || m.category === category)).sort((a,b) => a.date.localeCompare(b.date) || a.athlete.localeCompare(b.athlete));
  const grouped = shown.reduce<Record<string, Milestone[]>>((acc, m) => { (acc[m.date] ||= []).push(m); return acc; }, {});
  return <>
    <div className="page-heading"><div><p className="eyebrow">CELEBRATE THE ACHIEVEMENTS</p><h1>Milestone moments</h1><p>Find the athletes who reached a milestone in a particular month.</p></div><div className="heading-icon"><Award size={34}/></div></div>
    <section className="filter-panel milestone-filters"><label className="field"><span>Choose month</span><input type="month" value={month} onChange={e => setMonth(e.target.value)}/></label><label className="field"><span>Milestone type</span><select value={category} onChange={e => setCategory(e.target.value)}><option value="all">All milestones</option><option value="run">Run milestones</option><option value="volunteer">Volunteer milestones</option><option value="other">Other</option></select></label><div className="result-count"><strong>{shown.length}</strong><span>achievement{shown.length === 1 ? '' : 's'}</span></div></section>
    {shown.length === 0 ? <Empty>No milestones found for this month. If your scraper records milestones, check the supported fields in the README.</Empty> : <div className="timeline">{Object.entries(grouped).map(([date, items]) => <section className="timeline-day" key={date}><div className="timeline-date"><CalendarDays size={17}/><strong>{formatDate(date)}</strong></div><div className="milestone-list">{items.map(m => <article className="milestone-row" key={m.id}><div className="medal"><Award size={20}/></div><div className="milestone-person"><strong>{m.athlete}</strong><span>{m.event || 'parkrun'}</span></div><div className="milestone-title">{m.title}</div><span className={`pill ${m.category}`}>{m.category === 'run' ? 'Run' : m.category === 'volunteer' ? 'Volunteer' : 'Milestone'}</span></article>)}</div></section>)}</div>}
  </>;
}
