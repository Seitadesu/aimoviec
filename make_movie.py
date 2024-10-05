

from moviepy.editor import *

def create_movie(max_id, intro_text_data):
    # 動画のフレームレート、再生時間、サイズを指定
    fps = 30
    duration = 10
    video_size = (480, 480)
    audio_clip = AudioFileClip(f"static/contents/audio/modified_audio{max_id}.mp3")
    audio_duration = audio_clip.duration
    duration = audio_duration
    # 画像ファイルからImageClipオブジェクトを作成し、フレームレートを設定し、サイズをリサイズする
    video = ImageClip(f"static\image\generate\item_photo{max_id}_1.png", duration=duration).set_fps(fps).resize(video_size)
    # 音声ファイルからAudioFileClipオブジェクトを作成し、再生時間を設定する
    audio = AudioFileClip(f"static/contents/audio/modified_audio{max_id}.mp3").set_duration(duration)

    # CompositeVideoClipを使って、画像と音声を組み合わせたfinalを作成
    # set_pos("center")を使って画像を中央に配置する
    final = CompositeVideoClip([video.set_pos("center")])
    final = final.set_audio(audio)
    # 動画をファイルに書き出す
    # fpsやcodecを指定することで、動画のフレームレートやコーデックを設定する
    final.write_videofile(f"static/contents/movie/output{max_id}.mp4", fps=fps, codec="libx264")

    