import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { employeeService } from "@/services/employees";
import { Employee } from "@/types/employee";

export const useEmployees = () => {
  const queryClient = useQueryClient();

  const employees = useQuery({
    queryKey: ["employees"],
    queryFn: employeeService.getAll,
  });

  const createEmployee = useMutation({
    mutationFn: employeeService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employees"] });
    },
  });

  const updateEmployee = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Employee> }) =>
      employeeService.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employees"] });
    },
  });

  const deleteEmployee = useMutation({
    mutationFn: employeeService.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employees"] });
    },
  });

  return {
    employees,
    createEmployee,
    updateEmployee,
    deleteEmployee,
  };
};
