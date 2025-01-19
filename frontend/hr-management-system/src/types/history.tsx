export interface HistoryEntry {
  id: number;
  model_name: string;
  instance_id: number;
  utilisateur: string;
  date_modification: string;
  modifications: Record<string, string>;
}

export interface PaginatedHistory {
  count: number;
  next: string | null;
  previous: string | null;
  results: HistoryEntry[];
}
