class ContadorPintas:
    """
    Clase para contar apariciones de una pinta específica en una colección de dados.
    
    Implementa las reglas del juego Dudo tradicional chileno:
    - Conteo básico de pintas específicas
    - Ases como comodines (modo normal)
    - Modo especial (ronda de un dado) donde los Ases NO son comodines
    """
    
    def contar_pinta(self, dados, pinta, ases_comodines=False, modo_especial=False):
        """
        Cuenta las apariciones de una pinta específica en todos los dados proporcionados.
        
        Args:
            dados: Lista de objetos Dado o Mock con atributo 'valor'
            pinta: Entero entre 1 y 6 representando la pinta a contar
                  1=As, 2=Tonto, 3=Tren, 4=Cuadra, 5=Quina, 6=Sexto
            ases_comodines: Boolean que indica si los Ases (pinta 1) deben actuar como
                          comodines sumándose a la pinta buscada. Por defecto False.
            modo_especial: Boolean que indica si se está en ronda especial (un dado).
                         En este modo, los Ases NO actúan como comodines sin importar
                         el flag ases_comodines. Por defecto False.
        
        Returns:
            int: Número de dados que tienen la pinta solicitada, incluyendo Ases
                 como comodines si corresponde según las reglas
            
        Raises:
            ValueError: Si la pinta no está en el rango válido (1-6)
            
        Reglas del juego Dudo:
            - Modo normal: Los Ases pueden actuar como comodines si ases_comodines=True
            - Modo especial: Los Ases NUNCA actúan como comodines (precedencia sobre ases_comodines)
            - Los Ases NO actúan como comodines de sí mismos en ningún modo
        """
        # Validar entrada
        if pinta < 1 or pinta > 6:
            raise ValueError("La pinta debe estar entre 1 y 6")
        
        contador = 0
        
        for dado in dados:
            # Contar apariciones exactas de la pinta
            if dado.valor == pinta:
                contador += 1
            # Evaluar si el As debe actuar como comodín
            elif dado.valor == 1 and pinta != 1:  # Es un As y no estamos contando Ases
                # En modo especial, los Ases NUNCA son comodines
                if modo_especial:
                    continue  # No sumar el As como comodín
                # En modo normal, solo si ases_comodines está activado
                elif ases_comodines:
                    contador += 1
        
        return contador
