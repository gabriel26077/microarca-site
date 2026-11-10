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
<h2>Informações para estudantes e famílias</h2><p>O app não exige conta. Leia como funcionam o armazenamento dos projetos, a conexão com a placa e o acesso ao catálogo.</p>
<p><a class="primary" href="privacidade/">Política de Privacidade</a></p><p><a href="termos/">Termos de Uso</a></p>
<h2>Contato</h2><p><a href="mailto:gabrielsebastiao321dev@gmail.com">gabrielsebastiao321dev@gmail.com</a></p>'''
(site / 'index.html').write_text(page('Projeto educacional', home, './'), encoding='utf-8')
print('Site e dois documentos locais do app gerados.')
