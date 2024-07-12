import os
from datetime import datetime
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.http.request_options import RequestOptions
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from .ConsultorMongo import Handledbmongo



class SharePoint:
    def __init__(self):
        x = Handledbmongo().GetData("confBotInformes",{},{"_id":0})                
        dicDatos = x[0]["configshareit"]


        url_site=dicDatos["url_site"]
        site_name=dicDatos["site_name"]
        doc_library=dicDatos["doc_library"]
        self.USERNAME = dicDatos["USERNAME"]
        self.PASSWORD = dicDatos["PASSWORD"]
        self.Diccarpetasavences =dicDatos["CarpetasAvances"]
        self.Carpetahis = dicDatos["CarpetaHistoricos"]
        self.FolderHis = self.getCarpetaActual()
        
        

        self.SHAREPOINT_SITE = url_site
        self.SHAREPOINT_SITE_NAME = site_name
        self.SHAREPOINT_DOC = doc_library

   

    def getCarpetaActual(self):
        now = datetime.now()		
        current_year = now.year
        current_month = now.month
        return f"{self.Carpetahis}/{current_year}/{str(current_month).zfill(2) if current_month<10 else current_month}"

    def _auth(self):
        conn = ClientContext(self.SHAREPOINT_SITE).with_credentials(
            UserCredential(
                self.USERNAME,
                self.PASSWORD
            )
        )
        return conn

    def _get_files_list(self, folder_name):
        conn = self._auth()
        target_folder_url = f'{self.SHAREPOINT_DOC}/{folder_name}'	    
        print("="*30,target_folder_url)
        root_folder = conn.web.get_folder_by_server_relative_url(target_folder_url)
        root_folder.expand(["Files", "Folders"]).get().execute_query()
        return root_folder.files

    def get_folder_list(self, folder_name):
        conn = self._auth()
        target_folder_url = f'{self.SHAREPOINT_DOC}/{folder_name}'
        root_folder = conn.web.get_folder_by_server_relative_url(target_folder_url)
        root_folder.expand(["Folders"]).get().execute_query()
        return root_folder.folders

    def download_file(self, file_name, folder_name):
        conn = self._auth()
        file_url = f'/sites/{self.SHAREPOINT_SITE_NAME}/{self.SHAREPOINT_DOC}/{folder_name}/{file_name}'

        file = File.open_binary(conn, file_url)
        return file.content

    def download_latest_file(self, folder_name):
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        files_list = self._get_files_list(self.Diccarpetasavences[folder_name])
        file_dict = {}
        for file in files_list:
            dt_obj = datetime.strptime(file.time_last_modified, date_format)
            file_dict[file.name] = dt_obj
        # sort dict object to get the latest file
        file_dict_sorted = {key:value for key, value in sorted(file_dict.items(), key=lambda item:item[1], reverse=True)}    
        latest_file_name = next(iter(file_dict_sorted))
        content = self.download_file(latest_file_name, self.Diccarpetasavences[folder_name])
        return {latest_file_name: content}
    
    def download_all_files(self):
        #files_list = self._get_files_list(self.Diccarpetasavences[folder_name])
        files_list = self._get_files_list(self.FolderHis)           
        file_dict = {}
        for file in files_list:												
            #file_dict[file.name] = self.download_file(file.name, self.Diccarpetasavences[folder_name]
            file_dict[file.name] = self.download_file(file.name, self.FolderHis)

        return file_dict
    
    def download_all_files_avance(self,ciudad):
        print(self.Diccarpetasavences[ciudad])
        files_list = self._get_files_list(self.Diccarpetasavences[ciudad])           
        file_dict = {}
        for file in files_list:
            file_dict[file.name] = self.download_file(file.name, self.Diccarpetasavences[ciudad])

        return file_dict

    def upload_file(self, file_name, folder_name, content):
        conn = self._auth()
        target_folder_url = f'/sites/{self.SHAREPOINT_SITE_NAME}/{self.SHAREPOINT_DOC}/{folder_name}'
        target_folder = conn.web.get_folder_by_server_relative_path(target_folder_url)
        response = target_folder.upload_file(file_name, content).execute_query()
        return response

    def upload_file_in_chunks(self, file_path, folder_name, chunk_size, chunk_uploaded=None, **kwargs):
        conn = self._auth()
        target_folder_url = f'/sites/{self.SHAREPOINT_SITE_NAME}/{self.SHAREPOINT_DOC}/{folder_name}'
        target_folder = conn.web.get_folder_by_server_relative_path(target_folder_url)
        response = target_folder.files.create_upload_session(
            source_path=file_path,
            chunk_size=chunk_size,
            chunk_uploaded=chunk_uploaded,
            **kwargs
        ).execute_query()
        return response

    def get_list(self, list_name):
        conn = self._auth()
        target_list = conn.web.lists.get_by_title(list_name)
        items = target_list.items.get().execute_query()
        return items
        
    def get_file_properties_from_folder(self, folder_name):
        files_list = self._get_files_list(folder_name)
        properties_list = []
        for file in files_list:
            file_dict = {
                'file_id': file.unique_id,
                'file_name': file.name,
                'major_version': file.major_version,
                'minor_version': file.minor_version,
                'file_size': file.length,
                'time_created': file.time_created,
                'time_last_modified': file.time_last_modified
            }
            properties_list.append(file_dict)
            file_dict = {}
        return properties_list

    def delfolder(self,folder_name):
        print(print("Eliminar",folder_name))    			
        ctx = self._auth()				
        folder_name = f'{self.SHAREPOINT_DOC}/{folder_name}'
        folder = ctx.web.get_folder_by_server_relative_url(folder_name)
        ctx.load(folder)
        ctx.execute_query()
        folder.delete_object()
        ctx.execute_query()
        #ctx.close()


    def createFolder(self,path,name):		
        #folder_name = f'{path}/{folder_name}'		
        folder_name = f'{self.SHAREPOINT_DOC}/{path}'		
        print("Crear",folder_name)		
        ctx = self._auth()		
        folder = ctx.web.folders.add(folder_name)
        folder.update()
        ctx.execute_query()
        ctx.close()
        

    def delItemsInfolder(self,folder_name):    	
        files_list = self._get_files_list(folder_name)
        conn = self._auth()
        for file in files_list:    		
            print(file.name)
            file.delete_object()
            conn.execute_query()
        del conn

    def upfile(self,local_file_path,folder_url):    	
        conn = self._auth()
        #folder = conn.web.get_folder_by_server_relative_url(folder_url)
        target_folder = conn.web.get_folder_by_server_relative_url(folder_url)
        with open(local_file_path, "rb") as content_file:
            file_content = content_file.read()
            target_folder.upload_file(os.path.basename(local_file_path), file_content).execute_query()


    def delmakefolder(self,pathinforme,nombrecarpeta):		
        try:
            SharePoint().delfolder(pathinforme)		
        except Exception as e:
            print("Operacion fallida  ",e)
        
        try:
            SharePoint().createFolder(pathinforme,nombrecarpeta)
        except Exception as e:
            print("Operacion fallida  ",e)

    def UpfileToFolder(self,folderDw,folderSh):
        for file in os.listdir(folderDw):			
            binariofile=open(f"{folderDw}/{file}", "rb")	
            self.upload_file(file,folderSh,binariofile)
            binariofile.close()


