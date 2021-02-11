import requests
from datetime import datetime


# montando a string
# http://www.cemaden.gov.br/mapainterativo/download/downradares.php?radar=natal&produto=vol_250km_13steps.vol

class CemadenPull:
    add = 'http://www.cemaden.gov.br/mapainterativo/download/downradares.php?radar=natal&produto=vol_250km_13steps.vol'\
          '&arquivo='
    agora = datetime.now()
    mes = str(agora.month)
    minutos = str(agora.minute)
    hora = str(agora.hour + 3)  # GMT Brasil == -3
    day = str(agora.day)
    year = str(agora.year)
    arquivo_name = ""
    alternative_arquivo_name = ""

    def __init__(self):
        # corrigindo as strings
        if int(self.mes) < 10:
            self.mes = "0" + self.mes
        if int(self.day) < 10:
            self.day = "0" + str(self.day)
        if int(self.minutos) < 10:
            self.minutos = "00"
        else:
            self.minutos = str(int(self.minutos) - (int(self.minutos) % 10))
        if int(self.hora) < 10:
            self.hora = "0" + self.hora
        # montando os nomes dos arquivos
        self.arquivo_name = self.year + self.mes + self.day + self.hora + self.minutos
        self.alternative_arquivo_name = self.arquivo_name + "0300dBZ.vol.h5"
        self.arquivo_name = self.arquivo_name + "0200dBZ.vol.h5"

    # toda requisicao mal sucedida precisa reduzir o nome dos arquivos em 10 minutos
    # busca do ultimo arquivo disponível
    def reduzir_10_minutos(self):
        if int(self.minutos) >= 10:
            self.minutos = str(int(self.minutos) - 10)
        elif int(self.hora) >= 1:
            self.minutos = "50"
            self.hora = str(int(self.hora) - 1)
        elif int(self.day) >= 1:
            self.hora = "23"
            self.minutos = "50"
            self.day = str(int(self.day) - 1)
        elif int(self.mes) > 1:
            self.hora = "23"
            self.minutos = "50"
            self.day = self.__get_last_day(int(self.mes) - 1)
            self.mes = str(int(self.mes) - 1)
        else:
            self.hora = "23"
            self.minutos = "50"
            self.day = "31"
            self.mes = "12"
        # corrigindo as strings
        if int(self.mes) < 10:
            self.mes = "0" + str(int(self.mes))
        if int(self.day) < 10:
            self.day = "0" + str(int(self.day))
        if int(self.minutos) < 10:
            self.minutos = "00"
        else:
            self.minutos = str(int(self.minutos) - (int(self.minutos) % 10))
        if int(self.hora) < 10:
            self.hora = "0" + str(int(self.hora))
        # montando os nomes dos arquivos
        self.arquivo_name = self.year + self.mes + self.day + self.hora + self.minutos
        self.alternative_arquivo_name = self.arquivo_name + "0300dBZ.vol.h5"
        self.arquivo_name = self.arquivo_name + "0200dBZ.vol.h5"

    def __get_last_day(self, mes):
        meses = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        anos_bissextos = [x for x in range(2020, 2100, 4)]
        print(anos_bissextos)
        try:
            anos_bissextos.index(int(self.year))
            meses[2] = 29
            return str(meses[int(mes)])
        except:
            return str(meses[int(mes)])

    def get_arquivo_last(self, atraso=0):
        in_use = "arquive_name"
        s = 0
        while atraso > 0:
            atraso -= 1
            self.reduzir_10_minutos()
        for i in range(0, 10):  # 5 tentativas com cada arquivo 50 minutos de atraso
            if in_use == "arquive_name":
                s = requests.get(self.add + self.arquivo_name, allow_redirects=True)
                if s.text != 'ERRO: o arquivo solicitado não existe!':
                    open(self.arquivo_name, 'wb').write(s.content)
                    break
                else:
                    in_use = "alternative_arquivo_name"
            else:
                s = requests.get(self.add + self.alternative_arquivo_name, allow_redirects=True)
                if s.text != 'ERRO: o arquivo solicitado não existe!':
                    open(self.alternative_arquivo_name, 'wb').write(s.content)
                    break
                else:
                    in_use = "arquive_name"
                    print("Retring")
            self.reduzir_10_minutos()
        if s.text == 'ERRO: o arquivo solicitado não existe!':
            print('Erro no download')
            print("Status Code: " + str(s.status_code))
            raise Exception("Erro")
        else:
            if in_use == "arquive_name":
                print("arquivo: " + self.arquivo_name + " baixado com sucesso")
                return self.arquivo_name
            else:
                print("arquivo: " + self.alternative_arquivo_name + " baixado com sucesso")
                return self.alternative_arquivo_name
