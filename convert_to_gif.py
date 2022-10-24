import streamlit as st
from moviepy.editor import *
import base64

def cut_video(clip):
   duration = int(clip.duration)
   start = st.sidebar.number_input('Start time (seconds):',max_value=duration)
   end = st.sidebar.number_input('End time (seconds):',min_value=start+1,max_value=duration)
   clip = clip.subclip(start, end)
   return clip

def download_gif(filename):
    with open(filename,'rb') as f:
      contents = f.read()
      data_url = base64.b64encode(contents).decode("utf-8")
      st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="gif" width=100% height=100%>',
    unsafe_allow_html=True,)
      st.write('\n')
      st.download_button('Download GIF', f, file_name=filename)

st.title('Convert video to GIF')
uploaded_video = st.sidebar.file_uploader("Upload mp4 file",type=["mp4","mpeg"])

if uploaded_video is not None:
  st.video(uploaded_video)

  vid = uploaded_video.name
  with open(vid, mode='wb') as f:
      f.write(uploaded_video.read()) # save video to disk
  st_video = open(vid,'rb')      
  clip = VideoFileClip(vid)
  clip = cut_video(clip)

  ## manually concatenate clips
  # clip1 = clip.subclip(0, 7)
  # clip2 = clip.subclip(16, 21)
  # clip3 = clip.subclip(24, 42)
  #clip4 = clip.subclip(146, 152)
  # clip = concatenate_videoclips([clip1,clip2,clip3])

  fps = st.sidebar.number_input('Number of frames per second (fps):',max_value=20)
  gifname = vid.replace("mp4","gif")
  clip.write_gif(gifname,fps=fps)
  st.success("Successful Conversion!")
  st.write("Output GIF: ")
  download_gif(gifname)