from ftplib import FTP
from src.logging import registros
import os

diretorio_atual = os.path.dirname(os.path.realpath(__file__))
log = registros()


def baixar_extensao_especifica():
    # Pergunta ao usuário a forma de download, sendo alguma extensão especifica ou não
    try:
        condicao_baixar = input(
            "Gostaria de baixar com alguma extensão específica? Digite 0 (para não) ou 1 (para sim):"
        )

        if condicao_baixar != "1":
            print("Nenhuma extensão específica selecionada.\n")
            return condicao_baixar
        return condicao_baixar
    except Exception as e:
        log.error(f"Erro na entrada da resposta da forma de download: {e}")
        raise


def passa_extensao_especifica(condicao_baixar):
    # Caso a condição de download seja igual a 1, requisita a entrada do tipo de extensão
    try:
        if condicao_baixar == "1":
            print(
                "Por favor, informe o tipo de extensão desejada. Exemplos disponíveis:\n"
            )
            print(
                """
            .txt  - Arquivo de texto simples.
            .jpg  - Imagem no formato JPEG.
            .pdf  - Documento em formato PDF (Portable Document Format).
            .docx - Documento de texto do Microsoft Word.
            .xlsx - Planilha do Microsoft Excel.
            .mp3  - Arquivo de áudio no formato MP3.
            .mp4  - Arquivo de vídeo no formato MP4.
            .zip  - Arquivo compactado no formato ZIP.
            .html - Arquivo de código HTML para páginas da web.
            .exe  - Arquivo executável em sistemas Windows.
            """
            )
            tipo_extensao = input("\nDigite a extensão desejada (ex: .txt):")
            print(f"Você escolheu a extensão: {tipo_extensao}\n")
            return tipo_extensao
        elif (
            condicao_baixar != "1"
        ):  # Se a resposta for diferente de 1 retorna None para extensão
            tipo_extensao = None
            return tipo_extensao
    except Exception as e:
        log.error(f"Erro na entrada da resposta do tipo de extensão: {e}")
        raise


def requisita_credenciais():
    # Pergunta as informações de acesso para requisição ao servidor FTP
    try:
        print("Preencha as informações a seguir para iniciar a conexão:")

        host = input("Endereço do host (exemplo: ftp.us.debian.org):").strip()
        if not host:
            print("O endereço de host é obrigatório.")
            return requisita_credenciais()  # Retorna função

        port = input("Porta para conexão (o padrão é 21):").strip()
        if not port:
            port = 21  # Porta padrão caso esteja vazia
        else:
            try:
                port = int(port)
            except ValueError:
                print("A porta deve ser um número. Usando o padrão (21)")

        print("\nPreencha as credenciais, caso não tenha, deixar em branco:")

        # Se não houver usuário e senha definidas, defini como None
        usuario = input("Usuário de acesso:").strip()
        if not usuario:
            usuario = None

        senha = input("Senha de acesso:").strip()
        if not senha:
            senha = None

        return host, port, usuario, senha
    except Exception as e:
        log.error(f"Erro durante a requisição de credencias de acesso: {e}")
        raise


def iniciar_conexao(host, port=21, usuario=None, senha=None):
    try:
        # Estabelece conexão
        ftp = FTP(timeout=5, encoding="utf-8")
        ftp.connect(host=host, port=port)
        log.info("Conexão estabelecida com %s na porta %s.", host, port)

        # Realiza login como usuário ou anônimo
        if usuario or senha:
            ftp.login(user=usuario, passwd=senha)
            log.info(f"Acesso como usuário: {usuario}. Diretório atual: %s", ftp.pwd())
        else:
            ftp.login()
            log.info("Acesso como anônimo. Diretório atual: %s", ftp.pwd())

        return ftp
    except Exception as e:
        log.error("Erro ao iniciar conexão: %s", e)
        # Garante o encerramento da conexão
        finalizar_conexao(ftp)
        raise


def _adiciona_informacao(
    partes, tipo_letra, diretorio_completo, diretorios_navegados, fila
):
    # Caso as informações coletada com o parâmetro dir tenha o "tipo_letra" acrescentamos dentro da lista "fila"
    if partes[0].startswith(tipo_letra):
        if (
            diretorio_completo not in diretorios_navegados
        ):  # adiciona somente se o diretorio encontrado não esteja dentro de navegados
            fila.append(diretorio_completo)
            diretorios_navegados.add(diretorio_completo)
            log.info(
                f"Verificação realizada, informação adicionada: tipo: {tipo_letra}."
            )
            return True
    return False


def _baixar_arquivo(ftp, diretorio_completo):
    # Faz a transferencia do dado encontrado para a pasta local files dentro de src
    nome_arquivo = diretorio_completo.split("/")[-1]
    try:
        os.makedirs(os.path.join(diretorio_atual, "files"), exist_ok=True)

        with open(
            os.path.join(diretorio_atual, "files", nome_arquivo), "wb"
        ) as arquivo_local:
            ftp.retrbinary(f"RETR {diretorio_completo}", arquivo_local.write)
        log.info(f"Arquivo baixado com sucesso: {nome_arquivo}")
    except FileExistsError:
        pass
    except Exception as e:
        log.warning(f"Erro ao baixar arquivo {nome_arquivo}: {e}")


def _baixar_arquivo_com_extensao_especifica(
    ftp, partes, diretorio_completo, tipo_extensao
):
    # Condição para a função _baixar_arquivo, no entanto com a de extensão especificada
    if partes[-1].endswith(tipo_extensao):
        _baixar_arquivo(ftp, diretorio_completo)


def raspagem_sevidor(
    ftp,
    profundidade_maxima=10,
    condicao_baixar=False,
    tipo_extensao=None,
):
    try:
        # Realiza a navegação e download dos dados baseando-se nos dirétorios encontrados

        diretorios_navegados = set()
        profundidade_diretorio = 0
        fila = [""]

        # Laço para garantir que a fila e a profunidade não ultrapassem a profundidade máxima de diretórios
        while fila and profundidade_diretorio != profundidade_maxima:
            log.info(
                f"Processando nível {profundidade_diretorio}. Diretórios na fila: {len(fila)}"
            )
            diretorio_atual = fila.pop(
                0
            )  # Realiza a adição do diretório encontrado dentro da fila
            try:

                conteudo_diretorio = []
                ftp.dir(
                    diretorio_atual, conteudo_diretorio.append
                )  # Coleta as informações do diretório mapeado

                for inf in conteudo_diretorio:
                    log.info(f"Verificando entrada: {inf}")
                    partes = inf.split()
                    nome = partes[-1]
                    diretorio_completo = f"{diretorio_atual}/{nome}".strip("/")

                    # Faz a adição das informações desde que o tipo de dado inicie com a letra d "diretório" ou l "link de diretório"
                    if _adiciona_informacao(
                        partes=partes,
                        tipo_letra="d",
                        diretorio_completo=diretorio_completo,
                        diretorios_navegados=diretorios_navegados,
                        fila=fila,
                    ):
                        log.info(
                            f"Diretório encontrado e adicionado: {diretorio_completo}"
                        )

                    elif _adiciona_informacao(
                        partes=partes,
                        tipo_letra="l",
                        diretorio_completo=diretorio_completo,
                        diretorios_navegados=diretorios_navegados,
                        fila=fila,
                    ):

                        log.info(
                            f"Link simbólico encontrado e adicionado: {diretorio_completo}"
                        )

                    # Baixa o dado encontrado baseando-se no parâmetro passado inicialmente pelo usuário (todos os dados ou somente x extensão)
                    elif partes[0].startswith("-"):
                        if condicao_baixar != "1":
                            log.info(f"Arquivo encontrado: {diretorio_completo}")
                            _baixar_arquivo(ftp, diretorio_completo)
                        elif condicao_baixar == "1":
                            log.info(f"Arquivo encontrado: {diretorio_completo}")
                            _baixar_arquivo_com_extensao_especifica(
                                ftp, partes, diretorio_completo, tipo_extensao
                            )

            except Exception as e:
                log.error(f"Erro ao processar {diretorio_atual}: {e}")

            profundidade_diretorio += 1

        log.info("Processamento concluído.")
    except Exception as e:
        log.error(f"Erro ao tentar navegar/coletar as informações do sevidor: {e}")


def finalizar_conexao(ftp):
    # Realiza o fechamento da conexão caso esteja aberta
    try:
        if "ftp" in locals():
            ftp.quit()
            log.info("Conexão fechada com sucesso!")
    except Exception as e:
        log.error("Erro ao tentar encerrar a conexão %s", e)
