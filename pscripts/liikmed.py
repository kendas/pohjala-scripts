from argparse import ArgumentParser, FileType
from collections import namedtuple
from csv import DictReader
from io import StringIO
from itertools import groupby
import re
import sys


TAHESTIK = 'ABCDEFGHIJKLMNOPQRSŠZŽTUVWÕÄÖÜXY'
LINGID = ' · '.join('[[#{taht}|{taht}]]'.format(taht=t) for t in TAHESTIK)
WIKI_HEADER = """{{| cellpadding="4" style="border:1px #AAA solid; background:#F9F9F9; text-align: center;"
|-
|'''{lingid}'''
{{|border="0" cellpadding="4" style="text-align: center; font-size:90%"
|style="width:; background:#C6D8EF" |'''Nimi'''
|style="width:30px; background:#C6D8EF" |
|style="width:; background:#C6D8EF" |'''Telefon'''
|style="width:; background:#C6D8EF" |'''E-post'''
|style="width:; background:#C6D8EF" |'''Aadress'''
|style="width:; background:#C6D8EF" |'''Skype (s)'''
|style="width:; background:#C6D8EF" |'''Tegevusala'''
|style="width:; background:#C6D8EF" |'''Paberpost'''
|style="width:; background:#C6D8EF" |'''Märkused'''
""".format(lingid=LINGID)
WIKI_ROW = """|-{style}
|{anchors} {nimi} || {riik} || {telefon} || {epost} || {aadress} || {skype} || {tegevusala} || {paberpost} || {markused}
"""
WIKI_FOOTER = """|}}
|-{style}
|'''{lingid}'''
|}}
"""


Liige = namedtuple('Liige',
                   ['nimi', 'riik', 'telefon', 'epost', 'aadress', 'skype', 'tegevusala',
                    'paberpost', 'markused'])


def main():
    args = parse_args()
    with args.valjund as valjund:
        valjund.write(formaadi_wiki(loe_csv(args.sisend)))


def loe_csv(fail):
    """
    Loeb csv failist read ja tagastab nendele vastavad liikme kirjeldused
    :param file fail: Avatud csv fail.
    :return: Liikmete kirjeldused
    :rtype: list[Liige]
    """
    with fail:
        luger = DictReader(fail)
        for rida in luger:
            if rida['nimi'].strip():
                yield Liige(rida['nimi'].strip(),
                            '',
                            rida['telefon'],
                            rida['e-post'],
                            rida['aadress'],
                            rida['skype'],
                            rida['tegevusvaldkond'],
                            rida['paberpost'],
                            rida['märkused'])


def parse_args():
    parser = ArgumentParser(description="Võtab Google Spreatsheet'i tabelist liikmete "
                                        "nimekirja ja vormindab selle wiki formaati.")
    # parser.add_argument('spreadsheet',
    #                     help="Link Google Spreatsheet'ini")
    parser.add_argument('sisend',
                        type=FileType('r'),
                        nargs='?',
                        default=sys.stdin,
                        help="Sisendfail (csv) - vaikimisi stdin")
    parser.add_argument('valjund',
                        type=FileType('w'),
                        nargs='?',
                        default=sys.stdout,
                        help="valjundfail (WikiMedia formaat) - vaikimisi stdout")
    return parser.parse_args()


def formaadi_wiki(tabel):
    """
    Formaadib sisendtabeli wiki formaati.

    :param list[Liige] tabel: Sisendtabel
    :return:
    """
    tahestik = list(TAHESTIK)
    valjund = StringIO()
    valjund.write(WIKI_HEADER)
    i = -1
    for grupp, liikmed in groupby(sorted(tabel, key=lambda n: tahestiku_jarjekord(formaadi_nimi(n))),
                                  key=perekonnanime_esitaht):
        # Leiame vahele jäänud tähestiku tähed
        try:
            index = tahestik.index(grupp) + 1
        except ValueError:
            index = 0
        grupid = tahestik[:index]
        tahestik = tahestik[index:]

        for i, liige in enumerate(liikmed, start=i + 1):
            valjund.write(WIKI_ROW.format(style='style="background:#f5faff"' if i % 2 == 1 else '',
                                          anchors=''.join('<span id="{}"></span>'.format(taht)
                                                          for taht in grupid),
                                          nimi="[[{}]]".format(liige.nimi),
                                          riik='',
                                          telefon=liige.telefon,
                                          epost=liige.epost,
                                          aadress=liige.aadress,
                                          skype=liige.skype,
                                          tegevusala=liige.tegevusala,
                                          paberpost=liige.paberpost,
                                          markused=liige.markused))
            if grupid:
                grupid = []
    valjund.write(WIKI_FOOTER.format(style='style="background:#f5faff"' if i % 2 == 1 else '',
                                     lingid=LINGID))
    return valjund.getvalue()


def formaadi_nimi(liige):
    """
    Tagastab Liikme nime sorteeritava kuju: "Perekonnanimi, Eesnimi Eesnimi Eesnimi".
    :param Liige liige: liikme kirjeldus
    :return: Liikme nime sorteeritava kuju
    :rtype: str
    """
    skeem = '{perekonnanimi}, {eesnimed}'
    # Käime tagant poolt ettepoole ja otsime esimest sulgudeta nimeosa
    osad = liige.nimi.split(' ')
    while osad:
        if re.match(r'\(.*\)', osad[-1]):
            osad.pop(-1)
        else:
            break
    # Formaadime viimase (perekonnanime) ja ülejäänud osa (eesnimed)
    if osad:
        return skeem.format(perekonnanimi=osad[-1],
                            eesnimed=' '.join(osad[:-1]))
    # Juhuks, kui mingil põhjusel nimi on tühi väli või kõik osad on sulgudega
    return ''


def perekonnanime_esitaht(liige):
    """
    Tagastab Liikme nime perekonnanime esimese tähe (suur).
    :param Liige liige: Liikme kirjeldus
    :rtype: str
    """
    formaat = formaadi_nimi(liige)
    if formaat:
        return formaat[0].upper()
    else:
        return ''


def tahestiku_jarjekord(sona):
    return [
        TAHESTIK.index(t.upper()) if t.upper() in TAHESTIK else 100 + ord(t)
        for t in sona
    ]


if __name__ == '__main__':
    main()
