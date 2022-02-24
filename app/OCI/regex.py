import re

class Regex():
    """Classe para facilitar o processo de formatação com Regex"""

    def __init__(self):
        self=self


    def replace_dot(self, parameters):
        """
            Função que recebe um valor float, transoforma em string e então subistitui o ponto por virgula
            e no final retorna uma string formatada
        """
        value = format(parameters, '.2f')
        data = str(value)
        number = re.sub(r'(\d+)\.(\d+)',r"\1,\2", data)
        return number