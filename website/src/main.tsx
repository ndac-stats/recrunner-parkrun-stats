import React from 'react';
import ReactDOM from 'react-dom/client';
import { HashRouter, Route, Routes } from 'react-router-dom';
import { useEffect, useState } from 'react';

import SiteLayout from './components/SiteLayout';
import { ErrorState, Loading } from './components/Status';

import Overview from './pages/Overview';
import Milestones from './pages/Milestones';
import Results from './pages/Results';

import { loadResults } from './lib/data';

import type { ParkrunResult } from './types';

import './styles.css';

function App() {
  const [results, setResults] = useState<ParkrunResult[] | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    loadResults().then(setResults).catch(e => setError(e instanceof Error ? e.message : String(e)));
  }, []);

  return <HashRouter>
    <Routes>
      <Route element={<SiteLayout/>}>
        {error ? <Route path="*" element={<ErrorState message={error}/>}/> : !results ? <Route path="*" element={<Loading/>}/> : <>
          <Route path="/" element={<Overview results={results}/>}/>
          <Route path="/milestones" element={<Milestones results={results}/>}/>
          <Route path="/results" element={<Results results={results}/>}/>
          <Route path="*" element={<h1>Page not found</h1>}/>
        </>}
      </Route>
    </Routes>
  </HashRouter>;
}

ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
