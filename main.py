import os
import cv2
import time
from datetime import datetime
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich.align import Align

from config import EXTENSOES_ACEITAS, PROMPT_NOME_CRIATIVO, PROMPT_NOME_DESCRITIVO
from utils.inpainter import reconstruir_imagem
from utils.renamer import solicitar_nome_ia, renomear_arquivo_localmente

console = Console()

def validar_pasta(caminho: str) -> bool:
    caminho = caminho.strip().strip("'").strip('"')
    return os.path.exists(caminho) and os.path.isdir(caminho)

def varrer_imagens(caminho_pasta: str):
    arquivos_validos = []
    try:
        for nome_arquivo in os.listdir(caminho_pasta):
            caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
            if not os.path.isfile(caminho_completo): continue
            
            nome, extensao = os.path.splitext(nome_arquivo)
            if extensao.lower() in EXTENSOES_ACEITAS:
                arquivos_validos.append(nome_arquivo)
    except Exception as e:
        console.print(f"[bold red]Erro ao ler pasta:[/bold red] {e}")
    return arquivos_validos

def get_saudacao() -> str:
    hora = datetime.now().hour
    if 0 <= hora < 12:
        return "Bom dia"
    elif 12 <= hora < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

def obter_nome_usuario() -> str:
    try:
        nome = os.getlogin().split()[0].capitalize()
        return nome
    except:
        return "Usuário"

def exibir_tela_carregamento():
    with Progress(
        SpinnerColumn(spinner_name="dots", style="cyan"),
        TextColumn("[cyan]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Inicializando ImageAI Pro...", total=None)
        time.sleep(1.5)
    console.print("✅ [bold green]Sistema pronto.[/bold green]\n")
    time.sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho():
    titulo = pyfiglet.figlet_format("ImageAI Pro", font="slant")
    console.print(Align.center(f"[bold cyan]{titulo}[/bold cyan]"))
    sub_titulo = "v1.0  |  Processador de Imagens com IA  |  by Vítor Gomes"
    console.print(Align.center(f"[dim white]{sub_titulo}[/dim white]\n"))

def feature_remover_marca():
    console.print("\n[bold cyan]--- REMOVER MARCA D'ÁGUA ---[/bold cyan]")
    caminho_pasta = Prompt.ask("[bold white]Digite o caminho completo da pasta[/bold white]").strip().strip("'").strip('"')
    
    if not validar_pasta(caminho_pasta):
        console.print("[bold red]❌ Pasta não encontrada ou inválida![/bold red]")
        return
        
    menu_posicao = """[bold yellow]
  [1]  ↘  Canto inferior direito (Gemini)
  [2]  ↙  Canto inferior esquerdo
  [3]  ↗  Canto superior direito
  [4]  ↖  Canto superior esquerdo
  [5]  ✏  Customizado (inserir manualmente)[/bold yellow]"""
    
    console.print(Panel(menu_posicao, title="[bold white]📍 Onde está a marca d'água?[/bold white]", border_style="blue"))
    escolha_pos = IntPrompt.ask("[bold white]Escolha[/bold white]", choices=["1", "2", "3", "4", "5"])
    
    pct_largura = 15.0
    pct_altura = 8.0
    
    if escolha_pos == 5:
        pct_largura = float(Prompt.ask("[bold white]Percentual de largura (ex: 15)[/bold white]"))
        pct_altura = float(Prompt.ask("[bold white]Percentual de altura (ex: 8)[/bold white]"))
        
    imagens = varrer_imagens(caminho_pasta)
    if not imagens:
        console.print("[bold yellow]Nenhuma imagem compatível encontrada na pasta.[/bold yellow]")
        return
        
    pasta_saida = os.path.join(caminho_pasta, "Fotos Sem Marca D'agua")
    os.makedirs(pasta_saida, exist_ok=True)
    
    sucessos = 0
    erros = []
    
    tempo_inicio = time.time()

    with Progress(
        SpinnerColumn(spinner_name="point", style="cyan"),
        TextColumn("[cyan]Processando:[/cyan] [bold]{task.description}[/bold]"),
        BarColumn(style="cyan", complete_style="bold cyan"),
        TextColumn("[bold cyan]{task.percentage:>3.0f}%[/bold cyan]"),
        TextColumn("[dim white]({task.completed}/{task.total})[/dim white]"),
        TimeRemainingColumn(),
        console=console,
        transient=False,
    ) as progress:
        task_id = progress.add_task(imagens[0] if len(imagens) > 0 else "Preparando...", total=len(imagens))
        
        for nome_arq in imagens:
            progress.update(task_id, description=nome_arq)
            caminho_entrada = os.path.join(caminho_pasta, nome_arq)
            caminho_saida = os.path.join(pasta_saida, nome_arq)
            
            try:
                img_reconstruida = reconstruir_imagem(caminho_entrada, escolha_pos, pct_largura, pct_altura)
                if not cv2.imwrite(caminho_saida, img_reconstruida):
                    raise Exception("Falha ao salvar a imagem na pasta.")
                sucessos += 1
            except KeyboardInterrupt:
                progress.console.print("\n[bold yellow]⚠️ Processamento de imagens interrompido prematuramente![/bold yellow]")
                break
            except Exception as e:
                erros.append((nome_arq, str(e)))
                
            progress.advance(task_id)

    tempo_fim = time.time()
    minutos, segundos = divmod(int(tempo_fim - tempo_inicio), 60)
    
    console.print("\n")
    console.print(Panel("[bold green]          ✅ Processamento Concluído      [/bold green]", border_style="green", expand=False))
    
    tabela = Table(show_header=True, header_style="bold cyan", border_style="blue")
    tabela.add_column("Imagem")
    tabela.add_column("Status", justify="center")
    
    for proc_arq in imagens:
        erro_msg = next((err for arq, err in erros if arq == proc_arq), None)
        if erro_msg:
            tabela.add_row(proc_arq, "[bold red]❌ Erro[/bold red]")
        else:
            tabela.add_row(proc_arq, "[bold green]✅ Sucesso[/bold green]")
            
    console.print(tabela)
    console.print(f"[bold white]Total: {len(imagens)}  |  Sucesso: {sucessos}  |  Erros: {len(erros)}[/bold white]")
    console.print(f"[dim white]Pasta de saída:[/dim white] {pasta_saida}")
    console.print(f"[dim white]Tempo total:[/dim white] {minutos}m {segundos}s\n")


def feature_renomear_ia():
    console.print("\n[bold cyan]--- RENOMEAR IMAGENS COM IA ---[/bold cyan]")
    caminho_pasta = Prompt.ask("[bold white]Digite o caminho completo da pasta[/bold white]").strip().strip("'").strip('"')
    
    if not validar_pasta(caminho_pasta):
        console.print("[bold red]❌ Pasta não encontrada ou inválida![/bold red]")
        return
        
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        api_key = Prompt.ask("[bold white]Digite a sua API Key do OpenRouter[/bold white]", password=True)
        if not api_key:
            console.print("[bold red]A API Key é obrigatória para usar essa funcionalidade.[/bold red]")
            return

    menu_estilo = """[bold yellow]
  [1]  🎨  Criativo  — Curto, impactante, marketeiro
           Ex: "Resina_Oceano_Luxe.jpg"
           
  [2]  📋  Descritivo — Detalhado, técnico, completo
           Ex: "Tabua_Resina_Marmoreizada_Premium.jpg"[/bold yellow]"""
    
    console.print(Panel(menu_estilo, title="[bold white]✨ Qual estilo de nome deseja?[/bold white]", border_style="blue"))
    escolha_estilo = IntPrompt.ask("[bold white]Escolha[/bold white]", choices=["1", "2"])
    
    prompt_usado = PROMPT_NOME_CRIATIVO if escolha_estilo == 1 else PROMPT_NOME_DESCRITIVO
    
    imagens = varrer_imagens(caminho_pasta)
    if not imagens:
        console.print("[bold yellow]Nenhuma imagem compatível encontrada na pasta.[/bold yellow]")
        return
        
    sucessos = 0
    erros = []
    renomeados = []

    tempo_inicio = time.time()

    with Progress(
        SpinnerColumn(spinner_name="arc", style="cyan"),
        TextColumn("[cyan]IA Analisando:[/cyan] [bold]{task.description}[/bold]"),
        BarColumn(style="cyan", complete_style="bold cyan"),
        TextColumn("[bold cyan]{task.percentage:>3.0f}%[/bold cyan]"),
        TextColumn("[dim white]({task.completed}/{task.total})[/dim white]"),
        TimeRemainingColumn(),
        console=console,
        transient=False,
    ) as progress:
        task_id = progress.add_task(imagens[0] if len(imagens) > 0 else "Preparando...", total=len(imagens))
        
        for nome_arq in imagens:
            progress.update(task_id, description=nome_arq)
            caminho_entrada = os.path.join(caminho_pasta, nome_arq)
            
            try:
                novo_nome = solicitar_nome_ia(caminho_entrada, api_key, prompt_usado)
                caminho_novo = renomear_arquivo_localmente(caminho_entrada, novo_nome)
                novo_nome_final = os.path.basename(caminho_novo)
                
                renomeados.append((nome_arq, novo_nome_final))
                sucessos += 1
            except KeyboardInterrupt:
                progress.console.print("\n[bold yellow]⚠️ Análise de IA interrompida prematuramente![/bold yellow]")
                break
            except Exception as e:
                erros.append((nome_arq, str(e)))
                
            progress.advance(task_id)

    tempo_fim = time.time()
    minutos, segundos = divmod(int(tempo_fim - tempo_inicio), 60)

    # Resumo
    console.print("\n")
    console.print(Panel("[bold green]          ✅ Renomeação Concluída         [/bold green]", border_style="green", expand=False))
    
    tabela = Table(show_header=True, header_style="bold cyan", border_style="blue")
    tabela.add_column("Nome Anterior")
    tabela.add_column("Nome Novo")
    
    for proc_arq in imagens:
        tupla_sucesso = next((t for t in renomeados if t[0] == proc_arq), None)
        if tupla_sucesso:
            tabela.add_row(proc_arq, f"[bold green]{tupla_sucesso[1]}[/bold green]")
        else:
            tabela.add_row(proc_arq, "[bold red]❌ Falhou[/bold red]")
            
    console.print(tabela)
    console.print(f"[bold white]Total: {len(imagens)}  |  Sucesso: {sucessos}  |  Erros: {len(erros)}[/bold white]")
    console.print(f"[dim white]Tempo total:[/dim white] {minutos}m {segundos}s\n")
    
    if erros:
        console.print("[bold red]Erros reportados:[/bold red]")
        for err_arq, err_msg in erros:
            console.print(f" - {err_arq}: {err_msg}")


def main_menu():
    exibir_tela_carregamento()
    
    saudacao = get_saudacao()
    nome = obter_nome_usuario()
    msg_boas_vindas = f"{saudacao}, Senhor {nome}! O que deseja fazer hoje?"
    
    menu_principal = """[bold yellow]
   [1]  🧹  Remover Marca D'água
   [2]  ✏  Renomear Imagens com IA
   [0]  🚪  Sair[/bold yellow]"""
    
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            exibir_cabecalho()
            console.print(Align.center(Panel(f"[bold magenta]{msg_boas_vindas}[/bold magenta]", border_style="blue", expand=False)))
            console.print("\n")
            
            console.print(Align.center(Panel(menu_principal, title="[bold white]🖼  ImageAI Pro — Menu Principal[/bold white]", border_style="blue", expand=False)))
            console.print(Align.center("[dim white]Digite o número da opção desejada e pressione Enter.[/dim white]\n"))
            
            escolha = Prompt.ask("[bold white]Escolha[/bold white]", choices=["0", "1", "2"])
            
            if escolha == "0":
                console.print("\n")
                console.print(Align.center(Panel(f"[bold magenta]Até logo, Senhor {nome}! Volte sempre. 👋[/bold magenta]", border_style="blue", expand=False)))
                break
            elif escolha == "1":
                try:
                    feature_remover_marca()
                except KeyboardInterrupt:
                    console.print("\n[bold yellow]⚠️ Operação cancelada pelo usuário. Voltando ao menu principal...[/bold yellow]")
                input("\nPressione ENTER para voltar ao menu...")
            elif escolha == "2":
                try:
                    feature_renomear_ia()
                except KeyboardInterrupt:
                    console.print("\n[bold yellow]⚠️ Operação cancelada pelo usuário. Voltando ao menu principal...[/bold yellow]")
                input("\nPressione ENTER para voltar ao menu...")
        except KeyboardInterrupt:
            console.print("\n")
            console.print(Align.center(Panel(f"[bold magenta]Até logo, Senhor {nome}! Volte sempre. 👋[/bold magenta]", border_style="blue", expand=False)))
            break

if __name__ == "__main__":
    main_menu()
