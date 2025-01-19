export interface ServiceDistribution {
  id_service__nom_service: string;
  count: number;
}

export interface EducationDistribution {
  niveau_etudes: string;
  count: number;
}

export interface AnalyticsData {
  total: number;
  by_service: ServiceDistribution[];
  by_education: EducationDistribution[];
}
