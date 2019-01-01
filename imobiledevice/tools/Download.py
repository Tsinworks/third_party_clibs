import os, sys, platform, threading, time, urllib2, urllib, zipfile, tempfile, hashlib, logging

max_thread = 10
logging.basicConfig(level=logging.INFO)

class _RangeContentDownloader(threading.Thread):

    def __init__(self, id, url, start, end, part_file_name, file_lock):
        self.id = id
        self.url = url
        self.start = start
        self.end = end
        self.total_size = int(end) - int(start)
        self.part_path = part_file_name
        self.file = open(part_file_name, 'wb')
        self.written_size = 0
        self.session = None
        self.retry_setup_no = 0
        self.retry_receive_no = 0
        self.memcache_size = 1024 * 1024 * 4
        self.current_data = None

    def start_download(self):
        ret = self._setup_request()
        if ret > 0:
            while ret < 5 and ret != 0:
                ret = self._setup_request()
            if not self.session:
                logging.warning('chunk%d failed to setup session, after retry 5 times !', self.id)
        logging.info('start transfering chunk %d', self.id)
        ret = self._receive()
        if ret > 0:
            while ret < 5 and ret != 0:
                ret = self._receive()
        self.file.close()

    def _setup_request(self):
        try:
            req = urllib2.Request(self.url)
            req.headers['Range'] = 'bytes=%d-%d' % (self.start, self.end)
            self.session = urllib2.urlopen(req)
            return 0
        except Exception, e:
            self.retry_setup_no = self.retry_setup_no + 1
            logging.warning('chunk%d: _setup_request: retry time: %d', self.id, self.retry_setup_no)
            return self.retry_receive_no

    def _receive(self):
        try:
            buf_sz = 1024 * 4
            data_piece = self.session.read(buf_sz)
            pending_data = data_piece
            while data_piece:
                data_piece = self.session.read(buf_sz)
                if len(data_piece) < buf_sz:
                    # finish transfering
                    if data_piece:
                        pending_data = pending_data + data_piece
                    self._sendto_filestream(pending_data, len(pending_data))
                    logging.info('chunk%d: >>>> finish transfering section %d-%d', self.id, self.start, self.end)
                    break
                if not pending_data:
                    pending_data = data_piece
                else:
                    pending_data = pending_data + data_piece
                buf_sz = buf_sz * 2
                if len(pending_data) > self.memcache_size:
                    logging.info('pending data size larger than memcache size, need to write to file, size %d', len(pending_data))
                    self._sendto_filestream(pending_data, len(pending_data))
                    pending_data = None
            return 0
        except Exception, e:
            self.retry_receive_no = self.retry_receive_no + 1
            logging.warning('chunk%d: _receive: retry time: %d', self.id, self.retry_receive_no)
            return self.retry_receive_no

    def _sendto_filestream(self, data, offset):
        self.file.write(data)
        self.file.flush()
            
class Downloader(threading.Thread):
    def __init__(self, url):
        self.url = url
        self.threadNum = 16
        self.lock = threading.RLock()
        self.part_jobs = []
        threading.Thread.__init__(self)


    def getFilename(self):
        url = self.url
        protocol, s1 = urllib.splittype(url)
        host, path = urllib.splithost(s1)
        filename = path.split('/')[-1]
        if '.' not in filename:
            filename = None
        print "Do you want to change a filename?('y' or other words)"
        answer = raw_input()
        if answer == "y" or filename is None:
            print "Please input your new filename:"
            filename = raw_input()
        return filename

    def getLength(self):
        opener = urllib2.build_opener()
        req = opener.open(self.url)
        meta = req.info()
        length = int(meta.getheaders("Content-Length")[0])
        return length

    def get_range(self):
        ranges = []
        length = self.getLength()
        logging.info('Url: %s\n\tLength: %d MB' % (self.url, length / 1024 / 1024))
        offset = int(int(length) / self.threadNum)
        for i in range(self.threadNum):
            if i == (self.threadNum - 1):
                ranges.append((i*offset, length))
            else:
                ranges.append((i*offset,(i+1)*offset))
        return ranges

    def downloadThread(self, start, end, thread_id):
        part_file_path = os.path.join(tempfile.gettempdir(), '%s_part_%d' % (self.simple_file_name, thread_id))
        range_content = _RangeContentDownloader(thread_id, self.url, start, end, part_file_path, self.lock)
        self.part_jobs.append(range_content)
        range_content.start_download()

    def download(self, fileName=None, simple_name=None):
        filename = fileName if fileName else self.getFilename()
        self.simple_file_name = simple_name
        thread_list = []
        n = 0
        self.time_begin = time.time()
        start_offsets = []
        for ran in self.get_range():
            start, end = ran
            n += 1
            start_offsets.append(start)
            thread = threading.Thread(target=self.downloadThread,args=(start, end, n))
            thread_list.append(thread)
            thread.start()

        for i in thread_list:
             i.join()
        
        logging.info('finish download %s, next join the parts together', self.url)

        self.file = open(filename, 'wb')
        for i in range(self.threadNum):
            path = os.path.join(tempfile.gettempdir(), '%s_part_%d' % (simple_name, i+1))
            with open(path, 'rb') as p_file:
                self.file.seek(start_offsets[i])
                data = p_file.read(1024*1024*4)
                self.file.write(data)
                self.file.flush()
                while data:
                    data = p_file.read(1024*1024*4)
                    self.file.write(data)
                    self.file.flush()
                p_file.close()
            os.remove(path)
        self.file.close()

def download_and_extract(url, extract_dir):
    h = hashlib.md5()
    h.update(url)
    filename = str(h.hexdigest())
    down = Downloader(url)
    dfile_path = os.path.join(tempfile.gettempdir(), filename + '.zip')
    print dfile_path
    down.download(dfile_path, filename)
    zipFile = zipfile.ZipFile(dfile_path)
    zipFile.extractall(extract_dir)
    zipFile.close()