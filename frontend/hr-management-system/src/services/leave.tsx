import api from "./api";
import { PaginatedLeaves } from "@/types/leave";

export const leaveService = {
  getAll: async (): Promise<PaginatedLeaves> => {
    const { data } = await api.get("/leaves/");
    return data;
  },
};
