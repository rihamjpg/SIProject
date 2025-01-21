import { useParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { ArrowLeft, Pencil } from "lucide-react";
import { employeeService } from "@/services/employees";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { Employee } from "@/types/employee";
import { useToast } from "@/hooks/use-toast";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import * as z from "zod";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const employeeSchema = z.object({
  matricule: z.string().min(1, "Le matricule est requis"),
  nom: z.string().min(1, "Le nom est requis"),
  prenom: z.string().min(1, "Le prénom est requis"),
  date_naissance: z.string(),
  date_embauche: z.string(),
  adresse: z.string(),
  telephone_mobile: z.string(),
  telephone_fixe: z.string().nullable(),
  email_pro: z.string().email(),
  email_perso: z.string().email().nullable(),
  numero_securite_sociale: z.string(),
  situation_familiale: z.string(),
  nombre_enfants: z.number(),
  niveau_etudes: z.string(),
  diplome: z.string(),
  photo: z.any().nullable(),
  piece_identite: z.any().nullable(),
  actif: z.boolean(),
  id_service: z.number(),
  poste_occupe: z.string(),
  maladies: z.string().nullable(),
});
export const EmployeeDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [isEditing, setIsEditing] = useState(false);

  const {
    data: employee,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["employee", id],
    queryFn: () => employeeService.getById(Number(id)),
  });

  const form = useForm<Employee>({
    resolver: zodResolver(employeeSchema),
    defaultValues: employee,
  });
  const mutation = useMutation({
    mutationFn: (data: Employee) => employeeService.update(Number(id), data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["employee", id] });
      toast({
        title: "Succès",
        description: "Les modifications ont été enregistrées",
        className: "bg-green-50 border-green-500 text-green-900",
      });
      setIsEditing(false);
    },
    onError: () => {
      toast({
        title: "Erreur",
        description: "Une erreur est survenue lors de la modification",
        className: "bg-red-50 border-red-500 text-red-900",
      });
    },
  });

  const onSubmit = (data: Employee) => {
    mutation.mutate(data);
  };

  if (isLoading) return <EmployeeDetailsSkeleton />;
  if (isError) return <div>Une erreur est survenue</div>;
  if (!employee) return <div>Employé non trouvé</div>;

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Button
            variant="outline"
            size="icon"
            onClick={() => navigate("/employees")}
            className="h-10 w-10"
          >
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold">
              {employee.nom} {employee.prenom}
            </h1>
            <p className="text-gray-500">Matricule: {employee.matricule}</p>
          </div>
        </div>
        <div className="space-x-2">
          {isEditing ? (
            <>
              <Button
                variant="outline"
                onClick={() => {
                  setIsEditing(false);
                  form.reset();
                }}
              >
                Annuler
              </Button>
              <Button
                onClick={() => onSubmit(form.getValues())}
                className="bg-green-600 hover:bg-green-700 text-white"
                disabled={mutation.isPending}
              >
                {mutation.isPending ? "Enregistrement..." : "Sauvegarder"}
              </Button>
            </>
          ) : (
            <Button onClick={() => setIsEditing(true)} className="space-x-2">
              <Pencil className="h-4 w-4" />
              <span>Modifier</span>
            </Button>
          )}
        </div>
      </div>

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Personal Information Card */}
            <Card>
              <CardHeader>
                <CardTitle>Informations Personnelles</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-center mb-6">
                  {employee.photo ? (
                    <img
                      src={employee.photo}
                      alt={`${employee.nom} ${employee.prenom}`}
                      className="w-32 h-32 rounded-full object-cover border-4 border-primary/10"
                    />
                  ) : (
                    <div className="w-32 h-32 rounded-full bg-primary/10 flex items-center justify-center">
                      <span className="text-2xl text-primary">
                        {employee.nom[0]}
                        {employee.prenom[0]}
                      </span>
                    </div>
                  )}
                </div>
                {isEditing ? (
                  <div className="space-y-4">
                    <FormField
                      control={form.control}
                      defaultValue={employee.nom}
                      name="nom"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Nom</FormLabel>
                          <FormControl>
                            <Input {...field} value={field.value || ""} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      defaultValue={employee.prenom}
                      name="prenom"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Prénom</FormLabel>
                          <FormControl>
                            <Input {...field} value={field.value || ""} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      defaultValue={employee.date_naissance}
                      name="date_naissance"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Date de naissance</FormLabel>
                          <FormControl>
                            <Input type="date" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      defaultValue={employee.situation_familiale}
                      name="situation_familiale"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Situation familiale</FormLabel>
                          <Select
                            onValueChange={field.onChange}
                            defaultValue={field.value}
                          >
                            <SelectTrigger>
                              <SelectValue placeholder="Sélectionnez..." />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="CELIBATAIRE">
                                Célibataire
                              </SelectItem>
                              <SelectItem value="MARIE">Marié(e)</SelectItem>
                              <SelectItem value="DIVORCE">
                                Divorcé(e)
                              </SelectItem>
                            </SelectContent>
                          </Select>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      defaultValue={employee.nombre_enfants}
                      name="nombre_enfants"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Nombre d'enfants</FormLabel>
                          <FormControl>
                            <Input
                              type="number"
                              {...field}
                              onChange={(e) =>
                                field.onChange(parseInt(e.target.value))
                              }
                            />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                ) : (
                  <InfoGrid>
                    <InfoItem label="Nom" value={employee.nom} />
                    <InfoItem label="Prénom" value={employee.prenom} />
                    <InfoItem
                      label="Date de naissance"
                      value={format(new Date(employee.date_naissance), "PP", {
                        locale: fr,
                      })}
                    />
                    <InfoItem
                      label="Situation familiale"
                      value={employee.situation_familiale}
                    />
                    <InfoItem
                      label="Nombre d'enfants"
                      value={employee.nombre_enfants.toString()}
                    />
                    <InfoItem
                      label="N° Sécurité Sociale"
                      value={employee.numero_securite_sociale}
                    />
                  </InfoGrid>
                )}
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Coordonnées</CardTitle>
              </CardHeader>
              <CardContent>
                {isEditing ? (
                  <div className="space-y-4">
                    <FormField
                      control={form.control}
                      defaultValue={employee.adresse}
                      name="adresse"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Adresse</FormLabel>
                          <FormControl>
                            <Textarea {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      defaultValue={employee.telephone_mobile}
                      name="telephone_mobile"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Téléphone mobile</FormLabel>
                          <FormControl>
                            <Input {...field} value={field.value || ""} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      defaultValue={employee.telephone_fixe}
                      name="telephone_fixe"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Téléphone fixe</FormLabel>
                          <FormControl>
                            <Input {...field} value={field.value || ""} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      defaultValue={employee.email_pro}
                      name="email_pro"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Email professionnel</FormLabel>
                          <FormControl>
                            <Input type="email" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      defaultValue={employee.email_perso}
                      name="email_perso"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Email personnel</FormLabel>
                          <FormControl>
                            <Input type="email" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                ) : (
                  <>
                    <InfoGrid>
                      <InfoItem
                        label="Adresse"
                        value={employee.adresse}
                        fullWidth
                      />
                      <InfoItem
                        label="Téléphone mobile"
                        value={employee.telephone_mobile}
                      />
                      <InfoItem
                        label="Téléphone fixe"
                        value={employee.telephone_fixe || "-"}
                      />
                      <InfoItem
                        label="Email professionnel"
                        value={employee.email_pro}
                      />
                    </InfoGrid>
                    <InfoItem
                      label="Email personnel"
                      value={employee.email_perso || "-"}
                    />
                  </>
                )}
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Informations Professionnelles</CardTitle>
              </CardHeader>
              <CardContent>
                {isEditing ? (
                  <div className="space-y-4">
                    <FormField
                      control={form.control}
                      defaultValue={employee.poste_occupe}
                      name="poste_occupe"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Poste occupé</FormLabel>
                          <FormControl>
                            <Input {...field} value={field.value || ""} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      defaultValue={employee.date_embauche}
                      name="date_embauche"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Date d'embauche</FormLabel>
                          <FormControl>
                            <Input type="date" {...field} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      defaultValue={employee.niveau_etudes}
                      name="niveau_etudes"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Niveau d'études</FormLabel>
                          <FormControl>
                            <Input {...field} value={field.value || ""} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      defaultValue={employee.diplome}
                      name="diplome"
                      render={({ field }) => (
                        <FormItem>
                          <FormLabel>Diplôme</FormLabel>
                          <FormControl>
                            <Input {...field} value={field.value || ""} />
                          </FormControl>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                    <FormField
                      control={form.control}
                      name="actif"
                      render={({ field }) => (
                        <FormItem>
                          <div className="flex items-center space-x-2">
                            <FormControl>
                              <Switch
                                checked={field.value}
                                onCheckedChange={field.onChange}
                              />
                            </FormControl>
                            <FormLabel>Employé actif</FormLabel>
                          </div>
                          <FormMessage />
                        </FormItem>
                      )}
                    />
                  </div>
                ) : (
                  <InfoGrid>
                    <InfoItem
                      label="Poste occupé"
                      value={employee.poste_occupe}
                    />
                    <InfoItem label="Service" value={employee.service_name} />
                    <InfoItem
                      label="Date d'embauche"
                      value={format(new Date(employee.date_embauche), "PP", {
                        locale: fr,
                      })}
                    />
                    <InfoItem
                      label="Niveau d'études"
                      value={employee.niveau_etudes}
                    />
                    <InfoItem label="Diplôme" value={employee.diplome} />
                    <InfoItem
                      label="Statut"
                      value={employee.actif ? "Actif" : "Inactif"}
                    />
                  </InfoGrid>
                )}
              </CardContent>
            </Card>
          </div>
        </form>
      </Form>
    </div>
  );
};

// ... existing InfoItem, InfoGrid, and EmployeeDetailsSkeleton components ...
const InfoItem = ({
  label,
  value,
  fullWidth = false,
}: {
  label: string;
  value: string;
  fullWidth?: boolean;
}) => (
  <div className={fullWidth ? "col-span-2" : undefined}>
    <p className="text-sm text-gray-500">{label}</p>
    <p className="font-medium">{value}</p>
  </div>
);

const InfoGrid = ({ children }: { children: React.ReactNode }) => (
  <div className="grid grid-cols-2 gap-4">{children}</div>
);

const EmployeeDetailsSkeleton = () => (
  <div className="p-6 space-y-6">
    <div className="flex justify-between items-center">
      <div>
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-4 w-32 mt-2" />
      </div>
      <Skeleton className="h-10 w-24" />
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {[1, 2, 3].map((i) => (
        <Card key={i}>
          <CardHeader>
            <Skeleton className="h-6 w-40" />
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3, 4].map((j) => (
                <div key={j}>
                  <Skeleton className="h-4 w-24 mb-1" />
                  <Skeleton className="h-6 w-full" />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  </div>
);
