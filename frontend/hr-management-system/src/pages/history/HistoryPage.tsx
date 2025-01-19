import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { History } from "lucide-react";
import { historyService } from "@/services/history";

export const HistoryPage = () => {
  const { data, isLoading } = useQuery({
    queryKey: ["history"],
    queryFn: historyService.getAll,
  });

  if (isLoading) return <div>Chargement...</div>;

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Historique des modifications</h1>

      <div className="space-y-8">
        {data?.results.map((entry) => (
          <div key={entry.id} className="flex gap-4">
            <div className="mt-1">
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <History className="w-4 h-4 text-primary" />
              </div>
            </div>
            <div className="flex-1 space-y-2">
              <div className="flex items-center justify-between">
                <div className="font-medium">
                  {entry.model_name} #{entry.instance_id}
                </div>
                <time className="text-sm text-gray-500">
                  {format(
                    new Date(entry.date_modification),
                    "dd MMMM yyyy à HH:mm",
                    {
                      locale: fr,
                    }
                  )}
                </time>
              </div>
              <div className="text-sm text-gray-600">
                par {entry.utilisateur}
              </div>
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                {Object.entries(entry.modifications).map(([field, change]) => (
                  <div key={field} className="text-sm">
                    <span className="font-medium">{field}:</span> {change}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
