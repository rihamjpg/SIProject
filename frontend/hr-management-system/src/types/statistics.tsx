export interface RecruitmentStats {
  total_active: number;
  by_service: { service__nom_service: string; count: number }[];
  urgent_posts: number;
}

export interface LeaveStats {
  total_leaves: number;
  by_type: { type_conge: string; count: number }[];
}

export interface EvaluationStats {
  average_score: { note_globale__avg: number };
  evaluations_count: number;
  by_period: { periode: string; count: number }[];
}

export interface AttendanceStats {
  present_today: number;
  absent_today: number;
  monthly_hours: { heures_travaillees__sum: number };
}
