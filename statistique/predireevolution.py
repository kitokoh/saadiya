import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class LogAnalyzer:
    def __init__(self, log_directory):
        self.log_directory = log_directory
        self.data = None

    def read_log_file(self, file_name):
        log_path = os.path.join(self.log_directory, file_name)
        # Lire le fichier log en supposant qu'il est formaté en CSV
        self.data = pd.read_csv(log_path)

    def analyze_data(self):
        # Assumer que la colonne 'timestamp' contient des dates et 'value' contient des valeurs à analyser
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data.set_index('timestamp', inplace=True)
        
        # Resampler les données par jour (ou tout autre intervalle souhaité)
        self.data = self.data.resample('D').sum()  # Remplacez 'sum' par 'mean' selon vos besoins
        
        return self.data

    def predict_future(self, periods=30):
        # Modèle de prévision avec lissage exponentiel
        model = ExponentialSmoothing(self.data['value'], trend='add', seasonal='add', seasonal_periods=7)
        fit = model.fit()
        forecast = fit.forecast(periods)
        return forecast

    def plot_results(self, forecast):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data['value'], label='Données Historiques', color='blue')
        plt.plot(forecast.index, forecast, label='Prévisions', color='orange')
        plt.title('Analyse et Prévision des Logs')
        plt.xlabel('Date')
        plt.ylabel('Valeurs')
        plt.legend()
        plt.grid()
        plt.show()

# Utilisation de la classe
if __name__ == "__main__":
    # Remplacez par le chemin vers votre répertoire contenant le fichier log
    log_directory = "C:/chemin/vers/votre/répertoire"
    
    # Création d'une instance de la classe
    log_analyzer = LogAnalyzer(log_directory)
    
    # Lire le fichier log (remplacez 'log_file.csv' par le nom réel de votre fichier)
    log_analyzer.read_log_file('log_file.csv')
    
    # Analyser les données
    data = log_analyzer.analyze_data()
    
    # Prévoir l'évolution future
    forecast = log_analyzer.predict_future(periods=30)
    
    # Tracer les résultats
    log_analyzer.plot_results(forecast)
