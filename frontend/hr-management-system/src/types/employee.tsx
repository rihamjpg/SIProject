export interface Employee {
  id_employe: number;
  matricule: string;
  nom: string;
  prenom: string;
  email_pro: string;
  email_perso: string;
  date_naissance: string;
  date_embauche: string;
  adresse: string;
  telephone_mobile: string;
  telephone_fixe: string | null;
  numero_securite_sociale: string;
  situation_familiale: string;
  nombre_enfants: number;
  poste_occupe: string;
  niveau_etudes: string;
  diplome: string;
  service_name: string;
  id_service: number;
  actif: boolean;
  photo: string | null;
  piece_identite: string | null;
  competences: any[];
  maladies: any | null;
}

export type CreateEmployeeDTO = Omit<
  Employee,
  | "id_employe"
  | "service_name"
  | "photo"
  | "piece_identite"
  | "competences"
  | "maladies"
>;

export type UpdateEmployeeDTO = Partial<CreateEmployeeDTO>;
