from argparse import ArgumentParser
from collections import namedtuple
from io import StringIO
from itertools import groupby
import re


TAHESTIK = 'ABCDEFGHIJKLMNOPQRSŠZŽTUVÕÄÖÜXY'
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
    tabel = [
        Liige('Esimene Liige', '', '123456789', 'a@b.c', 'abcd', '', '??', 'ei', 'märkus'),
        Liige('Teine Liige', '', '123456789', 'a@b.cd', 'abcde', '', '???', 'jah', ''),
        Liige('Kolmas Tiige', '', '123456789', 'a@b.cd', 'abcde', '', '???', 'jah', ''),
    ]
    print(formaadi_wiki(tabel))


def parse_args():
    parser = ArgumentParser(description="Võtab Google Spreatsheet'i tabelist liikmete "
                                        "nimekirja ja vormindab selle wiki formaati.")
    parser.add_argument('spreadsheet',
                        help="Link Google Spreatsheet'ini")
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
    i = 0   # Tühi tabel ajab asja sassi muidu
    for grupp, liikmed in groupby(sorted(tabel, key=formaadi_nimi), key=perekonnanime_esitaht):
        # Leiame vahele jäänud tähestiku tähed
        try:
            index = tahestik.index(grupp) + 1
        except ValueError:
            index = 0
        grupid = tahestik[:index]
        tahestik = tahestik[index:]

        for liige in liikmed:
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
            grupid = []
            i += 1
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
        if re.match(r'\(\w+\)', osad[-1]):
            osad.pop(-1)
        else:
            break
    if osad:
        return skeem.format(perekonnanimi=osad[-1],
                            eesnimed=' '.join(osad[:-1]))
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


if __name__ == '__main__':
    main()
