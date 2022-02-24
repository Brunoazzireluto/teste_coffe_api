import os
import oci
from oci.object_storage import UploadManager
from app import photos

basedir = os.path.abspath(os.path.dirname(__file__))
file = 'oci_key'
key_file= os.path.join(basedir, file +"."+"pem")

config = {
    "user": 'ocid1.user.oc1..aaaaaaaavh5u3tuyp6iwnlq65ea6kqsowbyli3pejxa66t3ea7lrveaajb5q',
    "key_file": key_file,
    "fingerprint":'37:f1:a4:41:c9:aa:97:8b:70:dd:5e:53:be:06:d5:48',
    "tenancy": 'ocid1.tenancy.oc1..aaaaaaaa25jojhihrfvtldw6cxjq7agfoaittrfiyclkp5z3jzwchfippxya',
    "region": 'sa-saopaulo-1'
}

osc = oci.object_storage.ObjectStorageClient(config)
up = UploadManager(osc, allow_multipart_uploads=True)
namespace = 'gru0o0u6fuun'
bucket_name ='cafe'


class UploadOci():
    """ Classe para Facilitar o processo de Upload de Fotos para o Bucket da OCI"""

    #Função construtora
    def __init__(self, arq, name):
        self.arq = arq
        self.name = name

    def upload_image(self):
        """Função para fazer o upload do arquivo diretamente no bucket definido nas variaveis."""
        filename = photos.save(self.arq, name=self.name+'.'.upper()) # Salva a Foto no servidor
        path = os.path.abspath(photos.path(filename)) # Retorna o caminho da Foto
        name = photos.path(filename).split('/')# Define uma lista contendo todo o caminho para o arquivo.
        # Faz o upload do arquivo com as variaveis definidas anteriormente e o nome do arquivo, que está na ultima posicção da lista
        up.upload_file(namespace, bucket_name, name[-1].upper(), path, content_type=self.arq.content_type)
        os.remove(path) #Exclue o arquivo do servidor
        return 'https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/gru0o0u6fuun/b/cafe/o/'+name[-1].upper() # retorna o link publico


    def delete_image(self, name_arq):
        osc.delete_object(namespace, bucket_name, 'cafe/o/'+name_arq )