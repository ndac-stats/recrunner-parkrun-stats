import { NavLink, Outlet } from 'react-router-dom';
import { Award, Footprints, Home, Menu, Search } from 'lucide-react';
import { useState } from 'react';

export default function SiteLayout() {
  const [menuOpen, setMenuOpen] = useState(false);
  const links = [
    { to: '/', label: 'Overview', icon: Home },
    { to: '/milestones', label: 'Milestones', icon: Award },
    { to: '/results', label: 'Results', icon: Search },
  ];
  return <div className="app-shell">
    <header className="topbar">
      <NavLink to="/" className="brand"><span className="brand-mark"><Footprints size={23}/></span><span>parkrun <b>club stats</b></span></NavLink>
      <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle navigation"><Menu/></button>
      <nav className={menuOpen ? 'nav open' : 'nav'}>{links.map(({to,label,icon:Icon}) => <NavLink key={to} to={to} end={to === '/'} onClick={() => setMenuOpen(false)}><Icon size={17}/>{label}</NavLink>)}</nav>
    </header>
    <main className="main"><Outlet/></main>
    <footer>Club parkrun statistics <span>·</span> Data refreshed from the results repository</footer>
  </div>;
}
