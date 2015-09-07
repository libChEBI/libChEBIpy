'''
libChEBIpy (c) University of Manchester 2015

libChEBIpy is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=too-many-public-methods
import datetime
import math
import os
import unittest

from libchebipy import ChebiEntity, ChebiException, Comment, CompoundOrigin, \
    DatabaseAccession, Formula, Name, Reference, Relation, Structure
import libchebipy._parsers as parsers


class TestChebiEntity(unittest.TestCase):
    '''COMMENT'''

    def setUp(self):
        '''COMMENT'''
        self.__existing = ChebiEntity(4167)
        self.__secondary = ChebiEntity(5585)

    def test_get_non_existing(self):
        '''COMMENT'''
        self.assertRaises(ChebiException, ChebiEntity, -1)

    def test_get_id_existing(self):
        '''COMMENT'''
        self.assertTrue(self.__existing.get_id() == 4167)

    def test_get_id_secondary(self):
        '''COMMENT'''
        self.assertTrue(self.__secondary.get_id() == 5585)

    def test_get_formulae_existing(self):
        '''COMMENT'''
        this_formula = Formula('C6H12O6', 'KEGG COMPOUND')
        self.assertTrue(this_formula in self.__existing.get_formulae())

    def test_get_formulae_secondary(self):
        '''COMMENT'''
        this_formula = Formula('H2O', 'ChEBI')
        self.assertTrue(this_formula in self.__secondary.get_formulae())

    def test_get_formula_existing(self):
        '''COMMENT'''
        self.assertTrue(self.__existing.get_formula() == 'C6H12O6')

    def test_get_formula_secondary(self):
        '''COMMENT'''
        self.assertTrue(self.__secondary.get_formula() == 'H2O')

    def test_get_mass_existing(self):
        '''COMMENT'''
        self.assertEqual(self.__existing.get_mass(), 180.15588)

    def test_get_mass_secondary(self):
        '''COMMENT'''
        self.assertEqual(self.__secondary.get_mass(), 18.01530)

    def test_get_charge_existing(self):
        '''COMMENT'''
        self.assertEqual(self.__existing.get_charge(), 0)

    def test_get_charge_secondary(self):
        '''COMMENT'''
        self.assertEqual(self.__secondary.get_charge(), 0)

    def test_get_charge_secondary2(self):
        '''COMMENT'''
        self.assertEquals(-2, ChebiEntity(43474).get_charge())

    def test_get_comments_existing(self):
        '''COMMENT'''
        this_chebi_entity = ChebiEntity(29044)
        this_comment = Comment('General', 'General',
                               'The substituent name \'3-oxoprop-2-enyl\' is '
                               'incorrect but is used in various databases.',
                               datetime.datetime.strptime('2005-03-18',
                                                          '%Y-%M-%d'))
        self.assertTrue(this_comment in this_chebi_entity.get_comments())

    def test_get_comments_secondary(self):
        '''COMMENT'''
        this_chebi_entity = ChebiEntity(11505)
        this_comment = Comment('General', 'General',
                               'The substituent name \'3-oxoprop-2-enyl\' is '
                               'incorrect but is used in various databases.',
                               datetime.datetime.strptime('2005-03-18',
                                                          '%Y-%M-%d'))
        self.assertTrue(this_comment in this_chebi_entity.get_comments())

    def test_get_source_existing(self):
        '''COMMENT'''
        self.assertEqual(self.__existing.get_source(), 'KEGG COMPOUND')

    def test_get_source_secondary(self):
        '''COMMENT'''
        self.assertEqual(self.__secondary.get_source(), 'KEGG COMPOUND')

    def test_get_prnt_id_existing(self):
        '''COMMENT'''
        self.assertTrue(math.isnan(self.__existing.get_parent_id()))

    def test_get_prnt_id_secondary(self):
        '''COMMENT'''
        self.assertEqual(self.__secondary.get_parent_id(), 15377)

    def test_get_name_existing(self):
        '''COMMENT'''
        self.assertEqual(self.__existing.get_name(), 'D-glucopyranose')

    def test_get_name_secondary(self):
        '''COMMENT'''
        self.assertEqual(self.__secondary.get_name(), 'water')

    def test_get_definition_existing(self):
        '''COMMENT'''
        self.assertEqual(self.__existing.get_definition(),
                         'A glucopyranose having D-configuration.')

    def test_get_definition_secondary(self):
        '''COMMENT'''
        this_chebi_entity = ChebiEntity(41140)
        self.assertEqual(this_chebi_entity.get_definition(),
                         'D-Glucopyranose with beta configuration at the '
                         'anomeric centre.')

    def test_get_mod_on_existing(self):
        '''COMMENT'''
        self.assertTrue(self.__existing.get_modified_on() >
                        datetime.datetime.strptime('2014-01-01',
                                                   '%Y-%M-%d'))

    def test_get_mod_on_secondary(self):
        '''COMMENT'''
        self.assertIsNotNone(self.__secondary.get_modified_on())

    def test_get_created_by_existing(self):
        '''COMMENT'''
        self.assertEqual(self.__existing.get_created_by(), 'CHEBI')

    def test_get_created_by_secondary(self):
        '''COMMENT'''
        self.assertEqual(self.__secondary.get_created_by(), 'ops$mennis')

    def test_get_star_existing(self):
        '''COMMENT'''
        self.assertEqual(self.__existing.get_star(), 3)

    def test_get_star_secondary(self):
        '''COMMENT'''
        self.assertEqual(self.__secondary.get_star(), 3)

    def test_get_db_acc_existing(self):
        '''COMMENT'''
        dat_acc = DatabaseAccession('MetaCyc accession', 'D-Glucose',
                                    'MetaCyc')
        self.assertTrue(dat_acc in self.__existing.get_database_accessions())

    def test_get_db_acc_secondary(self):
        '''COMMENT'''
        dat_acc = DatabaseAccession('MetaCyc accession', 'WATER', 'MetaCyc')
        self.assertTrue(dat_acc in self.__secondary.get_database_accessions())

    def test_get_inchi_existing(self):
        '''COMMENT'''
        inchi = 'InChI=1S/C6H12O6/c7-1-2-3(8)4(9)5(10)6(11)12-2/' + \
            'h2-11H,1H2/t2-,3-,4+,5-,6?/m1/s1'
        self.assertEqual(self.__existing.get_inchi(), inchi)

    def test_get_inchi_secondary(self):
        '''COMMENT'''
        self.assertEqual(self.__secondary.get_inchi(), 'InChI=1S/H2O/h1H2')

    def test_get_inchi_key_existing(self):
        '''COMMENT'''
        self.assertEqual(self.__existing.get_inchi_key(),
                         'WQZGKKKJIJFFOK-GASJEMHNSA-N')

    def test_get_inchi_key_secondary(self):
        '''COMMENT'''
        self.assertEqual(self.__secondary.get_inchi_key(),
                         'XLYOFNOQVPJJNP-UHFFFAOYSA-N')

    def test_get_smiles_existing(self):
        '''COMMENT'''
        self.assertEqual(self.__existing.get_smiles(),
                         'OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O')

    def test_get_smiles_secondary(self):
        '''COMMENT'''
        self.assertEqual(self.__secondary.get_smiles(), '[H]O[H]')

    def test_get_mol_existing(self):
        '''COMMENT'''
        chebi_id = 73938
        this_chebi_entity = ChebiEntity(chebi_id)
        self.assertEqual(this_chebi_entity.get_mol(),
                         _read_mol_file(chebi_id))

    def test_get_mol_secondary(self):
        '''COMMENT'''
        self.assertEqual(self.__secondary.get_mol(), _read_mol_file(15377))

    def test_get_mol_file_existing(self):
        '''COMMENT'''
        chebi_id = 73938
        self.__get_mol_file(chebi_id, chebi_id)

    def test_get_mol_file_secondary(self):
        '''COMMENT'''
        read_id = 15377
        retrieved_id = 42857
        self.__get_mol_file(read_id, retrieved_id)

    def test_get_names_existing(self):
        '''COMMENT'''
        this_name = Name('Grape sugar', 'SYNONYM', 'KEGG COMPOUND', False,
                         'en')
        self.assertTrue(this_name in self.__existing.get_names())

    def test_get_names_secondary(self):
        '''COMMENT'''
        this_name = Name('eau', 'SYNONYM', 'ChEBI', False, 'fr')
        self.assertTrue(this_name in self.__secondary.get_names())

    def test_get_references_existing(self):
        '''COMMENT'''
        this_chebi_entity = ChebiEntity(15347)
        this_reference = Reference('WO2006008754', 'Patent', '',
                                   'NOVEL INTERMEDIATES FOR LINEZOLID '
                                   'AND RELATED COMPOUNDS')

        self.assertTrue(this_reference in this_chebi_entity.get_references())

    def test_get_references_secondary(self):
        '''COMMENT'''
        this_chebi_entity = ChebiEntity(22182)
        this_reference = Reference('WO2006008754', 'Patent', '',
                                   'NOVEL INTERMEDIATES FOR LINEZOLID '
                                   'AND RELATED COMPOUNDS')
        self.assertTrue(this_reference in this_chebi_entity.get_references())

    def test_get_cmp_orig_existing(self):
        '''COMMENT'''
        this_compound_origin = CompoundOrigin('Homo sapiens', 'NCBI:9606',
                                              None, None, None, None,
                                              'DOI', '10.1038/nbt.2488', None)
        self.assertTrue(this_compound_origin
                        in self.__existing.get_compound_origins())

    def test_get_cmp_orig_secondary(self):
        '''COMMENT'''
        this_compound_origin = CompoundOrigin('Homo sapiens', 'NCBI:9606',
                                              None, None, None, None,
                                              'DOI', '10.1038/nbt.2488', None)
        self.assertTrue(this_compound_origin
                        in self.__secondary.get_compound_origins())

    def test_get_out_existing(self):
        '''COMMENT'''
        this_relation = Relation('is_a', 17634, 'C')
        self.assertTrue(this_relation in self.__existing.get_outgoings())

    def test_get_out_secondary(self):
        '''COMMENT'''
        this_relation = Relation('has_role', 48360, 'C')
        self.assertTrue(this_relation in self.__secondary.get_outgoings())

    def test_get_in_existing(self):
        '''COMMENT'''
        this_relation = Relation('has_functional_parent', 15866, 'C')
        self.assertTrue(this_relation in self.__existing.get_incomings())

    def test_get_in_secondary(self):
        '''COMMENT'''
        this_relation = Relation('is_conjugate_acid_of', 29412, 'C')
        self.assertTrue(this_relation in self.__secondary.get_incomings())

    def __get_mol_file(self, read_id, retrieved_id):
        '''COMMENT'''
        mol_read = _read_mol_file(read_id)
        this_chebi_entity = ChebiEntity(retrieved_id)
        textfile_retrieved = open(this_chebi_entity.get_mol_filename(), 'r')
        mol_retrieved = textfile_retrieved.read()
        textfile_retrieved.close()
        self.assertEquals(mol_read, mol_retrieved)


class TestChemicalDataParser(unittest.TestCase):
    '''COMMENT'''

    def test_get_formulae_size(self):
        '''COMMENT'''
        self.assertTrue(1 < len(parsers.get_formulae(6504)))

    def test_get_formulae_size_neg(self):
        '''COMMENT'''
        self.assertTrue(0 == len(parsers.get_formulae(-1)))

    def test_get_formulae(self):
        '''COMMENT'''
        self.assertTrue(Formula('C8H11NO3', 'KEGG COMPOUND')
                        in parsers.get_formulae(1))

    def test_get_formulae_neg(self):
        '''COMMENT'''
        self.assertFalse(('C8H11NO3', 'KEGG COMPOUND')
                         in parsers.get_formulae(-1))

    def test_get_mass(self):
        '''COMMENT'''
        self.assertEqual(338.20790, parsers.get_mass(77120))

    def test_get_mass_neg(self):
        '''COMMENT'''
        self.assertTrue(math.isnan(parsers.get_mass(-1)))

    def test_get_charge(self):
        '''COMMENT'''
        self.assertEquals(-4, parsers.get_charge(77099))

    def test_get_charge_neg(self):
        '''COMMENT'''
        self.assertTrue(math.isnan(parsers.get_charge(-1)))


class TestCommentsParser(unittest.TestCase):
    '''COMMENT'''

    def test_get_comments_size(self):
        '''COMMENT'''
        self.assertTrue(3 < len(parsers.get_comments(5407)))

    def test_get_comments_size_empty(self):
        '''COMMENT'''
        self.assertTrue(0 == len(parsers.get_comments(7)))

    def test_get_comments_size_neg(self):
        '''COMMENT'''
        self.assertTrue(0 == len(parsers.get_comments(-1)))

    def test_get_comments(self):
        '''COMMENT'''
        self.assertIn(Comment
                      ('DatabaseAccession',
                       'DatabaseAccession',
                       'Z stereomer',
                       datetime.datetime.strptime('2006-09-01', '%Y-%M-%d')),
                      parsers.get_comments(5407))

    def test_get_comments_neg(self):
        '''COMMENT'''
        self.assertEqual(parsers.get_comments(-1), [])


class TestCompoundOriginsParser(unittest.TestCase):
    '''COMMENT'''

    def test_get_comp_orig_size(self):
        '''COMMENT'''
        self.assertTrue(4 < len(parsers.get_compound_origins(16415)))

    def test_get_comp_orig_size_empty(self):
        '''COMMENT'''
        self.assertEquals(0, len(parsers.get_compound_origins(1641)))

    def test_get_comp_orig_size_neg(self):
        '''COMMENT'''
        self.assertEquals(0, len(parsers.get_compound_origins(-1)))

    def test_get_cmp_orig(self):
        '''COMMENT'''
        comp_orig = CompoundOrigin('Neurospora crassa',
                                   'NCBI:5141',
                                   'mycelium',
                                   'BTO:0001436',
                                   '74 OR23 1',
                                   None,
                                   'PubMed Id',
                                   '21425845',
                                   'Lyophilized mycelia extracted with '
                                   'mixture of methanol and chloroform')
        self.assertIn(comp_orig, parsers.get_compound_origins(67813))


class TestCompoundsParser(unittest.TestCase):
    '''COMMENT'''

    def test_get_status(self):
        '''COMMENT'''
        self.assertEquals('C', parsers.get_status(584977))

    def test_get_status_neg(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_status(-1))

    def test_get_source(self):
        '''COMMENT'''
        self.assertEquals('ChEMBL', parsers.get_source(718203))

    def test_get_source_neg(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_source(-1))

    def test_get_parent_id(self):
        '''COMMENT'''
        self.assertEquals(34107, parsers.get_parent_id(76262))

    def test_get_parent_id_neg(self):
        '''COMMENT'''
        self.assertTrue(math.isnan(parsers.get_parent_id(-1)))

    def test_get_parent_id_undefined(self):
        '''COMMENT'''
        self.assertTrue(math.isnan(parsers.get_parent_id(41100)))

    def test_get_name(self):
        '''COMMENT'''
        name = '3,7-DIHYDROXY-2-NAPHTHOIC ACID'
        self.assertEquals(name, parsers.get_name(41106))

    def test_get_name_neg(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_name(-1))

    def test_get_name_null(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_name(7483))

    def test_get_definition(self):
        '''COMMENT'''
        definition = 'A glycerophosphocholine having an unspecified acyl ' + \
            'group attached at the 2-position.'
        self.assertEquals(definition, parsers.get_definition(11502))

    def test_get_definition_neg(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_definition(-1))

    def test_get_definition_null(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_definition(18945))

    def test_get_modified_on(self):
        '''COMMENT'''
        self.assertTrue(parsers.get_modified_on(57857) >
                        datetime.datetime.strptime('2014-01-01', '%Y-%M-%d'))

    def test_get_modified_on_neg(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_modified_on(-1))

    def test_get_modified_on_null(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_modified_on(6981))

    def test_get_created_by(self):
        '''COMMENT'''
        self.assertEquals('CHEBI', parsers.get_created_by(6030))

    def test_get_created_by_neg(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_created_by(-1))

    def test_get_star(self):
        '''COMMENT'''
        self.assertEquals(3, parsers.get_star(8082))

    def test_get_star_neg(self):
        '''COMMENT'''
        self.assertTrue(math.isnan(parsers.get_star(-1)))


class TestDatabaseAccessionParser(unittest.TestCase):
    '''COMMENT'''

    def test_get_dat_acc_size(self):
        '''COMMENT'''
        self.assertTrue(5 < len(parsers.get_database_accessions(7)))

    def test_get_dat_acc_size_neg(self):
        '''COMMENT'''
        self.assertEquals(0, len(parsers.get_database_accessions(-1)))

    def test_get_dat_acc_size_empty(self):
        '''COMMENT'''
        self.assertEquals(0, len(parsers.get_database_accessions(60260)))

    def test_get_dat_acc(self):
        '''COMMENT'''
        dat_acc = DatabaseAccession('PubMed citation', '214717', 'SUBMITTER')
        self.assertIn(dat_acc, parsers.get_database_accessions(60261))

    def test_get_dat_acc_neg_type(self):
        '''COMMENT'''
        dat_acc = DatabaseAccession('ChEBI', '214717', 'SUBMITTER')
        self.assertNotIn(dat_acc, parsers.get_database_accessions(60261))

    def test_get_dat_acc_neg_acc_no(self):
        '''COMMENT'''
        dat_acc = DatabaseAccession('PubMed citation', '123456', 'SUBMITTER')
        self.assertNotIn(dat_acc, parsers.get_database_accessions(60261))

    def test_get_dat_acc_neg_source(self):
        '''COMMENT'''
        dat_acc = DatabaseAccession('PubMed citation', '214717', 'PubChem')
        self.assertNotIn(dat_acc, parsers.get_database_accessions(60261))


class TestDownloader(unittest.TestCase):
    '''COMMENT'''

    def test_get_file(self):
        '''COMMENT'''
        self.assertIsNotNone(parsers.get_file('chebiId_inchi.tsv'))


class TestInchiParser(unittest.TestCase):
    '''COMMENT'''

    def test_get_inchi(self):
        '''COMMENT'''
        inchi = 'InChI=1S/H2O/h1H2'
        self.assertEqual(parsers.get_inchi(15377), inchi)

    def test_get_inchi_neg(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_inchi(-1))


class TestNamesParser(unittest.TestCase):
    '''COMMENT'''

    def test_get_names_size(self):
        '''COMMENT'''
        self.assertTrue(5 < len(parsers.get_names(14)))

    def test_get_names_size_neg(self):
        '''COMMENT'''
        self.assertEquals(0, len(parsers.get_names(-1)))

    def test_get_names_size_empty(self):
        '''COMMENT'''
        self.assertEquals(0, len(parsers.get_names(81100)))

    def test_get_names(self):
        '''COMMENT'''
        nme = Name('2-(p-Chloro-o-tolyloxy)propionic acid',
                   'SYNONYM', 'ChemIDplus', False, 'en')
        self.assertIn(nme, parsers.get_names(75711))


class TestReferenceParser(unittest.TestCase):
    '''COMMENT'''

    def test_get_references_size(self):
        '''COMMENT'''
        self.assertTrue(100 < len(parsers.get_references([76181])))

    def test_get_references_size_neg(self):
        '''COMMENT'''
        self.assertEquals(0, len(parsers.get_references([-1])))

    def test_get_references_size_empty(self):
        '''COMMENT'''
        self.assertEquals(0, len(parsers.get_references([1])))

    def test_get_references(self):
        '''COMMENT'''
        ref = Reference('O13340', 'UniProt', 'CC - INDUCTION',
                        'Podosporapepsin')
        self.assertIn(ref, parsers.get_references([27594]))

    def test_get_refs_three_tokens(self):
        '''COMMENT'''
        ref = Reference('49658669', 'PubChem')
        self.assertIn(ref, parsers.get_references([8]))


class TestRelationParser(unittest.TestCase):
    '''COMMENT'''

    def test_get_outgoings_size(self):
        '''COMMENT'''
        self.assertTrue(2 < len(parsers.get_outgoings(4167)))

    def test_get_incomings_size(self):
        '''COMMENT'''
        self.assertTrue(19 < len(parsers.get_incomings(4167)))

    def test_get_outgoings_neg_size(self):
        '''COMMENT'''
        self.assertTrue(0 == len(parsers.get_outgoings(-1)))

    def test_get_incomings_neg_size(self):
        '''COMMENT'''
        self.assertTrue(0 == len(parsers.get_incomings(-1)))

    def test_get_outgoings_empty_size(self):
        '''COMMENT'''
        self.assertTrue(0 == len(parsers.get_outgoings(1)))

    def test_get_incomings_empty_size(self):
        '''COMMENT'''
        self.assertTrue(0 == len(parsers.get_incomings(1)))

    def test_get_outgoings(self):
        '''COMMENT'''
        rel = Relation('is_a', 17634, 'C')
        self.assertIn(rel, parsers.get_outgoings(4167))

    def test_get_incomings(self):
        '''COMMENT'''
        rel = Relation('has_functional_parent', 15866, 'C')
        self.assertIn(rel, parsers.get_incomings(4167))


class TestStructuresParser(unittest.TestCase):
    '''COMMENT'''

    def test_get_inchi_key_missing(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_inchi_key(1))

    def test_get_inchi_key_neg(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_inchi_key(-1))

    def test_get_inchi_key(self):
        '''COMMENT'''
        this_structure = Structure(
                            'VIDUVSPOWYVZIC-IMJSIDKUSA-O',
                            Structure.InChIKey, 1)
        self.assertEquals(this_structure,
                          parsers.get_inchi_key(73938))

    def test_get_inchi_key_neg_struct(self):
        '''COMMENT'''
        this_structure = Structure(
                            'made_up',
                            Structure.InChIKey, 1)
        self.assertNotEquals(this_structure,
                             parsers.get_inchi_key(73938))

    def test_get_inchi_key_neg_type(self):
        '''COMMENT'''
        this_structure = Structure(
                            'VIDUVSPOWYVZIC-IMJSIDKUSA-O',
                            Structure.mol, 1)
        self.assertNotEquals(this_structure, parsers.get_inchi_key(73938))

    def test_get_inchi_key_neg_dim(self):
        '''COMMENT'''
        this_structure = Structure(
                            'VIDUVSPOWYVZIC-IMJSIDKUSA-O',
                            Structure.InChIKey, 123456)
        self.assertNotEquals(this_structure,
                             parsers.get_inchi_key(73938))

    def test_get_smiles_missing(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_smiles(1))

    def test_get_smiles_neg(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_smiles(-1))

    def test_get_smiles(self):
        '''COMMENT'''
        this_structure = Structure(
                            'NC(=[NH2+])NCC[C@H](O)[C@H]([NH3+])C([O-])=O',
                            Structure.SMILES, 1)
        self.assertEquals(this_structure, parsers.get_smiles(73938))

    def test_get_mol_missing(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_mol(1))

    def test_get_mol_neg(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_mol(-1))

    def test_get_mol(self):
        '''COMMENT'''
        self.__get_mol_id(73938)

    def test_get_mol_comma_name(self):
        '''COMMENT'''
        self.__get_mol_id(57587)

    def test_get_mol_file_missing(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_mol_filename(1))

    def test_get_mol_file_neg(self):
        '''COMMENT'''
        self.assertIsNone(parsers.get_mol_filename(-1))

    def test_get_mol_file(self):
        '''COMMENT'''
        directory = os.path.dirname(os.path.realpath(__file__))
        textfile_read = open(directory + '/ChEBI_73938.mol', 'r')
        mol_read = textfile_read.read()
        textfile_retrieved = open(parsers.get_mol_filename(73938), 'r')
        mol_retrieved = textfile_retrieved.read()
        textfile_read.close()
        textfile_retrieved.close()
        self.assertEquals(mol_read, mol_retrieved)

    def __get_mol_id(self, chebi_id):
        '''COMMENT'''
        directory = os.path.dirname(os.path.realpath(__file__))
        textfile_read = open(directory + '/ChEBI_' + str(chebi_id) +
                             '.mol', 'r')
        mol_read = textfile_read.read()
        this_structure = Structure(mol_read, Structure.mol, 2)
        self.assertEquals(this_structure, parsers.get_mol(chebi_id))


def _read_mol_file(chebi_id):
    '''COMMENT'''
    directory = os.path.dirname(os.path.realpath(__file__))
    textfile_read = open(directory + '/ChEBI_' + str(chebi_id) + '.mol', 'r')
    mol_file_read = textfile_read.read()
    textfile_read.close()
    return mol_file_read
