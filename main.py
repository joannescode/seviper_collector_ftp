from src.logging import registros
from src.seviper import (
    baixar_extensao_especifica,
    passa_extensao_especifica,
    requisita_credenciais,
    iniciar_conexao,
    raspagem_sevidor,
    finalizar_conexao,
)

log = registros()


def main():
    try:
        condicao_baixar = baixar_extensao_especifica()  # interação com o usuário
        tipo_extensao = passa_extensao_especifica(
            condicao_baixar
        )  # interação com o usuário
        host, port, usuario, senha = requisita_credenciais()  # interação com o usuário

        ftp = iniciar_conexao(
            host=host, port=port, usuario=usuario, senha=senha
        )  # abertura da conexão

        # coleta das informações (diretórios e dados)
        raspagem_sevidor(
            ftp=ftp,
            profundidade_maxima=50,
            condicao_baixar=condicao_baixar,
            tipo_extensao=tipo_extensao,
        )

    except Exception as e:
        log.error("Erro durante execução: %s", e)

    finally:
        finalizar_conexao(ftp=ftp)  # fechamento da conexão


if __name__ == "__main__":
    main()
