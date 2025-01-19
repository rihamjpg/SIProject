export interface Massrouf {
  id: number;
  employe_name: string;
  montant_demande: string;
  date_demande: string;
  statut: "EN_ATTENTE" | "APPROUVÉ" | "REJETÉ";
  justificatif: string | null;
  employe: number;
}

export interface PaginatedMassrouf {
  count: number;
  next: string | null;
  previous: string | null;
  results: Massrouf[];
}
