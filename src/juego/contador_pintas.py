class ContadorPintas:
    """
    Clase para contar apariciones de una pinta específica en una colección de dados.
    
    Soporta funcionalidad básica de conteo y opcionalmente puede tratar los Ases
    como comodines que suman a cualquier pinta apostada.
    """
    
    def contar_pinta(self, dados, pinta, ases_comodines=False):
        """
        Cuenta las apariciones de una pinta específica en todos los dados proporcionados.
        
        Args:
            dados: Lista de objetos Dado o Mock con atributo 'valor'
            pinta: Entero entre 1 y 6 representando la pinta a contar
                  1=As, 2=Tonto, 3=Tren, 4=Cuadra, 5=Quina, 6=Sexto
            ases_comodines: Boolean que indica si los Ases (pinta 1) deben actuar como
                          comodines sumándose a la pinta buscada. Por defecto False.
        
        Returns:
            int: Número de dados que tienen la pinta solicitada, incluyendo Ases
                 como comodines si está habilitado
            
        Raises:
            ValueError: Si la pinta no está en el rango válido (1-6)
        """
        # Validar entrada
        if pinta < 1 or pinta > 6:
            raise ValueError("La pinta debe estar entre 1 y 6")
        
        contador = 0
        
        for dado in dados:
            # Contar apariciones exactas de la pinta
            if dado.valor == pinta:
                contador += 1
            # Si los comodines están activados y el dado es un As (pinta 1)
            # y NO estamos contando Ases directamente, sumar como comodín
            elif ases_comodines and dado.valor == 1 and pinta != 1:
                contador += 1
        
        return contador
