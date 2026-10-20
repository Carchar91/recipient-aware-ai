#!/usr/bin/env python3
"""Render synthetic authored fixtures; never generates model responses."""
from pathlib import Path
import argparse, json
r=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
mismatches=[]
def emit(path,text):
    if args.check:
        if not path.exists() or path.read_text()!=text:mismatches.append(str(path.relative_to(r)))
    else:
        path.write_text(text)
import sys
sys.path.insert(0,str(r))
from rai.core import render_output,validate_output
idx=json.loads((r/'development/rc2/cases.json').read_text())
label='**синтетический авторский образец, не независимый тест и не измеренный результат**\n\nПодготовлен ИИ по авторскому уточнению. Это не результат нового изолированного запуска skill.\n'
texts={}
for c in idx:
 folder=r/'development/rc2'/c['case_id'];d=json.loads((folder/'input.json').read_text());o=json.loads((folder/'authored-output.json').read_text());assert not validate_output(d,o)
 text=render_output(d,o)
 texts[c['case_id']]=text
 emit(folder/'readable.md', label+'\n'+text)
ex=r/'examples/rc2';ex.mkdir(parents=True,exist_ok=True)
groups=[('01-profiler.md','Profiler — разные основания доверия',['dev-pf-audit','dev-pf-learning','dev-pf-sparse'],'Одна задача: обсудить пилот отчётности. В первом наборе адресат требует воспроизводимые расчёты и ранее вернул сводку без источников; во втором — прямо просит обратимый шаг и возможность не продолжать. Третий набор содержит только одну процедурную реплику. Различие карт опирается на материал, не на имя или должность.'),('02-profiler-plus.md','Profiler Plus — одно предложение, две рамки',['dev-pp-audit','dev-pp-learning'],'Условия одинаковы: 10 рабочих дней, 12 000 рублей, 240 обезличенных записей, без автоматического продления и записи в CRM. Один адресат просит возможность повторить расчёт; другой — ограниченную проверку гипотезы с возможностью остановиться. Ниже два готовых обращения, а не два психологических отчёта.'),('03-dopamine-hooks.md','Dopamine Hooks — движение через весь текст',['dev-dh-sequence'],'В исходнике разрозненно перечислены наблюдения вымышленной команды о 12 запросах и три поля карточки. Ниже полный текст: неопределённый результат → получатель → критерий завершения → карточка → смысл явного неизвестного → проверка одной формулировки.'),('04-reverse.md','Reverse — ответы в точке возникновения вопросов',['dev-rv-sequence'],'Исходное письмо: «Предлагаем перейти на новый порядок отчётности. Доступ уже готов. Займёт всего неделю. Подтвердите до пятницы, и начнём. Стоимость обсудим потом». Из подтверждённого контекста известны отдельный пилот, локальный пример и роль руководителя. Цена неизвестна; приватный резерв бюджета нельзя раскрывать.'),('05-rail.md','Rail — готовый комплект и честный блокер',['dev-rl-ready','dev-rl-gap'],'Мария уже уполномочена собирать предложения. Алексей проверяет соответствие, Игорь разрешает покупку. В первом случае есть спецификация, количество, синтетические контакты и предварительные цены; запрос и таблица подготовлены. Во втором отсутствует только количество: известную часть готовим, зависимую отправку блокируем. .example — вымышленные адреса, никаких сообщений не отправлено.')]
combined=['# Пять читаемых образцов rc.2\n',label,'\nЭто development cases и образцы ожидаемого поведения; их нельзя использовать как будущий held-out тест или свидетельство преимущества.\n']
for filename,title,ids,context in groups:
 parts=['# '+title+'\n',label,'\n'+context+'\n']
 for cid in ids:parts+=['\n---\n\n### '+cid+'\n',texts[cid]]
 text='\n'.join(parts);emit(ex/filename, text);combined.append(text)
emit(ex/'FIVE_READABLE_EXAMPLES_RU.md', '\n\n---\n\n'.join(combined))
emit(r/'development/rc2/README.md', '''# rc.2 development data

Nine synthetic authored cases and outputs, not isolated model responses and not held-out evaluation data. See cases.json for provenance and semantic review questions. `readable.md` renders each authored output; `examples/rc2/` groups them into five readable demonstrations. Rail folders contain actual local spec versions, request text and table files; all contacts are synthetic .example addresses. No sending or buying occurred.

Future held-out cases must be independently prepared and materially different, not renamed or paraphrased copies. These fixtures establish intended behavior only. No new model comparison is authorized by their presence.
''')
if mismatches:
    raise SystemExit('Readable sample drift: '+', '.join(mismatches))
print('PASS: nine labeled development outputs validate; five readable sample groups match.' if args.check else 'Built labeled readable development samples.')
