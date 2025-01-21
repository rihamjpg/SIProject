import api from "./api";
import {
  Employee,
  CreateEmployeeDTO,
  UpdateEmployeeDTO,
} from "@/types/employee";

export const employeeService = {
  getAll: async () => {
    console.log("getAll");
    const { data } = await api.get<Employee[]>("/employees/");
    return data;
  },

  getById: async (id: number) => {
    const { data } = await api.get<Employee>(`/employees/${id}/`);
    return data;
  },

  create: async (employee: CreateEmployeeDTO) => {
    console.log(employee);
    const { data } = await api.post<Employee>("/employees/", employee);
    return data;
  },

  update: async (id: number, employee: UpdateEmployeeDTO) => {
    const { data } = await api.patch<Employee>(`/employees/${id}/`, employee);
    return data;
  },

  delete: async (id: number) => {
    console.log("delete id ", id);
    await api.delete(`/employees/${id}/`);
  },
};
