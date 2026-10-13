import sys
src = open('phalom_src.html', encoding='utf-8').read()
fonts = open('fonts/fonts.css').read() + '\n' + open('fonts/sym.css').read()
page = src.replace('/*__FONTS__*/', fonts, 1)
open('phalom_artifact.html', 'w', encoding='utf-8').write(page)
head, body = page.split('</style>', 1)
doc = ('<!doctype html>\n<html lang="lo">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + head + '</style>\n</head>\n<body>' + body + '</body>\n</html>\n')
open(sys.argv[1], 'w', encoding='utf-8').write(doc)
print(len(page), len(doc))
