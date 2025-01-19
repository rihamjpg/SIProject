export interface Application {
  id: number;
  candidat_name: string;
  poste: string;
  date_candidature: string;
  statut: string;
  notes_recruteur: string;
  evaluation_entretien: string;
  date_entretien: string | null;
  resultat_entretien: string;
  documents_valides: boolean;
  decision_finale: string;
  candidat: number;
  recrutement: number;
}

export interface PaginatedApplications {
  count: number;
  next: string | null;
  previous: string | null;
  results: Application[];
}
