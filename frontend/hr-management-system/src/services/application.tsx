import api from "./api";
import { PaginatedApplications } from "@/types/application";

export const applicationService = {
  getAll: async (): Promise<PaginatedApplications> => {
    const { data } = await api.get("/applications/");
    return data;
  },
};
