"""Gera HTML estático e textos locais do app a partir dos documentos revisados."""
from pathlib import Path
import html
import re

site = Path(__file__).resolve().parent
app_assets = site.parent / 'ProjetoARCA/micro_arca_app/assets/legal'
app_assets.mkdir(parents=True, exist_ok=True)

def inline(text):
    text = html.escape(text)
    text = re.sub(r'\[([^]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

def page(title, content, prefix):
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — MicroARCA</title><meta name="description" content="Informações do projeto educacional MicroARCA.">
<link rel="stylesheet" href="{prefix}style.css"></head><body>
<header><a href="{prefix}index.html">✨ MicroARCA</a><nav aria-label="Documentos"><a href="{prefix}privacidade/">Privacidade</a><a href="{prefix}termos/">Termos de uso</a></nav></header>
<main>{content}</main><footer>Gabriel Sebastião do Nascimento Neto · <a href="mailto:gabrielsebastiao321dev@gmail.com">Contato e privacidade</a></footer></body></html>'''

for document, title in [('privacidade', 'Política de Privacidade'), ('termos', 'Termos de Uso'), ('exclusao', 'Solicitar exclusão de dados')]:
    source = (site / 'documentos' / f'{document}.md').read_text(encoding='utf-8')
    blocks = []
    for block in source.strip().split('\n\n'):
        text = ' '.join(block.splitlines())
        if text.startswith('## '):
            blocks.append(f'<h2>{inline(text[3:])}</h2>')
        elif text.startswith('# '):
            blocks.append(f'<h1>{inline(text[2:])}</h1>')
        elif block.startswith('- '):
            blocks.append('<ul>' + ''.join(f'<li>{inline(line[2:])}</li>' for line in block.splitlines()) + '</ul>')
        else:
            blocks.append(f'<p>{inline(text)}</p>')
    destination = site / document
    destination.mkdir(exist_ok=True)
    (destination / 'index.html').write_text(page(title, '\n'.join(blocks), '../'), encoding='utf-8')
    plain = re.sub(r'\[([^]]+)\]\(([^)]+)\)', r'\1: \2', source)
    plain = re.sub(r'^#{1,2} ', '', plain, flags=re.M).replace('**', '')
    plain = '\n\n'.join(block if block.startswith('- ') else ' '.join(block.splitlines()) for block in plain.split('\n\n'))
    plain = plain.replace('../privacidade/', 'https://gabriel26077.github.io/microarca-site/privacidade/')
    if document != 'exclusao':
        (app_assets / f'{document}.txt').write_text(plain, encoding='utf-8')

home = '''<h1>Programar, experimentar, aprender.</h1>
<p>O MicroARCA permite programar um ESP32 com MicroPython pelo celular Android, em blocos ou Python, e enviar programas por Bluetooth.</p>
<p>Foi pensado para pessoas a partir de 9 anos, com acompanhamento de um adulto nas atividades de crianças e adolescentes.</p>
<h2>Já participa dos testes?</h2><p><a class="primary" href="teste/">Participar do teste fechado</a></p><p>Veja como trocar do teste interno para o fechado, mantendo o app instalado.</p>
<h2>Informações para estudantes e famílias</h2><p>O app não exige conta. Leia como funcionam o armazenamento dos projetos, a conexão com a placa e o acesso ao catálogo.</p>
<p><a class="primary" href="privacidade/">Política de Privacidade</a></p><p><a href="termos/">Termos de Uso</a></p>
<h2>Contato</h2><p><a href="mailto:gabrielsebastiao321dev@gmail.com">gabrielsebastiao321dev@gmail.com</a></p>'''
(site / 'index.html').write_text(page('Projeto educacional', home, './'), encoding='utf-8', newline='\n')

test_page = '''<h1>Participe do teste do MicroARCA</h1>
<p>Já tem o MicroARCA instalado pela Play Store? Faça a troca do teste interno para o teste fechado seguindo os passos abaixo. Normalmente, você pode manter o app instalado e seus projetos.</p>
<aside class="notice"><strong>Antes de começar</strong><p>Aguarde o responsável pelo MicroARCA confirmar que o teste fechado foi liberado pelo Google. Se ele ainda estiver em análise, não saia do teste interno agora.</p></aside>
<p>Use a mesma conta Google cujo e-mail foi cadastrado na lista de testadores. O teste fechado está disponível para contas elegíveis no Brasil. Crianças e adolescentes devem seguir estes passos com um adulto responsável.</p>
<ol class="steps">
<li><h2>Saia do teste interno</h2><p>Abra a página abaixo e procure <strong>“Sair do programa”</strong> (o texto pode variar). Confirme a saída e volte para esta página. Se você nunca participou do teste interno, vá ao passo 2.</p>
<a class="primary" href="https://play.google.com/apps/internaltest/4701591841979490149" target="_blank" rel="noopener noreferrer">1. Abrir teste interno para sair <span class="new-tab">(nova aba)</span></a>
<p class="hint">Sair do programa de testes não é desinstalar o app. Não escolha participar novamente do teste interno.</p></li>
<li><h2>Aceite o teste fechado</h2><p>Abra a página abaixo e toque em <strong>“Participar dos testes”</strong> ou <strong>“Tornar-se um testador”</strong>. Confira se está usando a conta Google cadastrada. Se a página confirmar que você já é testador, a participação foi aceita.</p>
<a class="primary" href="https://play.google.com/apps/testing/com.microarca.app" target="_blank" rel="noopener noreferrer">2. Participar do teste fechado <span class="new-tab">(nova aba)</span></a></li>
<li><h2>Abra o app e teste</h2><p>Na Play Store, toque em <strong>“Atualizar”</strong>, se essa opção aparecer, ou em <strong>“Abrir”</strong>. Se você já tem a mesma versão instalada, pode não haver atualização.</p>
<a class="primary" href="https://play.google.com/store/apps/details?id=com.microarca.app" target="_blank" rel="noopener noreferrer">Abrir MicroARCA na Play Store <span class="new-tab">(nova aba)</span></a>
<p class="hint">Se você tem apenas o “MicroARCA Teste”, instalado por APK, ele é uma cópia separada. Instale também o MicroARCA pela Play Store; os projetos não são transferidos automaticamente entre as duas cópias.</p></li>
</ol>
<h2>Depois de entrar</h2><p>Permaneça no teste fechado por pelo menos <strong>14 dias consecutivos</strong>, experimente o app e conte o que funcionou ou precisa melhorar. O período anterior no teste interno não conta para essa etapa. Não é necessário deixar o app aberto o tempo todo.</p>
<h2>Não conseguiu participar?</h2><p>Confira a conta Google selecionada e se seu e-mail está na lista. A mudança entre os programas pode levar algum tempo. Se aparecer “App indisponível” ou “Não encontrado”, aguarde a confirmação de liberação e tente novamente. Não desinstale o app para resolver isso: você pode perder projetos locais.</p>
<p>Se continuar com dificuldade, <a href="mailto:gabrielsebastiao321dev@gmail.com?subject=Ajuda%20para%20participar%20do%20teste%20MicroARCA">peça ajuda por e-mail</a>, informando a mensagem que apareceu. Não envie senhas.</p>
<p class="hint">Esta página orienta a troca. A saída e o aceite precisam ser confirmados por você nas páginas do Google Play.</p>'''
test_dir = site / 'teste'
test_dir.mkdir(exist_ok=True)
(test_dir / 'index.html').write_text(page('Participar do teste', test_page, '../'), encoding='utf-8', newline='\n')
print('Site e dois documentos locais do app gerados.')
