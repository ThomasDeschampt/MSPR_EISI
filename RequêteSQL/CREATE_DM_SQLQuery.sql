USE MSPR_DM;

DROP TABLE IF EXISTS DM_Elections_Contexte;
CREATE TABLE DM_Elections_Contexte (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Ann�e INT,
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
    [Taux Criminalit�] FLOAT
);

DROP TABLE IF EXISTS DM_Emploi_Salaires;
CREATE TABLE DM_Emploi_Salaires (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Ann�e INT,
    TauxDeChomage DECIMAL(10,3),
    [Salari�s Secteur Priv�] DECIMAL(10,2),
    [Salari�s Secteur Public] DECIMAL(10,2),
    [Masse Salariale T+50 Brut] FLOAT,
    [Masse Salariale T+70 Brut] FLOAT,
    [Masse Salariale T+50 CVS] FLOAT,
    [Masse Salariale T+70 CVS] FLOAT,
    [Glissement Trimestriel T+50] FLOAT,
    [Glissement Trimestriel T+70] FLOAT,
    [Glissement Annuel T+50] FLOAT,
    [Glissement Annuel T+70] FLOAT,
    [Cat�gorie Socioprofessionnelle] NVARCHAR(100),
    [Proportion Fortement Limit�es] DECIMAL(10,1),
    [Proportion Limit�es] DECIMAL(10,1),
    [�ge D�part Retraite] DECIMAL(10,1),
    [Proportion Retrait�s � 61 Ans] DECIMAL(10,1),
    [Dur�e Emploi Avant Retraite] DECIMAL(10,1),
    [Dur�e Sans Emploi Avant Retraite] DECIMAL(10,1)
);

DROP TABLE IF EXISTS DM_Demographie_Consommation;
CREATE TABLE DM_Demographie_Consommation (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Ann�e INT,
    [Population] DECIMAL(10,1),
    [Naissances] DECIMAL(10,1),
    [D�c�s] DECIMAL(10,1),
    [Solde Naturel] DECIMAL(10,1),
    [Solde Migratoire] DECIMAL(10,1),
    [Ajustement] DECIMAL(10,1),
    [PIB] INT,
    [D�penses M�nages] DECIMAL(10,3),
    [Secteur Consommation] NVARCHAR(50),
    [Contrepartie] NVARCHAR(50),
    [Type D�pense] NVARCHAR(50),
    [Unit� Mesure] NVARCHAR(50),
    [Prix] NVARCHAR(50),
    [Transformation] NVARCHAR(50),
    [Produit] NVARCHAR(50),
    [Fr�quence] NVARCHAR(50),
    [Statut Observation] NVARCHAR(50),
    [Statut Confiance] NVARCHAR(50),
    [Ann�e R�f�rence Prix] INT,
    [D�cimales] INT,
    [Identifiant Table] NVARCHAR(50),
    [Multiplicateur Unit�] INT,
    [Derni�re Mise � Jour] NVARCHAR(50),
    [P�riode R�f�rence] INT,
    [Valeur Observation] DECIMAL(10,3)
);

DROP TABLE IF EXISTS DM_Insecurite;
CREATE TABLE DM_Insecurite (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Ann�e INT,
    [Nombre Crimes] FLOAT,
    [Taux Criminalit�] FLOAT,
    [Population INSEE] FLOAT
);
