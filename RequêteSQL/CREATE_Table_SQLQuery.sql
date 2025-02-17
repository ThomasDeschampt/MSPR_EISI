USE MSPR;

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
	REF_SECTOR NVARCHAR (50),
	COUNTERPART_AREA NVARCHAR (50),
	ACCOUNTING_ENTRY NVARCHAR (50),
	STO NVARCHAR (50),
	INSTR_ASSET NVARCHAR (50),
	ACTIVITY NVARCHAR (50),
	EXPENDITURE NVARCHAR (50),
	UNIT_MEASURE NVARCHAR (50),
	PRICES NVARCHAR (50),
	TRANSFORMATION NVARCHAR (50),
	PRODUCT NVARCHAR (50),
	FREQ NVARCHAR (50),
	OBS_STATUS NVARCHAR (50),
	CONF_STATUS NVARCHAR (50),
	REF_PERIOD_DETAIL NVARCHAR (50),
	REF_YEAR_PRICE INT,
	DECIMALS INT,
	TABLE_IDENTIFIER NVARCHAR (50), 
	UNIT_MULT INT,
	OBS_STATUS_FR NVARCHAR (50),
	LAST_UPDATE NVARCHAR (50), 
	TIME_PERIOD INT,
	OBS_VALUE DECIMAL (10,3)
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

DROP TABLE IF EXISTS DepartRetraite;
CREATE TABLE DepartRetraite(
	Id INT PRIMARY KEY IDENTITY(1,1),
	Annee INT,
	[Catégorie socioprofessionnelle] NVARCHAR (100),
	Proportion_fortement_limitees DECIMAL (10,1),
	Proportion_limitees DECIMAL (10,1),
	Age_depart DECIMAL (10,1),
	Proportion_retraites_61ans DECIMAL (10,1),
	Duree_emploi DECIMAL (10,1),
	Duree_sans_emploi DECIMAL (10,1),
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