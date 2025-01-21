import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { authService } from "@/services/auth";
import { Loader2 } from "lucide-react";

const registerSchema = z.object({
  email: z.string().email("Email invalide"),
  username: z.string().min(1, "Nom d'utilisateur requis"),
  password: z.string().min(6, "Mot de passe trop court"),
});

export const RegisterForm = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const form = useForm<z.infer<typeof registerSchema>>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: "",
      username: "",
      password: "",
    },
  });

  const onSubmit = async (data: z.infer<typeof registerSchema>) => {
    try {
      setIsLoading(true);
      setErrorMessage(""); // Clear previous error message
      await authService.register(data);
      navigate("/login");
    } catch (error) {
      setErrorMessage("Registration failed. Please try again.");
      console.error("Registration failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="w-full max-w-lg mx-auto p-6">
        <div className="mt-7 bg-white border border-gray-200 rounded-xl shadow-sm dark:bg-gray-800 dark:border-gray-700">
          <div className="p-4 sm:p-7">
            <div className="text-center mb-8">
              <h1 className="block text-2xl font-bold text-gray-800 dark:text-white">
                Inscription
              </h1>
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                Veuillez vous inscrire pour continuer
              </p>
            </div>

            {errorMessage && (
              <div className="mb-4 text-red-500 text-sm text-center bg-red-100 border border-red-400 rounded p-2">
                {errorMessage}
              </div>
            )}

            <Form {...form}>
              <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="space-y-5"
              >
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="block text-sm mb-2 dark:text-white">
                        Email
                      </FormLabel>
                      <FormControl>
                        <Input
                          className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600"
                          placeholder="nom@example.com"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage className="text-red-500 text-xs mt-2" />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="username"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="block text-sm mb-2 dark:text-white">
                        Nom d'utilisateur
                      </FormLabel>
                      <FormControl>
                        <Input
                          className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600"
                          placeholder="Nom d'utilisateur"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage className="text-red-500 text-xs mt-2" />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="block text-sm mb-2 dark:text-white">
                        Mot de passe
                      </FormLabel>
                      <FormControl>
                        <Input
                          className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600"
                          type="password"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage className="text-red-500 text-xs mt-2" />
                    </FormItem>
                  )}
                />
                <Button
                  type="submit"
                  className="w-full py-3 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600"
                  disabled={isLoading}
                >
                  {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
                  {isLoading ? "Inscription..." : "S'inscrire"}
                </Button>
              </form>
            </Form>
            <div className="text-center mt-4">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Déjà un compte?{" "}
                <Link to="/login" className="text-blue-600 hover:underline">
                  Connexion
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
