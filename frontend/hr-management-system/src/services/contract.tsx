import api from "./api";
import { PaginatedContracts } from "@/types/contract";

export const contractService = {
  getAll: async (page: number = 1): Promise<PaginatedContracts> => {
    const { data } = await api.get(`/contracts/?page=${page}`);
    return data;
  },
};
