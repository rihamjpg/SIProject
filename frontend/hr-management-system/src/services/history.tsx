import api from "./api";
import { PaginatedHistory } from "@/types/history";

export const historyService = {
  getAll: async (): Promise<PaginatedHistory> => {
    const { data } = await api.get("/history/");
    return data;
  },
};
