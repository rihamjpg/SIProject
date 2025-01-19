export interface Leave {
  id: number;
  employe_name: string;
  date_debut: string;
  date_fin: string;
  type_conge: "ANNUEL" | "MALADIE" | "MATERNITE";
  statut: "DEMANDE" | "APPROUVE" | "REFUSE";
  date_demande: string;
  date_reponse: string | null;
  nb_jours: number;
  justification: string;
  document_justificatif: string | null;
  solde_restant: number;
  solde_deductible: boolean;
  employe: number;
  valideur: number | null;
}

export interface PaginatedLeaves {
  count: number;
  next: string | null;
  previous: string | null;
  results: Leave[];
}
