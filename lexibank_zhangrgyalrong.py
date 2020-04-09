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
    Source = attr.ib(default=None)

class Dataset(MyDataset):
    dir = Path(__file__).parent
    id = "zhangrgyalrong"
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
        # add languages
        languages = args.writer.add_languages(lookup_factory='Name')
        languages_dict = {}
        for lan in self.languages:
            languages[lan['Name']] = {'Source' :lan['Source'], 'ID':lan['ID']}
        
        # add concepts
        concepts = {}
        for concept in self.concepts:
            idx = '{0}_{1}'.format(
                    concept['NUMBER'],
                    slug(concept['ENGLISH']))

            args.writer.add_concept(
                    ID=idx,
                    Name=concept['ENGLISH'],
                    Chinese_Gloss=concept['CHINESE'],
                    Gloss_in_Source=concept['GLOSS_IN_SOURCE']
                    )
            concepts[concept['CHINESE'].strip()] = idx

        for cogid, entry in progressbar(
                enumerate(data), desc="cldfify", total=len(data)
                ):
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
                                Cognateset_ID=cogid+1)
