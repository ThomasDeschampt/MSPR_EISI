USE MSPR;

DROP TABLE IF EXISTS Annees;
CREATE TABLE Annees(
    Id INT PRIMARY KEY IDENTITY(1,1),
	Année INT
);

DROP TABLE IF EXISTS Elections;
CREATE TABLE Elections(
    Id INT PRIMARY KEY IDENTITY(1,1),
	Année INT,
	Tour INT,
	Inscrits INT,
	Absentions INT,
	[%Abs/Ins] DECIMAL(10,2),
	Votants INT,
	[%Vot/Ins] DECIMAL(10,2),
	Blancsetnuls INT
);

DROP TABLE IF EXISTS Candidats;
CREATE TABLE Candidats(
    Id INT PRIMARY KEY IDENTITY(1,1),
	Année INT,
	Tour INT,
	Parti NVARCHAR (50),
	Bord NVARCHAR (50),
	Voix DECIMAL (10,2),
	[%_exp] DECIMAL(10,2)
);

DROP TABLE IF EXISTS Chomage;
CREATE TABLE Chomage(
	Id INT PRIMARY KEY IDENTITY(1,1),
	Année INT,
	TauxDeChomage DECIMAL (10,3)
);

DROP TABLE IF EXISTS ConsoMenage;
CREATE TABLE ConsoMenage(
	Id INT PRIMARY KEY IDENTITY(1,1),
	annee INT,
	valeur DECIMAL (10,2)
);



DROP TABLE IF EXISTS Demographie;
CREATE TABLE Demographie(
	Id INT PRIMARY KEY IDENTITY(1,1),
	Année INT,
	[Population au 1er janvier] DECIMAL (10,1),
	[Naissances vivantes] DECIMAL (10,1),
	Décès DECIMAL (10,1),
	[Solde naturel] DECIMAL (10,1),
	[Solde migratoire] DECIMAL (10,1),
	Ajustement DECIMAL (10,1)
);

DROP TABLE IF EXISTS Retraite;
CREATE TABLE Retraite(
	Id INT PRIMARY KEY IDENTITY(1,1),
	Annee INT,
	Taux_Retraite DECIMAL (10,2)
);

DROP TABLE IF EXISTS EmploisPrive;
CREATE TABLE EmploisPrive(
	Id INT PRIMARY KEY IDENTITY(1,1),
	Année INT,
	[Nombre de salariés] DECIMAL (10,2)
);

DROP TABLE IF EXISTS EmploisPublic;
CREATE TABLE EmploisPublic(
	Id INT PRIMARY KEY IDENTITY(1,1),
	Année INT,
	[Nombre de salariés] DECIMAL (10,2)
);

DROP TABLE IF EXISTS Insecurite;
CREATE TABLE Insecurite(
	Id INT PRIMARY KEY IDENTITY(1,1),
	annee INT,
	nombre FLOAT,
	taux_pour_mille FLOAT,
	insee_pop FLOAT
);

DROP TABLE IF EXISTS MasseSalariale;
CREATE TABLE MasseSalariale(
	Id INT PRIMARY KEY IDENTITY(1,1),
	Année INT,
	[Masse salariale à T+50 jours (brut)] FLOAT,
	[Masse salariale à T+70 jours (brut)] FLOAT,
	[Masse salariale à T+50 jours (cvs)] FLOAT,
	[Masse salariale à T+70 jours (cvs)] FLOAT,
	[Glissement trimestriel - Masse salariale à T+50 jours (cvs)] FLOAT,
	[Glissement trimestriel - Masse salariale à T+70 jours (cvs)] FLOAT,
	[Glissement annuel - Masse salariale à T+50 jours (cvs)] FLOAT,
	[Glissement annuel - Masse salariale à T+70 jours (cvs)] FLOAT,
);

DROP TABLE IF EXISTS Pib;
CREATE TABLE Pib(
	Id INT PRIMARY KEY IDENTITY(1,1),
	Année INT,
	PIB INT
);