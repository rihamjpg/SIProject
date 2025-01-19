export interface Recruitment {
  id: number;
  service_name: string;
  reference_poste: string;
  titre_poste: string;
  description_poste: string;
  competences_requises: string;
  experience_requise: string;
  niveau_etudes_requis: string;
  date_publication: string;
  date_cloture: string;
  statut: "OUVERT" | "FINALISE";
  postes_disponibles: number;
  salaire_propose: string;
  type_contrat_propose: "CDI" | "CDD";
  localisation_poste: string;
  urgent: boolean;
  service: number;
}

export interface PaginatedRecruitments {
  count: number;
  next: string | null;
  previous: string | null;
  results: Recruitment[];
}
