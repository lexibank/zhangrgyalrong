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
    Source = attr.ib(default=None)

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
        # add languages
        languages = args.writer.add_languages(lookup_factory='Name')
        languages_dict = {}
        for lan in self.languages:
            languages[lan['Name']] = {'Source' :lan['Source'], 'ID':lan['ID']}
        # add concepts
        concepts = args.writer.add_concepts(id_factory=lambda c: "%s_%s" % (c.id, slug(c.english)))
        concepts_dict = {}
        for concept in self.concepts:
            idx = concept['ID']+'_'+slug(concept['ENGLISH'])
            concepts_dict[concept['CHINESE'].strip()] = idx

        for cogid_, entry in progressbar(
                enumerate(data), desc="cldfify the data", total=len(data)
                ):
            cogid = cogid_ + 1
            for language, value in languages.items():
                if entry[language].strip():
                    for row in args.writer.add_forms_from_value(
                        Language_ID=value['ID'],
                        Parameter_ID=concepts_dict[entry["Chinese_character"]],
                        Value=entry[language],
                        Source=[value['Source']]
                        ):
                        args.writer.add_cognate(
                                lexeme=row,
                                Cognateset_ID=cogid)
