import unittest
import os
from ace import sources, database, datatable, exporter
import json
from os.path import dirname, join, exists, sep as pathsep
import os


def get_test_data_path():
    """Returns the path to test datasets, terminated with separator (/ vs \)"""
    # TODO: do not rely on __file__
    return join(dirname(__file__), 'data') + pathsep


class TestACE(unittest.TestCase):

    def setUp(self):
        self.db = database.Database('ace_test_database.tmp')
        self.manager = sources.SourceManager(self.db)

    def tearDown(self):
        os.remove('ace_test_database.tmp')

    # Just run some very basic tests for now, one per Source.
    # Make sure that the right number of tables, activations,
    # etc. are returned.
    def testFrontiersSource(self):
        filename = join(get_test_data_path(), 'frontiers.html')
        html = open(filename).read()
        source = self.manager.identify_source(html)
        article = source.parse_article(html)
        tables = article.tables
        self.assertEqual(len(tables), 3)
        t = tables[2]
        self.assertEqual(t.number, 5)
        self.assertIsNotNone(t.caption)
        self.assertEqual(t.n_activations, 13)

    def testScienceDirectSource(self):
        filename = join(get_test_data_path(), 'neuroimage.html')
        html = open(filename).read()
        source = self.manager.identify_source(html)
        article = source.parse_article(html)
        tables = article.tables
        self.assertEqual(len(tables), 3)
        t = tables[2]
        self.assertEqual(t.number, 4)
        self.assertIsNotNone(t.caption)
        self.assertEqual(t.n_activations, 30)

    def testPlosSource(self):
        filename = join(get_test_data_path(), 'plosone.html')
        html = open(filename).read()
        source = self.manager.identify_source(html)
        article = source.parse_article(html)
        tables = article.tables
        self.assertEqual(len(tables), 1)
        t = tables[0]
        self.assertEqual(t.number, 1)
        self.assertIsNotNone(t.caption)
        self.assertEqual(t.n_activations, 12)

    def testDatabaseProcessingStream(self):
        self.db.add_articles(get_test_data_path() + '*.html')
        self.assertEqual(len(self.db.articles), 6)
        exporter.export_database(self.db, 'exported_db.txt')
        self.assertTrue(exists('exported_db.txt'))
        os.remove('exported_db.txt')



suite = unittest.TestLoader().loadTestsFromTestCase(TestACE)

if __name__ == '__main__':
    unittest.main()
