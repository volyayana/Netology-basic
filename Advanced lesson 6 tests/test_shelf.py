import shelf_functions as sf

class TestShelf:

    def test_get_documents_success(self):
        assert sf.get_doc_owner_name('2207 876234') == 'Василий Гупкин'
    
    def test_get_documents_fail(self):
        assert sf.get_doc_owner_name('2207 876234') != 'Геннадий Покемонов'

    def test_get_documents_no_document(self):
        assert sf.get_doc_owner_name('2207 876235') == None
    
    def test_get_documents_empty_doc_number(self):
       assert sf.get_doc_owner_name('') == None

    
    def test_add_shelf_success(self):
        old_directories_len = len(sf.directories)
        assert sf.add_new_shelf(10) == (10, True)
        assert len(sf.directories) == old_directories_len + 1
    
    def test_add_shelf_empty_number(self):
        old_directories_len = len(sf.directories)
        assert sf.add_new_shelf()  == ('Укажите номер полки', False)

    def test_add_shelf_existing(self):
        old_directories_len = len(sf.directories)
        assert sf.add_new_shelf(10) == (10, False)
        assert len(sf.directories) == old_directories_len
        
    
    def test_remove_doc_success(self):
        old_documents_len = len(sf.directories['1'])
        assert sf.delete_doc('2207 876234') == ('2207 876234', True)
        assert len(sf.directories['1']) == old_documents_len - 1

    def test_remove_doc_non_existing(self):
        assert sf.delete_doc('2207 876234') == None

    def test_remove_doc_non_numeric_value(self):
        assert sf.delete_doc('-2813719') == None

    def test_remove_doc_empty_list(self):
        sf.delete_doc('11-2')
        sf.delete_doc('5455 028765')
        sf.delete_doc('10006')
        assert sf.delete_doc('10006') == None




if __name__ == '__main__':
    print(sf.get_doc_owner_name(''))