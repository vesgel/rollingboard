# -*- coding: utf-8 -*-
import urllib
import os
import tarfile


class DataManager:
    def __init__(self, data_path):
	self.data_path = data_path
	self.repo_base = "http://www.emrealadag.com/dosyalar/program/rollingboard"
	self.index_file = self.get_url("index.txt")
	self.fetch_available_data()
	
    def get_url(self, filename):
	return "%s/%s" % (self.repo_base, filename)

    def get_local_path(self, filename):
	return "%s/%s" % (self.data_path, filename)
	
    def fetch_available_data(self):
	records = urllib.urlopen(self.index_file).read().split("\n")
	self.record_list = map(lambda record: record.split("\t"), records)
    	
    def download_record(self, number):
	tarname = self.record_list[number][1]
	extracted_files = self._download_targz(self.get_url(tarname))
	os.system("mv %s %s" % ( " ".join(extracted_files) , self.data_path ) )
	os.remove(tarname)
    
    def _download_file(self, url):
	filename = url.split('/')[-1]
	print "Downloading", url
	webFile = urllib.urlopen(url)
	
	localFile = open(filename, 'w')
	localFile.write(webFile.read())
	webFile.close()
	localFile.close()
	return filename
	
    def untar(self, filename):
	if not filename: return
	new_filename = ".".join(filename.split('.')[:-2])
	
	tar = tarfile.open(filename, 'r:gz')
	names = tar.getnames()
	
	for item in tar:
	    tar.extract(item)
	print 'Extracted.'
	return names
	
    def _download_targz(self, url):
	
	filename = self._download_file(url)
	if filename:
	    extracted_files = self.untar(filename)
	else:
	    print "Could not _download"
	
	# The file extracted
	return extracted_files
if __name__ == "__main__":
    dm = DataManager("/home/emre/git/rollingboard/plasmoid/contents/data")
