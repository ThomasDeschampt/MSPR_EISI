USE MSPR_DM;

-- Supprimer les tables avant recréation
DROP TABLE IF EXISTS Faits_Elections;
DROP TABLE IF EXISTS Candidat;
DROP TABLE IF EXISTS Economie;
DROP TABLE IF EXISTS Demographie;
DROP TABLE IF EXISTS Insecurite;
DROP TABLE IF EXISTS Emplois;
DROP TABLE IF EXISTS DepartRetraite;
DROP TABLE IF EXISTS ConsoMenage;

-- Création des tables
CREATE TABLE Economie(
   Id_economie INT PRIMARY KEY IDENTITY(1,1),
   Taux_chomage DECIMAL(10,3),
   Pib INT,
   Annee INT
);

CREATE TABLE Demographie(
   Id_demographie INT PRIMARY KEY,
   Annee INT,
   Population DECIMAL(10,1),
   Naissances DECIMAL(10,1),
   Deces DECIMAL(10,1),
   SoldeNaturel DECIMAL(10,1),
   SoldeMigratoire DECIMAL(10,1),
   Ajustement DECIMAL(10,1)
);

CREATE TABLE Insecurite(
   Id_insecurite INT PRIMARY KEY,
   Annee INT,
   Nombre FLOAT,
   Taux_pour_mille FLOAT,
   insee_pop FLOAT
);

CREATE TABLE Emplois(
   Id_emploi INT PRIMARY KEY IDENTITY(1,1),
   Annee INT,
   Nombre_salaries_public FLOAT,
   Nombre_salaries_prive FLOAT,
   Masse_salariale_T50_jours_brut FLOAT,
   Glissement_trimestriel_masse_salariale_T50_jours_cvs FLOAT,
   Glissement_trimestriel_masse_salariale_T70_jours_cvs FLOAT,
   Glissement_annuel_masse_salariale_T50_jours_cvs FLOAT,
   Glissement_annuel_masse_salariale_T70_jours_cvs FLOAT,
   Masse_salariale_T70_jours_brut FLOAT,
   Masse_salariale_T50_jours_cvs FLOAT,
   Masse_salariale_T70_jours_cvs FLOAT
);

CREATE TABLE DepartRetraite(
   Id_depart_retraite INT PRIMARY KEY,
   Annee INT,
   Categorie_socioprofessionnelle NVARCHAR(100),
   Proportion_fortement_limitees DECIMAL(10,1),
   Proportion_limitees DECIMAL(10,1),
   Age_depart DECIMAL(10,1),
   Proportion_retraites_61ans DECIMAL(10,1),
   Duree_emploi DECIMAL(10,1),
   Duree_sans_emploi DECIMAL(10,1)
);

CREATE TABLE ConsoMenage(
   Id_conso_menage INT PRIMARY KEY,
   Ref_sector NVARCHAR(50),
   Accounting_entry NVARCHAR(50),
   Sto NVARCHAR(50),
   Instr_asset NVARCHAR(50),
   Activity NVARCHAR(50),
   Expenditure NVARCHAR(50),
   Unit_measure NVARCHAR(50),
   Prices NVARCHAR(50),
   Transformation NVARCHAR(50),
   Product NVARCHAR(50),
   Freq NVARCHAR(50),
   Obs_status NVARCHAR(50),
   Conf_status NVARCHAR(50),
   Ref_year_price DECIMAL(10,1),
   Decimals INT,
   Unit_mult INT,
   Obs_status_fr NVARCHAR(50),
   Annee INT,
   Obs_value DECIMAL(10,3),
   Counterpart_area NVARCHAR(50)
);

CREATE TABLE Candidat(
   Id_candidat INT PRIMARY KEY,
   Annee INT,
   Tour INT,
   Parti NVARCHAR(50),
   Bord NVARCHAR(50)
);

-- Création de Faits_Elections avec FK explicites
CREATE TABLE Faits_Elections(
   Id_fait_election INT PRIMARY KEY IDENTITY(1,1),
   Annee INT,
   Tour INT,
   Inscrits INT,
   Absentions INT,
   Pourcentage_Abstention DECIMAL(10,2),
   Votants INT,
   Pourcentage_Votants DECIMAL(10,2),
   BlancsNuls INT,
   Nombre_de_voix DECIMAL(10,2),
   Ratio_voix_exprime DECIMAL(10,2),
   Id_demographie INT,
   Id_conso_menage INT,
   Id_emploi INT,
   Id_insecurite INT,
   Id_economie INT,
   Id_depart_retraite INT,
   Id_candidat INT,
   CONSTRAINT FK_FaitsElections_Candidat FOREIGN KEY(Id_candidat) REFERENCES Candidat(Id_candidat),
   CONSTRAINT FK_FaitsElections_Demographie FOREIGN KEY(Id_demographie) REFERENCES Demographie(Id_demographie),
   CONSTRAINT FK_FaitsElections_ConsoMenage FOREIGN KEY(Id_conso_menage) REFERENCES ConsoMenage(Id_conso_menage),
   CONSTRAINT FK_FaitsElections_Emplois FOREIGN KEY(Id_emploi) REFERENCES Emplois(Id_emploi),
   CONSTRAINT FK_FaitsElections_Insecurite FOREIGN KEY(Id_insecurite) REFERENCES Insecurite(Id_insecurite),
   CONSTRAINT FK_FaitsElections_Economie FOREIGN KEY(Id_economie) REFERENCES Economie(Id_economie),
   CONSTRAINT FK_FaitsElections_DepartRetraite FOREIGN KEY(Id_depart_retraite) REFERENCES DepartRetraite(Id_depart_retraite)
);
