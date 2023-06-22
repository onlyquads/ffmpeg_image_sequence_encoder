# ffmpeg image sequence encoder
 

##  What it does:
It's a super minimalistic ffmpeg encoder I made to quickly encode .exr image sequences into light and easy to play .x264 movie file.
It works as standalone app or directly inside maya.

Just select any .exr file from a sequence and hit encode.
The output file will be saved into the same directory as the .exr sequence file.

![standalone version](https://garcia-nicolas.com/wp-content/uploads/2023/06/encoder_script-e1687466584746.png)

*Currently only supports .exr sequences.*
*EDIT - Now also supports .jpg, .jpeg, .tiff and .png image sequences.*

## Standalone Installation:
Copy the 'ffmpeg_image_sequence_encoder' folder wherever you want.
You want to make sure to tweak the path to your ffmpeg installation inside the 'functions.py' file:
```bash
def get_ffmpeg_path():

    # MAKE SURE FFMPEG PATH IS SETUP CORRECTLY FOR YOUR PLATFORM HERE:

    # WINDOWS
    if platform.system() == 'Windows':
        ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg'
        return ffmpeg_path
    # MAC OS
    if platform.system() == 'Darwin':
        ffmpeg_path = '/opt/homebrew/Cellar/ffmpeg/6.0/bin/ffmpeg'
        return ffmpeg_path
    # LINUX
    if platform.system() == 'Linux':
        ffmpeg_path = '/usr/local/bin/ffmpeg'
        return ffmpeg_path
```

Then launch the main.py with a python launcher.


## Maya Installation:
Copy the 'ffmpeg_image_sequence_encoder' folder into your maya/script directory and run these with python:

You'll probably have to tweak the path to your ffmpeg installation inside the 'functions.py', see the Standalone installation point just above.
Save the file and relaunch Maya if needed.

```bash
from ffmpeg_image_sequence_encoder import main
window = main.Encoding_Window()
window.show()
```


## License

[MIT](https://choosealicense.com/licenses/mit/)