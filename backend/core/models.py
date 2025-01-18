from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

CONFIDENTIALITE_CHOICES = [
    ('PUBLIC', 'Public'),
    ('PRIVE', 'Privé'),
    ('CONFIDENTIEL', 'Confidentiel')
]

class Employe(models.Model):
    SITUATION_FAMILIALE_CHOICES = [
        ('CELIBATAIRE', 'Célibataire'),
        ('MARIE', 'Marié(e)'),
        ('DIVORCE', 'Divorcé(e)'),
        ('VEUF', 'Veuf/Veuve'),
    ]

    NIVEAU_ETUDES_CHOICES = [
        ('BAC', 'Baccalauréat'),
        ('LICENCE', 'Licence'),
        ('MASTER', 'Master'),
        ('MAGISTERE', 'Magistère'),
        ('DOCTORAT', 'Doctorat'),
        ('AUTRE', 'Autre'),
    ]

    id_employe = models.AutoField(primary_key=True)
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_naissance = models.DateField()
    date_embauche = models.DateField()
    adresse = models.TextField()
    telephone_fixe = models.CharField(max_length=15, null=True, blank=True)
    telephone_mobile = models.CharField(max_length=15, null=True, blank=True)
    email_pro = models.EmailField(unique=True, db_index=True)
    email_perso = models.EmailField(null=True, blank=True)
    numero_securite_sociale = models.CharField(max_length=50)
    situation_familiale = models.CharField(max_length=20, choices=SITUATION_FAMILIALE_CHOICES)
    nombre_enfants = models.IntegerField(default=0)
    niveau_etudes = models.CharField(max_length=50, choices=NIVEAU_ETUDES_CHOICES)
    diplome = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    piece_identite = models.FileField(upload_to='documents/', null=True, blank=True)
    actif = models.BooleanField(default=True)
    id_service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, related_name='employes')
    poste_occupe = models.CharField(max_length=50)
    maladies = models.TextField(null=True, blank=True)

    def clean(self):
        if self.email_perso == self.email_pro:
            raise ValidationError("Les emails professionnels et personnels doivent être différents.")
        
        if self.date_embauche and self.date_naissance and self.date_embauche <= self.date_naissance:
            raise ValidationError("La date d'embauche doit être postérieure à la date de naissance.")

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule})"
    

class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    code_service = models.CharField(max_length=20, unique=True, db_index=True)
    nom_service = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    localisation = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    email_service = models.EmailField(null=True, blank=True)
    id_responsable = models.ForeignKey('Employe', on_delete=models.SET_NULL, null=True, related_name='responsable_service')
    actif = models.BooleanField(default=True)
    date_creation = models.DateField(auto_now_add=True)
    effectif_actuel = models.IntegerField(default=0)

    def __str__(self):
        return self.nom_service

class Contrat(models.Model):
    TYPE_CONTRAT_CHOICES = [
        ('CDI', 'Contrat à Durée Indéterminée'),
        ('CDD', 'Contrat à Durée Déterminée'),
        ('STAGE', 'Stage'),
        ('APPRENTISSAGE', 'Contrat d’apprentissage'),
    ]
    employe = models.ForeignKey(Employe, on_delete=models.PROTECT)
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    date_signature = models.DateField()
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    salaire_journalier = models.DecimalField(max_digits=10, decimal_places=2)
    devise = models.CharField(max_length=10, default='DZD')
    statut = models.CharField(max_length=50)
    periode_essai = models.BooleanField(default=True)
    duree_periode_essai = models.PositiveIntegerField(default=0)
    fin_periode_essai = models.DateField(null=True, blank=True)
    conditions_particulieres = models.TextField(blank=True)
    motif_fin = models.TextField(blank=True)
    archive = models.BooleanField(default=False)
    date_archive = models.DateField(null=True, blank=True)
    document_contrat = models.FileField(upload_to='contrats/')

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.date_fin and self.date_debut and self.date_fin <= self.date_debut:
            raise ValidationError("La date de fin doit être ultérieure à la date de début.")

    def __str__(self):
        return f"Contrat {self.type_contrat} - {self.employe}"
    
class Conge(models.Model):
    STATUT_CHOICES = [
        ('DEMANDE', 'Demande en cours'),
        ('APPROUVE', 'Approuvé'),
        ('REFUSE', 'Refusé'),
        ('ANNULE', 'Annulé'),
        ('TERMINE', 'Terminé'),
    ]

    TYPE_CONGE_CHOICES = [
        ('ANNUEL', 'Congé Annuel'),
        ('MALADIE', 'Congé Maladie'),
        ('MATERNITE', 'Congé Maternité'),
        ('PATERNITE', 'Congé Paternité'),
        ('SANS_SOLDE', 'Congé Sans Solde'),
        ('FORMATION', 'Congé pour Formation'),
        ('OBSEQUES', 'Congé pour Obsèques'),
        ('AUTRE', 'Autre'),
    ]

    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='conges')
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_conge = models.CharField(max_length=20, choices=TYPE_CONGE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='DEMANDE')
    date_demande = models.DateField(auto_now_add=True)
    date_reponse = models.DateField(null=True, blank=True)
    nb_jours = models.PositiveIntegerField()
    valideur = models.ForeignKey(
        Employe, on_delete=models.SET_NULL, null=True, related_name='conges_valides'
    )
    justification = models.TextField()
    document_justificatif = models.FileField(upload_to='conges/justificatifs/', blank=True)
    solde_restant = models.FloatField()
    solde_deductible = models.BooleanField(default=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.date_fin and self.date_debut and self.date_fin <= self.date_debut:
            raise ValidationError("La date de fin doit être ultérieure à la date de début.")

    def __str__(self):
        return f"Congé {self.type_conge} - {self.employe.nom} ({self.date_debut} à {self.date_fin})"

    
class Salaire(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.PROTECT)
    contrat = models.ForeignKey(Contrat, on_delete=models.PROTECT)
    date_paiement = models.DateField()
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    prime_rendement = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prime_anciennete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    heures_supplementaires = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taux_horaire_sup = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    indemnites = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avance_salaire = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    justificatif = models.CharField(max_length=255, blank=True)
    montant_final = models.DecimalField(max_digits=10, decimal_places=2)
    mois = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    annee = models.PositiveIntegerField()
    mode_paiement = models.CharField(max_length=50)
    reference_paiement = models.CharField(max_length=100)
    fiche_paie_generee = models.BooleanField(default=False)
    statut_paiement = models.CharField(max_length=50)

    class Meta:
        unique_together = ['employe', 'mois', 'annee']

    def __str__(self):
        return f"Salaire {self.mois}/{self.annee} - {self.employe}"
    
class Massrouf(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVÉ', 'Approuvé'),
        ('REJETÉ', 'Rejeté')
    ]
    employe = models.ForeignKey('Employe', on_delete=models.CASCADE)
    montant_demande = models.DecimalField(max_digits=10, decimal_places=2)
    date_demande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, choices=[('EN_ATTENTE', 'En attente'), ('APPROUVÉ', 'Approuvé'), ('REJETÉ', 'Rejeté')])
    justificatif = models.FileField(upload_to='salary/advances/', null=True, blank=True)

    def __str__(self):
        return f"Demande de Massrouf par {self.employe} - {self.montant_demande}"


class Recrutement(models.Model):
    STATUT_CHOICES = [
    ('OUVERT', 'Ouvert'),  
    ('FERME', 'Fermé'), 
    ('EN_COURS', 'En cours de traitement'),  
    ('EN_ATTENTE', 'En attente de décision'),  
    ('ANNULE', 'Annulé'),  
    ('FINALISE', 'Finalisé'),  
    ]
    reference_poste = models.CharField(max_length=50, unique=True, db_index=True)
    titre_poste = models.CharField(max_length=100)
    description_poste = models.TextField()
    competences_requises = models.TextField()
    experience_requise = models.TextField()
    niveau_etudes_requis = models.CharField(max_length=100)
    date_publication = models.DateField()
    date_cloture = models.DateField()
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES)
    postes_disponibles = models.PositiveIntegerField()
    salaire_propose = models.DecimalField(max_digits=10, decimal_places=2)
    type_contrat_propose = models.CharField(max_length=20)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    localisation_poste = models.CharField(max_length=200)
    urgent = models.BooleanField(default=False)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.date_cloture and self.date_publication and self.date_cloture <= self.date_publication:
            raise ValidationError("La date de clôture doit être ultérieure à la date de publication.")
        
    def __str__(self):
        return f"{self.titre_poste} ({self.reference_poste})"

class Candidat(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)  # will be hashed methinks?
    telephone = models.CharField(max_length=20)
    cv = models.FileField(upload_to='candidats/cv/')
    lettre_motivation = models.FileField(upload_to='candidats/lettres/')
    date_inscription = models.DateTimeField(auto_now_add=True)
    compte_verifie = models.BooleanField(default=False)
    code_confirmation = models.CharField(max_length=100, blank=True)
    date_confirmation = models.DateTimeField(null=True, blank=True)
    source_recrutement = models.CharField(max_length=100)
    documents = models.FileField(upload_to='candidats/documents/', blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Candidature(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    recrutement = models.ForeignKey(Recrutement, on_delete=models.CASCADE)
    date_candidature = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50)
    notes_recruteur = models.TextField(blank=True)
    evaluation_entretien = models.TextField(blank=True)
    date_entretien = models.DateTimeField(null=True, blank=True)
    resultat_entretien = models.CharField(max_length=50, blank=True)
    documents_valides = models.BooleanField(default=False)
    decision_finale = models.TextField(blank=True)

    class Meta:
        unique_together = ['candidat', 'recrutement']

    def __str__(self):
        return f"Candidature de {self.candidat} pour {self.recrutement}"

class Evaluation(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_evaluation = models.DateField()
    evaluateur = models.ForeignKey(Employe, on_delete=models.PROTECT, related_name='evaluations_effectuees')
    note_globale = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    commentaires = models.TextField()
    periode = models.CharField(max_length=50)
    objectifs_fixes = models.TextField()
    objectifs_atteints = models.TextField()
    axes_amelioration = models.TextField()
    besoins_formation = models.TextField()
    entretien_realise = models.BooleanField(default=False)
    document_evaluation = models.FileField(upload_to='evaluations/')
    date_prochaine_evaluation = models.DateField()

    def __str__(self):
        return f"Evaluation de {self.employe} - {self.date_evaluation}"

class Formation(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    formateur = models.ForeignKey(Employe, on_delete=models.PROTECT)
    lieu = models.CharField(max_length=200)
    cout = models.DecimalField(max_digits=10, decimal_places=2)
    duree_heures = models.PositiveIntegerField()
    type_formation = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50)
    places_disponibles = models.PositiveIntegerField()
    statut = models.CharField(max_length=50)
    objectifs = models.TextField()
    prerequis = models.TextField()
    certificat = models.FileField(upload_to='formations/certificats/', blank=True, null=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.date_fin and self.date_debut and self.date_fin <= self.date_debut:
            raise ValidationError("La date de fin doit être ultérieure à la date de début.")

    def __str__(self):
        return f"Formation {self.titre} - {self.employe}"

class Pointage(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_pointage = models.DateField()
    heure_arrivee = models.TimeField()
    heure_depart = models.TimeField()
    present = models.BooleanField(default=True)
    conge = models.BooleanField(default=False)
    justification_absence = models.TextField(blank=True)
    justificatif = models.FileField(upload_to='pointages/justificatifs/', blank=True)
    heures_travaillees = models.DecimalField(max_digits=5, decimal_places=2)
    heures_supplementaires = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    validateur = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, related_name='pointages_valides')
    jour_ferie = models.BooleanField(default=False)
    commentaire = models.TextField(blank=True)

    class Meta:
        unique_together = ['employe', 'date_pointage']

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.heure_depart and self.heure_arrivee and self.heure_depart <= self.heure_arrivee:
            raise ValidationError("L'heure de départ doit être ultérieure à l'heure d'arrivée.")
        
    def __str__(self):
        return f"Pointage {self.employe} - {self.date_pointage}"
        
class Competence(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    employes = models.ManyToManyField('Employe', related_name='competences')
    
    def __str__(self):
        return self.nom


class Favori(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    nom_fonctionnalite = models.CharField(max_length=100)
    icone = models.FileField(upload_to='favoris/icones/', blank=True)
    position_ordre = models.PositiveIntegerField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    class Meta:
        unique_together = ['employe', 'nom_fonctionnalite']
        ordering = ['position_ordre']

    def __str__(self):
        return f"Favori {self.nom_fonctionnalite} - {self.employe}"


class Archive(models.Model):
    nom_archive = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    date_archive = models.DateField(auto_now_add=True)
    contenu = models.JSONField(default=dict)  

    def __str__(self):
        return f"Archive: {self.nom_archive} ({self.date_archive})"
    
class Document(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    type_document = models.CharField(max_length=100)
    nom_fichier = models.CharField(max_length=255)
    date_upload = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    confidentialite = models.CharField(max_length=20, choices=CONFIDENTIALITE_CHOICES)
    
class Historique(models.Model):
    model_name = models.CharField(max_length=100, verbose_name="Nom du modèle")  
    instance_id = models.IntegerField(verbose_name="ID de l'instance")  
    utilisateur = models.CharField(max_length=150, verbose_name="Utilisateur à l'origine")  
    date_modification = models.DateTimeField(auto_now_add=True, verbose_name="Date de modification")
    modifications = models.JSONField(default=dict, verbose_name="Modifications")  

    def __str__(self):
        return f"Modification {self.model_name} (ID {self.instance_id}) - {self.date_modification.strftime('%d/%m/%Y %H:%M')}"



class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_employee = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']