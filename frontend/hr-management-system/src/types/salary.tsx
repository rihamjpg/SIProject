export interface Salary {
  id: number;
  employe_name: string;
  date_paiement: string;
  salaire_base: string;
  prime_rendement: string;
  prime_anciennete: string;
  heures_supplementaires: string;
  taux_horaire_sup: string;
  indemnites: string;
  avance_salaire: string;
  justificatif: string;
  montant_final: string;
  mois: number;
  annee: number;
  mode_paiement: string;
  reference_paiement: string;
  fiche_paie_generee: boolean;
  statut_paiement: string;
  employe: number;
  contrat: number;
}

export interface PaginatedSalaries {
  count: number;
  next: string | null;
  previous: string | null;
  results: Salary[];
}
