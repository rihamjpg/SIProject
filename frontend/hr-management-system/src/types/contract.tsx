export interface Contract {
  id: number;
  employe_name: string;
  type_contrat: "CDI" | "CDD";
  date_debut: string;
  date_fin: string | null;
  date_signature: string;
  salaire_base: string;
  salaire_journalier: string;
  devise: string;
  statut: "ACTIF" | "TERMINE";
  periode_essai: boolean;
  duree_periode_essai: number;
  fin_periode_essai: string | null;
  conditions_particulieres: string;
  motif_fin: string;
  archive: boolean;
  date_archive: string | null;
  document_contrat: string | null;
  employe: number;
}

export interface PaginatedContracts {
  count: number;
  next: string | null;
  previous: string | null;
  results: Contract[];
}
