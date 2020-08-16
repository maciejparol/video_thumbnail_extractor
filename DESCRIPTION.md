##My definition of a non-empty frame:
Non-empty frame - one that contains at least one non-black pixel. 
However, applications for rendering or conversion are not able to perfectly translate colors, 
I treat a non-empty frame as an image whose pixels do not deviate from the black color.

##The application has two modes:
###1) Standard definition of a non-empty frame - where at least one pixel is not black:
```shell script
ExtractThumbnailFromVideo().extract("<your_video_path>")
```

###2) Modified definition of non-empty frame - where the difference between shades of color may have tolerances (Standard deviation of population of all colors in the frame)
```shell script
ExtractThumbnailFromVideo(tolerance_threshold = 1).extract ( "<your_video_path>")
```
tolerance_threshold can be between 1 - 127

## Extra challenge 
We can do it by testing the standard deviation of all the colors in the frame ... 
My algorithm has it implemented :)
