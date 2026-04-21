def mascarar_cpf(cpf: str) -> str:
    """
    Mascara CPF para exibição pública
    Ex: 123.456.789-00 → 123.***.***-**
    """
    if not cpf:
        return None
    
    cpf_limpo = re.sub(r'\D', '', cpf)
    
    if len(cpf_limpo) != 11:
        return cpf  # Retorna original se estiver inválido
    
    return f'{cpf_limpo[:3]}.***.***-**'