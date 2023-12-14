-- init.sql

-- Créez la table mytable
CREATE TABLE camions (
  camion_id INT NOT NULL AUTO_INCREMENT,
  camion_pos_x FLOAT NOT NULL,
  camion_pos_y FLOAT NOT NULL,
  PRIMARY KEY (camion_id)
);

CREATE TABLE livraisons (
  livraison_id INT NOT NULL AUTO_INCREMENT,
  camion_id INT NOT NULL,
  etat_livraison INT NOT NULL,
  PRIMARY KEY (livraison_id),
  FOREIGN KEY (camion_id) REFERENCES camions (camion_id)
);

CREATE TABLE colis (
  colis_id INT NOT NULL AUTO_INCREMENT,
  livraison_id INT NOT NULL,
  adresse_x FLOAT NOT NULL,
  adresse_y FLOAT NOT NULL,
  etat_colis TINYINT NOT NULL,
  PRIMARY KEY (colis_id),
  FOREIGN KEY (livraison_id) REFERENCES livraisons (livraison_id)
);

INSERT INTO camions (camion_pos_x, camion_pos_y) VALUES (0, 0), (0, 0), (0, 0);