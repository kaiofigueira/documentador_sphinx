import fileinput
import os
import shutil
import subprocess
import tkinter as tk
import sys
from tkinter import filedialog
from pathlib import Path

from safe_file_manager import SafeFileManager

# from weasyprint import HTML
# import pdfkit

class DocumentadorSphinx:
    """
    Classe para facilitar a documentação usando Sphinx.

    Attributes:
        source_dir (str): O diretório do código-fonte a ser documentado.
        output_dir (str): O diretório onde os arquivos HTML serão gerados.
        docs_dir (str): O diretório onde serão armazenados os documentos.
        api_docs_dir (str): O diretório onde serão armazenados os documentos da API.
    """
    
    def __init__(self, source_dir):
        """
        Inicializa a classe DocumentadorSphinx. Nela é atribuido onde será inserido o output do sistema, caminho da pasta documentos e da apidoc.

        Args:
            source_dir (str): O diretório do código-fonte a ser documentado.
        
        Returns:
            None
        """
        self.source_dir = source_dir

        # Diretorio onde os arquivos html serão gerados.
        self.output_dir = r'_build'

        self.docs_dir = r'documentos'
        self.html_dir = os.path.join(self.docs_dir, self.output_dir, r'html')
        self.api_docs_dir = os.path.join(self.docs_dir, r'apidoc')

        self.project_name = self.obter_nome_projeto()

    # def converter_html_para_pdf_weasyprint(self):
    #     """
    #     Converte os arquivos HTML gerados pelo Sphinx em arquivos PDF.

    #     Args:
    #         None

    #     Returns:
    #         None
    #     """
    #     # Verificar se o diretório de HTML existe
    #     html_dir = self.html_dir
    #     if not os.path.exists(html_dir):
    #         print("Diretório HTML não encontrado. Primeiro, execute a construção do HTML.")
    #         return

    #     # Verificar se os arquivos HTML necessários estão presentes
    #     required_files = ['genindex.html', 'index.html']  # Adicione outros arquivos HTML se necessário
    #     missing_files = [file for file in required_files if file not in os.listdir(html_dir)]
    #     if missing_files:
    #         print(f"Os seguintes arquivos HTML necessários estão faltando: {missing_files}")
    #         return

    #     # Criar um diretório para os arquivos PDF, se não existir
    #     pdf_dir = os.path.join(self.docs_dir, 'pdf')
    #     if not os.path.exists(pdf_dir):
    #         os.makedirs(pdf_dir)

    #     # Converter cada arquivo HTML para PDF usando WeasyPrint
    #     for html_file in os.listdir(html_dir):
    #         if html_file.endswith('.html'):
    #             input_path = os.path.join(html_dir, html_file)
    #             output_file = os.path.splitext(html_file)[0] + '.pdf'
    #             output_path = os.path.join(pdf_dir, output_file)
    #             HTML(filename=input_path).write_pdf(output_path)

    #     print("PDFs gerados com sucesso.")

    # def converter_html_para_pdf_pdfkit(self):
    #     """
    #     Converte os arquivos HTML gerados pelo Sphinx em arquivos PDF.

    #     Args:
    #         None

    #     Returns:
    #         None
    #     """
    #     # Verificar se o diretório de HTML existe
    #     html_dir = self.html_dir
    #     if not os.path.exists(html_dir):
    #         print("Diretório HTML não encontrado. Primeiro, execute a construção do HTML.")
    #         return

    #     # Verificar se os arquivos HTML necessários estão presentes
    #     required_files = ['genindex.html', 'index.html']  # Adicione outros arquivos HTML se necessário
    #     missing_files = [file for file in required_files if file not in os.listdir(html_dir)]
    #     if missing_files:
    #         print(f"Os seguintes arquivos HTML necessários estão faltando: {missing_files}")
    #         return

    #     # Criar um diretório para os arquivos PDF, se não existir
    #     pdf_dir = os.path.join(self.docs_dir, 'pdf')
    #     if not os.path.exists(pdf_dir):
    #         os.makedirs(pdf_dir)

    #     # Converter cada arquivo HTML para PDF
    #     for html_file in os.listdir(html_dir):
    #         if html_file.endswith('.html'):
    #             input_path = os.path.join(html_dir, html_file)
    #             output_file = os.path.splitext(html_file)[0] + '.pdf'
    #             output_path = os.path.join(pdf_dir, output_file)
    #             pdfkit.from_file(input_path, output_path)

    #     print("PDFs gerados com sucesso.")
        
    def obter_nome_projeto(self):
        """
        Obtem o nome do projeto.

        Args:
            None
        
        Returns:
            None
        """
        conf_path = os.path.join(self.docs_dir, 'conf.py')
        with open(conf_path, 'r') as conf_file:
            for line in conf_file:
                if line.startswith('project ='):
                    return line.split('=')[1].strip().strip("'").strip('"')

    def gerar_documentacao(self):
        """Gera a documentação usando o Sphinx."""
        source_dir = SafeFileManager.ensure_abs(self.source_dir)
        docs_dir = SafeFileManager.ensure_abs(self.docs_dir)
        api_docs_dir = SafeFileManager.ensure_abs(self.api_docs_dir)
        output_dir = SafeFileManager.ensure_abs(Path(self.docs_dir) / self.output_dir)

        # limpa pastas antigas
        delete_ok = True
        try:
            if api_docs_dir.exists():
                SafeFileManager.rmtree_safe(api_docs_dir)
            if output_dir.exists():
                SafeFileManager.rmtree_safe(output_dir)
        except PermissionError:
            delete_ok = False

        SafeFileManager.mkdir(api_docs_dir)
        SafeFileManager.mkdir(docs_dir)

        # usa python -m sphinx.ext.apidoc (funciona em qualquer SO)
        cmd = [
            sys.executable, "-m", "sphinx.ext.apidoc",
            "-f", "-e", "-M",
            "-o", str(api_docs_dir),
            str(source_dir),
        ]
        subprocess.run(cmd, check=True)

        print("Documentação criada com sucesso")

    def construir_html(self):
        """
        Constrói o output do sistema que são os arquivos HTML da documentação. A index.html encontra-se em 'documentos/_build/html/'

        Args:
            None

        Returns:
            None
        """

        # Mudar para o diretorio de documentação
        os.chdir(self.docs_dir)

        # Criar o diretorio do output, se ele não existir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Executar make html
        subprocess.run([r'.\make.bat', 'html'], check=True)

        # Voltar ao diretório original
        os.chdir('..')

        print("Html feito com sucesso")

    def construir_pdf(self):
        """
        Constrói o output do sistema que são os arquivos PDF da documentação.
        
        Args:
            None
            
        Returns:
            None
        """
        
        # Mudar para o diretório de documentação
        os.chdir(self.docs_dir)

        # Criar o diretório do output, se ele não existir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Executar make latex para gerar os arquivos LaTeX
        subprocess.run([r'.\make.bat', 'latexpdf'], check=True)

        # # Executar make para compilar o PDF a partir dos arquivos LaTeX
        # subprocess.run([r'.\make.bat', 'pdf'], check=True)
        #         # Executar make para compilar o PDF a partir dos arquivos LaTeX
        # subprocess.run([r'.\make.bat', 'all-pdf'], check=True)

        # Mover o PDF gerado para o diretório de output
        shutil.move(os.path.join(self.docs_dir, '_build', 'latex', self.project_name + '.pdf'), self.output_dir)

        # Voltar ao diretório original
        os.chdir('..')

        print("PDF feito com sucesso")
            
    
    def mudar_nome_projeto(self, nome_projeto):
        """
        Altera o nome do projeto na configuração do Sphinx.

        Args:
            nome (str): O novo nome do projeto.

        Returns:
            None
        """
        conf_file = os.path.join(self.docs_dir, 'conf.py')
        for line in fileinput.input(conf_file, inplace=True):
            if line.startswith('project = '):
                print(f"project = '{nome_projeto}'")
            else:
                print(line, end='')
        print("Alteração feita com sucesso.")

    def adicionar_documento(self, descricao: str) -> None:
        """
        Adiciona um arquivo .md aos docs e referencia no toctree do index.rst.
        """
        root = tk.Tk()
        root.withdraw()

        caminho_md = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
        if not caminho_md:
            print("Operação cancelada.")
            return

        docs_dir = Path(self.docs_dir)
        docs_dir.mkdir(parents=True, exist_ok=True)

        src_md = Path(caminho_md)
        nome_arquivo = src_md.name
        nome_sem_ext = src_md.stem
        dst_md = docs_dir / nome_arquivo

        # Copia preservando metadata
        shutil.copy2(src_md, dst_md)

        # Garante que o .md tem um título H1 para não virar <no title>
        try:
            texto = dst_md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # se o arquivo original não for UTF-8, lê em cp1252 e regrava em UTF-8
            texto = dst_md.read_text(encoding="cp1252", errors="replace")
        if not texto.lstrip().startswith("# "):
            # coloca H1 com a descrição no topo
            texto = f"# {descricao}\n\n{texto}"
            dst_md.write_text(texto, encoding="utf-8", newline="\n")

        # Atualiza o index.rst (sempre em UTF-8)
        index_path = docs_dir / "index.rst"
        if not index_path.exists():
            raise FileNotFoundError(f"index.rst não encontrado em {index_path}")

        linhas = index_path.read_text(encoding="utf-8").splitlines(keepends=True)

        # Encontra o bloco .. toctree:: e insere a referência (sem extensão)
        entrada = f"   {nome_sem_ext}\n"

        # não duplica
        if any(l.strip() == nome_sem_ext for l in linhas):
            print("Documento já referenciado no toctree.")
            return

        i = 0
        while i < len(linhas) and linhas[i].strip() != ".. toctree::":
            i += 1
        if i == len(linhas):
            raise RuntimeError("Bloco '.. toctree::' não encontrado no index.rst.")

        # pula opções do toctree (linhas começando com 3 espaços e dois-pontos)
        j = i + 1
        while j < len(linhas) and (linhas[j].startswith("   :") or linhas[j].strip() == ""):
            j += 1

        # insere a entrada logo após o cabeçalho/opções (antes de outras entradas)
        linhas.insert(j, entrada)

        # salva em UTF-8 sempre
        index_path.write_text("".join(linhas), encoding="utf-8", newline="\n")

        print("Adição feita com sucesso.")
    def deletar_documento(self, nome_arquivo):
        """
        Deleta um documento da documentação.

        Args:
            nome_arquivo (str): O nome do arquivo a ser deletado.

        Returns:
            None
        """
        import os

        # Passo 1: Deletar o arquivo da pasta 'documentos'
        arquivo_md = os.path.join(self.docs_dir, nome_arquivo + '.md')
        if os.path.exists(arquivo_md):
            os.remove(arquivo_md)

        # Passo 2: Remover o nome do arquivo do arquivo 'index.rst'
        index_rst_file = os.path.join(self.docs_dir, 'index.rst')

        # Usa encoding UTF-8 pra evitar UnicodeDecodeError no Windows
        with open(index_rst_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Iterar sobre as linhas e remover as correspondências
        lines_to_remove = []
        for i, line in enumerate(lines):
            if line.strip().startswith(f":doc:`{nome_arquivo}`"):
                # Remove a linha com o nome do arquivo e a linha subsequente
                lines_to_remove.extend([i, i + 1])
            elif line.strip() == f"{nome_arquivo}":
                # Remove a linha com o nome do arquivo quando encontrada em 'modules'
                lines_to_remove.append(i)

        # Remove as linhas marcadas para exclusão
        lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]

        # Passo 3: Salvar as alterações no arquivo 'index.rst'
        with open(index_rst_file, 'w', encoding='utf-8', newline='\n') as file:
            file.writelines(lines)

        print("Deleção feita com sucesso")
