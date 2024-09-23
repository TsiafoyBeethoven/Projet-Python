import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QComboBox, QHBoxLayout, QGroupBox, QStatusBar
from PyQt5.QtCore import Qt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class ProjetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Analyse de Données')
        self.setGeometry(100, 100, 500, 400)
        
        # Barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        layout = QVBoxLayout()

        # GroupBox pour l'importation de fichier
        file_group = QGroupBox("Importer des Données")
        file_layout = QVBoxLayout()
        self.status_label = QLabel('Statut: Aucun fichier chargé', self)
        file_layout.addWidget(self.status_label)

        self.open_button = QPushButton('Ouvrir un fichier CSV ou XLS', self)
        self.open_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.open_button.clicked.connect(self.ouvrir_fichier)
        file_layout.addWidget(self.open_button)

        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # ComboBox pour choisir la méthode de visualisation
        self.visualisation_combo = QComboBox(self)
        self.visualisation_combo.addItems([
            'Choisir une visualisation',
            'Boxplot',
            'Pairplot',
            'Heatmap',
            'Violinplot'
        ])
        layout.addWidget(self.visualisation_combo)

        # Bouton de visualisation
        self.visualise_button = QPushButton('Visualiser', self)
        self.visualise_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        self.visualise_button.clicked.connect(self.visualiser_selection)
        layout.addWidget(self.visualise_button)

        # Bouton de nettoyage
        self.clean_button = QPushButton('Nettoyer les données', self)
        self.clean_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")
        self.clean_button.clicked.connect(self.nettoyer_fichier)
        layout.addWidget(self.clean_button)

        # Configuration du conteneur
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def ouvrir_fichier(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "Fichier CSV (*.csv);;Fichier Excel (*.xlsx)")
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.data = pd.read_csv(file_path)
                elif file_path.endswith('.xlsx'):
                    self.data = pd.read_excel(file_path)
                self.status_label.setText(f'Fichier chargé: {file_path}')
                self.status_bar.showMessage(f'Fichier chargé: {file_path}', 5000)
            except Exception as e:
                self.status_label.setText(f"Echec du chargement: {str(e)}")
                self.data = None

    def visualiser_selection(self):
        choice = self.visualisation_combo.currentText()
        if choice == 'Boxplot':
            self.visualiser_boxplot()
        elif choice == 'Pairplot':
            self.visualiser_pairplot()
        elif choice == 'Heatmap':
            self.visualiser_heatmap()
        elif choice == 'Violinplot':
            self.visualiser_violinplot()
        else:
            self.status_label.setText('Veuillez choisir une visualisation.')

    def visualiser_boxplot(self):
        if self.data is not None:
            numeric_data = self.data.select_dtypes(include=['float64', 'int64'])
            if numeric_data.empty:
                self.status_label.setText('Aucune donnée numérique à visualiser.')
                return
            
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=numeric_data)
            plt.title('Boxplot des colonnes numériques')
            plt.xticks(rotation=45)
            plt.show()

    def visualiser_pairplot(self):
        if self.data is not None:
            numeric_data = self.data.select_dtypes(include=['float64', 'int64'])
            if numeric_data.empty:
                self.status_label.setText('Aucune donnée numérique à visualiser.')
                return
            
            sns.pairplot(numeric_data)
            plt.show()

    def visualiser_heatmap(self):
        if self.data is not None:
            numeric_data = self.data.select_dtypes(include=['float64', 'int64'])
            if numeric_data.empty:
                self.status_label.setText('Aucune donnée numérique à visualiser.')
                return
            
            plt.figure(figsize=(10, 6))
            corr = numeric_data.corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Heatmap des corrélations')
            plt.show()

    def visualiser_violinplot(self):
        if self.data is not None:
            numeric_data = self.data.select_dtypes(include=['float64', 'int64'])
            if numeric_data.empty:
                self.status_label.setText('Aucune donnée numérique à visualiser.')
                return
            
            plt.figure(figsize=(10, 6))
            sns.violinplot(data=numeric_data)
            plt.title('Violinplot des colonnes numériques')
            plt.xticks(rotation=45)
            plt.show()

    def nettoyer_fichier(self):
        if self.data is not None:
            fichier_nettoye = self.data.dropna()
            self.data = fichier_nettoye
            self.status_label.setText('Nettoyage réussi.')
        else:
            self.status_label.setText('Aucun fichier à nettoyer.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProjetApp()
    window.show()
    sys.exit(app.exec_())
