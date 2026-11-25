export interface ParkrunRunner {
  parkrunId: string;
  firstName: string;
  lastName: string;
  displayName: string;
  parkrunJoinDate: string;
  active: boolean;
}


export interface ParkrunResult {
  parkrunId: string;
  event: string;
  runDate: string;
  runNumber: number;
  position: number;
  timeSeconds: number;
  ageGrade: number;
  pb: boolean;
}
