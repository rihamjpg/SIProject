import api from "./api";
import { PaginatedSkills } from "@/types/skill";

export const skillService = {
  getAll: async (): Promise<PaginatedSkills> => {
    const { data } = await api.get("/skills/");
    return data;
  },
};
