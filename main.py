import subprocess
import sys

vlc="c:\\Program Files\\VideoLAN\VLC\\vlc.exe" #default vlc path
input_f=sys.argv[1] #path to file
options={} #dictionary with input options

def choose_v():
    #choice of video codec
    vcodec=input("""select a video codec
    1. H264
    2. MPEG-2
    3. MJPEG \n""")

    match vcodec:
        case '1':
            options['vcodec']='h264'
        case '2':
            options['vcodec'] = 'mp2v'
        case '3':
            options['vcodec'] = 'MJPG'
        case _:
            print("unsupported video codec")

def choose_a():
    #choice of audio codec
    acodec=input("""select an audio codec
    1. mp3
    2. mpga \n""")

    match acodec:
        case '1':
            options['acodec']='mp3'
        case '2':
            options['acodec'] = 'mpga'
        case _:
            print("unsupported audio codec")

def choose_vb():
    #bit rate value
    vb=input("Enter the bit rate\n")
    options['vb']=vb

def choose_ab():
    #audio bit rate value
    ab=input("Enter the audio bit rate\n")
    options['ab'] = ab

def choose_scale():
    #image scaling value
    scale=input("Enter image scaling\n")
    options['scale'] = scale

def choose_fps():
    #fps
    fps=input("Enter fps\n")
    options['fps'] = fps


def save():
    #save and transcode the video file
    #if any parameters are selected
    if options:     
        output=input("Enter the path of the output file\n")
        # linking input options to parameters
        tr_info=[f"{k}={v}" for k,v in options.items()]
        tr_info=','.join(tr_info) #join parameters from the array using the ,
        print(tr_info)
        transcode="--sout=#transcode{"+tr_info+"}:standard{access=file,mux=ts,dst="+output+"}"
        #starting the process of transcoding a video file
        subprocess.run([vlc, input_f, transcode, "vlc://quit" ], shell=True)
    else:
        print("No option selected")

if __name__ == '__main__':
    #program menu and option selection
    while True:
        action=input("""Select video transcoding options
1. video codec
2. audio codec
3. bit rate of video
4. audio bit rate
5. image scaling
6. frame rate
7. transcode
Other: exit\n""")
        match action:
            case '1':
                choose_v()
            case '2':
                choose_a()
            case '3':
                choose_vb()
            case '4':
                choose_ab()
            case '5':
                choose_scale()
            case '6':
                choose_fps()
            case '7':
                save()
            case _:
                exit(0)


