import type { Milestone, ParkrunResult } from '../types';

// local sample data
const DATA_URL = `${import.meta.env.BASE_URL}../data/results.json`;
// GitHub based data
// const DATA_URL = 'https://raw.githubusercontent.com/ndac-stats/recrunner-parkrun-stats/main/data/results.json';

console.log(`Using data from ${DATA_URL}`)

const RUN_MILESTONES = new Set([50, 100, 250, 500, 1000, 1500, 2000]);

function first(obj: Record<string, unknown>, keys: string[]): unknown {
  for (const key of keys) if (obj[key] !== undefined && obj[key] !== null && obj[key] !== '') return obj[key];
  return undefined;
}
function asString(value: unknown): string { return value == null ? '' : String(value); }
function asBoolean(value: unknown): boolean {
  if (typeof value === 'boolean') return value;
  if (typeof value === 'number') return value !== 0;
  return ['true', 'yes', '1', 'y'].includes(String(value ?? '').trim().toLowerCase());
}
function asNumber(value: unknown): number | undefined {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string') { const n = Number(value.replace(/[^0-9.]/g, '')); return Number.isFinite(n) ? n : undefined; }
  return undefined;
}
function parseDate(value: unknown): string {
  if (!value) return '';
  const raw = String(value);
  const d = new Date(raw);
  return Number.isNaN(d.getTime()) ? raw : d.toISOString().slice(0, 10);
}
function secondsFromTime(value: unknown): number | undefined {
  if (typeof value !== 'string') return undefined;
  const parts = value.trim().split(':').map(Number);
  if (parts.some(Number.isNaN)) return undefined;
  return parts.reduce((total, part) => total * 60 + part, 0);
}
function unwrap(payload: unknown): Record<string, unknown>[] {
  if (Array.isArray(payload)) return payload as Record<string, unknown>[];
  if (!payload || typeof payload !== 'object') return [];
  const obj = payload as Record<string, unknown>;
  for (const key of ['results', 'data', 'items', 'records']) if (Array.isArray(obj[key])) return obj[key] as Record<string, unknown>[];
  return [];
}

export function normaliseResults(payload: unknown): ParkrunResult[] {
  return unwrap(payload).map((row, index) => {
    const athlete = asString(first(row, ['athlete', 'athlete_name', 'name', 'runner', 'parkrunner', 'participant']));
    const time = asString(first(row, ['time', 'result', 'finish_time', 'elapsed_time']));
    return {
      id: asString(first(row, ['id', 'result_id'])) || `${athlete}-${first(row, ['date', 'run_date'])}-${index}`,
      athlete,
      athleteId: asString(first(row, ['athlete_id', 'parkrun_id', 'athleteId', 'id_parkrunner'])) || undefined,
      event: asString(first(row, ['event', 'event_name', 'location', 'parkrun', 'venue'])),
      date: parseDate(first(row, ['date', 'run_date', 'event_date', 'Date'])),
      runNumber: asNumber(first(row, ['run_number', 'runNumber', 'number_of_runs', 'total_runs'])),
      position: asNumber(first(row, ['position', 'pos', 'overall_position', 'finish_position'])),
      time,
      timeSeconds: asNumber(first(row, ['time_seconds', 'seconds'])) ?? secondsFromTime(time),
      ageGrade: first(row, ['age_grade', 'ageGrade', 'agegrade']) as string | number | undefined,
      pb: asBoolean(first(row, ['pb', 'is_pb', 'personal_best'])),
      milestone: asString(first(row, ['milestone', 'milestones', 'achievement'])) || undefined,
      milestoneType: asString(first(row, ['milestone_type', 'milestoneType'])) || undefined,
      milestoneName: asString(first(row, ['milestone_name', 'milestoneName'])) || undefined,
      volunteerMilestone: asString(first(row, ['volunteer_milestone', 'volunteerMilestone'])) || undefined,
      raw: row,
    };
  }).filter(r => r.athlete && r.date);
}

export function extractMilestones(results: ParkrunResult[]): Milestone[] {
  const output: Milestone[] = [];
  for (const r of results) {
    const explicit = r.milestoneName || r.milestone;
    if (explicit) {
      const category = /volunteer/i.test(`${r.milestoneType ?? ''} ${explicit}`) ? 'volunteer' : /run|club|parkrun/i.test(`${r.milestoneType ?? ''} ${explicit}`) ? 'run' : 'other';
      const title = Array.isArray(explicit) ? explicit.join(', ') : String(explicit);
      output.push({ id: `${r.id}-milestone`, athlete: r.athlete, athleteId: r.athleteId, date: r.date, title, category, event: r.event });
      continue;
    }
    if (r.volunteerMilestone) output.push({ id: `${r.id}-volunteer`, athlete: r.athlete, athleteId: r.athleteId, date: r.date, title: r.volunteerMilestone, category: 'volunteer', event: r.event });
    // Optional fallback: calculate run milestones when a cumulative run count is present in each result row.
    if (r.runNumber && RUN_MILESTONES.has(r.runNumber)) output.push({ id: `${r.id}-run`, athlete: r.athlete, athleteId: r.athleteId, date: r.date, title: `${r.runNumber} parkruns`, category: 'run', event: r.event });
  }
  return output;
}

// local loadResults
export async function loadResults(): Promise<ParkrunResult[]> {
  const response = await fetch(DATA_URL, { cache: 'no-store' });
  if (!response.ok) throw new Error(`Could not load ${DATA_URL} (HTTP ${response.status}).`);
  return normaliseResults(await response.json());
}

// GitHub based loadResults
// export async function loadResults(): Promise<ParkrunResult[]> {
//   const response = await fetch(DATA_URL);

//   if (!response.ok) {
//     throw new Error('Unable to load parkrun results');
//   }

//   return response.json();
// }

export function monthKey(date: string): string { return date.slice(0, 7); }
export function formatDate(date: string): string {
  const parsed = new Date(`${date}T00:00:00`);
  return Number.isNaN(parsed.getTime()) ? date : parsed.toLocaleDateString('en-AU', { day: 'numeric', month: 'short', year: 'numeric' });
}
