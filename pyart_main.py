import matplotlib.pyplot as plt
import pyart
from CemadenPull import CemadenPull
from balao import balao
import csv
import os
from pathlib import Path
import manage

class pyart_main:
    radar = pyart.aux_io.read_sinarame_h5("2020050606400300dBZ.vol.h5")  # "2020050606400300dBZ.vol.h5")
    angle = 0
    elevation_step = 0
    radar_altitude = 80
    radar_longitude = -35.5
    radar_latitude = -5.9
    raio = 566614.9
    file = CemadenPull()
    arq = "2020050606400300dBZ.vol.h5"

    def __init__(self):
        # Utilizando biblioteca pyart
        print("lendo radar com pyart")
        self.file = CemadenPull()
        try:
            self.arq = self.file.get_arquivo_last()
            self.radar = pyart.aux_io.read_sinarame_h5(self.arq)  # "2020050606400300dBZ.vol.h5")
        except:
            # noinspection PyPackageRequirements
            try:
                self.arq = self.file.get_arquivo_last(1)
                self.radar = pyart.aux_io.read_sinarame_h5(self.arq)  # "2020050606400300dBZ.vol.h5")
            except:
                try:
                    self.arq = self.file.get_arquivo_last(2)
                    self.radar = pyart.aux_io.read_sinarame_h5(self.arq)  # "2020050606400300dBZ.vol.h5")
                except:
                    try:
                        self.arq = self.file.get_arquivo_last(3)
                        self.radar = pyart.aux_io.read_sinarame_h5(self.arq)  # "2020050606400300dBZ.vol.h5")
                    except:
                        print("Problemas na aquisição de dados, dados defasados")
                        self.radar = pyart.aux_io.read_sinarame_h5("2020050606400300dBZ.vol.h5")
        self.radar_altitude = self.radar.altitude['data'][0]
        self.radar_longitude = self.radar.longitude['data'][0]
        self.radar_latitude = self.radar.latitude['data'][0]
        self.elevation_step = 0
        baloon = balao()
        self.raio, _ = baloon.get_distancia_radar(self.radar_latitude, self.radar_longitude, self.radar_altitude)
        _, self.elevation_step = baloon.get_angulo_radar(self.radar_altitude)
        print("posicao do radar: latitude = " + str(self.radar_latitude) + " longitude = " + str(
            self.radar_longitude) + " altitude = " + str(self.radar_altitude))
        self.angle = baloon.get_angulo_true_noth(self.radar_latitude, self.radar_longitude)
        print("distancia 2d da antena: " + str(self.raio))
        print("inclinacao relativa (step): " + str(self.elevation_step))

    def get_refletividade(self):
        # Corrigindo problema Associando a refletividade aos valores binários de dBZ
        self.radar.fields['reflectivity']['units'] = 'dBZ'
        xsect = pyart.util.cross_section_ppi(self.radar, [self.angle])  # 0 a 360 graus (angulo de rotação true north)
        # considerando o range do radar = 250km (meters between gates)
        # data[999]=250km data[0.25*raio_metros/1000]= reflectivity no raio
        # sweep 0 a 12 (passo de elevação 0.5 graus / passo 0 init=0.5degrees)
        print("Dados de reflectivity")
        refletivity = xsect.fields['reflectivity']['data'][self.elevation_step][
                  int(self.raio / xsect.range['meters_between_gates'])]
        print(refletivity)
        BASE_DIR = Path(__file__).resolve().parent
        arquivo = os.path.join(BASE_DIR, 'Tupan_2')
        arquivo = os.path.join(arquivo, 'base')
        arquivo = os.path.join(arquivo, 'static')
        arquivo = os.path.join(arquivo, 'downloads')
        arquivo = os.path.join(arquivo, 'csv_default.csv')
        with open(arquivo, 'w', newline='') as csvfile:
            to_be_writed = csv.writer(csvfile, delimiter=';')
            to_be_writed.writerow([str(refletivity)])
        return xsect.fields['reflectivity']['data'][self.elevation_step][
            int(self.raio / xsect.range['meters_between_gates'])]

    def plot_ppi(self):
        # Plotando PPI elevação 0.5 graus (fixed angle?)
        # Corrigindo problema Associando a refletividade aos valores binários de dBZ
        display = pyart.graph.RadarDisplay(self.radar)
        self.radar.fields['reflectivity']['units'] = 'dBZ'
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        display.plot('reflectivity', 0, vmin=-32, vmax=64., cmap='pyart_NWSRef')
        display.plot_range_rings([50, 100, 150, 250])
        plt.show()

    def plot_rhi(self):
        # Plotando RHI
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        # Selecionando seção ppi para realizar o rhi
        xsect = pyart.util.cross_section_ppi(self.radar, [self.angle])  # 0 a 360 graus (angulo de rotação true north)
        display = pyart.graph.RadarDisplay(xsect)
        display.set_limits(ylim=[0, 15])
        display.set_limits(xlim=[0, 250])
        display.plot('reflectivity', 0, vmin=-32, vmax=64., cmap='pyart_NWSRef')
        plt.show()

    # radarnatal http://www.cemaden.gov.br/mapainterativo/download/downradares.php?radar=natal&produto=vol_250km_13steps.vol
    # arquivo 2021011921400200dBZ.vol.h5


start = pyart_main()
start.plot_rhi()
start.plot_ppi()
start.get_refletividade()
