import { useQuery } from "@tanstack/react-query";
import { serviceService } from "@/services/service";

export const useServices = () => {
  return useQuery({
    queryKey: ["services"],
    queryFn: serviceService.getAll,
  });
};
