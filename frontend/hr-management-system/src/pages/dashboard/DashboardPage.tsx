import { useQueries } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { dashboardService } from "@/services/dashboard";
import { Loader2, Users, Clock, FileText, Star } from "lucide-react";
import {
  AttendanceStats,
  EvaluationStats,
  LeaveStats,
  RecruitmentStats,
} from "@/types/statistics";

const DashboardPage = () => {
  const results = useQueries({
    queries: [
      {
        queryKey: ["recruitmentStats"],
        queryFn: dashboardService.getRecruitmentStats,
      },
      { queryKey: ["leaveStats"], queryFn: dashboardService.getLeaveStats },
      {
        queryKey: ["evaluationStats"],
        queryFn: dashboardService.getEvaluationStats,
      },
      {
        queryKey: ["attendanceStats"],
        queryFn: dashboardService.getAttendanceStats,
      },
    ],
  });

  const isLoading = results.some((result) => result.isLoading);

  if (isLoading) {
    return <Loader2 className="h-8 w-8 animate-spin" />;
  }

  const [recruitmentStats, leaveStats, evaluationStats, attendanceStats] =
    results.map((result) => result.data) as [
      RecruitmentStats,
      LeaveStats,
      EvaluationStats,
      AttendanceStats
    ];

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Tableau de Bord</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Présence</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {attendanceStats?.present_today}
            </div>
            <p className="text-xs text-muted-foreground">
              {attendanceStats?.monthly_hours.heures_travaillees__sum} heures ce
              mois
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Congés</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{leaveStats?.total_leaves}</div>
            <p className="text-xs text-muted-foreground">
              {leaveStats?.by_type[0]?.count}{" "}
              {leaveStats?.by_type[0]?.type_conge}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Recrutements</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {recruitmentStats?.total_active}
            </div>
            <p className="text-xs text-muted-foreground">
              {recruitmentStats?.urgent_posts} postes urgents
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Note Moyenne</CardTitle>
            <Star className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {evaluationStats?.average_score.note_globale__avg.toFixed(1)}/20
            </div>
            <p className="text-xs text-muted-foreground">
              {evaluationStats?.evaluations_count} évaluations
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default DashboardPage;
