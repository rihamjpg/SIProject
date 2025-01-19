export interface Attendance {
  id: number;
  employe_name: string;
  date_pointage: string;
  heure_arrivee: string;
  heure_depart: string;
  present: boolean;
  conge: boolean;
  justification_absence: string;
  justificatif: string | null;
  heures_travaillees: string;
  heures_supplementaires: string;
  jour_ferie: boolean;
  commentaire: string;
  employe: number;
  validateur: number | null;
}

export interface PaginatedAttendance {
  count: number;
  next: string | null;
  previous: string | null;
  results: Attendance[];
}
