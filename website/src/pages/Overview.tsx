import { Link } from 'react-router-dom';
import { Award, CalendarDays, Footprints, Search, TrendingUp } from 'lucide-react';
import type { ParkrunResult } from '../types';
import { formatDate } from '../lib/data';

export default function Overview({ results }: { results: ParkrunResult[] }) {
  const athletes = new Set(results.map(r => r.athlete)).size;
  const events = new Set(results.map(r => r.event).filter(Boolean)).size;
  const latest = [...results].sort((a,b) => b.date.localeCompare(a.date))[0];
  const pbs = results.filter(r => r.pb).length;
  return <>
    <section className="hero"><div><p className="eyebrow">YOUR CLUB · YOUR RESULTS</p><h1>Every run tells<br/><span>a story.</span></h1><p className="hero-copy">Explore athlete performances, celebrate milestones and discover the stories behind your club's parkrun results.</p><div className="hero-actions"><Link className="button yellow" to="/results"><Search size={17}/> Explore results</Link><Link className="button outline" to="/milestones"><Award size={17}/> View milestones</Link></div></div><div className="hero-art"><div className="art-circle"><Footprints size={94} strokeWidth={1.2}/></div><span className="art-tag">SATURDAY<br/>9:00 AM</span></div></section>
    <section className="stats-grid">
      <div className="stat-card"><span className="stat-icon"><Footprints/></span><span className="stat-label">Recorded results</span><strong>{results.length.toLocaleString('en-AU')}</strong></div>
      <div className="stat-card"><span className="stat-icon"><span>♙</span></span><span className="stat-label">Athletes</span><strong>{athletes.toLocaleString('en-AU')}</strong></div>
      <div className="stat-card"><span className="stat-icon"><CalendarDays/></span><span className="stat-label">Events</span><strong>{events.toLocaleString('en-AU')}</strong></div>
      <div className="stat-card"><span className="stat-icon"><TrendingUp/></span><span className="stat-label">Personal bests</span><strong>{pbs.toLocaleString('en-AU')}</strong></div>
    </section>
    <section className="section-heading"><div><p className="eyebrow">KEEP EXPLORING</p><h2>Find your next insight</h2></div></section>
    <div className="feature-grid">
      <Link to="/milestones" className="feature-card"><span className="feature-icon"><Award/></span><h3>Milestone moments</h3><p>See which athletes reached a parkrun milestone in any month.</p><span className="feature-link">Explore milestones →</span></Link>
      <Link to="/results" className="feature-card"><span className="feature-icon"><Search/></span><h3>Results explorer</h3><p>Search and filter the full results history by athlete, event and date.</p><span className="feature-link">Search results →</span></Link>
      <div className="feature-card muted-card"><span className="feature-icon"><TrendingUp/></span><h3>More insights coming</h3><p>Event popularity, athlete progression and more can be added as new pages.</p><span className="feature-link">Coming soon</span></div>
    </div>
    {latest && <p className="data-note">Latest result in this dataset: <strong>{formatDate(latest.date)}</strong></p>}
  </>;
}
