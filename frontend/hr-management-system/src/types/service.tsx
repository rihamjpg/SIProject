export interface Service {
  id_service: number;
  code_service: string;
  nom_service: string;
  description: string;
  localisation: string;
  telephone: string | null;
  email_service: string;
  actif: boolean;
  date_creation: string;
  effectif_actuel: number;
  id_responsable: number | null;
}

export interface ServicesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Service[];
}

export type CreateServiceDTO = Omit<Service, "id">;
export type UpdateServiceDTO = Partial<CreateServiceDTO>;
