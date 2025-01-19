export interface Skill {
  id: number;
  employes_count: number;
  nom: string;
  description: string;
  employes: number[];
}

export interface PaginatedSkills {
  count: number;
  next: string | null;
  previous: string | null;
  results: Skill[];
}
