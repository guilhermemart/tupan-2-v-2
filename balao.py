from math import sqrt
from math import atan
from math import pi


class balao:
    altitude = 78.5
    latitude = -5.90449
    longitude = -35.25402
    dist_radar2d = 1000
    dist_radar3d = 1100
    degress = 0  # angulo true north

    def __init__(self, altitude=78.5, latitude=-6, longitude=-35.75412):
        self.altitude = altitude
        self.longitude = longitude
        self.latitude = latitude

    def get_distancia_radar(self, lat_radar, lon_radar, alt_radar):
        delta_lat = (self.latitude - lat_radar) * 2 * pi * 6371000 / 360
        delta_lon = (self.longitude - lon_radar) * 2 * pi * 6371000 / 360
        delta_alt = self.altitude - alt_radar
        self.dist_radar2d = sqrt(pow(delta_lat, 2) + pow(delta_lon, 2))  # distancia no plano da antena
        self.dist_radar3d = sqrt(pow(self.dist_radar2d, 2) + pow(delta_alt, 2))  # distancia balao a antena
        return self.dist_radar2d, self.dist_radar3d

    # calculo do angulo do balao em relacao a antena
    # radar trabalha com passos de 0.5 graus minimo de 0.5 graus e maximo de 7.5 graus
    # 0.5=step 0 7.5= step 13
    def get_angulo_radar(self, alt_radar):
        cateto_oposto = self.altitude - alt_radar
        hipotenusa = self.dist_radar3d
        angulo = 360*atan(cateto_oposto / abs(hipotenusa))/(2*pi)
        if angulo < 1:
            angulo = 0.5
            step = 0
        elif 1 <= angulo < 1.5:
            angulo = 1
            step = 1
        elif 1.5 <= angulo < 2:
            angulo = 1.5
            step = 2
        elif 2 <= angulo < 2.5:
            angulo = 2
            step = 3
        elif 2.5 <= angulo < 3:
            angulo = 2.5
            step = 4
        elif 3 <= angulo < 3.5:
            angulo = 3
            step = 5
        elif 3.5 <= angulo < 4:
            angulo = 3.5
            step = 6
        elif 4 <= angulo < 4.5:
            angulo = 4
            step = 7
        elif 4.5 <= angulo < 5:
            angulo = 4.5
            step = 8
        elif 5 <= angulo < 5.5:
            angulo = 5
            step = 9
        elif 5.5 <= angulo < 6:
            angulo = 6
            step = 10
        elif 6 <= angulo < 6.5:
            angulo = 6.5
            step = 11
        else: # 6.5 <= angulo:
            angulo = 7
            step = 12
        return angulo, step

    def get_angulo_true_noth(self, lat_radar, lon_radar):
        delta_lat = (self.latitude - lat_radar) * 2 * pi * 6371000 / 360
        delta_lon = (self.longitude - lon_radar) * 2 * pi * 6371000 / 360
        # Angulo true north 0 degres = 90 degres cartesianos
        # Os angulos aumentam no sentido horario (invertido do carttesiano)
        angulo_base = 90
        if delta_lat < 0 and delta_lon < 0:
            angulo_base = 270
        elif delta_lat < 0 and delta_lon > 0:
            angulo_base = 360
        elif delta_lat > 0 and delta_lon < 0:
            angulo_base = 180
        self.degress = angulo_base-atan(abs(delta_lon/delta_lat))
        return self.degress
