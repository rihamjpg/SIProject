import api from "./api";
import { AnalyticsData } from "@/types/analytics";

export const getAnalytics = async (): Promise<AnalyticsData> => {
  try {
    console.log("Calling analytics endpoint...");
    const response = await api.get("/analytics/dashboard/");
    console.log("Analytics response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Analytics error:", error);
    throw error;
  }
};
