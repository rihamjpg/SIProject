import api from "@/services/auth";
import { Service } from "@/types/service";

export const serviceService = {
  getAll: async (): Promise<Service[]> => {
    const response = await api.get("/services/");
    return response.data;
  },
};
