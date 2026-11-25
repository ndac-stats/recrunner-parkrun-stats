export interface ParkrunResult {
  id: string;
  athlete: string;
  athleteId?: string;
  event: string;
  date: string;
  runNumber?: number;
  position?: number;
  time?: string;
  timeSeconds?: number;
  ageGrade?: string | number;
  pb?: boolean;
  milestone?: string;
  milestoneType?: string;
  milestoneName?: string;
  volunteerMilestone?: string;
  raw: Record<string, unknown>;
}

export interface Milestone {
  id: string;
  athlete: string;
  athleteId?: string;
  date: string;
  title: string;
  category: 'run' | 'volunteer' | 'other';
  event?: string;
}
