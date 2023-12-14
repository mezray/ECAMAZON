// Importez les bibliothèques React nécessaires
import React, { useState } from 'react';
import axios from 'axios';

// The rest of your code...

function App() {

  // Définissez les états pour stocker les données du formulaire
  const [colisData, setColisData] = useState({
    id: '',
    adresse_x: '',
    adresse_y: ''
  });
  // Ajoutez un nouvel état pour stocker les données de la position du colis
  const [posColisData, setPosColisData] = useState({
    colis_id: '',
    etat_colis: ''
  });

  // Ajoutez un nouvel état pour stocker les données du camion
  const [camionData, setCamionData] = useState({
    camion_id: '',
    camion_pos_x: '',
    camion_pos_y: ''
  });

  // Ajoutez un nouvel état pour stocker les données de livraison
  const [livraisonData, setLivraisonData] = useState([]);


  // Définissez les gestionnaires d'événements pour mettre à jour les états
  const handleColisChange = (e) => {
    setColisData({ ...colisData, [e.target.name]: e.target.value });
  };

  // Ajoutez un nouveau gestionnaire d'événements pour mettre à jour l'état de la position du colis
  const handlePosColisChange = (e) => {
    setPosColisData({ ...posColisData, [e.target.name]: e.target.value });
  };

  // Ajoutez un nouveau gestionnaire d'événements pour mettre à jour l'état du camion
  const handleCamionChange = (e) => {
    setCamionData({ ...camionData, [e.target.name]: e.target.value });
  };

  // Ajoutez une nouvelle fonction pour envoyer la requête API
  const getLivraison = async () => {
    try {
      const response = await axios.get('http://localhost:5000/getLivraison');
      setLivraisonData(response.data);
    } catch (error) {
      console.error('Erreur lors de la récupération des données de livraison', error);
    }
  };

  // Définissez les fonctions pour envoyer les requêtes API
  const addColis = async () => {
    try {
      const response = await axios.post('http://localhost:5000/add_colis', colisData);
      console.log(response.data);
    } catch (error) {
      console.error('Erreur lors de l\'ajout de colis', error);
    }
  };

  // Ajoutez une nouvelle fonction pour envoyer la requête API
  const postPosColis = async () => {
    try {
      const response = await axios.post('http://localhost:5000/postPosColisFromDevice', posColisData);
      console.log(response.data);
    } catch (error) {
      console.error('Erreur lors de la mise à jour de la position du colis', error);
    }
  };

  // Ajoutez une nouvelle fonction pour envoyer la requête API
  const postPosCamion = async () => {
    try {
      const response = await axios.post('http://localhost:5000/postPosCamionFromDevice', camionData);
      console.log(response.data);
    } catch (error) {
      console.error('Erreur lors de la mise à jour de la position du camion', error);
    }
  };


  return (
    <div>
      <h1>Ajouter un Colis</h1>
      <form>
        <div>
          <label>ID:</label>
          <input type="text" name="id" onChange={handleColisChange} />
        </div>
        <div>
          <label>Adresse X:</label>
          <input type="text" name="adresse_x" onChange={handleColisChange} />
        </div>
        <div>
          <label>Adresse Y:</label>
          <input type="text" name="adresse_y" onChange={handleColisChange} />
        </div>
        <div>
          <button type="button" onClick={addColis}>Ajouter Colis</button>
        </div>
      </form>

      <h1>Modifier la Position du Colis</h1>
      <form>
        <div>
          <label>Colis ID:</label>
          <input type="text" name="colis_id" onChange={handlePosColisChange} />
        </div>
        <div>
          <label>Nouvel État du Colis:</label>
          <input type="text" name="etat_colis" onChange={handlePosColisChange} />
        </div>
        <button type="button" onClick={postPosColis}>Modifier Position du Colis</button>
      </form>

      <h1>Modifier la Position du Camion</h1>
      <form>
        <div>
          <label>Camion ID:</label>
          <input type="text" name="camion_id" onChange={handleCamionChange} />
        </div>
        <div>
          <label>Nouvelle Position X du Camion:</label>
          <input type="text" name="camion_pos_x" onChange={handleCamionChange} />
        </div>
        <div>
          <label>Nouvelle Position Y du Camion:</label>
          <input type="text" name="camion_pos_y" onChange={handleCamionChange} />
        </div>
        <button type="button" onClick={postPosCamion}>Modifier Position du Camion</button>
      </form>
      <h1>Données de Livraison</h1>
      <button type="button" onClick={getLivraison}>Récupérer les données de livraison</button>
      <table>
        <thead>
          <tr>
            <th>Livraison ID</th>
            <th>Colis ID</th>
            <th>Adresse X</th>
            <th>Adresse Y</th>
            <th>État du Colis</th>
          </tr>
        </thead>
        <tbody>
          {livraisonData.map((livraison, index) => (
            <tr key={index}>
              <td>{livraison.livraison_id}</td>
              <td>{livraison.colis_id}</td>
              <td>{livraison.adresse_x}</td>
              <td>{livraison.adresse_y}</td>
              <td>{livraison.etat_colis}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>

  );
}

export default App;
