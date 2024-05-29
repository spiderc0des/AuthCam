import kivy
import gi
gi.require_version('Gst', '1.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from datetime import datetime
from kivy.uix.label import Label

from PIL import Image as PILImage
import uuid_function
from kivy.clock import Clock
import send_to_api
import hash


from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MyGrid(Widget):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.camera = Camera(play=True)
        self.camera.resolution = (640, 480)  # Set resolution to match your needs
        self.camera.size_hint_y = 0.85
        self.ids.cam.add_widget(self.camera)


    # def capture(self):
    #         filename = f'photos/{datetime.now()}.png'
    #         self.camera.export_to_png(filename)
    #         uuid = uuid_function.add_uuid(filename)
    #         hash_value = hash.hash_image(filename)
    #         api_response = send_to_api.send_data_to_api(uuid, hash_value, 'http://127.0.0.1:8000/api/v1/upload/')

    #         print(api_response)

    def display_message(self, message):
        message_label = Label(text=message, size_hint=(None, None), size=(800, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(message_label)
        # Schedule the removal of the label after 5 seconds
        Clock.schedule_once(lambda dt: self.remove_widget(message_label), 3)

    def capture(self):
        # Define filename based on current timestamp
        filename = f'photos/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
        self.camera.export_to_png(filename)  # Assume self.camera is properly set up

        # Create a layout for popup
        layout = BoxLayout(orientation='vertical')
        img = Image(source=filename)
        layout.add_widget(img)

        # Button to OK the process
        btn_ok = Button(text='OK', size_hint=(1, 0.2))
        layout.add_widget(btn_ok)

        # Create a popup
        popup = Popup(title="Confirm Image Capture",
                      content=layout,
                      size_hint=(0.9, 0.9))
        btn_ok.bind(on_press=lambda x: self.process_image(filename, popup))
        popup.open()

    def process_image(self, filename, popup):
        # Close the popup
        popup.dismiss()

        # Continue processing
        uuid = uuid_function.add_uuid(filename)
        hash_value = hash.hash_image(filename)
        api_response = send_to_api.send_data_to_api(uuid, hash_value, 'http://127.0.0.1:8000/api/v1/upload/')
        
        if api_response != 'Failed to establish a new connection':

    # Check the response from the API
            if api_response.status_code == 201:
                # Create content for the new popup
                ok_btn = Button(text='OK', size_hint=(1, 0.3))
                label = Label(text='Image info successfully sent to DB', size_hint=(1, 0.7))
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(label)
                layout.add_widget(ok_btn)

                # Create the popup
                success_popup = Popup(title='Success!', content=layout, size_hint=(None, None), size=(300, 200))
                ok_btn.bind(on_press=success_popup.dismiss)  # Bind the button press to dismiss the popup
                success_popup.open()
        else:
            self.display_message('Network error!')

    def check_touch_capture(self, instance, touch):
        # Check if touch is within the instance's bounds
        if instance.collide_point(*touch.pos):
            self.capture()


    def check_touch_open(self, instance, touch):
            # Check if touch is within the instance's bounds
            if instance.collide_point(*touch.pos):
                self.open_file_chooser()

    def open_file_chooser(self):
        # Create the file chooser
        filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'],  # Filter to only show image files
                                        size_hint=(None, None), size=(400, 400))

        # Create a layout for Popup
        layout = BoxLayout(orientation='vertical')
        select_button = Button(text='Select', size_hint=(1, 0.1))
        layout.add_widget(filechooser)
        layout.add_widget(select_button)

        # Create Popup
        popup = Popup(title='Choose an Image', content=layout,
                    size_hint=(None, None), size=(500, 500), auto_dismiss=True)

        # Bind the on_press event of the button to a method to handle selection
        select_button.bind(on_press=lambda x: self.handle_selected(filechooser.path, filechooser.selection, popup))

        # Open the Popup
        popup.open()

    def handle_selected(self, path, selection, popup):
        # Handle the file selected
        if selection:
            selected_path = selection[0]  # Get the first selected file
            print(f'Selected file: {selected_path}')

            if selected_path:
                extracted_uuid = uuid_function.retrieve_uuid(selected_path)
                if extracted_uuid != 'No EXIF data found in image.' and 'No UUID found in EXIF UserComment.':
                    re_calculated_hash = hash.hash_image(selected_path)
                    api_response = send_to_api.send_data_to_api(extracted_uuid, re_calculated_hash, 'http://127.0.0.1:8000/api/v1/verify/')
                else:
                    return 'Unable to extract uuid'
                
                if api_response != 'Failed to establish a new connection':
          
                # Check the response from the server
                    if api_response.status_code == 302:
                        # Here you can add what to do with the selected file, e.g., open or display it
                        image = Image(source=selected_path)
                    
                        # Create a layout and add the image widget to it
                        layout = BoxLayout()
                        layout.add_widget(image)

                        
                        # Create a new Popup to show the image
                        image_popup = Popup(title='Selected Image', content=layout, size_hint=(None, None), size=(800, 800))
                        image_popup.open()



                        return api_response.text

                    elif api_response.status_code == 412:
                        return api_response.text

                    elif api_response.status_code == 404:
                        return api_response.text
                else:
                    self.display_message('Network error')

                
        popup.dismiss()  # Close the popup

class AuthCam(App):
    def build(self):
        return MyGrid()
    
if __name__ == '__main__':
    AuthCam().run()
