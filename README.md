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
Then launch the main.py with a python launcher.
Make sure you setup ffmpeg path in file -> set ffmpeg path


## Maya Installation:
Copy the 'ffmpeg_image_sequence_encoder' folder into your maya/script directory and run these with python:

```bash
from ffmpeg_image_sequence_encoder import main
window = main.Encoding_Window()
window.show()
```
Make sure you setup ffmpeg path in file -> set ffmpeg path

## License

[MIT](https://choosealicense.com/licenses/mit/)