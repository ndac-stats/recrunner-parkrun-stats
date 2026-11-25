import type { ReactNode } from 'react';
export function Loading() { return <div className="state">Loading results…</div>; }
export function ErrorState({ message }: { message: string }) { return <div className="state error"><strong>Unable to load results</strong><p>{message}</p><p>Check that <code>public/data/results.json</code> exists and contains valid JSON.</p></div>; }
export function Empty({ children = 'No matching results found.' }: { children?: ReactNode }) { return <div className="empty">{children}</div>; }
