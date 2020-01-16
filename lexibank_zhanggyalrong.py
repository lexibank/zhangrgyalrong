from collections import OrderedDict
from pathlib import Path

import attr
from clldutils.misc import slug
from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as MyDataset
from pylexibank.forms import FormSpec
from pylexibank.util import progressbar

@attr.s
class CustomConcept(Concept):
    Chinese_Gloss = attr.ib(default=None)
    Gloss_in_Source = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    Chinese_Name = attr.ib(default=None)
    Family = attr.ib(default="Sino-Tibetan")
    Name_in_Source = attr.ib(default=None)

class Dataset(MyDataset):
    dir = Path(__file__).parent
    id = "zhanggyalrong"
    concept_class = CustomConcept
    language_class = CustomLanguage
    form_spec = FormSpec(
        missing_data=[''],
        separators=";/,",
        strip_inside_brackets=False,
        brackets={'(': ')', '[': ']'},
        replacements=[
            ('-', '+'),
            ('*', ''),
            ('[', ''),
            (']', ''),
            ('(', ''),
            (')', '')
            ]
    )

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        data = self.raw_dir.read_csv("zhang2019-oc-rgyal.tsv", dicts=True,
                delimiter="\t")
        languages = {}
        for lan in self.languages:
            args.writer.add_language(
                ID = lan['ID'],
                Name=lan['Name'],
                Chinese_Name=lan['Chinese_Name'],
                Glottocode=lan['Glottocode'],
                Latitude=lan['Latitude'],
                Longitude=lan['Longitude']
            )
            languages[lan['Name']] = {'Source' :lan['Source'], 'ID':lan['ID']}

        concepts = {}git
        for concept in self.concepts:
            idx = concept['ID'].split('-')[-1]+'_'+slug(concept['ENGLISH'])
            args.writer.add_concept(
                    ID=idx,
                    Name=concept['ENGLISH'],
                    Chinese_Gloss=concept['CHINESE'].strip(),
                    Gloss_in_Source=concept['GLOSS_IN_SOURCE']
                    )
            concepts[concept['CHINESE'].strip()] = idx

        for cogid_, entry in progressbar(
                enumerate(data), desc="cldfify the data", total=len(data)
                ):
            cogid = cogid_ + 1
            for language, value in languages.items():
                if entry[language].strip():
                    for row in args.writer.add_forms_from_value(
                        Language_ID=value['ID'],
                        Parameter_ID=concepts[entry["Chinese_character"]],
                        Value=entry[language],
                        Source=[value['Source']]
                        ):
                        args.writer.add_cognate(
                                lexeme=row,
                                Cognateset_ID=cogid)
