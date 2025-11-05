# Template de Docstrings

Abaixo está um exemplo de como escrever docstrings no formato Google-style, para que o Sphinx e o Napoleon gerem a documentação corretamente.

```python
class Classe:
    """Explica de forma breve o propósito da classe.

    Attributes:
        atributo1 (str): Descreve o que é o atributo1.
        atributo2 (int): Descreve o que é o atributo2.
    """

    def funcao1(self) -> None:
        """Descreve o que essa função faz.

        Returns:
            None
        """
        pass

    def funcao2(self, parametro: str) -> None:
        """Explica o propósito da função.

        Args:
            parametro (str): Explica o que é esse parâmetro.

        Returns:
            None
        """
        pass

    def funcao3(self, parametro: int) -> float:
        """Explica o que a função faz e o que ela retorna.

        Args:
            parametro (int): Descreve o parâmetro usado.

        Returns:
            float: Resultado do processamento.
        """
        return float(parametro)

    def funcao4(self, parametro: int) -> float:
        """Explica o que a função faz, o que ela retorna e os tratamentos de erros da mesma.

        Args:
            parametro (int): Descreve o parâmetro usado.

        Returns:
            list: Resultado do processamento.

        Raises:
            ValueError: Se parametro não for uma lista.
        """
        return parametro
