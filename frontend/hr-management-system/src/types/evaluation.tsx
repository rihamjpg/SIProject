export interface Evaluation {
  id: number;
  employe_name: string;
  evaluateur_name: string;
  date_evaluation: string;
  note_globale: number;
  commentaires: string;
  periode: string;
  objectifs_fixes: string;
  objectifs_atteints: string;
  axes_amelioration: string;
  besoins_formation: string;
  entretien_realise: boolean;
  document_evaluation: string | null;
  date_prochaine_evaluation: string;
  employe: number;
  evaluateur: number;
}

export interface PaginatedEvaluations {
  count: number;
  next: string | null;
  previous: string | null;
  results: Evaluation[];
}
