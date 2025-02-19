# Generated by Django 4.2.7 on 2025-01-18 23:46

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Archive",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom_archive", models.CharField(max_length=150)),
                ("description", models.TextField(blank=True, null=True)),
                ("date_archive", models.DateField(auto_now_add=True)),
                ("contenu", models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name="Candidat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
                ("prenom", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("mot_de_passe", models.CharField(max_length=128)),
                ("telephone", models.CharField(max_length=20)),
                ("cv", models.FileField(upload_to="candidats/cv/")),
                ("lettre_motivation", models.FileField(upload_to="candidats/lettres/")),
                ("date_inscription", models.DateTimeField(auto_now_add=True)),
                ("compte_verifie", models.BooleanField(default=False)),
                ("code_confirmation", models.CharField(blank=True, max_length=100)),
                ("date_confirmation", models.DateTimeField(blank=True, null=True)),
                ("source_recrutement", models.CharField(max_length=100)),
                (
                    "documents",
                    models.FileField(blank=True, upload_to="candidats/documents/"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Employe",
            fields=[
                ("id_employe", models.AutoField(primary_key=True, serialize=False)),
                ("matricule", models.CharField(max_length=50, unique=True)),
                ("nom", models.CharField(max_length=50)),
                ("prenom", models.CharField(max_length=50)),
                ("date_naissance", models.DateField()),
                ("date_embauche", models.DateField()),
                ("adresse", models.TextField()),
                (
                    "telephone_fixe",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "telephone_mobile",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "email_pro",
                    models.EmailField(db_index=True, max_length=254, unique=True),
                ),
                (
                    "email_perso",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("numero_securite_sociale", models.CharField(max_length=50)),
                (
                    "situation_familiale",
                    models.CharField(
                        choices=[
                            ("CELIBATAIRE", "Célibataire"),
                            ("MARIE", "Marié(e)"),
                            ("DIVORCE", "Divorcé(e)"),
                            ("VEUF", "Veuf/Veuve"),
                        ],
                        max_length=20,
                    ),
                ),
                ("nombre_enfants", models.IntegerField(default=0)),
                (
                    "niveau_etudes",
                    models.CharField(
                        choices=[
                            ("BAC", "Baccalauréat"),
                            ("LICENCE", "Licence"),
                            ("MASTER", "Master"),
                            ("MAGISTERE", "Magistère"),
                            ("DOCTORAT", "Doctorat"),
                            ("AUTRE", "Autre"),
                        ],
                        max_length=50,
                    ),
                ),
                ("diplome", models.CharField(max_length=50)),
                (
                    "photo",
                    models.ImageField(blank=True, null=True, upload_to="photos/"),
                ),
                (
                    "piece_identite",
                    models.FileField(blank=True, null=True, upload_to="documents/"),
                ),
                ("actif", models.BooleanField(default=True)),
                ("poste_occupe", models.CharField(max_length=50)),
                ("maladies", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Historique",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "model_name",
                    models.CharField(max_length=100, verbose_name="Nom du modèle"),
                ),
                ("instance_id", models.IntegerField(verbose_name="ID de l'instance")),
                (
                    "utilisateur",
                    models.CharField(
                        max_length=150, verbose_name="Utilisateur à l'origine"
                    ),
                ),
                (
                    "date_modification",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date de modification"
                    ),
                ),
                (
                    "modifications",
                    models.JSONField(default=dict, verbose_name="Modifications"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id_service", models.AutoField(primary_key=True, serialize=False)),
                (
                    "code_service",
                    models.CharField(db_index=True, max_length=20, unique=True),
                ),
                ("nom_service", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "localisation",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("telephone", models.CharField(blank=True, max_length=15, null=True)),
                (
                    "email_service",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("actif", models.BooleanField(default=True)),
                ("date_creation", models.DateField(auto_now_add=True)),
                ("effectif_actuel", models.IntegerField(default=0)),
                (
                    "id_responsable",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="responsable_service",
                        to="core.employe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Recrutement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "reference_poste",
                    models.CharField(db_index=True, max_length=50, unique=True),
                ),
                ("titre_poste", models.CharField(max_length=100)),
                ("description_poste", models.TextField()),
                ("competences_requises", models.TextField()),
                ("experience_requise", models.TextField()),
                ("niveau_etudes_requis", models.CharField(max_length=100)),
                ("date_publication", models.DateField()),
                ("date_cloture", models.DateField()),
                (
                    "statut",
                    models.CharField(
                        choices=[
                            ("OUVERT", "Ouvert"),
                            ("FERME", "Fermé"),
                            ("EN_COURS", "En cours de traitement"),
                            ("EN_ATTENTE", "En attente de décision"),
                            ("ANNULE", "Annulé"),
                            ("FINALISE", "Finalisé"),
                        ],
                        max_length=50,
                    ),
                ),
                ("postes_disponibles", models.PositiveIntegerField()),
                (
                    "salaire_propose",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("type_contrat_propose", models.CharField(max_length=20)),
                ("localisation_poste", models.CharField(max_length=200)),
                ("urgent", models.BooleanField(default=False)),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.service"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Massrouf",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "montant_demande",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("date_demande", models.DateTimeField(auto_now_add=True)),
                (
                    "statut",
                    models.CharField(
                        choices=[
                            ("EN_ATTENTE", "En attente"),
                            ("APPROUVÉ", "Approuvé"),
                            ("REJETÉ", "Rejeté"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "justificatif",
                    models.FileField(
                        blank=True, null=True, upload_to="salary/advances/"
                    ),
                ),
                (
                    "employe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.employe"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Formation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titre", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("date_debut", models.DateField()),
                ("date_fin", models.DateField()),
                ("lieu", models.CharField(max_length=200)),
                ("cout", models.DecimalField(decimal_places=2, max_digits=10)),
                ("duree_heures", models.PositiveIntegerField()),
                ("type_formation", models.CharField(max_length=100)),
                ("niveau", models.CharField(max_length=50)),
                ("places_disponibles", models.PositiveIntegerField()),
                ("statut", models.CharField(max_length=50)),
                ("objectifs", models.TextField()),
                ("prerequis", models.TextField()),
                (
                    "certificat",
                    models.FileField(
                        blank=True, null=True, upload_to="formations/certificats/"
                    ),
                ),
                (
                    "formateur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.employe"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Evaluation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_evaluation", models.DateField()),
                (
                    "note_globale",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(20),
                        ]
                    ),
                ),
                ("commentaires", models.TextField()),
                ("periode", models.CharField(max_length=50)),
                ("objectifs_fixes", models.TextField()),
                ("objectifs_atteints", models.TextField()),
                ("axes_amelioration", models.TextField()),
                ("besoins_formation", models.TextField()),
                ("entretien_realise", models.BooleanField(default=False)),
                ("document_evaluation", models.FileField(upload_to="evaluations/")),
                ("date_prochaine_evaluation", models.DateField()),
                (
                    "employe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.employe"
                    ),
                ),
                (
                    "evaluateur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="evaluations_effectuees",
                        to="core.employe",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="employe",
            name="id_service",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="employes",
                to="core.service",
            ),
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type_document", models.CharField(max_length=100)),
                ("nom_fichier", models.CharField(max_length=255)),
                ("date_upload", models.DateTimeField(auto_now_add=True)),
                ("description", models.TextField(blank=True)),
                (
                    "confidentialite",
                    models.CharField(
                        choices=[
                            ("PUBLIC", "Public"),
                            ("PRIVE", "Privé"),
                            ("CONFIDENTIEL", "Confidentiel"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "employe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.employe"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Contrat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type_contrat",
                    models.CharField(
                        choices=[
                            ("CDI", "Contrat à Durée Indéterminée"),
                            ("CDD", "Contrat à Durée Déterminée"),
                            ("STAGE", "Stage"),
                            ("APPRENTISSAGE", "Contrat d’apprentissage"),
                        ],
                        max_length=20,
                    ),
                ),
                ("date_debut", models.DateField()),
                ("date_fin", models.DateField(blank=True, null=True)),
                ("date_signature", models.DateField()),
                ("salaire_base", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "salaire_journalier",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("devise", models.CharField(default="DZD", max_length=10)),
                ("statut", models.CharField(max_length=50)),
                ("periode_essai", models.BooleanField(default=True)),
                ("duree_periode_essai", models.PositiveIntegerField(default=0)),
                ("fin_periode_essai", models.DateField(blank=True, null=True)),
                ("conditions_particulieres", models.TextField(blank=True)),
                ("motif_fin", models.TextField(blank=True)),
                ("archive", models.BooleanField(default=False)),
                ("date_archive", models.DateField(blank=True, null=True)),
                ("document_contrat", models.FileField(upload_to="contrats/")),
                (
                    "employe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.employe"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Conge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_debut", models.DateField()),
                ("date_fin", models.DateField()),
                (
                    "type_conge",
                    models.CharField(
                        choices=[
                            ("ANNUEL", "Congé Annuel"),
                            ("MALADIE", "Congé Maladie"),
                            ("MATERNITE", "Congé Maternité"),
                            ("PATERNITE", "Congé Paternité"),
                            ("SANS_SOLDE", "Congé Sans Solde"),
                            ("FORMATION", "Congé pour Formation"),
                            ("OBSEQUES", "Congé pour Obsèques"),
                            ("AUTRE", "Autre"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "statut",
                    models.CharField(
                        choices=[
                            ("DEMANDE", "Demande en cours"),
                            ("APPROUVE", "Approuvé"),
                            ("REFUSE", "Refusé"),
                            ("ANNULE", "Annulé"),
                            ("TERMINE", "Terminé"),
                        ],
                        default="DEMANDE",
                        max_length=20,
                    ),
                ),
                ("date_demande", models.DateField(auto_now_add=True)),
                ("date_reponse", models.DateField(blank=True, null=True)),
                ("nb_jours", models.PositiveIntegerField()),
                ("justification", models.TextField()),
                (
                    "document_justificatif",
                    models.FileField(blank=True, upload_to="conges/justificatifs/"),
                ),
                ("solde_restant", models.FloatField()),
                ("solde_deductible", models.BooleanField(default=True)),
                (
                    "employe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="conges",
                        to="core.employe",
                    ),
                ),
                (
                    "valideur",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="conges_valides",
                        to="core.employe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Competence",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                (
                    "employes",
                    models.ManyToManyField(
                        related_name="competences", to="core.employe"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("is_employee", models.BooleanField(default=False)),
                ("is_hr", models.BooleanField(default=False)),
                ("is_manager", models.BooleanField(default=False)),
                ("verification_token", models.CharField(blank=True, max_length=100)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Salaire",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_paiement", models.DateField()),
                ("salaire_base", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "prime_rendement",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "prime_anciennete",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "heures_supplementaires",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "taux_horaire_sup",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "indemnites",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "avance_salaire",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("justificatif", models.CharField(blank=True, max_length=255)),
                ("montant_final", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "mois",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ]
                    ),
                ),
                ("annee", models.PositiveIntegerField()),
                ("mode_paiement", models.CharField(max_length=50)),
                ("reference_paiement", models.CharField(max_length=100)),
                ("fiche_paie_generee", models.BooleanField(default=False)),
                ("statut_paiement", models.CharField(max_length=50)),
                (
                    "contrat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.contrat"
                    ),
                ),
                (
                    "employe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.employe"
                    ),
                ),
            ],
            options={
                "unique_together": {("employe", "mois", "annee")},
            },
        ),
        migrations.CreateModel(
            name="Pointage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_pointage", models.DateField()),
                ("heure_arrivee", models.TimeField()),
                ("heure_depart", models.TimeField()),
                ("present", models.BooleanField(default=True)),
                ("conge", models.BooleanField(default=False)),
                ("justification_absence", models.TextField(blank=True)),
                (
                    "justificatif",
                    models.FileField(blank=True, upload_to="pointages/justificatifs/"),
                ),
                (
                    "heures_travaillees",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                (
                    "heures_supplementaires",
                    models.DecimalField(decimal_places=2, default=0, max_digits=5),
                ),
                ("jour_ferie", models.BooleanField(default=False)),
                ("commentaire", models.TextField(blank=True)),
                (
                    "employe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.employe"
                    ),
                ),
                (
                    "validateur",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="pointages_valides",
                        to="core.employe",
                    ),
                ),
            ],
            options={
                "unique_together": {("employe", "date_pointage")},
            },
        ),
        migrations.CreateModel(
            name="Favori",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom_fonctionnalite", models.CharField(max_length=100)),
                ("icone", models.FileField(blank=True, upload_to="favoris/icones/")),
                ("position_ordre", models.PositiveIntegerField()),
                ("date_ajout", models.DateTimeField(auto_now_add=True)),
                ("actif", models.BooleanField(default=True)),
                (
                    "employe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.employe"
                    ),
                ),
            ],
            options={
                "ordering": ["position_ordre"],
                "unique_together": {("employe", "nom_fonctionnalite")},
            },
        ),
        migrations.CreateModel(
            name="Candidature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_candidature", models.DateTimeField(auto_now_add=True)),
                ("statut", models.CharField(max_length=50)),
                ("notes_recruteur", models.TextField(blank=True)),
                ("evaluation_entretien", models.TextField(blank=True)),
                ("date_entretien", models.DateTimeField(blank=True, null=True)),
                ("resultat_entretien", models.CharField(blank=True, max_length=50)),
                ("documents_valides", models.BooleanField(default=False)),
                ("decision_finale", models.TextField(blank=True)),
                (
                    "candidat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.candidat"
                    ),
                ),
                (
                    "recrutement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.recrutement",
                    ),
                ),
            ],
            options={
                "unique_together": {("candidat", "recrutement")},
            },
        ),
    ]
