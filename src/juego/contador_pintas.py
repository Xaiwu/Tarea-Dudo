class ContadorPintas:
    """
    Clase para contar apariciones de una pinta específica en una colección de dados.
    
    En esta implementación básica, cuenta únicamente las apariciones exactas
    de la pinta solicitada, sin funcionalidad de comodines.
    """
    
    def contar_pinta(self, dados, pinta):
        """
        Cuenta las apariciones de una pinta específica en todos los dados proporcionados.
        
        Args:
            dados: Lista de objetos Dado o Mock con atributo 'valor'
            pinta: Entero entre 1 y 6 representando la pinta a contar
                  1=As, 2=Tonto, 3=Tren, 4=Cuadra, 5=Quina, 6=Sexto
        
        Returns:
            int: Número de dados que tienen exactamente la pinta solicitada
            
        Raises:
            ValueError: Si la pinta no está en el rango válido (1-6)
        """
        # Validar entrada
        if pinta < 1 or pinta > 6:
            raise ValueError("La pinta debe estar entre 1 y 6")
        
        # Contar apariciones exactas de la pinta
        contador = 0
        for dado in dados:
            if dado.valor == pinta:
                contador += 1
        
        return contador
