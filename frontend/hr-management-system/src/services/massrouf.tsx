import api from "./api";
import { PaginatedMassrouf } from "@/types/massrouf";

export const massroufService = {
  getAll: async (): Promise<PaginatedMassrouf> => {
    const { data } = await api.get("/massroufs/");
    return data;
  },
};
