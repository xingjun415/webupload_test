import threading, uuid, os, shutil

class FolderManager:
    __tmp_lock = threading.Lock()
    __merge_file_lock = threading.Lock()

    __data_dir = './data'

    @classmethod
    def get_tmp_folder(cls, filename):
        tmp_folder = os.path.join( cls.__data_dir,filename + '__tmp')
        if not os.path.exists(tmp_folder):
            with cls.__tmp_lock:
                if not os.path.exists(tmp_folder):
                    os.makedirs(tmp_folder)

        return tmp_folder


    @classmethod
    def get_tmp_file_name(cls, filename, chunk_count, chunk_index):
        return filename + '.{0}__{1}'.format(chunk_count, chunk_index)


    @classmethod
    def get_tmp_file_path(cls, filename, chunk_count, chunk_index):
        return os.path.join(cls.get_tmp_folder(filename), cls.get_tmp_file_name(filename, chunk_count, chunk_index))


    @classmethod
    def get_save_path(cls, filename):
        save_path = os.path.join( cls.__data_dir, str(uuid.uuid1()))
        os.makedirs(save_path)
        return os.path.join(save_path, filename)


    @classmethod
    def is_need_merge(cls, chunk_count, tmp_file_path):
        if os.path.exists(tmp_file_path):
            file_list = os.listdir(tmp_file_path)
            return len(file_list) == chunk_count
        return False


    @classmethod
    def save_tmp_file(cls, uploadfile, chunk_count, chunk_index):
        tmp_file_path = cls.get_tmp_file_path( uploadfile.name, chunk_count, chunk_index)
        with open(tmp_file_path, 'wb') as tmp_file:
            tmp_file.write(uploadfile.read())

        return cls.merge_save_file(uploadfile.name, cls.get_tmp_folder(uploadfile.name), chunk_count)

    @classmethod
    def merge_save_file(cls, filename, tmp_folder, chunk_count):
        print("Merge : thread id ==> ", threading.get_ident())
        if cls.is_need_merge(chunk_count, tmp_folder):
            with cls.__merge_file_lock:
                if not cls.is_need_merge(chunk_count, tmp_folder):
                    print("Merge : thread id ==> {0}, no need merge, another thread merged".format(threading.get_ident()))
                    return None

                print("Merge : thread id ==> {0}, merge".format(threading.get_ident()))
                sorted_file_list = cls.__get_sorted_file_list(tmp_folder)
                save_path = cls.get_save_path(filename)
                with open(save_path, 'wb') as save_file:
                    for tmp_filename in sorted_file_list:
                        with open(os.path.join( tmp_folder, tmp_filename), 'rb') as tmp_file:
                            save_file.write(tmp_file.read())

                cls.clear_tmp_file(filename)
            return save_path
        print("Merge : thread id ==> {0}, no need merge".format(threading.get_ident()))
        return None

    @classmethod
    def clear_tmp_file(cls, filename):
        tmp_folder = cls.get_tmp_folder(filename)
        shutil.rmtree(tmp_folder, ignore_errors = True)


    @classmethod
    def __get_sorted_file_list(cls, tmp_folder):
        file_list = os.listdir(tmp_folder)
        return sorted(file_list, key = lambda x : cls.__parse_chunk_index(x))


    @classmethod
    def __parse_chunk_count(cls, tmp_filename):
        return int(tmp_filename.rsplit('.', 1)[1].split('__')[0])

    @classmethod
    def __parse_chunk_index(cls, tmp_filename):
        return int(tmp_filename.rsplit('.', 1)[1].split('__')[1])
