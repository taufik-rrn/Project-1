from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton



import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope and credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# Authorize the client
client = gspread.authorize(creds)

class MyGoogleSheetApp(MDApp):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=2)

        # Text input for entering unique ID
        self.unique_id_input = MDTextField(hint_text='Enter Unique ID',
                                           size_hint_x=None,width=300)

        # Text input for entering Alamat
        self.alamat_input = MDTextField(hint_text='Alamat', size_hint_x=None, width=300)

        # Text input for entering Status Tempat Tinggal
        self.status_tempat_tinggal_input = MDTextField(hint_text='Status Tempat Tinggal', size_hint_x=None, width=300)

        # Text input for entering Akses Air Bersih
        self.akses_air_bersih = MDTextField(hint_text="Akses Air Bersih", size_hint_x=None, width=300)

        # Text input for entering Keterangan Wc
        self.keterangan_wc = MDTextField(hint_text="Keterangan Wc", size_hint_x=None, width=300)

        # Text input for entering Keterangan
        self.keterangan = MDTextField(hint_text="Keterangan", size_hint_x=None, width=300)

        # Labels to display the fetched data
        self.nik_label = MDLabel(text='', halign='left')
        self.nama_kepala_keluarga_label = MDLabel(text='', halign='left')
        self.nama_istri_label = MDLabel(text='', halign='left')
        self.status_label = MDLabel(text='', halign='center')  # Status label for user feedback

        # Button to trigger data fetching
        enter_button = MDRaisedButton(text='Enter', on_release=self.fetch_data)


        layout.add_widget(self.unique_id_input)
        layout.add_widget(enter_button)
        layout.add_widget(self.status_label)  # Add status label to the layout
        layout.add_widget(self.nik_label)
        layout.add_widget(self.nama_kepala_keluarga_label)
        layout.add_widget(self.nama_istri_label)
        layout.add_widget(self.alamat_input)
        layout.add_widget(self.status_tempat_tinggal_input)
        layout.add_widget(self.akses_air_bersih)
        layout.add_widget(self.keterangan_wc)
        layout.add_widget(self.keterangan)



        # Open the spreadsheet and worksheet once
        self.spreadsheet = client.open_by_key('1ZkclB9q3MxXAeJ-P2hXujou1997uaEVxHwT-ycC6NGA')
        self.worksheet = self.spreadsheet.sheet1  # Assuming the data is on the first sheet

        return layout

    def fetch_data(self, instance):
        unique_id = self.unique_id_input.text

        try:
            # Find the row number of the cell containing the unique ID in column A
            cell = self.worksheet.find(unique_id)
            row_number = cell.row

            # Fetch data from columns C, D, and E for the specified row
            data = self.worksheet.row_values(row_number)

            # Update labels with fetched data
            self.nik_label.text = "NIK: " + data[2]  # Column C
            self.nama_kepala_keluarga_label.text = "Nama Kepala Keluarga: " + data[3]  # Column D
            self.nama_istri_label.text = "Nama Istri: " + data[4]  # Column E

            # Update Alamat column (Column F) with user input
            alamat = self.alamat_input.text
            self.worksheet.update_cell(row_number, 6, alamat)

            # Automatically update Column J with the value of Column C + '.jpg'
            self.worksheet.update_cell(row_number, 10, data[2] + '.jpg')

            # Automatically update Column K with the value of Column C + '(2)' + '.jpg'
            self.worksheet.update_cell(row_number, 11, data[2] + '(2)' + '.jpg')

            # Update Status Tempat Tinggal (Column l) with user input
            status_tempat_tinggal = self.status_tempat_tinggal_input.text
            self.worksheet.update_cell(row_number, 12, status_tempat_tinggal)

            # Update Akses Air Bersih (Column M) with user input
            akses_air_bersih = self.akses_air_bersih.text
            self.worksheet.update_cell(row_number, 13, akses_air_bersih)

            # Update Keterangan Wc (Column N) with user input
            keterangan_wc = self.keterangan_wc.text
            self.worksheet.update_cell(row_number, 14, keterangan_wc)

            # Update Keterangan (Column O) with user input
            keterangan = self.keterangan.text
            self.worksheet.update_cell(row_number, 15, keterangan)


        except gspread.exceptions.APIError as e:
            self.status_label.text = f'An error occurred: {str(e)}'
        except Exception as e:
            self.status_label.text = f'An error occurred: {str(e)}'


if __name__ == '__main__':
    MyGoogleSheetApp().run()
