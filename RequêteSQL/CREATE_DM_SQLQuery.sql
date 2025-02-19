USE MSPR_DM;

DROP TABLE IF EXISTS DM_Elections_Contexte;
CREATE TABLE DM_Elections_Contexte (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Année INT,
    Tour INT,
    Inscrits INT,
    Abstentions INT,
    [%Abs/Ins] DECIMAL(10,2),
    Votants INT,
    [%Vot/Ins] DECIMAL(10,2),
    Blancsetnuls INT,
    Parti NVARCHAR(50),
    Bord NVARCHAR(50),
    Voix DECIMAL(10,2),
    [%_exp] DECIMAL(10,2),
    TauxDeChomage DECIMAL(10,3),
    PIB INT,
    [Nombre Crimes] FLOAT,
    [Taux Criminalité] FLOAT
);

DROP TABLE IF EXISTS DM_Emploi_Salaires;
CREATE TABLE DM_Emploi_Salaires (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Année INT,
    TauxDeChomage DECIMAL(10,3),
    [Salariés Secteur Privé] DECIMAL(10,2),
    [Salariés Secteur Public] DECIMAL(10,2),
    [Masse Salariale T+50 Brut] FLOAT,
    [Masse Salariale T+70 Brut] FLOAT,
    [Masse Salariale T+50 CVS] FLOAT,
    [Masse Salariale T+70 CVS] FLOAT,
    [Glissement Trimestriel T+50] FLOAT,
    [Glissement Trimestriel T+70] FLOAT,
    [Glissement Annuel T+50] FLOAT,
    [Glissement Annuel T+70] FLOAT,
    [Catégorie Socioprofessionnelle] NVARCHAR(100),
    [Proportion Fortement Limitées] DECIMAL(10,1),
    [Proportion Limitées] DECIMAL(10,1),
    [Âge Départ Retraite] DECIMAL(10,1),
    [Proportion Retraités à 61 Ans] DECIMAL(10,1),
    [Durée Emploi Avant Retraite] DECIMAL(10,1),
    [Durée Sans Emploi Avant Retraite] DECIMAL(10,1)
);

DROP TABLE IF EXISTS DM_Demographie_Consommation;
CREATE TABLE DM_Demographie_Consommation (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Année INT,
    [Population] DECIMAL(10,1),
    [Naissances] DECIMAL(10,1),
    [Décès] DECIMAL(10,1),
    [Solde Naturel] DECIMAL(10,1),
    [Solde Migratoire] DECIMAL(10,1),
    [Ajustement] DECIMAL(10,1),
    [PIB] INT,
    [Dépenses Ménages] DECIMAL(10,3),
    [Secteur Consommation] NVARCHAR(50),
    [Contrepartie] NVARCHAR(50),
    [Type Dépense] NVARCHAR(50),
    [Unité Mesure] NVARCHAR(50),
    [Prix] NVARCHAR(50),
    [Transformation] NVARCHAR(50),
    [Produit] NVARCHAR(50),
    [Fréquence] NVARCHAR(50),
    [Statut Observation] NVARCHAR(50),
    [Statut Confiance] NVARCHAR(50),
    [Année Référence Prix] INT,
    [Décimales] INT,
    [Identifiant Table] NVARCHAR(50),
    [Multiplicateur Unité] INT,
    [Dernière Mise à Jour] NVARCHAR(50),
    [Période Référence] INT,
    [Valeur Observation] DECIMAL(10,3)
);

DROP TABLE IF EXISTS DM_Insecurite;
CREATE TABLE DM_Insecurite (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Année INT,
    [Nombre Crimes] FLOAT,
    [Taux Criminalité] FLOAT,
    [Population INSEE] FLOAT
);
